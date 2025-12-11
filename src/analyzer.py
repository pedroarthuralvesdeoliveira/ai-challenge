import json
from google import genai
from google.genai import types
from models  import ContractAnalysys, ContractRisk 

DEFAULT_MODEL = "gemini-1.5-flash-latest"

SYSTEM_PROMPT = """You are a Senior Contract Risk Analyst specializing in construction and IT contracts.

Your task is to critically analyze contracts, focusing on:
- Vague payment terms
- Uncapped liability
- Ambiguous scope of work
- Missing termination terms
- Missing insurance requirements
- Broad indemnification clauses
- Overly unilateral terms (e.g., Independent Contractor Agreements)

Be detailed in explanations and practical in remediation suggestions.

CRITICAL: You must adhere strictly to the provided JSON schema for your response. The root element MUST be the object containing the key 'risks', which is an array of risk objects. Do NOT include any extra fields, preambles, or markdown formatting outside of the JSON object itself."""


def analyze_contract_with_gemini(
    contract_text: str,
    api_key: str,
    model: str = DEFAULT_MODEL
) -> ContractAnalysys:
    """
    Analyze contract using Google Gemini API with structured output enforced by Pydantic schema.
    """
    client = genai.Client(api_key=api_key)
    
    schema_dict = ContractAnalysys.model_json_schema()
    
    user_prompt = f"Analyze this contract and identify all significant risks. CONTRACT TEXT:\n\n{contract_text}"
    
    response_text = ""
    
    try:
        response = client.models.generate_content(
            model=model,
            contents=[user_prompt],
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT, 
                temperature=0.2,
                response_mime_type="application/json",
                response_schema=schema_dict 
            )
        )
        
        response_text = response.text.strip()
        
        # Limpeza (safety net contra markdown)
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        parsed_json = json.loads(response_text)
        
        final_data_for_pydantic = parsed_json
        
        if isinstance(parsed_json, dict):
            # Try to find the 'risks' key within a unique wrapping key
            if len(parsed_json) == 1:
                root_key = next(iter(parsed_json.keys()))
                if isinstance(parsed_json[root_key], dict) and 'risks' in parsed_json[root_key]:
                    final_data_for_pydantic = parsed_json[root_key]

            # If the final object contains the 'risks' key, filter everything to keep only it.
            if 'risks' in final_data_for_pydantic and isinstance(final_data_for_pydantic['risks'], list):
                # Ensure Pydantic receives ONLY the object {"risks": [...]}
                final_data_for_pydantic = {"risks": final_data_for_pydantic["risks"]}
            
            # If the final object is a list, wrap it in {"risks": [...]}
            elif isinstance(final_data_for_pydantic, list):
                 final_data_for_pydantic = {"risks": final_data_for_pydantic}


        analysis = ContractAnalysys(**final_data_for_pydantic)
        
        return analysis
    
    except json.JSONDecodeError as e:
        return ContractAnalysys(risks=[
            ContractRisk(
                risk_type="Analysis Error (JSON Decode)",
                clause_text=f"Raw Response Start: {response_text[:100]}...",
                explanation=f"Failed to analyze LLM response. The model did not return valid JSON. Error: {str(e)}",
                remediation_suggestion="Try again or use a 'Pro' model."
            )
        ])
    
    except Exception as e:
        error_explanation = str(e)
        if "API key not valid" in error_explanation or "UNAUTHENTICATED" in error_explanation:
            error_explanation = "Invalid or missing Google AI API key."
        elif "validation error for ContractAnalysys" in error_explanation:
             error_explanation = f"Pydantic validation error: JSON structure does not match expected schema. {error_explanation}"
        
        return ContractAnalysys(risks=[
            ContractRisk(
                risk_type="System/Validation Error",
                clause_text="N/A",
                explanation=f"Error during analysis: {error_explanation}",
                remediation_suggestion="Verify API key and connection. If LLM fails, try a more robust model (1.5 Pro)."
            )
        ])


def analyze_contract_with_gemini_pro(
    contract_text: str,
    api_key: str
) -> ContractAnalysys:
    """
    Analyze contract using Gemini 1.5 Pro for more thorough analysis.
    """
    return analyze_contract_with_gemini(
        contract_text=contract_text,
        api_key=api_key,
        model="gemini-1.5-pro-latest"
    )