from unittest import TestCase
import os
import subprocess
from itertools import product

from systemrdl import RDLCompiler
from peakrdl_cheader.exporter import CHeaderExporter
from peakrdl_cheader.c_standards import CStandard


def get_permutations(spec):
    param_list = []
    for v in product(*spec.values()):
        param_list.append(dict(zip(spec, v)))
    return param_list

class BaseHeaderTestcase(TestCase):
    rdl_file = "testcases/basic.rdl"

    # Export parameters
    std = CStandard.latest
    generate_bitfields = False
    bitfield_order_ltoh = True
    reuse_typedefs = True
    wide_reg_subword_size = 32
    explode_top = False

    @classmethod
    def get_run_dir(cls) -> str:
        this_dir = os.path.dirname(__file__)
        run_dir = os.path.join(this_dir, cls.__name__ + ".out")
        return run_dir

    @property
    def output_dir(self) -> str:
        return self.get_run_dir()

    def do_export(self):
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)

        rdl_path = os.path.join(os.path.dirname(__file__), self.rdl_file)

        rdlc = RDLCompiler()
        rdlc.compile_file(rdl_path)
        top_node = rdlc.elaborate()

        x = CHeaderExporter()
        x.export(
            top_node,
            path=os.path.join(self.output_dir, "out.h"),
            std=self.std,
            generate_bitfields=self.generate_bitfields,
            bitfield_order_ltoh=self.bitfield_order_ltoh,
            reuse_typedefs=self.reuse_typedefs,
            wide_reg_subword_size=self.wide_reg_subword_size,
            explode_top=self.explode_top,
            instantiate=False,
            inst_offset=0,
            testcase=True,
        )

    def do_compile(self):
        args = [
            "gcc",
            "--std", self.std.name,
            os.path.join(self.output_dir, "out.h.test.c"),
            "-o", os.path.join(self.output_dir, "test.exe"),
        ]
        ret = subprocess.run(args, capture_output=True)
        print(" ".join(args))
        print(ret.stdout.decode('utf-8'))
        print(ret.stderr.decode('utf-8'))
        self.assertEqual(ret.returncode, 0)

    def do_run(self):
        args = [os.path.join(self.output_dir, "test.exe")]
        ret = subprocess.run(args, capture_output=True)
        print(" ".join(args))
        print(ret.stdout.decode('utf-8'))
        print(ret.stderr.decode('utf-8'))
        self.assertEqual(ret.returncode, 0)

    def test_me(self):
        self.do_export()
        self.do_compile()
        self.do_run()
