import os
import json
from typing import Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.bug import Bug
from app.models.prediction import Prediction
from app.models.feedback import Feedback
from app.utils.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/dashboard", tags=["Dashboard Analytics"])

@router.get("/statistics")
def get_dashboard_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    
    total_bugs = db.query(Bug).count()
    open_bugs = db.query(Bug).filter(Bug.status == "Open").count()
    in_progress = db.query(Bug).filter(Bug.status == "In Progress").count()
    resolved_bugs = db.query(Bug).filter(Bug.status == "Resolved").count()
    closed_bugs = db.query(Bug).filter(Bug.status == "Closed").count()
    
    # Severity breakdown
    sev_counts = (
        db.query(Prediction.predicted_severity, func.count(Prediction.id))
        .group_by(Prediction.predicted_severity)
        .all()
    )
    sev_dict = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    for sev, count in sev_counts:
        if sev in sev_dict:
            sev_dict[sev] = count
            
    # Priority breakdown
    pri_counts = (
        db.query(Prediction.predicted_priority, func.count(Prediction.id))
        .group_by(Prediction.predicted_priority)
        .all()
    )
    pri_dict = {"P1": 0, "P2": 0, "P3": 0, "P4": 0}
    for pri, count in pri_counts:
        if pri in pri_dict:
            pri_dict[pri] = count

    # Category breakdown
    cat_counts = (
        db.query(Prediction.predicted_category, func.count(Prediction.id))
        .group_by(Prediction.predicted_category)
        .all()
    )
    cat_dict = {cat: count for cat, count in cat_counts if cat}

    # Module breakdown & risk
    mod_counts = (
        db.query(Bug.module, func.count(Bug.id))
        .group_by(Bug.module)
        .all()
    )
    mod_dict = {mod: count for mod, count in mod_counts if mod}

    # Feedback counts
    feedback_count = db.query(Feedback).count()

    # Load Model Evaluation Report if available
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    report_file = os.path.join(base_dir, "models", "evaluation_report.json")
    model_eval = None
    if os.path.exists(report_file):
        try:
            with open(report_file, "r", encoding="utf-8") as f:
                model_eval = json.load(f)
        except Exception:
            pass

    return {
        "metrics": {
            "total_bugs": total_bugs,
            "open_bugs": open_bugs,
            "in_progress_bugs": in_progress,
            "resolved_bugs": resolved_bugs,
            "closed_bugs": closed_bugs,
            "critical_bugs": sev_dict.get("Critical", 0),
            "high_priority_bugs": pri_dict.get("P1", 0) + pri_dict.get("P2", 0),
            "feedback_count": feedback_count
        },
        "charts": {
            "severity_distribution": sev_dict,
            "priority_distribution": pri_dict,
            "category_distribution": cat_dict,
            "module_distribution": mod_dict
        },
        "model_evaluation": model_eval
    }
