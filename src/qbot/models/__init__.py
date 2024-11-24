"""
QBot models module containing vector store and model management components.
"""

from typing import List, Optional, Dict, Any

from .vector_store import VectorStore

__all__ = ['VectorStore']

# Model configuration
DEFAULT_MODELS = {
    'embedding': 'mxbai-embed-large',
    'completion': 'llama3.2'
}

# Vector store settings
VECTOR_STORE_SETTINGS = {
    'collection_name': 'docs',
    'embedding_dimension': 384,
    'metric': 'cosine',
    'max_documents': 10000
}


class ModelRegistry:
    """Registry for managing model availability and versions."""

    @classmethod
    def list_available_models(cls) -> List[str]:
        """List all available models."""
        # Implementation would check Ollama's available models
        pass

    @classmethod
    def verify_model(cls, model_name: str) -> bool:
        """Verify if a model is available."""
        # Implementation would verify model availability
        pass

    @classmethod
    def get_model_info(cls, model_name: str) -> Dict[str, Any]:
        """Get information about a specific model."""
        # Implementation would return model details
        pass