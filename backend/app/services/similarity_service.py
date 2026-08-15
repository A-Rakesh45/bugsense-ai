from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.models.bug import Bug
from training.preprocess import combine_bug_features

def find_top_similar_bugs(
    db: Session,
    current_bug_id: int,
    title: str,
    description: str,
    steps_to_reproduce: str = "",
    expected_result: str = "",
    actual_result: str = "",
    top_n: int = 5
) -> List[Dict[str, Any]]:
    
    historical_bugs = db.query(Bug).all()
    if not historical_bugs:
        return []
        
    current_text = combine_bug_features(title, description, steps_to_reproduce, expected_result, actual_result)
    
    bug_ids = []
    corpus = []
    bug_map = {}
    
    for b in historical_bugs:
        if b.id == current_bug_id:
            continue
        comb = combine_bug_features(b.title, b.description, b.steps_to_reproduce, b.expected_result, b.actual_result)
        corpus.append(comb)
        bug_ids.append(b.id)
        bug_map[b.id] = b
        
    if not corpus:
        return []
        
    try:
        vectorizer = TfidfVectorizer(max_features=3000, ngram_range=(1, 2))
        corpus_vectors = vectorizer.fit_transform(corpus)
        current_vector = vectorizer.transform([current_text])
        
        sim_scores = cosine_similarity(current_vector, corpus_vectors)[0]
        
        indexed_scores = list(zip(bug_ids, sim_scores))
        indexed_scores.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for bug_id, score in indexed_scores[:top_n]:
            if score > 0.05: # Minimum cutoff threshold
                b = bug_map[bug_id]
                pred_sev = b.prediction.predicted_severity if b.prediction else "Medium"
                results.append({
                    "id": b.id,
                    "title": b.title,
                    "status": b.status,
                    "module": b.module,
                    "similarity_score": round(float(score), 4),
                    "similarity_percentage": round(float(score) * 100, 1),
                    "predicted_severity": pred_sev,
                    "created_at": b.created_at
                })
        return results
    except Exception as e:
        print(f"Error computing similarity scores: {e}")
        return []
