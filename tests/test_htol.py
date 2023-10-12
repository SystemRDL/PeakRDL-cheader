import base

class TestHTOL(base.BaseHeaderTestcase):
    rdl_file = "testcases/widths_and_mem.rdl"
    generate_bitfields = True
    explode_top = False
    bitfield_order_ltoh = False
    def test_htol(self) -> None:
        # Can't actually run test because gcc on this arch is ltoh
        self.do_export()
        self.do_compile()
