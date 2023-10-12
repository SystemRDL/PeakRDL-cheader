Generated Header Contents
=========================

Block Structs
-------------
TODO: Add details. possible unions, anon unions

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


Register bitfield structs
-------------------------

If enabled, each register is represented by a nested union & struct definition.
This allows a register value to be accessed in aggregate, or by its individual
bit-fields.

TODO: Add details. union structure. Overlapping fields

TODO: Add section on wide regs?
