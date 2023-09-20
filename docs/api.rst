Python API
==========

Example
-------

The following example shows the compiling an SystemRDL file and then generating
the C header using the Python API.

.. code-block:: python

    from systemrdl import RDLCompiler
    from peakrdl_cheader.exporter import CHeaderExporter

    # compile the SystemRDL
    rdlc = RDLCompiler()
    rdlc.compile_file('basic.rdl')
    top = rdlc.elaborate(top_def_name='basic').top

    # generate the C header
    exporter = CHeaderExporter()
    exporter.export(node=top, path='out.h')


Exporter Class
--------------

.. autoclass:: peakrdl_cheader.exporter.CHeaderExporter
    :members:
