from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.feedback import FeedbackCreate, FeedbackOut
from app.models.feedback import Feedback
from app.models.prediction import Prediction
from app.models.user import User
from app.utils.dependencies import get_current_user, require_roles

router = APIRouter(prefix="/feedback", tags=["AI Prediction Feedback"])

@router.post("", response_model=FeedbackOut, status_code=status.HTTP_201_CREATED)
def submit_feedback(
    feedback_in: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Admin", "Tester"]))
):
    """Submit human tester/admin correction for an AI prediction."""
    prediction = db.query(Prediction).filter(Prediction.id == feedback_in.prediction_id).first()
    if not prediction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prediction with ID {feedback_in.prediction_id} not found."
        )
        
    feedback = Feedback(
        prediction_id=feedback_in.prediction_id,
        corrected_severity=feedback_in.corrected_severity,
        corrected_priority=feedback_in.corrected_priority,
        corrected_category=feedback_in.corrected_category,
        corrected_by_id=current_user.id,
        model_version="v1.0",
        notes=feedback_in.notes
    )
    db.add(feedback)
    
    # Optionally update prediction values to match human ground truth
    if feedback_in.corrected_severity:
        prediction.predicted_severity = feedback_in.corrected_severity
    if feedback_in.corrected_priority:
        prediction.predicted_priority = feedback_in.corrected_priority
    if feedback_in.corrected_category:
        prediction.predicted_category = feedback_in.corrected_category

    db.commit()
    db.refresh(feedback)
    return feedback

@router.get("", response_model=List[FeedbackOut])
def list_feedback(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve audit log of AI prediction corrections."""
    return db.query(Feedback).order_by(Feedback.created_at.desc()).all()
