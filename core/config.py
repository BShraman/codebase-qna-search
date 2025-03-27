import os
from dotenv import load_dotenv
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI
from llama_index.embeddings.huggingface_api import HuggingFaceInferenceAPIEmbedding

# Load environment variables from .env file
load_dotenv()

class Config:
    SERVICE:str = os.getenv("SERVICE","openai")
    HUGGING_FACE_HUB_TOKEN:str = os.getenv("HUGGING_FACE_HUB_TOKEN","")
    OPENAI_API_KEY:str = os.getenv("OPENAI_API_KEY","")

    SYSTEM_MESSAGE = "You are a helpful assistant specialized in answering questions and retrieving information about the codebase. Provide accurate and concise responses."
    if SERVICE == "openai":
        EMBED_MODEL = OpenAIEmbedding()
        LLM = HuggingFaceInferenceAPI(model_name="Qwen/Qwen2.5-Coder-32B-Instruct")
        #LLM = OpenAI()
    else:    
        #EMBED_MODEL = HuggingFaceInferenceAPIEmbedding(model_name="BAAI/bge-small-en-v1.5")
        EMBED_MODEL = OpenAIEmbedding()
        LLM = HuggingFaceInferenceAPI(model_name="Qwen/Qwen2.5-Coder-32B-Instruct")

config = Config()