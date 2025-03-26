import os
from typing import TypedDict, Optional

class CodebaseState(TypedDict):
    """
    Represents the state of the codebase with various attributes related to 
    document processing, query handling, and configuration.

    Attributes:
        documents (Optional[str]): Path or reference to the documents being processed.
        nodes (Optional[str]): Serialized or structured representation of nodes.
        index (Optional[str]): Index data for document retrieval.
        source_nodes (Optional[str]): Source nodes used in processing.

        is_document_parsing (Optional[bool]): Indicates if document parsing is in progress.

        query (Optional[str]): User query for which a response is being generated.
        response (Optional[str]): Generated response for the user query.

        doc_path (Optional[str]): Input directory path for documents.

        vector_store (Optional[str]): Path or reference to the vector store.
        chromadb (Optional[str]): Configuration or instance of ChromaDB.
        collection_name (Optional[str]): Name of the collection in ChromaDB.
        persist_dir (Optional[str]): Directory for persisting ChromaDB data.
        is_chromadb_exists (Optional[bool]): Indicates if ChromaDB configuration exists.
    """
    
    # Document-related attributes
    documents: Optional[str]
    nodes: Optional[str]
    index: Optional[str]
    source_nodes: Optional[str]

    # Document parsing state
    is_document_parsing: Optional[bool]

    # User query and response
    query: Optional[str]
    response: Optional[str]

    # Input directory path
    doc_path: Optional[str]

    # ChromaDB configuration
    vector_store: Optional[str]
    chromadb: Optional[str]
    collection_name: Optional[str]
    persist_dir: Optional[str]
    is_chromadb_exists: Optional[bool]