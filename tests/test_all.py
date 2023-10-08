import base

from parameterized import parameterized_class
from peakrdl_cheader.c_standards import CStandard

cstds = set(CStandard)
cstds.remove(CStandard.gnu23) # Not available yet

@parameterized_class(base.get_permutations({
    "rdl_file": ["testcases/basic.rdl"],
    "std": cstds,
    "generate_bitfields": [True, False],
    "reuse_typedefs": [True, False],
    "explode_top": [True, False],
}))
class TestAll(base.BaseHeaderTestcase):
    pass
