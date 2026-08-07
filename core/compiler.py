import pypandoc
import os

def compile_markdown_to_docx(markdown_content: str, output_path: str, reference_docx: str = None):
    """
    Compiles Markdown string (with LaTeX math support) into a DOCX file.
    """
    extra_args = []
    if reference_docx and os.path.exists(reference_docx):
        extra_args.append(f'--reference-doc={reference_docx}')
        
    # format 'markdown+tex_math_dollars' to support LaTeX equations.
    pypandoc.convert_text(
        markdown_content,
        'docx',
        format='markdown+tex_math_dollars',
        outputfile=output_path,
        extra_args=extra_args
    )
