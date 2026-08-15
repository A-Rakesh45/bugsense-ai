from typing import Dict, Any

SEVERITY_WEIGHTS = {
    "Critical": 100,
    "High": 75,
    "Medium": 45,
    "Low": 20
}

PRIORITY_WEIGHTS = {
    "P1": 100,
    "P2": 75,
    "P3": 45,
    "P4": 20
}

HIGH_RISK_KEYWORDS = [
    "crash", "data leak", "vulnerability", "payment failed", 
    "deadlock", "sql injection", "outage", "buffer overflow", "oom"
]

def calculate_risk_score(
    severity: str,
    priority: str,
    title: str = "",
    description: str = "",
    environment: str = "Production"
) -> Dict[str, Any]:
    """
    Transparent Risk Scoring Formula:
    Risk = Min(100, (Severity_Weight * 0.40) + (Priority_Weight * 0.35) + Keyword_Bonus + Env_Bonus)
    """
    w_sev = SEVERITY_WEIGHTS.get(severity, 45)
    w_pri = PRIORITY_WEIGHTS.get(priority, 45)
    
    base_score = (w_sev * 0.40) + (w_pri * 0.35)
    
    # Keyword risk bonus
    full_text = (title + " " + description).lower()
    keyword_bonus = 0
    detected_keywords = []
    for kw in HIGH_RISK_KEYWORDS:
        if kw in full_text:
            keyword_bonus += 7.5
            detected_keywords.append(kw)
    keyword_bonus = min(15.0, keyword_bonus)
    
    # Environment bonus
    env_bonus = 10.0 if "production" in environment.lower() else 0.0
    
    final_score = min(100.0, round(base_score + keyword_bonus + env_bonus, 1))
    
    if final_score >= 86:
        risk_level = "Critical"
    elif final_score >= 66:
        risk_level = "High"
    elif final_score >= 36:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return {
        "risk_score": final_score,
        "risk_level": risk_level,
        "breakdown": {
            "severity_weight_component": round(w_sev * 0.40, 1),
            "priority_weight_component": round(w_pri * 0.35, 1),
            "keyword_bonus": round(keyword_bonus, 1),
            "detected_keywords": detected_keywords,
            "environment_bonus": env_bonus
        }
    }
