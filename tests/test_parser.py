import pytest

from pathlib import Path
from src.parser import extract_text_from_pdf

def test_extract_text_from_pdf_file_not_found():
    """Tests if FileNotFoundError is raised for an invalid path."""
    
    non_existent_path = Path("non_existent_file.pdf")
    
    with pytest.raises(FileNotFoundError) as excinfo:
        extract_text_from_pdf(non_existent_path)
    
    assert "PDF file not found" in str(excinfo.value)
    

def test_extract_text_from_pdf_success():
    """Tests if the extraction returns text for a valid PDF (Simulation)."""
    tests_dir = Path(__file__).parent
    file_name = "Service Agreement.pdf"
    contract_path = tests_dir.parent / "assets" / file_name
    
    contract_text = extract_text_from_pdf(contract_path)
    assert "BrightWave LLC" in contract_text 
    assert len(contract_text) > 100 
