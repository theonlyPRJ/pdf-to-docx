import fitz  # PyMuPDF
from pdf2docx import Converter
import pytesseract
from docx import Document
from PIL import Image

def has_text_vectors(pdf_path: str) -> bool:
    """Checks if a PDF has selectable text vectors."""
    doc = fitz.open(pdf_path)
    for page in doc:
        text = page.get_text()
        if text.strip():
            return True
    return False

def convert_pdf_to_docx(pdf_path: str, docx_path: str):
    """
    Converts a PDF to DOCX. Uses native vector conversion if possible,
    falling back to OCR if the PDF is scanned.
    """
    if has_text_vectors(pdf_path):
        print(f"Text vectors detected in {pdf_path}. Using native pdf2docx conversion.")
        cv = Converter(pdf_path)
        cv.convert(docx_path, start=0, end=None)
        cv.close()
    else:
        print(f"No text vectors detected in {pdf_path}. Falling back to OCR (pytesseract).")
        convert_scanned_pdf_to_docx(pdf_path, docx_path)

def convert_scanned_pdf_to_docx(pdf_path: str, docx_path: str):
    """
    Fallback method to extract text from scanned PDFs via OCR and save to DOCX.
    """
    doc = fitz.open(pdf_path)
    word_doc = Document()
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # Run OCR
        text = pytesseract.image_to_string(img)
        
        # Add to word doc
        word_doc.add_paragraph(text)
        if page_num < len(doc) - 1:
            word_doc.add_page_break()
            
    word_doc.save(docx_path)
