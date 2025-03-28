import nest_asyncio
from core.graph.state_graph import StateGraph

nest_asyncio.apply()

def main(query: str = None):
    from core.config import config
    
    # Initialize and process the codebase
    compiled_graph = StateGraph().compiled_graph()
    result = compiled_graph.invoke({
        "doc_path": config.DOC_PATH,
        "collection_name": config.COLLECTION_NAME,
        "persist_dir": config.PERSIST_DIR,
        "query": query,
        "is_chromadb_exists": False,
        "document_nodes": None,
    })

    return result

if __name__ == "__main__":
    query = "Where is static_analysis_agent method and explain its scope ?"
    main(query)