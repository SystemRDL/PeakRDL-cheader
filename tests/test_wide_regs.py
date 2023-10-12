import base

from parameterized import parameterized_class

@parameterized_class(base.get_permutations({
    "std": base.ALL_CSTDS,
    "reuse_typedefs": [True, False],
    "instantiate": [True, False],
}))
class TestWideRegs(base.BaseHeaderTestcase):
    rdl_file = "testcases/wide_regs.rdl"
    generate_bitfields = False # Do not support bitfields for wide regs yet
    explode_top = False
    def test_wide_regs(self) -> None:
        self.do_test()
