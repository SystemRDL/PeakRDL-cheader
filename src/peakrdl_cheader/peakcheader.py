"""
Command Line tool for the PeakRDL Python
"""

#!/usr/bin/env python3
import argparse
from typing import List, Optional

from systemrdl import RDLCompiler # type: ignore
from systemrdl.node import Node, AddrmapNode # type: ignore
from peakrdl.ipxact import IPXACTImporter # type: ignore

from .exporter import CHeaderExporter


def build_command_line_parser() -> argparse.ArgumentParser:
    """
    generates the command line argument parser to be used by the module.

    Returns:
        command line args parser
    """
    parser = argparse.ArgumentParser(
        description='Generate Python output from systemRDL')
    parser.add_argument('infile', metavar='file', type=str,
                        help='input systemRDL file')

    parser.add_argument('--include_dir', type=str, action='append',
                        metavar='dir',
                        help='add dir to include search path')
    parser.add_argument('--outdir', type=str, default='.',
                        help='output director (default: %(default)s)')
    parser.add_argument('--top', type=str,
                        help='specify top level addrmap (default operation will use last defined '
                             'global addrmap)')
    parser.add_argument('--verbose', '-v', action='count', default=0,
                        help='set logging verbosity')
    parser.add_argument('--ipxact', dest='ipxact', nargs='*',
                        type=str)

    return parser


def compile_rdl(infile:str,
                incl_search_paths:Optional[List[str]]=None,
                top:Optional[str]=None,
                ipxact_files:Optional[List[str]]=None) -> AddrmapNode:
    """
    Compile the systemRDL

    Args:
        infile: top level systemRDL file
        incl_search_paths: list of additional paths where dependent systemRDL files can be
            retrived from. Set to ```none``` if no additional paths are required.
        top: name of the top level address map
        ipxact_files: any IP-XACT files that must be precompiled before compiling the systemRDL

    Returns:

    """
    rdlc = RDLCompiler()
    if ipxact_files is not None:

        ipxact = IPXACTImporter(rdlc)
        if isinstance(ipxact_files, list):
            for ipxact_file in ipxact_files:
                ipxact.import_file(ipxact_file)
        else:
            raise ValueError(f'This ipxact_files should be a list got {type(ipxact_files)}')

    rdlc.compile_file(infile, incl_search_paths=incl_search_paths)
    return rdlc.elaborate(top_def_name=top).top


def generate(root:Node, outdir:str) -> List[str]:
    """
    Generate a PeakRDL output package from compiled systemRDL

    Args:
        root: node in the systemRDL from which the code should be generated
        outdir: directory to store the result in
        autoformatoutputs: If set to True the code will be run through autopep8 to
                clean it up. This can slow down large jobs or mask problems

    Returns:
        List of strings with the module names generated

    """
    print(f'Info: Generating python for {root.inst_name} in {outdir}')
    modules = CHeaderExporter().export(root, outdir)

    return modules

def main_function():
    """
    Main function for the Command Line tool, this needs to be separated out so that it can be
    referenced in setup.py

    Returns:
        None

    """

    cli_parser = build_command_line_parser()
    args = cli_parser.parse_args()

    print('***************************************************************')
    print('* Compile the SystemRDL                                       *')
    print('***************************************************************')
    spec = compile_rdl(args.infile, incl_search_paths=args.include_dir,
                       top=args.top, ipxact_files=args.ipxact)

    print('***************************************************************')
    print('* Generate the Python Package                                 *')
    print('***************************************************************')
    generate(spec, args.outdir)

if __name__ == '__main__':
    main_function()
