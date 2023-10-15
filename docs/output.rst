Generated Header Contents
=========================

Block Structs
-------------
All blocks such as ``addrmap``, ``regfile`` and ``mem`` components are represented
as struct definitions. To ensure proper address layout, these are always declared
as packed.

Overlapping registers
^^^^^^^^^^^^^^^^^^^^^
If a pair of read-only + write-only register occupy the same address, they will
be represented by an anonymous union of the two.
If anonymous unions are not supported by the C-standard you have selected, the
union will be named based on the two registers.


Bit-fiddling Field Macros
-------------------------
Each field is accompanied by several ``#define`` macros.
These allow register fields to be manipulated using bitwise boolean operations.

The macro names are prefixed such that their definitions will not collide with
other fields of the same name.

.. data:: FIELD_NAME_bm

    Field bit-mask.

    All bits of a register that belong to this field are set to 1.
    Useful for bitwise setting/clearing or masking a field's value.


.. data:: FIELD_NAME_bp

    Field bit position.

    Offset of the low-bit of the field.
    Useful for bit-shifting values into and out of the field.

.. data:: FIELD_NAME_bw

    Field bit width.

    Width of the field in bits.

.. data:: FIELD_NAME_reset

    Field reset value.

    Only emitted if a field definition provides a constant reset value.


Register bit-field structs
--------------------------

If enabled, each register is represented by a nested union & struct definition.
This allows a register value to be accessed in aggregate, or by its individual
bit-fields.

.. important::

    The packing order of bit-fields is implementation-defined and may not be the
    same depending on the compiler or target architecture you use.
    In order to enable bit-field generation, you need to explicitly specify which
    bit packing order of your compiler: Low-to-high (LTOH) or High-to-low (HTOL)

    LTOH is generally more common, but always be sure to verify. Running the
    generated testcase on your target is an easy way to confirm.

If enabled, the register union will contain the following members:

.f
    Contains a struct of bit-fields that represent the register.

.w
    Contains a word member that represents the aggregate register.

.fr, .fw
    If one or more read-only + write-only fields overlap, these fields are moved
    to alternate union members so that they can be accessed explicitly.


Wide Registers
--------------

C's ``<stdint.h>`` types only extend up to 64-bit types.

If a register is encountered that is larger than this, the generated
header will represent it using an array of smaller sub-words.
