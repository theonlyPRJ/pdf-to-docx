from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import tempfile
import os
import shutil
from pathlib import Path
from core.converter import convert_pdf_to_docx
from core.compiler import compile_markdown_to_docx

app = FastAPI(title="PDF-to-DOCX Studio")

# Setup static and templates directories
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    try:
        return templates.TemplateResponse(request=request, name="index.html")
    except Exception as e:
        import traceback
        return HTMLResponse(content=f"<h1>500 Internal Server Error</h1><pre>{traceback.format_exc()}</pre>", status_code=500)

@app.post("/api/convert")
async def convert_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return {"error": "Must be a PDF file"}
        
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
        shutil.copyfileobj(file.file, tmp_pdf)
        pdf_path = tmp_pdf.name
        
    docx_path = pdf_path.replace(".pdf", ".docx")
    
    try:
        convert_pdf_to_docx(pdf_path, docx_path)
        return FileResponse(
            docx_path, 
            filename=file.filename.replace(".pdf", ".docx"),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/compile")
async def compile_md(markdown: str = Form(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_docx:
        docx_path = tmp_docx.name
        
    reference_path = str(BASE_DIR / "reference.docx")
    if not os.path.exists(reference_path):
        reference_path = None
        
    try:
        compile_markdown_to_docx(markdown, docx_path, reference_path)
        return FileResponse(
            docx_path,
            filename="compiled.docx",
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
