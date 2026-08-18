import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from preprocess import combine_bug_features

def train_and_save_models():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    dataset_path = os.path.join(base_dir, "training", "bug_dataset.csv")
    models_dir = os.path.join(base_dir, "models")
    os.makedirs(models_dir, exist_ok=True)
    
    print(f"Generating high-precision balanced dataset at {dataset_path}...")
    from generate_synthetic_data import generate_dataset
    generate_dataset(dataset_path, 1600)
        
    print(f"Loading dataset from {dataset_path}...")
    df = pd.read_csv(dataset_path)
    
    print("Preprocessing bug text features...")
    cleaned_texts = []
    for idx, row in df.iterrows():
        combined = combine_bug_features(
            title=str(row.get("title", "")),
            description=str(row.get("description", "")),
            steps_to_reproduce=str(row.get("steps_to_reproduce", "")),
            expected_result=str(row.get("expected_result", "")),
            actual_result=str(row.get("actual_result", ""))
        )
        cleaned_texts.append(combined)
        
    df["combined_text"] = cleaned_texts
    
    X = df["combined_text"]
    y_severity = df["severity"]
    y_priority = df["priority"]
    y_category = df["category"]
    
    # SINGLE train_test_split on index to keep X, y_sev, y_pri, y_cat aligned 100%!
    train_idx, test_idx = train_test_split(
        np.arange(len(df)), test_size=0.2, random_state=42, stratify=y_category
    )
    
    X_train = X.iloc[train_idx]
    y_sev_train = y_severity.iloc[train_idx]
    y_pri_train = y_priority.iloc[train_idx]
    y_cat_train = y_category.iloc[train_idx]
    
    print("Fitting TF-IDF Vectorizer...")
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2), sublinear_tf=True)
    X_train_tfidf = vectorizer.fit_transform(X_train)
    
    print("Training Severity Model (Logistic Regression)...")
    severity_model = LogisticRegression(C=5.0, max_iter=1000, random_state=42)
    severity_model.fit(X_train_tfidf, y_sev_train)
    
    print("Training Priority Model (Logistic Regression)...")
    priority_model = LogisticRegression(C=5.0, max_iter=1000, random_state=42)
    priority_model.fit(X_train_tfidf, y_pri_train)
    
    print("Training Category Model (Logistic Regression)...")
    category_model = LogisticRegression(C=5.0, max_iter=1000, random_state=42)
    category_model.fit(X_train_tfidf, y_cat_train)
    
    # Save Joblib Artifacts
    vec_file = os.path.join(models_dir, "tfidf_vectorizer.joblib")
    sev_file = os.path.join(models_dir, "severity_model.joblib")
    pri_file = os.path.join(models_dir, "priority_model.joblib")
    cat_file = os.path.join(models_dir, "category_model.joblib")
    
    joblib.dump(vectorizer, vec_file)
    joblib.dump(severity_model, sev_file)
    joblib.dump(priority_model, pri_file)
    joblib.dump(category_model, cat_file)
    
    print("All ML models successfully trained and serialized to disk!")
    print(f"- Vectorizer: {vec_file}")
    print(f"- Severity Model: {sev_file}")
    print(f"- Priority Model: {pri_file}")
    print(f"- Category Model: {cat_file}")

if __name__ == "__main__":
    train_and_save_models()
