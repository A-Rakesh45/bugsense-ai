from pydantic import BaseModel, ConfigDict
from typing import Optional, List
import datetime
from app.schemas.auth import UserOut

class BugCreate(BaseModel):
    title: str
    description: str
    steps_to_reproduce: Optional[str] = None
    expected_result: Optional[str] = None
    actual_result: Optional[str] = None
    environment: Optional[str] = "Production"
    app_version: Optional[str] = "v1.0.0"
    browser_device: Optional[str] = "Chrome 120 / Windows 11"
    module: Optional[str] = "General"

class BugUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    steps_to_reproduce: Optional[str] = None
    expected_result: Optional[str] = None
    actual_result: Optional[str] = None
    environment: Optional[str] = None
    app_version: Optional[str] = None
    browser_device: Optional[str] = None
    module: Optional[str] = None
    status: Optional[str] = None  # Open, In Progress, Resolved, Closed

class PredictionOut(BaseModel):
    id: int
    predicted_severity: str
    predicted_priority: str
    predicted_category: str
    confidence: float
    risk_score: float
    risk_level: str
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class SimilarBugCompact(BaseModel):
    id: int
    title: str
    status: str
    module: str
    similarity_score: float
    predicted_severity: Optional[str] = None
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class BugOut(BaseModel):
    id: int
    title: str
    description: str
    steps_to_reproduce: Optional[str] = None
    expected_result: Optional[str] = None
    actual_result: Optional[str] = None
    environment: str
    app_version: str
    browser_device: str
    module: str
    status: str
    created_by_id: int
    created_by: UserOut
    created_at: datetime.datetime
    updated_at: datetime.datetime
    prediction: Optional[PredictionOut] = None

    model_config = ConfigDict(from_attributes=True)

class BugDetailOut(BugOut):
    similar_bugs: List[SimilarBugCompact] = []
