# tests/test_vector_store.py
import pytest
from qbot.models.vector_store import VectorStore

def test_vector_store_initialization():
    store = VectorStore()
    assert store.collection is not None

def test_generate_response():
    store = VectorStore()
    response = store.generate_response("What are llamas related to?")
    assert isinstance(response, str)
    assert len(response) > 0