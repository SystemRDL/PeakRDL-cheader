from typing import Union

from systemrdl.node import AddressableNode, AddrmapNode, Node, MemNode, RegfileNode, RegNode
from .design_state import DesignState

def get_node_prefix(ds: DesignState, root_node: Union[AddrmapNode, MemNode, RegfileNode], node: AddressableNode) -> str:
    if ds.use_custom:
        hier_sep = "_"
        xtern_prefix = "xtern_"
    else:
        hier_sep = "__"
        xtern_prefix = "xtern__"

    if ds.reuse_typedefs:
        prefix = node.get_global_type_name(hier_sep)
        if prefix is None:
            # Unable to determine a reusable type name. Fall back to hierarchical path
            # Add prefix to prevent collision when mixing namespace methods
            prefix = xtern_prefix + node.get_rel_path(
                root_node.parent,
                hier_separator=hier_sep,
                array_suffix="x",
                empty_array_suffix="x"
            )
    else:
        prefix = node.get_rel_path(
            root_node.parent,
            hier_separator=hier_sep,
            array_suffix="x",
            empty_array_suffix="x"
        )

    if ds.use_custom and isinstance(node, RegNode):
        parts = prefix.rsplit(hier_sep, 1)
        if len(parts) > 1:
            prefix = f"{parts[0]}{hier_sep}R_{parts[1]}"
        else:
            prefix = f"R_{prefix}"

    return prefix

def get_struct_name(ds: DesignState, root_node: Union[AddrmapNode, MemNode, RegfileNode], node: AddressableNode) -> str:
    if node.is_array and node.array_stride > node.size: # type: ignore # is_array implies array_stride is not none
        # Stride is larger than size of actual element.
        # Struct will be padded up, and therefore needs a unique name
        pad_suffix = f"__stride{node.array_stride:x}"
    else:
        pad_suffix = ""

    return get_node_prefix(ds, root_node, node) + pad_suffix + "_t"


def get_friendly_name(ds: DesignState, root_node: Union[AddrmapNode, MemNode, RegfileNode], node: Node) -> str:
    """
    Returns a useful string that helps identify the typedef in
    a comment
    """
    if ds.reuse_typedefs:
        friendly_name = node.get_global_type_name("::")

        if friendly_name is None:
            # Unable to determine a reusable type name. Fall back to hierarchical path
            friendly_name = node.get_rel_path(root_node.parent)
    else:
        friendly_name = node.get_rel_path(root_node.parent)

    return node.component_type_name + " - " + friendly_name

def roundup_pow2(x: int) -> int:
    return 1<<(x-1).bit_length()
