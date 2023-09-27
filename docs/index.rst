Introduction
============

PeakRDL CHeader is a python package which can be used to generate a register
abstraction layer C Header from a SystemRDL definition.

Installing
----------

Install from `PyPi`_ using pip

.. code-block:: bash

    python3 -m pip install peakrdl-cheader

.. _PyPi: https://pypi.org/project/peakrdl-cheader


Quick Start
-----------
The easiest way is to use the `PeakRDL command line tool <https://peakrdl.readthedocs.io/>`_:

.. code-block:: bash

    peakrdl c-header example.rdl -o example.h

Otherwise, if you want to embed this tool into your own script there is a :ref:`python_api`.


.. toctree::
    :hidden:

    self
    configuring
    api
    licensing
