import os
import tempfile
from unittest import TestCase

from systemrdl import RDLCompiler, RDLCompileError
from peakrdl_cheader.exporter import CHeaderExporter


class TestIdentifierCollisions(TestCase):
    ambiguous_registers = """
        addrmap test {
            regfile {
                reg { field {} val[32]; } value;
            } conf;
            reg { field {} val[16]; } conf__value;
        };
    """

    def export(self, source, reject=False, **kwargs):
        with tempfile.TemporaryDirectory() as directory:
            rdl_path = os.path.join(directory, "test.rdl")
            header_path = os.path.join(directory, "out.h")
            with open(rdl_path, "w", encoding="utf-8") as stream:
                stream.write(source)
            compiler = RDLCompiler()
            compiler.compile_file(rdl_path)
            top = compiler.elaborate()

            if reject:
                with self.assertRaises(RDLCompileError):
                    CHeaderExporter().export(top, header_path, **kwargs)
                self.assertFalse(os.path.exists(header_path))
                return ""
            CHeaderExporter().export(top, header_path, **kwargs)
            with open(header_path, encoding="utf-8") as stream:
                return stream.read()

    def test_ambiguous_register_prefix(self):
        for reuse_typedefs in (True, False):
            with self.subTest(reuse_typedefs=reuse_typedefs):
                self.export(self.ambiguous_registers, reject=True,
                            reuse_typedefs=reuse_typedefs)

    def test_ambiguous_struct_name(self):
        source = """
            addrmap test {
                regfile {
                    regfile { reg { field {} val[32]; } first_reg; } inner;
                } block;
                regfile { reg { field {} val[16]; } second_reg; } block__inner;
            };
        """
        for reuse_typedefs in (True, False):
            with self.subTest(reuse_typedefs=reuse_typedefs):
                self.export(source, reject=True, reuse_typedefs=reuse_typedefs)

    def test_uppercase_macro_collision(self):
        self.export("""
            addrmap test {
                reg { field {} val[32]; } value;
                reg { field {} val[16]; } VALUE;
            };
        """, reject=True)

    def test_reused_and_parameterized_types(self):
        source = """
            reg shared_reg #(longint WIDTH=32) { field {} val[WIDTH]; };
            addrmap test {
                shared_reg first;
                shared_reg second;
                shared_reg #(.WIDTH(16)) third;
            };
        """
        for reuse_typedefs in (True, False):
            with self.subTest(reuse_typedefs=reuse_typedefs):
                header = self.export(source, reuse_typedefs=reuse_typedefs,
                                     generate_bitfields=True)
                self.assertIn('_bw 32', header)
                self.assertIn('_bw 16', header)

    def test_explode_top_excludes_direct_registers(self):
        for reuse_typedefs in (True, False):
            with self.subTest(reuse_typedefs=reuse_typedefs):
                header = self.export(self.ambiguous_registers,
                                     reuse_typedefs=reuse_typedefs, explode_top=True)
                self.assertIn('_bw 32', header)
                self.assertNotIn('_bw 16', header)
