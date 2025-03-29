from core.state import CodebaseState

class VectorDB:
    def __init__(self):
        import logging
        logging.basicConfig(level=logging.INFO) 
        self.logger = logging.getLogger(__name__)

    def vector_db(self, state: CodebaseState):
        """
        Stores data into a ChromaDB vector database using LlamaIndex.
        This method initializes a persistent ChromaDB client, creates or retrieves
        a collection, and stores nodes into the vector database. It also creates
        a storage context and index for managing the data.
        Args:
            state (CodebaseState): The state object containing the following keys:
                - "collection_name" (str): The name of the ChromaDB collection.
                - "persist_dir" (str): The directory path for persisting the database.
                - "nodes" (list): A list of nodes to be stored in the vector database.
        Returns:
            CodebaseState: The updated state object with the "vector_store" key added.
        """

        from llama_index.core import VectorStoreIndex
        from llama_index.vector_stores.chroma import ChromaVectorStore
        from llama_index.core import StorageContext
        import chromadb

        collection_name = state.get("collection_name")
        persist_dir = state.get("persist_dir")

        # Retrieve nodes from state
        nodes = state.get("nodes")
        if not nodes:
            raise ValueError("No nodes found in state!")

        # Initialize ChromaDB client (persistent mode)
        chroma_client = chromadb.PersistentClient(path=persist_dir)

        # Create a collection explicitly (optional but recommended for customization)
        chroma_collection = chroma_client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        
        # Initialize ChromaVectorStore with the collection
        vector_store = ChromaVectorStore(
            chroma_client=chroma_client,
            chroma_collection=chroma_collection
        )

        # Create storage context and index
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex(
            nodes=nodes,
            storage_context=storage_context,
            show_progress=True  # progress bar for large datasets
        )

        # Persist the index (not strictly necessary for ChromaDB, but useful for LlamaIndex metadata)
        storage_context.persist(persist_dir=persist_dir)

        state["vector_store"] = vector_store
        self.logger.info("Vector DB Processed")
        return state
    
    def get_collection(self, state: CodebaseState) -> bool:
        """Checks if a collection exists in ChromaDB.

        Args:
            persist_dir: The directory where ChromaDB is persisted.
            collection_name: The name of the collection to check.

        Returns:
            True if the collection exists, False otherwise.
        """
        import chromadb
        persist_dir = state.get("persist_dir")
        collection_name = state.get("collection_name")
        try:
            client = chromadb.PersistentClient(path=persist_dir)
            client.get_collection(name=collection_name)  
            chromdb = True
        except Exception as e:
            chromdb = False
            
        state["is_chromadb_exists"] = chromdb

        print("ChromaDB Exists: ", chromdb)
        return state