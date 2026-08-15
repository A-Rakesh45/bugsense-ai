from pydantic import BaseModel, ConfigDict
from typing import Optional
import datetime
from app.schemas.auth import UserOut

class FeedbackCreate(BaseModel):
    prediction_id: int
    corrected_severity: Optional[str] = None
    corrected_priority: Optional[str] = None
    corrected_category: Optional[str] = None
    notes: Optional[str] = None

class FeedbackOut(BaseModel):
    id: int
    prediction_id: int
    corrected_severity: Optional[str] = None
    corrected_priority: Optional[str] = None
    corrected_category: Optional[str] = None
    corrected_by_id: int
    corrected_by: UserOut
    model_version: str
    notes: Optional[str] = None
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)
