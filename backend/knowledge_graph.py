def get_graph_data(publications):
    # Example structure: nodes (publications, topics), edges (relations)
    return {
        "nodes": [
            {"id": "pub1", "label": "Publication 1", "type": "publication"},
            {"id": "topic1", "label": "Microgravity", "type": "topic"},
        ],
        "edges": [
            {"source": "pub1", "target": "topic1", "type": "has_topic"},
        ]
    }
