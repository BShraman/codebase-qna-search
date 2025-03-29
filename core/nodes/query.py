from core.state import CodebaseState

class Query:
    def __init__(self):
        from core.config import config
        import logging
        logging.basicConfig(level=logging.INFO) 
 
        self.logger = logging.getLogger(__name__)
        self.llm = config.LLM
        self.SYSTEM_PROMPT = (
            "You are a codebase expert assistant. Follow these strict rules:\n"
            "- Always retrieve answers **only from the provided documents**; do not make up information.\n"
            "- **Cite the exact file names and locations** whenever possible.\n"
            "- Provide structured, precise answers with **minimal but relevant explanations**.\n"
            "- If the user's question requires code, provide a **direct snippet with proper formatting**.\n"
            "- If a question is unclear, ask clarifying questions instead of guessing.\n"
            "- If information is unavailable in the documents, explicitly say so.\n"
            "- Reject off-topic requests and avoid discussing anything unrelated to the codebase.\n"
            "- If the question is about a function, class, or module, include relevant metadata (e.g., parameters, return types, and docstrings if available).\n"
            )

    def query_vector_db(self, state: CodebaseState):
        """
        Queries a vector database using a pre-existing index and returns the response along with source nodes.
        This method interacts with a vector database to retrieve information based on a user-provided query.
        It uses a persistent Chroma vector store and a pre-built index to perform the query without re-indexing.
        The response is generated using a chat engine powered by a language model.
        Args:
            state (CodebaseState): The current state of the codebase, containing necessary parameters such as:
                - "collection_name" (str): The name of the collection in the vector database.
                - "persist_dir" (str): The directory where the vector database is persisted.
                - "query" (str): The user-provided query string.
        Returns:
            CodebaseState: The updated state containing:
                - "response" (str): The response generated by the chat engine.
                - "source_nodes" (list): A list of unique file names from the source nodes used in the response.
        """

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
        # input = f"System: {self.SYSTEM_PROMPT}\nUser: {query}"
        input = f"""
        System: {self.SYSTEM_PROMPT}

        Context:
        - You have access to codebase documents.
        - If a function, class, or module is mentioned, locate it and provide structured details.
        - Cite the exact file path(s) when available.

        Instructions:
        - Answer only based on provided documents.
        - If unsure, explicitly state that the information is not available.
        - Format responses with headers, bullet points, and code blocks where necessary.

        User Query:
        {query}
        """

        chat_engine = index.as_chat_engine(chat_mode="openai", 
                                           llm=self.llm, 
                                           verbose=False,
                                           max_iterations=5)
        
        response = chat_engine.chat(input)

        state.update({
        "response": str(response),
        "source_nodes": list({node.metadata.get("file_name", "Unknown File") for node in response.source_nodes})
        })

        return state
    
    def get_response(self, state: CodebaseState):
        """
        Retrieves the response from the language model (LLM) stored in the given state.
        This method checks if the "response" key exists in the provided `state`. If the key
        is missing, it raises a `ValueError` indicating that the `query_documents` node
        must be executed first. It also logs the final response and any associated source
        documents for debugging purposes.
        Args:
            state (CodebaseState): The current state object containing the response and 
                                   optionally the source nodes.
        Returns:
            dict: A dictionary containing the final output with the key "final_output".

        """
        if "response" not in state:
            raise ValueError("Run query_documents node first")
        
        # You can access both response and source nodes
        self.logger.info(f"Final Response: {state['response']}")
        self.logger.info(f"Source Documents: {state.get('source_nodes', [])}")
        
        # Return modified state or just the response
        return {"final_output": state["response"]}

