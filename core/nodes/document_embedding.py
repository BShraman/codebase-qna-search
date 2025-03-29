
from core.state import CodebaseState
from core.config import config

class DocumentEmbedding:
    def __init__(self):
        import logging
        logging.basicConfig(level=logging.INFO) 
        self.logger = logging.getLogger(__name__)

        self.OPENAI_API_KEY = config.OPENAI_API_KEY
        self.embedding_model = config.EMBED_MODEL

    def document_loader(self, state: CodebaseState):
        """
        Loads documents from a specified directory and stores them in the provided state.
        This method uses the `SimpleDirectoryReader` to read documents from the directory
        specified in the `doc_path` key of the `state` object. The loaded documents are
        then stored in the `documents` key of the `state`.
        Args:
            state (CodebaseState): The state object containing the `doc_path` key, which
                specifies the directory path to load documents from.
        Returns:
            CodebaseState: The updated state object with the loaded documents stored
            under the `documents` key.
        """
        
        from llama_index.core import SimpleDirectoryReader

        doc_path = state.get("doc_path")
        if not doc_path:
            raise ValueError("No document path found in state!")

        # Load documents
        reader = SimpleDirectoryReader(input_dir=doc_path)
        documents = reader.load_data()

        if not documents:
            raise ValueError("No documents found in the specified path!")

        # Store documents in state
        state["documents"] = documents
        self.logger.info("Document Loader Completed")
        return state

    def document_embedding(self, state: CodebaseState):
        """
        Processes and embeds documents into nodes using a pipeline of transformations.
        This method retrieves documents from the provided `CodebaseState`, applies a series of 
        transformations including sentence splitting, title extraction, and embedding, and stores 
        the resulting nodes back into the state.
        Args:
            state (CodebaseState): The state object containing the documents to be processed.
        Returns:
            CodebaseState: The updated state containing the processed nodes.
        Steps:
            1. Retrieve documents from the state.
            2. Apply transformations using the `IngestionPipeline`:
                - Sentence splitting with a chunk size of 512 and overlap of 50.
                - Title extraction.
                - Embedding using the specified embedding model.
            3. Run the pipeline asynchronously to generate nodes.
            4. Store the resulting nodes in the state.
            5. Print a completion message and return the updated state.
        """
        
        from llama_index.core.node_parser import SentenceSplitter
        from llama_index.core.extractors import TitleExtractor
        from llama_index.core.ingestion import IngestionPipeline
        import asyncio

        # Retrieve documents from state
        documents = state.get("documents")


        pipeline = IngestionPipeline(
            transformations=[
                SentenceSplitter(chunk_size=512, chunk_overlap=50), # Allows more complete context
                TitleExtractor(),
                self.embedding_model,
            ]
        )
        
        nodes = asyncio.run(pipeline.arun(documents=documents))

        if not nodes:
            raise ValueError("No nodes found in state!")

        # Store nodes in state
        state["nodes"] = nodes
        self.logger.info("Document Embedding Completed")

        return state