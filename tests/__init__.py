"""
QBot test suite initialization and configuration.
"""

import os
import sys
import pytest
from typing import Generator, Any

# Add src directory to Python path for test imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Test configuration
TEST_CONFIG = {
    'OLLAMA_HOST': 'localhost',
    'OLLAMA_PORT': '11434',
    'DEFAULT_MODEL': 'llama3.2',
    'EMBEDDING_MODEL': 'mxbai-embed-large'
}

# Mock data for tests
MOCK_DOCUMENTS = [
    "Test document 1 about llamas and their habits",
    "Test document 2 about camel family relationships",
    "Test document 3 about South American animals"
]

MOCK_EMBEDDINGS = [
    [0.1, 0.2, 0.3],  # Mock embedding vector
    [0.4, 0.5, 0.6],  # Mock embedding vector
    [0.7, 0.8, 0.9]  # Mock embedding vector
]


@pytest.fixture
def mock_vector_store() -> Generator[Any, None, None]:
    """Fixture for creating a mock vector store."""
    from qbot.models.vector_store import VectorStore

    # Create a mock vector store
    store = VectorStore()

    # Add mock data
    for i, (doc, embedding) in enumerate(zip(MOCK_DOCUMENTS, MOCK_EMBEDDINGS)):
        store.collection.add(
            ids=[str(i)],
            embeddings=[embedding],
            documents=[doc]
        )

    yield store


@pytest.fixture
def mock_ollama_response() -> Dict[str, Any]:
    """Fixture for mocking Ollama API responses."""
    return {
        'response': 'This is a mock response from the language model.',
        'context': None,
        'done': True
    }


@pytest.fixture
def mock_config() -> Dict[str, str]:
    """Fixture for providing test configuration."""
    return TEST_CONFIG.copy()


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers",
        "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers",
        "slow: mark test as slow running"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection based on markers and conditions."""
    if config.getoption("--skip-slow"):
        skip_slow = pytest.mark.skip(reason="Skip slow tests")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)