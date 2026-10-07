import os

import base


class TestExportParameters(base.BaseHeaderTestcase):
    rdl_file = "testcases/params.rdl"
    export_parameters = True

    def test_parameter_defines(self) -> None:
        self.do_test()

        header_path = os.path.join(self.output_dir, "out.h")
        with open(header_path, encoding="utf-8") as f:
            header = f.read()

        self.assertIn("#define FOO__BAR 3UL", header)
        self.assertIn("#define FOO__NEG -1L", header)
        self.assertIn("#define FOO__ENABLE 1", header)
        self.assertIn('#define FOO__NAME "hello"', header)

        # Struct array dimensions remain numeric literals
        self.assertIn("regs[3]", header)
        self.assertNotIn("regs[FOO__BAR]", header)


class TestExportParametersDisabled(base.BaseHeaderTestcase):
    rdl_file = "testcases/params.rdl"
    export_parameters = False

    def test_no_parameter_defines(self) -> None:
        self.do_test()

        header_path = os.path.join(self.output_dir, "out.h")
        with open(header_path, encoding="utf-8") as f:
            header = f.read()

        self.assertNotIn("#define FOO__BAR", header)
        self.assertIn("regs[3]", header)
