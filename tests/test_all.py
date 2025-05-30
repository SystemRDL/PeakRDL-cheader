import glob

import base

from parameterized import parameterized_class

exceptions = [
    "testcases/wide_regs.rdl",
    "testcases/udps.rdl",
]
files = glob.glob("testcases/*.rdl")
files = [file for file in files if file not in exceptions]

@parameterized_class(base.get_permutations({
    "rdl_file": files,
    "std": base.ALL_CSTDS,
    "generate_bitfields": [True, False],
    "reuse_typedefs": [True, False],
    "explode_top": [True, False],
    "instantiate": [True, False],
}))
class TestAll(base.BaseHeaderTestcase):
    def test_all(self) -> None:
        self.do_test()
