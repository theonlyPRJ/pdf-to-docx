import unittest
from core.converter import has_text_vectors, convert_pdf_to_docx

class TestConverter(unittest.TestCase):
    def test_has_text_vectors(self):
        self.assertTrue(callable(has_text_vectors))

    def test_convert_pdf_to_docx(self):
        self.assertTrue(callable(convert_pdf_to_docx))
