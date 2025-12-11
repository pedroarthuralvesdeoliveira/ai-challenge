from pydantic import BaseModel, Field
from typing import List

class ContractRisk(BaseModel): 
    """
    Schema for a single identified contract risk
    """

    risk_type: str = Field(
        description = "Type of risk (e.g., 'Uncapped Liability', 'Vague Payment Terms')"
    )

    clause_text: str = Field(
        description = "Text of the clause that contains the risk"
    )
    
    explanation: str = Field(
        description = "Why this is a risk and its potential legal/financial impact"
    )
    
    remediation_suggestion: str = Field(
        description = "How the clause could be modified to mitigate the risk"
    )
    
class ContractAnalysys(BaseModel):
    """
    Root schema containing all identified risks.
    """
    
    risks: List[ContractRisk] = Field(
        description = "List of all identified risks"
    )
    
    def to_dict(self):
        """
        Convert to dictionary for JSON serialization.
        """
        return self.model_dump()