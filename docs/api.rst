Python API
**********

PeakRDL Python can be used from a python API to generate the python package.
This approach may be useful if multiple operations need to be sequenced for
example:

* A build process that has multiple files dependencies
* A build process that needs other IP-XACT inputs
* A build process that will use other tools form the PeakRDL Suite, for example:

    * building HTML documentation with PeakRDL HTML
    * building UVM using PeakRDL UVM

Example
=======

The following example shows the compiling an SystemRDL file and then generating
the python register abstraction layer using PeakRDL Python.

.. code-block:: python

    from systemrdl import RDLCompiler
    from peakrdl_python.exporter import CHeaderExporter

    # compile the systemRDL
    rdlc = RDLCompiler()
    rdlc.compile_file('basic.rdl')
    spec = rdlc.elaborate(top_def_name='basic').top

    # generate the python package register abstraction layer
    exporter = CHeaderExporter()
    exporter.export(node=spec, path='generated_code')


PythonExporter
==============

.. autoclass:: peakrdl_python.exporter.CHeaderExporter
    :members:
    :special-members: __init__