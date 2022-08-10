"""
A set of utility functions that perform supplementary processing on a node in a compiled
system RDL dataset.
"""
from typing import Iterable

import textwrap

from systemrdl.node import Node, RegNode  # type: ignore
from systemrdl.node import FieldNode, AddressableNode  # type: ignore
from systemrdl.node import MemNode  # type: ignore

def get_fully_qualified_type_name(node: Node) -> str:
    """
    Returns the fully qualified class type name, i.e. with scope prefix
    """
    scope_path = node.inst.get_scope_path(scope_separator='_')

    # TODO if the node is a integer field we can use the base class no
    #      need to generate a unique instance, if it has not documentation
    #      properties


    inst_type_name = node.inst.type_name
    if inst_type_name is None:
        inst_type_name = node.inst_name

    if (scope_path == '') or (scope_path is None):
        return inst_type_name

    return scope_path + '_' + inst_type_name


def get_array_dim(node: AddressableNode):
    """
    Returns the class type name
    """
    assert node.is_array
    assert len(node.array_dimensions) == 1
    return node.array_dimensions[0]


def get_dependent_component(node: AddressableNode) -> Iterable[Node]:
    """
    iterable of nodes that have a component which is used by a
    descendant, this list is de-duplicated and reversed to components
    are declared before their parents who use them

    :param node: node to analysis
    :return: nodes that are dependent on the specified node
    """
    components_needed = []
    for child_node in node.descendants(in_post_order=True):
        child_inst = child_node.inst

        if child_inst in components_needed:
            # already covered the component
            continue

        components_needed.append(child_inst)

        yield child_node


def get_dependent_enum(node: AddressableNode):
    """
    iterable of enums which is used by a descendant of the input node,
    this list is de-duplicated

    :param node: node to analysis
    :return: nodes that are dependent on the specified node
    """
    enum_needed = []
    for child_node in node.descendants():
        if isinstance(child_node, FieldNode):
            if 'encode' in child_node.list_properties():
                # found an field with an enumeration

                field_enum = child_node.get_property('encode')
                fully_qualified_enum_name = fully_qualified_enum_type(field_enum, node)

                if fully_qualified_enum_name not in enum_needed:
                    enum_needed.append(fully_qualified_enum_name)
                    yield field_enum


def fully_qualified_enum_type(field_enum, root_node: AddressableNode):
    """
    Returns the fully qualified class type name, for an enum
    """
    if not hasattr(field_enum, '_parent_scope'):
        # this happens if the enum is has been declared in an IPXACT file
        # which is imported
        return field_enum.__name__

    parent_scope = getattr(field_enum, '_parent_scope')

    if root_node.inst.original_def == parent_scope:
        return field_enum.__name__

    dependent_components = get_dependent_component(root_node)

    for component in dependent_components:
        if component.inst.original_def == parent_scope:
            return get_fully_qualified_type_name(component) + '_' + field_enum.__name__

    raise RuntimeError('Failed to find parent node to reference')


def get_table_block(node: Node) -> str:
    """
    Converts the documentation for a systemRDL node into a nicely formated table that can be
    inserted into the docstring of the class

    Args:
        node: node to be analysed

    Returns:
        A string that represents a sphinx table
    """
    row_break = '+--------------+' \
                '-------------------------------------------------------------------------+'
    if ('name' in node.list_properties()) or ('desc' in node.list_properties()):
        table_strs = [row_break,
                      '| SystemRDL    |'
                      ' Value                                                                   |',
                      '| Field        |'
                      '                                                                         |',
                      '+==============+'
                      '=========================================================================+']
        if 'name' in node.list_properties():
            table_strs.append("| Name         | .. raw:: html".ljust(88, ' ') + ' |')
            table_strs.append("|              | ".ljust(88, ' ') + ' |')
            name_rows = textwrap.wrap(node.get_html_name(), width=88,
                                      initial_indent="|              |      ",
                                      subsequent_indent="|              |      ")
            for name_row in name_rows:
                table_strs.append(name_row.ljust(88, ' ') + ' |')
            table_strs.append(row_break)

        if 'desc' in node.list_properties():
            table_strs.append("| Description  | .. raw:: html".ljust(88, ' ') + ' |')
            table_strs.append("|              | ".ljust(88, ' ') + ' |')
            desc_rows = textwrap.wrap(node.get_html_desc(), width=88,
                                      initial_indent="|              |      ",
                                      subsequent_indent="|              |      ")
            for desc_row in desc_rows:
                table_strs.append(desc_row.ljust(88, ' ') + ' |')
            table_strs.append(row_break)

        return_string = '\n'.join(table_strs)
    else:
        return_string = ''

    return return_string

def get_field_bitmask_int(node: FieldNode) -> int:
    """
    Integer bitmask for a field

    Args:
        node: node to be analysed

    Returns:
        bitmask as a string prefixed by 0x

    """

    if not isinstance(node, FieldNode):
        raise TypeError(f'node is not a {type(FieldNode)} got {type(node)}')

    return sum(2 ** x for x in range(node.low, node.high + 1))

def get_field_bitmask_hex_string(node: FieldNode) -> str:
    """
    Hexadecimal bitmask for a field

    Args:
        node: node to be analysed

    Returns:
        bitmask as a string prefixed by 0x

    """
    if not isinstance(node, FieldNode):
        raise TypeError(f'node is not a {type(FieldNode)} got {type(node)}')
    bitmask = get_field_bitmask_int(node)
    return f'0x{bitmask:X}'


def get_field_inv_bitmask_hex_string(node: FieldNode) -> str:
    """
    Hexadecimal for the inverse bitmask for a field

    Args:
        node: node to be analysed

    Returns:
        inverse bitmask as a string prefixed by 0x

    """
    if not isinstance(node, FieldNode):
        raise TypeError(f'node is not a {type(FieldNode)} got {type(node)}')
    reg_bitmask = (2 ** (node.parent.size * 8)) - 1
    inv_bitmask = reg_bitmask ^ get_field_bitmask_int(node)
    return f'0x{inv_bitmask:X}'


def get_field_max_value_hex_string(node: FieldNode) -> str:
    """
    Hexadecimal for the maximum value that can be represented in a field

    Args:
        node: node to be analysed

    Returns:
        bitmask as a string prefixed by 0x

    """
    if not isinstance(node, FieldNode):
        raise TypeError(f'node is not a {type(FieldNode)} got {type(node)}')
    max_value = ((2 ** (node.high - node.low + 1)) - 1)
    return f'0x{max_value:X}'


def uses_enum(node: AddressableNode) -> bool:
    """
    analyses a node to determine if there are any enumerations used by descendant fields

    Args:
        node: node to analysed

    Returns: True if there are enumeration used, otherwise False
    """
    for child_node in node.descendants():
        if isinstance(child_node, FieldNode):
            if 'encode' in child_node.list_properties():
                return_value = True
                break
    else:
        return_value = False

    return return_value


def get_reg_max_value_hex_string(node: RegNode) -> str:
    """
    Hexadecimal for the maximum value that can be represented in a register

    Args:
        node: node to be analysed

    Returns:
        bitmask as a string prefixed by 0x

    """
    if not isinstance(node, RegNode):
        raise TypeError(f'node is not a {type(RegNode)} got {type(node)}')

    max_value = ((2 ** (node.size * 8)) - 1)
    return f'0x{max_value:X}'

def get_reg_writable_fields(node: RegNode) -> Iterable[FieldNode]:
    """
    Iterable that yields all the writable fields from the reg node

    Args:
        node: node to be analysed

    Yields:
        writeable fields

    """
    if not isinstance(node, RegNode):
        raise TypeError(f'node is not a {type(RegNode)} got {type(node)}')

    for field in node.fields():
        if field.is_sw_writable is True:
            yield field


def get_reg_readable_fields(node: RegNode) -> Iterable[FieldNode]:
    """
    Iterable that yields all the readable fields from the reg node

    Args:
        node: node to be analysed

    Yields:
        readable fields

    """
    if not isinstance(node, RegNode):
        raise TypeError(f'node is not a {type(RegNode)} got {type(node)}')

    for field in node.fields():
        if field.is_sw_readable is True:
            yield field

def uses_memory(node: AddressableNode) -> bool:
    """
    analyses a node to determine if there are any memories used by descendants

    Args:
        node: node to analysed

    Returns: True if there are memories used
    """
    for child_node in node.descendants():
        if isinstance(child_node, MemNode):
            return_value = True
            break
    else:
        return_value = False

    return return_value

def get_memory_max_entry_value_hex_string(node: MemNode) -> str:
    """
    Hexadecimal for the maximum value that can be represented in a register

    Args:
        node: node to be analysed

    Returns:
        bitmask as a string prefixed by 0x

    """
    if not isinstance(node, MemNode):
        raise TypeError(f'node is not a {type(MemNode)} got {type(node)}')

    max_value = ((2 ** (node.get_property('memwidth'))) - 1)
    return f'0x{max_value:X}'

def get_array_typecode(width: int) -> str:
    """
        python array typecode

        Args:
            width: in tbits

        Returns:
            string to pass into the array generator

        """
    if width == 32:
        return 'L'

    if width == 64:
        return 'Q'

    if width == 16:
        return 'I'

    if width == 8:
        return 'B'

    raise ValueError(f'unhandled width {width:d}')

def get_memory_width_bytes(node: MemNode) -> int:
    """
    width of the memory in bytes

    Args:
        node: node to be analysed

    Returns:
        width in bytes

    """
    if not isinstance(node, MemNode):
        raise TypeError(f'node is not a {type(MemNode)} got {type(node)}')

    return node.get_property('memwidth') >> 3
