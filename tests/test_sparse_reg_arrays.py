import os

import base


# Note: testcases/sparse_reg_arrays.rdl is also compiled and run with every
# export option combination by test_all.py. This checks the shape of the output.
class TestSparseRegArrayHeader(base.BaseHeaderTestcase):
    rdl_file = "testcases/sparse_reg_arrays.rdl"

    def test_padded_types(self) -> None:
        self.do_export()
        with open(os.path.join(self.output_dir, "out.h"), encoding="utf-8") as f:
            header = f.read()

        # Each sparse array element is padded out to the array stride, so a
        # sparse instance gets its own type, separate from dense instances of
        # the same register.
        self.assertIn("ctrl_reg__stride10_t sparse[4];", header)
        self.assertIn("uint32_t dense[4];", header)
        self.assertIn("uint8_t RESERVED[0x10];", header)
        self.assertIn("ctrl_reg__stride8_t grid[2][3];", header)
        self.assertIn("data64_reg__stride20_t words[2];", header)
        self.assertIn("uint8_t RESERVED[0x20];", header)
