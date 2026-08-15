import os
import json
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_recall_fscore_support
from preprocess import combine_bug_features

def evaluate_models():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    dataset_path = os.path.join(base_dir, "training", "bug_dataset.csv")
    models_dir = os.path.join(base_dir, "models")
    
    vec_file = os.path.join(models_dir, "tfidf_vectorizer.joblib")
    sev_file = os.path.join(models_dir, "severity_model.joblib")
    pri_file = os.path.join(models_dir, "priority_model.joblib")
    cat_file = os.path.join(models_dir, "category_model.joblib")
    
    if not (os.path.exists(vec_file) and os.path.exists(sev_file)):
        print("Trained models not found. Please run train_models.py first.")
        return
        
    print("Loading models and vectorizer...")
    vectorizer = joblib.load(vec_file)
    severity_model = joblib.load(sev_file)
    priority_model = joblib.load(pri_file)
    category_model = joblib.load(cat_file)
    
    df = pd.read_csv(dataset_path)
    cleaned_texts = [
        combine_bug_features(
            row.get("title", ""),
            row.get("description", ""),
            row.get("steps_to_reproduce", ""),
            row.get("expected_result", ""),
            row.get("actual_result", "")
        )
        for _, row in df.iterrows()
    ]
    df["combined_text"] = cleaned_texts
    
    X = df["combined_text"]
    y_severity = df["severity"]
    y_priority = df["priority"]
    y_category = df["category"]
    
    # Split
    _, X_test, _, y_sev_test = train_test_split(X, y_severity, test_size=0.2, random_state=42, stratify=y_severity)
    _, _, _, y_pri_test = train_test_split(X, y_priority, test_size=0.2, random_state=42, stratify=y_priority)
    _, _, _, y_cat_test = train_test_split(X, y_category, test_size=0.2, random_state=42, stratify=y_category)
    
    X_test_tfidf = vectorizer.transform(X_test)
    
    # Predictions
    y_sev_pred = severity_model.predict(X_test_tfidf)
    y_pri_pred = priority_model.predict(X_test_tfidf)
    y_cat_pred = category_model.predict(X_test_tfidf)
    
    def calc_metrics(y_true, y_pred, labels):
        acc = accuracy_score(y_true, y_pred)
        p, r, f1, _ = precision_recall_fscore_support(y_true, y_pred, average="weighted")
        cm = confusion_matrix(y_true, y_pred, labels=labels).tolist()
        return {
            "accuracy": round(float(acc) * 100, 2),
            "precision": round(float(p) * 100, 2),
            "recall": round(float(r) * 100, 2),
            "f1_score": round(float(f1) * 100, 2),
            "labels": labels,
            "confusion_matrix": cm
        }
    
    report = {
        "model_version": "v1.0",
        "dataset_size": len(df),
        "test_split_size": len(X_test),
        "feature_count": len(vectorizer.get_feature_names_out()),
        "severity_metrics": calc_metrics(y_sev_test, y_sev_pred, ["Critical", "High", "Medium", "Low"]),
        "priority_metrics": calc_metrics(y_pri_test, y_pri_pred, ["P1", "P2", "P3", "P4"]),
        "category_metrics": calc_metrics(y_cat_test, y_cat_pred, list(np.unique(y_category)))
    }
    
    report_file = os.path.join(models_dir, "evaluation_report.json")
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        
    print("\n========== MODEL EVALUATION SUMMARY ==========")
    print(f"Severity Model  -> Accuracy: {report['severity_metrics']['accuracy']}% | F1: {report['severity_metrics']['f1_score']}%")
    print(f"Priority Model  -> Accuracy: {report['priority_metrics']['accuracy']}% | F1: {report['priority_metrics']['f1_score']}%")
    print(f"Category Model  -> Accuracy: {report['category_metrics']['accuracy']}% | F1: {report['category_metrics']['f1_score']}%")
    print(f"\nDetailed evaluation report saved to {report_file}")

if __name__ == "__main__":
    evaluate_models()
