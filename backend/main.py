from fastapi import FastAPI, Query
from backend.data_pipeline import read_csv, fetch_abstract
from backend.summarizer import summarize
from backend.semantic_search import get_similar_publications, preload_embeddings
from backend.knowledge_graph import get_graph_data

app = FastAPI()

CSV_PATH = "data/SB_publication_PMC.csv"

# Preload publications and embeddings on startup
publications = read_csv(CSV_PATH)
preload_embeddings(publications)

@app.get("/publications")
def list_publications():
    result = []
    for pub in publications:
        abstract = fetch_abstract(pub['Link'])
        pub['abstract'] = abstract
        pub['summary'] = summarize(abstract) if abstract else ""
        result.append(pub)
    return result

@app.get("/search")
def search_publications(query: str = Query(..., description="Search query (natural language)")):
    return get_similar_publications(query)

@app.get("/knowledge-graph")
def knowledge_graph():
    return get_graph_data(publications)