import os
from dotenv import load_dotenv
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI
from llama_index.embeddings.huggingface_api import HuggingFaceInferenceAPIEmbedding
import logging
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

class Config:
    SERVICE:str = os.getenv("SERVICE","openai")
    HUGGING_FACE_HUB_TOKEN:str = os.getenv("HUGGING_FACE_HUB_TOKEN","")
    OPENAI_API_KEY:str = os.getenv("OPENAI_API_KEY","")
    DOC_PATH:str = os.getenv("DOC_PATH","./data/codebase")
    COLLECTION_NAME:str = os.getenv("COLLECTION_NAME","code_review_agent")
    PERSIST_DIR:str = os.getenv("PERSIST_DIR","./data/vectordb")

    SYSTEM_MESSAGE = "You are a helpful assistant specialized in answering questions and retrieving information about the codebase. Provide accurate and concise responses."
    if SERVICE == "openai":
        EMBED_MODEL = OpenAIEmbedding()
        LLM = OpenAI()
    else:
        logger.info("Service is not an OpenAI")
        
config = Config()