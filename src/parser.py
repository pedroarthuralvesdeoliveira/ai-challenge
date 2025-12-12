from paddleocr import PaddleOCR
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
        if not full_text.strip():
            try: 
                print("Attempting to extract text from image...")
                full_text = extract_text_from_image(str(path))
            except Exception as e:
                raise ValueError("No text found in the PDF") from e
        
        return full_text
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from PDF using PyMuPDF: {e}") from e

def extract_text_from_image(path: Union[str, Path]) -> str:
    """Extracts text from an image using PaddleOCR.

    - path: path to the image file.     
    """
    path = Path(path)
    if not path.exists():
        print(f"Image file not found: {path}")
        raise FileNotFoundError(f"Image file not found: {path}")

    try:
        ocr = PaddleOCR(use_textline_orientation=True, lang="en")
        result = ocr.predict(str(path))

        full_text = ""
        for res in result:
            if "rec_texts" in res:
                full_text += " ".join(res["rec_texts"]) + "\n\n"
        
        # Print the extracted text
        print(f"Extracted text from image: {full_text}")
        
        # Return the extracted text
        return full_text.strip()
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from image using PaddleOCR: {e}") from e
