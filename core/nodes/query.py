from core.state import CodebaseState

class Query:
    def __init__(self):
        from core.config import config

        self.llm = config.LLM

    def query_vector_db(self, state: CodebaseState):
        """Document Querying"""
        from llama_index.core import load_index_from_storage
        from llama_index.core import VectorStoreIndex
        from llama_index.vector_stores.chroma import ChromaVectorStore
        import chromadb
        from llama_index.llms.openai import OpenAI

        collection_name = state.get("collection_name")
        persist_dir = state.get("persist_dir")


        # Reload the existing index (no re-indexing!)
        chroma_client = chromadb.PersistentClient(path=persist_dir)
        chroma_collection = chroma_client.get_collection(collection_name)
        vector_store = ChromaVectorStore(chroma_client=chroma_client, chroma_collection=chroma_collection)
        index = VectorStoreIndex.from_vector_store(vector_store)  # Reuses existing embeddings

        # Query anytime
        query = state.get("query")
        query_engine = index.as_query_engine(llm=self.llm,response_mode="tree_summarize")
        response = query_engine.query(query)

        state.update({
            "response": str(response),
            "source_nodes": [node.text for node in response.source_nodes]  # Optional
        })

        return state
    
    def get_response(self, state: CodebaseState):
        """Get the response from the LLM"""
        if "response" not in state:
            raise ValueError("Run query_documents node first")
        
        # You can access both response and source nodes
        print(f"Final Response: {state['response']}")
        print(f"Source Documents: {state.get('source_nodes', [])}")
        
        # Return modified state or just the response
        return {"final_output": state["response"]}

