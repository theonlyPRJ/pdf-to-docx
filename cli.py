import click
import uvicorn
from core.converter import convert_pdf_to_docx
from core.compiler import compile_markdown_to_docx

@click.group()
def cli():
    """PDF-to-DOCX Studio CLI"""
    pass

@cli.command()
@click.argument('pdf_path', type=click.Path(exists=True))
@click.argument('docx_path', type=click.Path())
def convert(pdf_path, docx_path):
    """Convert a PDF file to DOCX format."""
    click.echo(f"Converting {pdf_path} to {docx_path}...")
    convert_pdf_to_docx(pdf_path, docx_path)
    click.echo("Conversion complete!")

@cli.command()
@click.argument('markdown_file', type=click.Path(exists=True))
@click.argument('docx_path', type=click.Path())
@click.option('--reference', type=click.Path(exists=True), default=None, help='Reference DOCX template')
def compile(markdown_file, docx_path, reference):
    """Compile a Markdown file to DOCX format."""
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    click.echo(f"Compiling {markdown_file} to {docx_path}...")
    compile_markdown_to_docx(content, docx_path, reference)
    click.echo("Compilation complete!")

@cli.command()
@click.option('--host', default='127.0.0.1', help='Host to bind')
@click.option('--port', default=8000, help='Port to bind')
def serve(host, port):
    """Start the FastAPI web server."""
    click.echo(f"Starting web server on {host}:{port}...")
    uvicorn.run("app:app", host=host, port=port, reload=True)

if __name__ == '__main__':
    cli()
