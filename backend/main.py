from fastapi import FastAPI, Query
from backend.data_pipeline import read_csv, fetch_abstract
from backend.summarizer import summarize
from backend.semantic_search import get_similar_publications, preload_embeddings
from backend.knowledge_graph import get_graph_data

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
    include_abstract: bool = Query(False, description="If true, fetch abstract & summary (slower)"),
):
    # slice first, then optionally enrich
    page = publications[skip:skip + limit]
    result = []

    if not include_abstract:
        # fast path: no network calls
        for pub in page:
            result.append({
                **pub,
                "abstract": "",
                "summary": "",
            })
        return {"items": result, "count": len(publications), "returned": len(result), "skip": skip, "limit": limit}

    # slow path: fetch abstract per item (do this only for small pages)
    for pub in page:
        link = pub.get("Link")
        abstract = fetch_abstract(link) if link else ""
        summary = summarize(abstract) if abstract else ""
        result.append({**pub, "abstract": abstract, "summary": summary})

    return {"items": result, "count": len(publications), "returned": len(result), "skip": skip, "limit": limit}

@app.get("/search")
def search_publications(query: str = Query(..., description="Search query (natural language)")):
    return get_similar_publications(query)

@app.get("/knowledge-graph")
def knowledge_graph():
    return get_graph_data(publications)
