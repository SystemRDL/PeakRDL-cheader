.. _python_api:

Python API
==========
If you want to embed this tool into your own script, you can do so with the
following API.


Example
-------

The following example shows how to compile a SystemRDL file and then generate
the C header using the Python API.

.. code-block:: python

    from systemrdl import RDLCompiler
    from peakrdl_cheader.exporter import CHeaderExporter

    # compile the SystemRDL
    rdlc = RDLCompiler()
    rdlc.compile_file('example.rdl')
    top = rdlc.elaborate()

    # generate the C header
    exporter = CHeaderExporter()
    exporter.export(node=top, path='out.h')


Exporter Class
--------------

.. autoclass:: peakrdl_cheader.exporter.CHeaderExporter
    :members:
