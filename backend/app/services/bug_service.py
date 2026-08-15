from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from fastapi import HTTPException, status
from app.models.bug import Bug
from app.models.prediction import Prediction
from app.models.similar_bug import SimilarBug
from app.schemas.bug import BugCreate, BugUpdate
from app.services.ml_service import ml_service
from app.services.risk_service import calculate_risk_score
from app.services.similarity_service import find_top_similar_bugs

def create_bug_with_ai(db: Session, bug_in: BugCreate, user_id: int) -> Bug:
    # 1. Create main bug record
    new_bug = Bug(
        title=bug_in.title,
        description=bug_in.description,
        steps_to_reproduce=bug_in.steps_to_reproduce,
        expected_result=bug_in.expected_result,
        actual_result=bug_in.actual_result,
        environment=bug_in.environment or "Production",
        app_version=bug_in.app_version or "v1.0.0",
        browser_device=bug_in.browser_device or "Chrome 120 / Windows 11",
        module=bug_in.module or "General",
        status="Open",
        created_by_id=user_id
    )
    db.add(new_bug)
    db.commit()
    db.refresh(new_bug)

    # 2. Run ML Prediction Service
    pred_res = ml_service.predict(
        title=new_bug.title,
        description=new_bug.description,
        steps_to_reproduce=new_bug.steps_to_reproduce or "",
        expected_result=new_bug.expected_result or "",
        actual_result=new_bug.actual_result or "",
        environment=new_bug.environment
    )

    # 3. Calculate Risk Score & Level
    risk_res = calculate_risk_score(
        severity=pred_res["predicted_severity"],
        priority=pred_res["predicted_priority"],
        title=new_bug.title,
        description=new_bug.description,
        environment=new_bug.environment
    )

    # 4. Save Prediction record to Database
    prediction = Prediction(
        bug_id=new_bug.id,
        predicted_severity=pred_res["predicted_severity"],
        predicted_priority=pred_res["predicted_priority"],
        predicted_category=pred_res["predicted_category"],
        confidence=pred_res["confidence"],
        risk_score=risk_res["risk_score"],
        risk_level=risk_res["risk_level"]
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    # 5. Compute & Cache Top-5 Similar Bugs
    similar_matches = find_top_similar_bugs(
        db=db,
        current_bug_id=new_bug.id,
        title=new_bug.title,
        description=new_bug.description,
        steps_to_reproduce=new_bug.steps_to_reproduce or "",
        expected_result=new_bug.expected_result or "",
        actual_result=new_bug.actual_result or "",
        top_n=5
    )

    for item in similar_matches:
        sim_record = SimilarBug(
            source_bug_id=new_bug.id,
            similar_bug_id=item["id"],
            similarity_score=item["similarity_score"]
        )
        db.add(sim_record)
    db.commit()

    db.refresh(new_bug)
    return new_bug

def get_bugs(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    status: Optional[str] = None,
    severity: Optional[str] = None,
    priority: Optional[str] = None,
    module: Optional[str] = None,
    search: Optional[str] = None
) -> List[Bug]:
    query = db.query(Bug)

    if status:
        query = query.filter(Bug.status == status)
    if module:
        query = query.filter(Bug.module == module)

    if severity or priority:
        query = query.join(Prediction, Bug.id == Prediction.bug_id)
        if severity:
            query = query.filter(Prediction.predicted_severity == severity)
        if priority:
            query = query.filter(Prediction.predicted_priority == priority)

    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                Bug.title.ilike(search_pattern),
                Bug.description.ilike(search_pattern),
                Bug.module.ilike(search_pattern)
            )
        )

    return query.order_by(desc(Bug.created_at)).offset(skip).limit(limit).all()

def get_bug_by_id(db: Session, bug_id: int) -> Bug:
    bug = db.query(Bug).filter(Bug.id == bug_id).first()
    if not bug:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bug with ID {bug_id} not found."
        )
    return bug

def update_bug(db: Session, bug_id: int, bug_in: BugUpdate) -> Bug:
    bug = get_bug_by_id(db, bug_id)
    update_data = bug_in.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(bug, field, value)
        
    db.commit()
    db.refresh(bug)
    return bug

def delete_bug(db: Session, bug_id: int) -> bool:
    bug = get_bug_by_id(db, bug_id)
    db.delete(bug)
    db.commit()
    return True
