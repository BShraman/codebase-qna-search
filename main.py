import sys
import nest_asyncio
from core.graph.state_graph import StateGraph

nest_asyncio.apply()

def main():
    query = "How Many Function are there in total?"

    # Initialize and process the codebase
    compiled_graph = StateGraph().compiled_graph()
    result = compiled_graph.invoke({
        "doc_path": "./data",
        "is_document_parsing": True,
        "collection_name": "codebase",
        "persist_dir": "./data/vectordb",
        "query": query,
        "is_chromadb_exists": False,
        "document_nodes": None,
    })

    return result

if __name__ == "__main__":
    main()