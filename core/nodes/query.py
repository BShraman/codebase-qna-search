from core.state import CodebaseState

class Query:
    def __init__(self):
        from core.config import config

        self.llm = config.LLM
        self.SYSTEM_PROMPT = (
            "You are a codebase expert assistant. Follow these rules:\n"
            "- Provide concise, accurate answers about the code\n"
            "- Always cite file sources when available\n"
            "- Reject off-topic requests\n")

    def query_vector_db(self, state: CodebaseState):
        """Document Querying"""
        from llama_index.core import VectorStoreIndex
        from llama_index.vector_stores.chroma import ChromaVectorStore
        import chromadb

        collection_name = state.get("collection_name")
        persist_dir = state.get("persist_dir")

        # Reload the existing index (no re-indexing!)
        chroma_client = chromadb.PersistentClient(path=persist_dir)
        chroma_collection = chroma_client.get_collection(collection_name)
        vector_store = ChromaVectorStore(chroma_client=chroma_client, chroma_collection=chroma_collection)
        index = VectorStoreIndex.from_vector_store(vector_store)

        # Query anytime
        query = state.get("query")
        input = f"System: {self.SYSTEM_PROMPT}\nUser: {query}"

        chat_engine = index.as_chat_engine(chat_mode="openai", 
                                           llm=self.llm, 
                                           verbose=True,
                                           max_iterations=5)
        
        response = chat_engine.chat(input)

        state.update({
        "response": str(response),
        "source_nodes": list({node.metadata.get("file_name", "Unknown File") for node in response.source_nodes})
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

