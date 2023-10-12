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
    rdl_file = ""

    # Export parameters
    std = CStandard.latest
    generate_bitfields = False
    bitfield_order_ltoh = True
    reuse_typedefs = True
    wide_reg_subword_size = 32
    explode_top = False
    instantiate = False

    @classmethod
    def get_run_dir(cls) -> str:
        this_dir = os.path.dirname(__file__)
        run_dir = os.path.join(this_dir, "test.out", cls.__name__)
        return run_dir

    @property
    def output_dir(self) -> str:
        return self.get_run_dir()

    @classmethod
    def _write_params(cls) -> None:
        """
        Write out the class parameters to a file so that it is easier to debug
        how a testcase was parameterized
        """
        path = os.path.join(cls.get_run_dir(), "params.txt")

        with open(path, 'w') as f:
            for k, v in cls.__dict__.items():
                if k.startswith("_") or callable(v):
                    continue
                f.write(f"{k}: {repr(v)}\n")

    def do_export(self):
        os.makedirs(self.output_dir, exist_ok=True)

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
            instantiate=self.instantiate,
            inst_offset=0,
            testcase=True,
        )

        self._write_params()

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

    def do_test(self):
        self.do_export()
        self.do_compile()
        self.do_run()


ALL_CSTDS = set(CStandard)
ALL_CSTDS.remove(CStandard.gnu23) # Not available yet
