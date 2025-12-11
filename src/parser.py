from pathlib import Path
from typing import Union
import pymupdf 

def extract_text_from_pdf(path: Union[str, Path]) -> str:
    """
    Extracts text from a PDF using PyMuPDF.

    - path: path to the PDF file.
    - Returns a string with the extracted text (may be empty if the PDF is an image/scan).
    - Raises FileNotFoundError if the file does not exist.
    - Raises RuntimeError if the PyMuPDF library is not available or an error occurs during extraction.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {path}")

    try:
        doc = pymupdf.open(str(path))
        pages_text = []
        for page in doc:
            # "text" gives the plain textual content of the page
            page_text = page.get_text("text") or ""
            pages_text.append(page_text)
        doc.close()

        # Join pages with double newline and trim
        full_text = "\n\n".join(p.strip() for p in pages_text if p and p.strip())
        return full_text
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from PDF using PyMuPDF: {e}") from e
