from typing import TYPE_CHECKING

from peakrdl.plugins.exporter import ExporterSubcommandPlugin #pylint: disable=import-error
from peakrdl.config import schema #pylint: disable=import-error

from .exporter import CHeaderExporter
from .c_standards import CStandard

if TYPE_CHECKING:
    import argparse
    from systemrdl.node import AddrmapNode

class Exporter(ExporterSubcommandPlugin):
    short_desc = "Generate a C header definition of an address space"

    cfg_schema = {
        "std": schema.Choice(list(CStandard.__members__.keys())),
        "type_style": schema.Choice(['lexical', 'hier']),
        "subword_size": schema.Integer(),
        "bitfields": schema.Choice(["ltoh", "htol", "none"]),
    }

    def add_exporter_arguments(self, arg_group: 'argparse._ActionsContainer') -> None:
        arg_group.add_argument(
            "--std",
            choices=list(CStandard.__members__.keys()),
            default=None,
            help=f"""
            Select the C standard that generated output will conform to. [{CStandard.latest.name}]
            """
        )

        arg_group.add_argument(
            "--bitfields",
            choices=["ltoh", "htol", "none"],
            default=None,
            help="""
            Enable generation of register bitfield structs to provide bit-level access
            to fields.

            Since the packing order of C struct bitfields is implementation defined, the
            packing order must be explicitly specified. [none]
            """
        )

        arg_group.add_argument(
            "--type-style",
            dest="type_style",
            choices=['lexical', 'hier'],
            default=None,
            help="""Choose how typedef names are generated.
            The 'lexical' style will use RDL lexical scope & type names where
            possible and attempt to re-use equivalent type definitions.
            The 'hier' style uses component's hierarchy as the struct type name. [lexical]
            """
        )

        arg_group.add_argument(
            "--subword-size",
            type=int,
            default=None,
            help="""
            C's <stdint.h> types only extend up to 64-bit types.

            If a register is encountered that is larger than this, the generated
            header will represent it using an array of smaller sub-words.
            Set the desired sub-word size of 8, 16, 32 or 64. [32]
            """
        )

    def do_export(self, top_node: 'AddrmapNode', options: 'argparse.Namespace') -> None:
        std_name = options.std or self.cfg['std'] or "latest"
        std = CStandard[std_name]

        bitfields = options.bitfields or self.cfg['bitfields'] or "none"
        generate_bitfields = bitfields != "none"
        bitfield_order_ltoh = bitfields == "ltoh"

        type_style = options.type_style or self.cfg['type_style'] or "lexical"
        reuse_typedefs = type_style == "lexical"

        subword_size = options.subword_size or self.cfg['subword_size'] or 32

        x = CHeaderExporter()
        x.export(
            top_node,
            path=options.output,
            std=std,
            generate_bitfields=generate_bitfields,
            bitfield_order_ltoh=bitfield_order_ltoh,
            reuse_typedefs=reuse_typedefs,
            wide_reg_subword_size=subword_size,
        )
