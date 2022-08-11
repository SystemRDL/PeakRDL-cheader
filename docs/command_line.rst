Command Line Interface
**********************

PeakRDL Python can either be run from within another Python script or using the
command line program.

.. code-block:: bash

    peakrdl_cheader basic.rdl --outdir peakcheader_output


Detailed Arguments
==================

.. argparse::
   :module: peakrdl_cheader.peakcheader
   :func: build_command_line_parser
   :prog: peakcheader