from typing import Any

from systemrdl.component import Field
from systemrdl.node import Node, FieldNode
from systemrdl.udp import UDPDefinition


class IsSigned(UDPDefinition):
    name = "is_signed"
    valid_components = {Field}
    valid_type = bool
    default_assignment = True

    def validate(self, node: "Node", value: Any) -> None:
        # "counter" fields can not be signed
        if value and node.get_property("counter"):
            self.msg.error(
                "The property is_signed=true is not supported for counter fields.",
                node.inst.property_src_ref["is_signed"]
            )

        # incompatible with "encode" fields
        if value and node.get_property("encode") is not None:
            self.msg.error(
                "The property is_signed=true is not supported for fields encoded as an enum.",
                node.inst.property_src_ref["is_signed"]
            )

    def get_unassigned_default(self, node: "Node") -> Any:
        """
        No unassigned default.
        """
        assert isinstance(node, FieldNode)
        if node.get_property("fracwidth") is not None:
            # default unsigned for fixed-point fields
            return False
        # otherwise no default
        return None
