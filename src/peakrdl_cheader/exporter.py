from typing import Any, Union
import os
import re

import jinja2 as jj
from systemrdl.node import RootNode, AddrmapNode

from .design_state import DesignState
from .design_scanner import DesignScanner
from .generators import DefGenerator
from . import utils

class CHeaderExporter:
    def __init__(self) -> None:
        loader = jj.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates"))
        self.jj_env = jj.Environment(
            loader=loader,
            undefined=jj.StrictUndefined
        )

    def export(self, node: Union[RootNode, AddrmapNode], path: str, **kwargs: Any) -> None:
        """
        Parameters
        ----------
        node: AddrmapNode
            Top-level SystemRDL node to export.
        path: str
            Output header file path
        std: CStandard
            Select which GNU C standard to conform to
        reuse_typedefs: bool
            By default, the exporter will attempt to re-use typedefs for
            nodes that are equivalent. This allows for better modularity and type reuse.
            Struct type names are derived using the SystemRDL component's type
            name and declared lexical scope path.

            If this is not desireable, override this parameter to ``False`` and structs
            will be generated more naively using their hierarchical paths.
        generate_bitfields: bool
            If set, registers are exported as nested union/structs to provide structured
            access to individual bitfields.
        bitfield_order_ltoh: bool
            The packing order of C struct bitfields is implementation defined.
            If True, packing will assume low-to-high bit-packing order.
        wide_reg_subword_size: int
            C's <stdint.h> types only extend up to 64-bit types.
            If a register is encountered that is larger than this, the generated
            header will represent it using an array of smaller sub-words.
            Set the desired sub-word size.
            Shall be 8, 16, 32 or 64.
        """
        # If it is the root node, skip to top addrmap
        if isinstance(node, RootNode):
            top_node = node.top
        else:
            top_node = node

        self.ds = DesignState(top_node, kwargs)

        # Check for stray kwargs
        if kwargs:
            raise TypeError(f"got an unexpected keyword argument '{list(kwargs.keys())[0]}'")

        # Validate and collect info for export
        DesignScanner(self.ds).run()

        # TODO: Add option to explode top-level
        top_nodes = [
            top_node,
        ]

        context = {
            "ds": self.ds,
            "header_guard_def": re.sub(r"[^\w]", "_", os.path.basename(path)).upper(),
            "top_nodes": top_nodes,
            "get_struct_name": utils.get_struct_name,
        }

        # Write output
        with open(path, "w", encoding='utf-8') as f:
            # Stream header via jinja
            template = self.jj_env.get_template("header.h")
            template.stream(context).dump(f)
            f.write("\n")

            def_gen = DefGenerator(self.ds)
            for node in top_nodes:
                def_gen.stream(f, node)

            # TODO: add optional "bare metal" exports

            # Stream footer via jinja
            template = self.jj_env.get_template("footer.h")
            template.stream(context).dump(f)

            # Ensure newline before EOF
            f.write("\n")

        # TODO: Write out optional testcase C file
