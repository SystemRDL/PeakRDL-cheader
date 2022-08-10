#!/usr/bin/env python3

import sys
import os

import peakrdl_cheader.peakcheader as pch

from glob import glob

test_case_path = os.path.join('tests', 'testcases')

if len(sys.argv) == 1:
    testcases = glob(os.path.join(test_case_path,'*.rdl'))
else:
    testcases = glob(os.path.join(test_case_path,'{}.rdl').format(sys.argv[1]))

#-------------------------------------------------------------------------------
results = {}
for case in testcases:
    print("Case: ", case)
    rdl_file = case
    testcase_name = os.path.splitext(os.path.basename(case))[0]

    if testcase_name == 'multifile':
        # this needs the simple.xml file included
        root = pch.compile_rdl(rdl_file, ipxact_files=[os.path.join(test_case_path, 'simple.xml')])
    else:
        root = pch.compile_rdl(rdl_file)
    modules = pch.generate(root, os.path.join('testcase_output', 'raw'))

    print("\n-----------------------------------------------------------------\n")

print("\tALL TESTS COMPLETED\n")