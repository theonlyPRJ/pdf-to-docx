import unittest
from core.compiler import compile_markdown_to_docx

class TestCompiler(unittest.TestCase):
    def test_compile_markdown_to_docx(self):
        self.assertTrue(callable(compile_markdown_to_docx))
