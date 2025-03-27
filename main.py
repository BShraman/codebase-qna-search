import nest_asyncio
from core.graph.state_graph import StateGraph
from IPython.display import Image 

nest_asyncio.apply()

def main(query: str = None):
    
    # Initialize and process the codebase
    compiled_graph = StateGraph().compiled_graph()
    result = compiled_graph.invoke({
        "doc_path": "./data/codebase",
        "collection_name": "code_review_agent",
        "persist_dir": "./data/vectordb",
        "query": query,
        "is_chromadb_exists": False,
        "document_nodes": None,
    })

    return result

if __name__ == "__main__":
    query = "How many method are there in CodeReviewAgent class ?"
    main(query)