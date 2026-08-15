import re
import string

# Standard English stopwords set (lightweight & dependency-free)
STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are",
    "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both",
    "but", "by", "can", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does",
    "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had",
    "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her",
    "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd",
    "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself",
    "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off",
    "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own",
    "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some",
    "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then",
    "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this",
    "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we",
    "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's",
    "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't",
    "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself",
    "yourselves"
}

def preprocess_text(text: str) -> str:
    """
    Clean, normalize, tokenize, and strip stopwords from bug text.
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Lowercase
    text = text.lower()
    
    # Remove HTML tags if present
    text = re.sub(r"<[^>]+>", " ", text)
    
    # Remove URLs
    text = re.sub(r"http\S+|www\S+|https\S+", " ", text, flags=re.MULTILINE)
    
    # Remove special punctuation and digits noise
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\d+", " ", text)
    
    # Tokenize and remove stopwords
    tokens = text.split()
    cleaned_tokens = [w for w in tokens if w not in STOPWORDS and len(w) > 1]
    
    return " ".join(cleaned_tokens)

def combine_bug_features(
    title: str,
    description: str,
    steps_to_reproduce: str = "",
    expected_result: str = "",
    actual_result: str = ""
) -> str:
    """
    Combine all textual fields of a bug report into a unified representation.
    """
    parts = [
        title or "",
        description or "",
        steps_to_reproduce or "",
        expected_result or "",
        actual_result or ""
    ]
    raw_combined = " ".join(parts)
    return preprocess_text(raw_combined)
