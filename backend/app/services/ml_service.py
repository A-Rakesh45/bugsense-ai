import os
import joblib
import numpy as np
from typing import Dict, Any, List
from training.preprocess import combine_bug_features, preprocess_text

class MLService:
    def __init__ (self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.models_dir = os.path.join(self.base_dir, "models")
        
        self.vectorizer = None
        self.severity_model = None
        self.priority_model = None
        self.category_model = None
        
        self._load_models()

    def _load_models(self):
        vec_path = os.path.join(self.models_dir, "tfidf_vectorizer.joblib")
        sev_path = os.path.join(self.models_dir, "severity_model.joblib")
        pri_path = os.path.join(self.models_dir, "priority_model.joblib")
        cat_path = os.path.join(self.models_dir, "category_model.joblib")
        
        if os.path.exists(vec_path) and os.path.exists(sev_path):
            try:
                self.vectorizer = joblib.load(vec_path)
                self.severity_model = joblib.load(sev_path)
                self.priority_model = joblib.load(pri_path)
                self.category_model = joblib.load(cat_path)
                print("ML Models & TF-IDF Vectorizer successfully loaded for production inference.")
            except Exception as e:
                print(f"Error loading ML models: {e}")
        else:
            print("Warning: ML model joblib artifacts not found. Heuristic fallback will be used until trained.")

    def predict(
        self,
        title: str,
        description: str,
        steps_to_reproduce: str = "",
        expected_result: str = "",
        actual_result: str = "",
        environment: str = "Production"
    ) -> Dict[str, Any]:
        
        combined_text = combine_bug_features(
            title, description, steps_to_reproduce, expected_result, actual_result
        )
        
        signals = []
        raw_text_lower = (title + " " + description + " " + steps_to_reproduce + " " + actual_result).lower()
        
        if "crash" in raw_text_lower or "outage" in raw_text_lower or "deadlock" in raw_text_lower:
            signals.append("Application Crash / System Outage Detected")
        if "payment" in raw_text_lower or "debit" in raw_text_lower or "checkout" in raw_text_lower:
            signals.append("Financial / Payment Subsystem Affected")
        if "sql injection" in raw_text_lower or "vulnerability" in raw_text_lower or "overflow" in raw_text_lower:
            signals.append("Critical Security Vulnerability Detected")
        if "production" in environment.lower():
            signals.append("Production Environment Impact")
            
        if not signals:
            signals.append("Standard Functional / Quality Defect Pattern")

        # Use trained models if available
        if self.vectorizer and self.severity_model:
            X_vec = self.vectorizer.transform([combined_text])
            
            sev_pred = self.severity_model.predict(X_vec)[0]
            sev_probs = self.severity_model.predict_proba(X_vec)[0]
            sev_conf = float(np.max(sev_probs))
            
            pri_pred = self.priority_model.predict(X_vec)[0]
            cat_pred = self.category_model.predict(X_vec)[0]
            
            return {
                "predicted_severity": sev_pred,
                "predicted_priority": pri_pred,
                "predicted_category": cat_pred,
                "confidence": round(sev_conf, 2),
                "signals": signals
            }
            
        # Robust Heuristic Fallback if models are not yet trained on disk
        if any(w in raw_text_lower for w in ["sql injection", "crash", "deadlock", "vulnerability"]):
            sev = "Critical"
            pri = "P1"
            cat = "Security" if "sql" in raw_text_lower or "vulnerability" in raw_text_lower else "Functional"
            conf = 0.94
        elif any(w in raw_text_lower for w in ["slow", "latency", "memory leak", "timeout"]):
            sev = "High"
            pri = "P2"
            cat = "Performance"
            conf = 0.88
        elif any(w in raw_text_lower for w in ["ui", "button", "dropdown", "color", "alignment", "typo"]):
            sev = "Low"
            pri = "P4"
            cat = "UI/UX"
            conf = 0.85
        else:
            sev = "Medium"
            pri = "P3"
            cat = "Functional"
            conf = 0.80

        return {
            "predicted_severity": sev,
            "predicted_priority": pri,
            "predicted_category": cat,
            "confidence": conf,
            "signals": signals
        }

ml_service = MLService()
