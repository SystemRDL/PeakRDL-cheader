Configuring PeakRDL-cheader
============================

If using the `PeakRDL command line tool <https://peakrdl.readthedocs.io/>`_,
some aspects of the ``c-header`` command can be configured  via the PeakRDL TOML
file. Any equivalent command-line options will always take precedence.

All C header-specific options are defined under the ``[c-header]`` TOML heading.

For example:

.. code-block:: toml

    [c-header]
    std = "gnu17"
    type_style = "lexical"
    subword_size = 32
    bitfields = "ltoh"



.. data:: std

    Select the C standard that generated output will conform to.


.. data:: type_style

    Choose how typedef names are generated.

    The ``lexical`` style will use RDL lexical scope & type names where
    possible and attempt to re-use equivalent type definitions.

    The ``hier`` style uses component's hierarchy as the struct type name.


.. data:: bitfields

    Enable generation of register bitfield structs to provide bit-level access
    to fields.

    Since the packing order of C struct bitfields is implementation defined, the
    packing order must be explicitly specified as ``ltoh`` or ``htol``.


.. data:: subword_size

    C's ``<stdint.h>`` types only extend up to 64-bit types.

    If a register is encountered that is larger than this, the generated
    header will represent it using an array of smaller sub-words.
    Set the desired sub-word size of 8, 16, 32 or 64.
