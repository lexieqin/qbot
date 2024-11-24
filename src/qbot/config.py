# src/chatbot/config.py
import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'localhost')
OLLAMA_PORT = os.getenv('OLLAMA_PORT', '11434')
DEFAULT_MODEL = os.getenv('DEFAULT_MODEL', 'llama3.2')
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'mxbai-embed-large')