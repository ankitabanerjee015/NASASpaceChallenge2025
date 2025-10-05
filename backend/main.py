from fastapi import FastAPI, Query
from backend.data_pipeline import read_csv, fetch_abstract
from backend.summarizer import summarize
from backend.semantic_search import get_similar_publications, preload_embeddings
from backend.knowledge_graph import get_graph_data

import logging

app = FastAPI()
CSV_PATH = "data/SB_publication_PMC.csv"

publications = read_csv(CSV_PATH)
preload_embeddings(publications)

@app.get("/health")
def health():
    return {"status": "ok", "count": len(publications)}

@app.get("/publications")
def list_publications(
    skip: int = Query(0, ge=0, description="Items to skip"),
    limit: int = Query(20, ge=1, le=100, description="Max items to return"),
):
    page = publications[skip:skip + limit]
    result = []

    def ensure_dict(pub):
        if isinstance(pub, dict):
            return pub
        if hasattr(pub, "to_dict"):
            return pub.to_dict()
        if isinstance(pub, (tuple, list)):
            keys = ["Title", "Link"]  # adjust to match your publication fields
            return {k: v for k, v in zip(keys, pub)}
        try:
            return dict(pub)
        except Exception as e:
            logging.error(f"Could not convert pub to dict: {type(pub)}, {pub}, error: {e}")
            return None

    def build_item(pub, abstract="", summary=""):
        if pub is None:
            return None
        try:
            item = {**pub, "abstract": abstract, "summary": summary}
            for k, v in item.items():
                if not isinstance(v, (str, int, float, bool, type(None))):
                    item[k] = str(v)
            return item
        except Exception as e:
            logging.error(f"Could not build item: {type(pub)}, {pub}, error: {e}")
            return None

    # Always fetch abstract and summary for every publication
    for pub in page:
        pub = ensure_dict(pub)
        link = pub.get("Link") if pub else ""
        print(f"Calling fetch_abstract for: {link}")
        abstract = fetch_abstract(link) if link else ""
        print(f"Fetched abstract: {abstract[:100]}")  # <--- Add this line
        if not isinstance(abstract, str):
            abstract = str(abstract) if abstract is not None else ""
        summary = summarize(abstract) if abstract else ""
        if not isinstance(summary, str):
            summary = str(summary) if summary is not None else ""
        item = build_item(pub, abstract, summary)
        if item is not None:
            result.append(item)

    return {"items": result, "count": len(publications), "returned": len(result), "skip": skip, "limit": limit}

@app.get("/search")
def search_publications(query: str = Query(..., description="Search query (natural language)")):
    return get_similar_publications(query)

@app.get("/knowledge-graph")
def knowledge_graph():
    return get_graph_data(publications)
