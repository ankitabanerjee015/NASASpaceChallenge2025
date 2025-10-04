import numpy as np
from typing import List, Dict, Tuple, Any

# If you use sklearn, you can keep it, but we'll make our own safe cosine
def _cosine_sim(a, b) -> float:
    """
    Robust cosine similarity: returns a Python float (not a numpy array).
    """
    va = np.asarray(a, dtype=np.float32).ravel()
    vb = np.asarray(b, dtype=np.float32).ravel()
    if va.size == 0 or vb.size == 0:
        return 0.0
    denom = (np.linalg.norm(va) * np.linalg.norm(vb)) + 1e-9
    if denom == 0.0:
        return 0.0
    return float(np.dot(va, vb) / denom)  # <-- ensure scalar float

# If you cache/prepare embeddings at startup:
def preload_embeddings(publications: List[Dict[str, Any]]):
    """
    Ensure all pub['embedding'] are float32 numpy arrays (or None).
    """
    for pub in publications:
        emb = pub.get("embedding")
        if emb is None:
            continue
        # Handle strings like "[0.1, 0.2, ...]" or lists
        if isinstance(emb, str):
            try:
                # very defensive: try to parse serialized list
                emb = np.array(eval(emb), dtype=np.float32)  # or json.loads if JSON
            except Exception:
                emb = None
        else:
            emb = np.asarray(emb, dtype=np.float32)
        pub["embedding"] = emb

# Example stub — replace with your actual model call
def _embed_text(text: str) -> np.ndarray:
    """
    Return a vector for the query. Must be same dimension as pub embeddings.
    Replace with your real embedding code.
    """
    # TODO: swap with your embedding function
    # return model.encode(text).astype(np.float32)
    # TEMP fallback (avoid crashes if not wired yet):
    return np.zeros(768, dtype=np.float32)

def get_similar_publications(query: str, k: int = 10) -> List[Dict[str, Any]]:
    """
    Compute cosine similarity between the query embedding and each publication embedding,
    sort by score (DESC), and return top-k with a scalar 'score'.
    Falls back to simple text search if embeddings are not available.
    """
    q_emb = _embed_text(query)
    scored: List[Tuple[float, Dict[str, Any]]] = []
    has_embeddings = False

    # You'll probably import publications or receive them — adapt accordingly.
    # If this function already has access to a global 'publications', use it.
    from backend.main import publications  # if you keep it simple; otherwise inject

    for pub in publications:
        emb = pub.get("embedding")
        if emb is None or (isinstance(emb, np.ndarray) and emb.size == 0):
            continue
        has_embeddings = True
        score = _cosine_sim(q_emb, emb)   # <-- scalar float
        scored.append((score, pub))

    # Fallback to simple text search if no embeddings are available
    if not has_embeddings:
        query_lower = query.lower()
        for pub in publications:
            title = pub.get("Title", "").lower()
            # Simple relevance score based on query term matching
            score = 0.0
            if query_lower in title:
                # Exact match in title gets high score
                score = 1.0
            elif any(term in title for term in query_lower.split()):
                # Partial match gets lower score
                score = 0.5
            
            if score > 0:
                scored.append((score, pub))

    # IMPORTANT: sort by key (score), not by whole tuple/array
    scored.sort(key=lambda x: x[0], reverse=True)

    top = []
    for score, pub in scored[:k]:
        item = dict(pub)  # shallow copy so we don't mutate originals
        item["score"] = round(float(score), 4)  # ensure json-serializable scalar
        top.append(item)
    return top
