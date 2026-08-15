from pydantic import BaseModel, ConfigDict
from typing import List, Optional
import datetime

class PredictionRequest(BaseModel):
    bug_id: int

class PredictionResponse(BaseModel):
    bug_id: int
    predicted_severity: str
    predicted_priority: str
    predicted_category: str
    confidence: float
    risk_score: float
    risk_level: str
    explanation_signals: List[str] = []

    model_config = ConfigDict(from_attributes=True)
