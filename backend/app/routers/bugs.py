from typing import List, Optional
from fastapi import APIRouter, Depends, status, Query, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.bug import BugCreate, BugUpdate, BugOut, BugDetailOut, SimilarBugCompact
from app.schemas.prediction import PredictionResponse
from app.models.user import User
from app.models.similar_bug import SimilarBug
from app.utils.dependencies import get_current_user, require_roles
from app.services.bug_service import (
    create_bug_with_ai,
    get_bugs,
    get_bug_by_id,
    update_bug,
    delete_bug
)
from app.services.ml_service import ml_service
from app.services.risk_service import calculate_risk_score
from app.services.similarity_service import find_top_similar_bugs

router = APIRouter(prefix="/bugs", tags=["Bug Management"])

@router.post("", response_model=BugOut, status_code=status.HTTP_201_CREATED)
def create_bug(
    bug_in: BugCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Admin", "Tester"]))
):
    """Create a new bug report & auto-trigger NLP, ML Prediction & Risk Engine."""
    return create_bug_with_ai(db, bug_in, current_user.id)

@router.get("", response_model=List[BugOut])
def list_bugs(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: Optional[str] = None,
    severity: Optional[str] = None,
    priority: Optional[str] = None,
    module: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List bugs with pagination, text search & multi-field filtering."""
    return get_bugs(db, skip, limit, status, severity, priority, module, search)

@router.get("/{bug_id}", response_model=BugDetailOut)
def get_bug(
    bug_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get single bug detailed record with predictions and similar historical bugs."""
    bug = get_bug_by_id(db, bug_id)
    
    # Retrieve top similar bugs
    sim_records = db.query(SimilarBug).filter(SimilarBug.source_bug_id == bug_id).all()
    similar_list = []
    for sr in sim_records:
        sb = sr.similar_bug
        if sb:
            pred_sev = sb.prediction.predicted_severity if sb.prediction else "Medium"
            similar_list.append(
                SimilarBugCompact(
                    id=sb.id,
                    title=sb.title,
                    status=sb.status,
                    module=sb.module,
                    similarity_score=round(sr.similarity_score * 100, 1),
                    predicted_severity=pred_sev,
                    created_at=sb.created_at
                )
            )
            
    bug_detail = BugDetailOut.model_validate(bug)
    bug_detail.similar_bugs = similar_list
    return bug_detail

@router.put("/{bug_id}", response_model=BugOut)
def edit_bug(
    bug_id: int,
    bug_in: BugUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Admin", "Tester", "Developer"]))
):
    """Update bug details or status."""
    return update_bug(db, bug_id, bug_in)

@router.delete("/{bug_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_bug(
    bug_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Admin"]))
):
    """Delete a bug record (Admin only)."""
    delete_bug(db, bug_id)
    return None

@router.post("/{bug_id}/predict", response_model=PredictionResponse)
def retrigger_prediction(
    bug_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Re-trigger ML inference & Risk Engine for an existing bug report."""
    bug = get_bug_by_id(db, bug_id)
    
    pred_res = ml_service.predict(
        title=bug.title,
        description=bug.description,
        steps_to_reproduce=bug.steps_to_reproduce or "",
        expected_result=bug.expected_result or "",
        actual_result=bug.actual_result or "",
        environment=bug.environment
    )
    
    risk_res = calculate_risk_score(
        severity=pred_res["predicted_severity"],
        priority=pred_res["predicted_priority"],
        title=bug.title,
        description=bug.description,
        environment=bug.environment
    )
    
    # Update existing prediction record
    if bug.prediction:
        bug.prediction.predicted_severity = pred_res["predicted_severity"]
        bug.prediction.predicted_priority = pred_res["predicted_priority"]
        bug.prediction.predicted_category = pred_res["predicted_category"]
        bug.prediction.confidence = pred_res["confidence"]
        bug.prediction.risk_score = risk_res["risk_score"]
        bug.prediction.risk_level = risk_res["risk_level"]
        db.commit()
        db.refresh(bug.prediction)
        
    return PredictionResponse(
        bug_id=bug.id,
        predicted_severity=pred_res["predicted_severity"],
        predicted_priority=pred_res["predicted_priority"],
        predicted_category=pred_res["predicted_category"],
        confidence=pred_res["confidence"],
        risk_score=risk_res["risk_score"],
        risk_level=risk_res["risk_level"],
        explanation_signals=pred_res["signals"]
    )

@router.get("/{bug_id}/similar", response_model=List[SimilarBugCompact])
def get_similar_bugs(
    bug_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Fetch Top-5 textually similar historical bugs with similarity match %."""
    bug = get_bug_by_id(db, bug_id)
    sim_matches = find_top_similar_bugs(
        db=db,
        current_bug_id=bug.id,
        title=bug.title,
        description=bug.description,
        steps_to_reproduce=bug.steps_to_reproduce or "",
        expected_result=bug.expected_result or "",
        actual_result=bug.actual_result or "",
        top_n=5
    )
    
    compact_list = []
    for item in sim_matches:
        compact_list.append(
            SimilarBugCompact(
                id=item["id"],
                title=item["title"],
                status=item["status"],
                module=item["module"],
                similarity_score=item["similarity_percentage"],
                predicted_severity=item["predicted_severity"],
                created_at=item["created_at"]
            )
        )
    return compact_list
