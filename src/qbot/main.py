from flask import Flask, request, jsonify, render_template
from qbot.models.vector_store import VectorStore
from qbot.utils.document_manager import DocumentManager
import logging
from typing import Dict, Any, Optional
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
vector_store = VectorStore()
document_manager = DocumentManager()

# Add route for web interface
@app.route('/')
def chat_interface():
    """Serve the chat interface"""
    return render_template('chat.html')

def handle_error(error: Exception) -> Dict[str, Any]:
    """Handle different types of errors and return appropriate response"""
    logger.error(f"Error occurred: {str(error)}", exc_info=True)

    if isinstance(error, FileNotFoundError):
        return {"error": "Document file not found"}, 404
    elif isinstance(error, ValueError):
        return {"error": str(error)}, 400
    else:
        return {"error": "Internal server error"}, 500


@app.route('/health', methods=['GET'])
def health_check() -> Dict[str, str]:
    """Health check endpoint"""
    try:
        # Verify vector store is initialized
        if vector_store.collection is None:
            raise Exception("Vector store not initialized")
        return {"status": "healthy"}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {"status": "unhealthy", "error": str(e)}


@app.route('/ask', methods=['POST'])
def ask() -> Dict[str, Any]:
    """Main endpoint for asking questions"""
    start_time = time.time()

    try:
        data = request.json
        if not data:
            raise ValueError("No data provided")

        prompt = data.get('prompt')
        if not prompt:
            raise ValueError("No prompt provided")

        logger.info(f"Received prompt: {prompt}")

        # Generate response
        response = vector_store.generate_response(prompt)

        # Calculate processing time
        processing_time = time.time() - start_time

        logger.info(f"Generated response in {processing_time:.2f} seconds")

        return {
            "response": response,
            "processing_time": f"{processing_time:.2f}s"
        }


    except Exception as e:
        return handle_error(e)

@app.route('/ask-json', methods=['POST'])
def ask_structured() -> Dict[str, Any]:
    """Endpoint for asking questions with JSON-structured responses"""
    start_time = time.time()

    try:
        data = request.json
        if not data:
            raise ValueError("No data provided")

        prompt = data.get('prompt')
        if not prompt:
            raise ValueError("No prompt provided")

        logger.info(f"Received prompt: {prompt}")

        # Generate structured response
        response_data = vector_store.generate_structured_response(prompt)

        # Calculate processing time
        processing_time = time.time() - start_time

        logger.info(f"Generated response in {processing_time:.2f} seconds")

        return {
            "status": "success",
            "data": {
                **response_data,
                "processing_time": f"{processing_time:.2f}s"
            }
        }

    except Exception as e:
        return handle_error(e)

@app.route('/documents', methods=['GET'])
def get_documents() -> Dict[str, Any]:
    """Get all documents in the knowledge base"""
    try:
        documents = document_manager.get_documents()
        return {
            "count": len(documents),
            "documents": documents
        }
    except Exception as e:
        return handle_error(e)


@app.route('/documents', methods=['POST'])
def add_documents() -> Dict[str, Any]:
    """Add new documents to the knowledge base"""
    try:
        data = request.json
        if not data:
            raise ValueError("No data provided")

        documents = data.get('documents')
        if not documents:
            raise ValueError("No documents provided")

        if not isinstance(documents, list):
            raise ValueError("Documents must be provided as a list")

        logger.info(f"Adding {len(documents)} new documents")

        # Add documents
        success = document_manager.add_documents(documents)
        if success:
            # Reinitialize vector store with new documents
            global vector_store
            vector_store = VectorStore()
            return {
                "message": "Documents added successfully",
                "count": len(documents)
            }
        else:
            raise Exception("Failed to add documents")

    except Exception as e:
        return handle_error(e)


@app.route('/documents', methods=['DELETE'])
def clear_documents() -> Dict[str, Any]:
    """Clear all documents from the knowledge base"""
    try:
        success = document_manager.clear_documents()
        if success:
            # Reinitialize vector store with empty collection
            global vector_store
            vector_store = VectorStore()
            return {"message": "All documents cleared successfully"}
        else:
            raise Exception("Failed to clear documents")

    except Exception as e:
        return handle_error(e)


@app.route('/stats', methods=['GET'])
def get_stats() -> Dict[str, Any]:
    """Get statistics about the knowledge base"""
    try:
        documents = document_manager.get_documents()
        return {
            "total_documents": len(documents),
            "average_document_length": sum(len(d) for d in documents) / len(documents) if documents else 0,
            "status": "operational"
        }
    except Exception as e:
        return handle_error(e)


def initialize_app() -> None:
    """Initialize the application"""
    try:
        logger.info("Initializing application...")
        global vector_store
        vector_store = VectorStore()
        logger.info("Application initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize application: {str(e)}")
        raise


if __name__ == "__main__":
    try:
        initialize_app()
        logger.info("Starting QBot server...")
        app.run(host='0.0.0.0', port=8080, debug=True)
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")