import json
import pytest
from unittest.mock import patch
from src.models import ContractAnalysys
from src.analyzer import analyze_contract_with_gemini, analyze_contract_with_gemini_pro

MOCK_GEMINI_SUCCESS_JSON = {
    "risks": [
        {
            "risk_type": "Vague Payment Terms",
            "clause_text": "payable \"upon satisfactory progress.\"",
            "explanation": "Payment terms are subjective, lacking specific dates or milestones.",
            "remediation_suggestion": "Define clear milestones or dates (e.g., '30 days after milestone completion')."
        },
        {
            "risk_type": "Uncapped Liability",
            "clause_text": "Contractor shall be liable for any and all damages...",
            "explanation": "Liability is unlimited, exposing the Contractor to extreme financial risk.",
            "remediation_suggestion": "Add a cap on liability, typically limited to the total contract value."
        }
    ]
}

# 2. JSON returned (Wrapping)
MOCK_GEMINI_WRAPPED_JSON = {
    "contract_analysis": {
        "risks": [
            {
                "risk_type": "Missing Termination Clause",
                "clause_text": "No termination clause is provided.",
                "explanation": "Lack of termination rights makes exiting the agreement difficult.",
                "remediation_suggestion": "Add mutual termination clauses with and without cause."
            }
        ]
    }
}

class MockGeminiResponse:
    def __init__(self, text):
        self.text = text
        self.candidates = []


@patch('src.analyzer.genai.Client')
def test_analyze_contract_success(mock_client):
    """Tests the success scenario with a perfectly formatted JSON."""
    
    mock_response_text = json.dumps(MOCK_GEMINI_SUCCESS_JSON)
    mock_client.return_value.models.generate_content.return_value = MockGeminiResponse(mock_response_text)

    analysis = analyze_contract_with_gemini(
        contract_text="Some contract text",
        api_key="mock_key"
    )

    # Assert
    assert isinstance(analysis, ContractAnalysys)
    assert len(analysis.risks) == 2
    assert analysis.risks[0].risk_type == "Vague Payment Terms"
    assert "liable for any and all damages" in analysis.risks[1].clause_text

@patch('src.analyzer.genai.Client')
def test_analyze_contract_unwrapping(mock_client):
    """Tests the logic of 'unwrapping' for JSONs wrapped in extra keys."""
    
    # Simulate the response from the API (JSON wrapped in extra keys)
    mock_response_text = json.dumps(MOCK_GEMINI_WRAPPED_JSON)
    mock_client.return_value.models.generate_content.return_value = MockGeminiResponse(mock_response_text)

    analysis = analyze_contract_with_gemini(
        contract_text="Another contract text",
        api_key="mock_key"
    )

    # Assert
    assert isinstance(analysis, ContractAnalysys)
    assert len(analysis.risks) == 1
    assert analysis.risks[0].risk_type == "Missing Termination Clause"

@patch('src.analyzer.genai.Client')
def test_analyze_contract_invalid_json(mock_client):
    """Tests error handling when the LLM returns non-JSON text."""
    
    # Simulate the response from the API (invalid JSON)
    mock_response_text = "ERROR: The model failed to generate JSON output."
    mock_client.return_value.models.generate_content.return_value = MockGeminiResponse(mock_response_text)

    # Execute the analysis function
    analysis = analyze_contract_with_gemini(
        contract_text="Contract text",
        api_key="mock_key"
    )

    # Assert
    assert len(analysis.risks) == 1
    assert analysis.risks[0].risk_type == "Analysis Error (JSON Decode)"
    assert "Failed to analyze LLM response" in analysis.risks[0].explanation

@patch('src.analyzer.genai.Client')
def test_analyze_contract_api_key_invalid(mock_client):
    """Tests error handling for API failures (e.g., invalid key)."""
    
    # Simulates an API exception (e.g. UNAUTHENTICATED)
    mock_client.return_value.models.generate_content.side_effect = Exception("401 UNAUTHENTICATED: API key not valid")

    # Execute the analysys function
    analysis = analyze_contract_with_gemini(
        contract_text="Contract text",
        api_key="invalid_key"
    )

    # Assert
    assert len(analysis.risks) == 1
    assert analysis.risks[0].risk_type == "System/Validation Error"
    assert "Invalid or missing Google AI API key" in analysis.risks[0].explanation