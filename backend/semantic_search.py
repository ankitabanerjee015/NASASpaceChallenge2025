def get_graph_data(publications):
    # Example: build a simple knowledge graph connecting publications by shared keywords in titles
    nodes = []
    edges = []
    keyword_map = {}

    for idx, pub in enumerate(publications):
        node_id = f"pub{idx}"
        nodes.append({"id": node_id, "label": pub["Title"], "type": "publication"})
        # Extract keywords (very simple: split title by space)
        for word in pub["Title"].split():
            keyword = word.lower().strip(",.:-")
            if len(keyword) > 3:
                if keyword not in keyword_map:
                    keyword_map[keyword] = f"kw_{keyword}"
                    nodes.append({"id": keyword_map[keyword], "label": keyword, "type": "keyword"})
                edges.append({"source": node_id, "target": keyword_map[keyword], "type": "has_keyword"})
    return {"nodes": nodes, "edges": edges}