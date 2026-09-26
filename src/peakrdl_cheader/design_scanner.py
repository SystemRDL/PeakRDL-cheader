from typing import Optional, List, Dict

from systemrdl.walker import RDLListener, RDLWalker, WalkerAction
from systemrdl.node import AddrmapNode, MemNode, RegfileNode, RegNode, AddressableNode

from .design_state import DesignState
from . import utils

class DesignScanner(RDLListener):
    def __init__(self, ds: DesignState) -> None:
        self.ds = ds
        self.msg = ds.top_node.env.msg

        self.prev_reg_stack: List[Optional[RegNode]]
        self.prev_reg_stack = []
        self.reg_prefix_origins: Dict[str, str] = {}
        self.struct_origins: Dict[str, str] = {}

    @property
    def top_node(self) -> AddrmapNode:
        return self.ds.top_node

    def run(self) -> None:
        RDLWalker().walk(self.top_node, self)
        if self.msg.had_error:
            self.msg.fatal(
                "Unable to export due to previous errors"
            )


    def enter_AddressableComponent(self, node: AddressableNode) -> Optional[WalkerAction]:
        self.check_namespace(node)
        if not isinstance(node, RegNode):
            self.prev_reg_stack.append(None)
        return WalkerAction.Continue


    def check_namespace(self, node: AddressableNode) -> None:
        root_node: AddressableNode = self.top_node
        if self.ds.explode_top:
            if node == self.top_node:
                return
            root_node = node
            while root_node.parent != self.top_node:
                assert isinstance(root_node.parent, AddressableNode)
                root_node = root_node.parent
            if isinstance(root_node, RegNode):
                return
        assert isinstance(root_node, (AddrmapNode, MemNode, RegfileNode))

        # Keep scope boundaries distinct from underscores in RDL identifiers.
        # Repeated instances of the same type still have the same origin.
        if isinstance(node, RegNode):
            name = utils.get_node_prefix(self.ds, root_node, node).upper()
            origin = utils.get_node_prefix(self.ds, root_node, node, "::")
            self.check_name(name, origin, node, self.reg_prefix_origins)
            if not self.ds.generate_bitfields:
                return

        name = utils.get_struct_name(self.ds, root_node, node)
        origin = utils.get_struct_name(self.ds, root_node, node, "::")
        self.check_name(name, origin, node, self.struct_origins)


    def check_name(self, name: str, origin: str, node: AddressableNode, origins: Dict[str, str]) -> None:
        previous = origins.setdefault(name, origin)
        if previous != origin:
            self.msg.error(
                f"Generated name '{name}' collides between '{previous}' and '{origin}'.",
                node.inst_src_ref
            )

    def exit_AddressableComponent(self, node: AddressableNode) -> Optional[WalkerAction]:
        if not isinstance(node, RegNode):
            self.prev_reg_stack.pop()
        return WalkerAction.Continue

    def enter_Reg(self, node: RegNode) -> Optional[WalkerAction]:

        # Collect information about overlapping fields, if any.
        overlapping_fields = []
        fields = list(node.fields())
        reg_bitmask = 0
        for i, field in enumerate(fields):
            field_bitmask = ((1 << field.width) - 1) << field.low
            if field_bitmask & reg_bitmask:
                # this field overlaps with a prior one
                # Determine which one
                for prior_field in fields[0:i]:
                    if prior_field.high >= field.low:
                        if prior_field.inst_name not in overlapping_fields:
                            overlapping_fields.append(prior_field.inst_name)

                if field.inst_name not in overlapping_fields:
                    overlapping_fields.append(field.inst_name)

            reg_bitmask |= field_bitmask
        if overlapping_fields:
            # Save infor about this register for later.
            self.ds.overlapping_fields[node.get_path()] = overlapping_fields


        # Check previous adjacent register for overlap
        prev_reg = self.prev_reg_stack[-1]
        if prev_reg and ((prev_reg.raw_address_offset + prev_reg.total_size) > node.raw_address_offset):
            # registers overlap!

            # Registers shall be co-located.
            # This restriction guarantees that overlaps can only happen in pairs,
            # and avoids the more complex overlap scenarios that involve multiple registers.
            if (
                prev_reg.raw_address_offset != node.raw_address_offset # Same offset
                or prev_reg.size != node.size # Same size
                or prev_reg.total_size != node.total_size # Same array footprint
            ):
                self.msg.error(
                    "C header export currently only supports registers that are co-located. "
                    f"See registers: '{prev_reg.inst_name}' and '{node.inst_name}.'",
                    node.inst_src_ref
                )

            # Save information about register overlap pair
            self.ds.overlapping_reg_pairs[prev_reg.get_path()] = node.inst_name

        # Check for sparse register arrays
        if node.is_array and node.array_stride > node.size: # type: ignore # is_array implies array_stride is not none
            self.msg.error(
                "C header export does not support sparse arrays of registers. "
                f"See register: '{node.inst_name}.'",
                node.inst_src_ref
            )

        return WalkerAction.SkipDescendants

    def exit_Reg(self, node: RegNode) -> None:
        self.prev_reg_stack[-1] = node
