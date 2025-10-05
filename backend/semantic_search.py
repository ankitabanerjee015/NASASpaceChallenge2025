import numpy as np
from typing import List, Dict, Tuple, Any
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

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
    for pub in publications:
        title = pub.get("Title", "")
        summary = pub.get("summary", "")
        abstract = pub.get("abstract", "")
        text = " ".join([title, summary, abstract]).strip()
        if text == "":
            pub["embedding"] = None
        else:
            pub["embedding"] = model.encode(text, show_progress_bar=False).astype(np.float32)


def _embed_text(text: str) -> np.ndarray:
    """
    Return a vector for the query. Must be same dimension as pub embeddings.
    Uses a real embedding model.
    """
    return model.encode(text, show_progress_bar=False).astype(np.float32)

def get_similar_publications(query: str, k: int = 10) -> List[Dict[str, Any]]:
    q_emb = _embed_text(query)
    scored: List[Tuple[float, Dict[str, Any]]] = []

    from backend.main import publications

    for pub in publications:
        emb = pub.get("embedding")
        if emb is None or (isinstance(emb, np.ndarray) and emb.size == 0):
            continue
        score = _cosine_sim(q_emb, emb)
        scored.append((score, pub))

    scored.sort(key=lambda x: x[0], reverse=True)

    top = []
    for score, pub in scored[:k]:
        item = dict(pub)
        item["score"] = round(float(score), 4)
        # Convert embedding to a list for JSON serialization
        if isinstance(item.get("embedding"), np.ndarray):
            item["embedding"] = item["embedding"].tolist()
        top.append(item)
    return top
