
import asyncio

from core.state import CodebaseState
from core.config import config

class DocumentEmbedding:
    def __init__(self):
        from huggingface_hub import login

        self.OPENAI_API_KEY = config.OPENAI_API_KEY
        self.HUGGING_FACE_HUB_TOKEN = config.HUGGING_FACE_HUB_TOKEN
        self.embedding_model = config.EMBED_MODEL

        login(token=self.HUGGING_FACE_HUB_TOKEN)

    def document_loader(self, state: CodebaseState):
        """Document Loader""" 
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
        print("Document Loader Completed")
        return state

    def document_embedding(self, state: CodebaseState):
        """Document Embedding"""
        from llama_index.core.node_parser import SentenceSplitter
        from llama_index.embeddings.openai import OpenAIEmbedding
        from llama_index.core.extractors import TitleExtractor
        from llama_index.core.ingestion import IngestionPipeline
        import asyncio

        # Retrieve documents from state
        documents = state.get("documents")

        # Convert documents into nodes
        # splitter = SentenceSplitter(chunk_size=1024)
        pipeline = IngestionPipeline(
            transformations=[
                SentenceSplitter(chunk_size=25, chunk_overlap=0),
                TitleExtractor(),
                self.embedding_model,
            ]
        )
        #nodes = splitter.get_nodes_from_documents(documents)
        nodes = asyncio.run(pipeline.arun(documents=documents))

        if not nodes:
            raise ValueError("No nodes found in state!")

        # Store nodes in state
        state["nodes"] = nodes
        print("Document Embedding Completed")

        return state