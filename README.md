# QBot - AI-Powered Q&A Bot

A Python-based chatbot using Ollama for LLM inference and ChromaDB for vector storage, enabling context-aware responses.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Docker and Docker Compose
- Ollama installed locally (for development without Docker)
- Kubernetes (K8s) cluster (for deployment)

### Installation

1. Clone the repository
```bash
git clone https://github.com/lexieqin/qbot.git
cd qbot
```

2. Using Docker (Recommended)
```bash
# Build and run all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d
```

3. Local Development Setup
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Unix/macOS
.\venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .
```

## 💻 Usage

### Running the Chatbot

1. Using Docker:
```bash
docker-compose up
```

2. Local Development:
```bash
# Start Ollama service
ollama serve

# In a new terminal
python -m src.chatbot.main
```

### API Endpoints

#### Chat Endpoint
```bash
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What are llamas related to?"}'
```

Response format:
```json
{
    "response": "Based on the information, llamas are members of the camelid family and are closely related to vicuñas and camels."
}
```

## 🏗️ Project Structure
```
chatbot_project/
├── src/
│   └── chatbot/
│       ├── main.py          # Flask application
│       ├── config.py        # Configuration settings
│       ├── utils/           # Utility functions
│       └── models/          # Vector store implementation
├── tests/                   # Test files
├── Dockerfile              # Container definition
├── docker-compose.yml      # Service orchestration
├── kubernetes/             # Kubernetes manifests
│   ├── deployment.yaml
│   ├── pvc.yaml
│   └── service.yaml
└── requirements.txt        # Python dependencies
```

## ⚙️ Configuration

Environment variables can be set in docker-compose.yml or .env file:

```env
OLLAMA_HOST=localhost
OLLAMA_PORT=11434
DEFAULT_MODEL=llama3.2
EMBEDDING_MODEL=mxbai-embed-large
```

## 🔧 Development

1. Running Tests
```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

2. Code Formatting
```bash
# Install black
pip install black

# Format code
black src/ tests/
```

## 🚀 Deployment

### Docker Deployment
```bash
# Production deployment
docker-compose --profile production up -d

# With monitoring
docker-compose --profile monitoring up -d
```

### Kubernetes (K8s) Deployment
```bash
# Navigate to the kubernetes directory
cd kubernetes

# Apply the Kubernetes manifests
kubectl apply -f .
```

### Resource Requirements
- Minimum 4GB RAM
- 2 CPU cores
- 10GB storage for models

### Dynamically Adding Documents

To dynamically add documents to your chatbot's knowledge base, you can use the `DocumentManager` class in the `src/chatbot/utils/document_manager.py` file.

1. Fetch the documents from an external source (e.g., a file storage service):
```python
from src.chatbot.utils.document_manager import DocumentManager

document_manager = DocumentManager(
    embedding_model_path='path/to/sentence-transformer-model',
    document_source_url='https://example.com/api/documents'
)

document_manager.fetch_documents()
```

2. Update the chatbot's document embeddings:
```python
all_documents = document_manager.get_documents()
all_document_embeddings = document_manager.get_document_embeddings()

# Use the updated documents and embeddings in your chatbot logic
```

This will ensure that your chatbot's knowledge base is dynamically updated with the latest documents from the external source.

### API Endpoints

The QBot application exposes the following API endpoints:

#### 1. `/` (GET)
- **Description**: Serves the chat interface for the QBot application.
- **Response**: Renders the `chat.html` template, which provides the user interface for the chatbot.

#### 2. `/health` (GET)
- **Description**: Performs a health check for the application.
- **Response**: Returns a JSON response with a `status` field indicating whether the application is "healthy" or "unhealthy". If unhealthy, an `error` field is also included with a description of the issue.

#### 3. `/ask` (POST)
- **Description**: Handles user questions and generates responses.
- **Request**: Expects a JSON object with a `prompt` field containing the user's question.
- **Response**: Returns a JSON object with a `response` field containing the generated answer, and a `processing_time` field indicating the time taken to generate the response.

#### 4. `/documents` (GET)
- **Description**: Retrieves all documents in the knowledge base.
- **Response**: Returns a JSON object with a `count` field indicating the number of documents, and a `documents` field containing the list of document texts.

#### 5. `/documents` (POST)
- **Description**: Adds new documents to the knowledge base.
- **Request**: Expects a JSON object with a `documents` field containing a list of document texts to be added.
- **Response**: Returns a JSON object with a `message` field indicating the success of the operation, and a `count` field indicating the number of documents added.

#### 6. `/documents` (DELETE)
- **Description**: Clears all documents from the knowledge base.
- **Response**: Returns a JSON object with a `message` field indicating the success of the operation.

#### 7. `/stats` (GET)
- **Description**: Retrieves statistics about the knowledge base.
- **Response**: Returns a JSON object with the following fields:
  - `total_documents`: The total number of documents in the knowledge base.
  - `average_document_length`: The average length of the documents in the knowledge base.
  - `status`: The current status of the application (should be "operational").

### Error Handling
The application includes a `handle_error` function that is responsible for handling different types of exceptions that may occur during the execution of the API endpoints. It logs the error and returns an appropriate JSON response with an `error` field, along with a corresponding HTTP status code.

### Initialization
The `initialize_app` function is called when the application starts up. It initializes the `VectorStore` and `DocumentManager` instances, which are then used by the API endpoints to manage the knowledge base.


## 📊 Monitoring

The project includes:
1. Health checks
2. Prometheus metrics
3. Grafana dashboards

Access monitoring:
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

## 🔒 Security

1. Environment Variables
- Use .env file for local development
- Use secrets management in production

2. API Security
- Rate limiting implemented
- Input validation
- Error handling

## 🐛 Troubleshooting

Common issues and solutions:

1. Ollama Service Not Starting
```bash
# Check Ollama logs
docker-compose logs ollama

# Verify port availability
netstat -an | grep 11434
```

2. Model Download Issues
```bash
# Manual model download
ollama pull llama3.2
ollama pull mxbai-embed-large
```

## 📝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- Lexie Qin - Initial work

## 🙏 Acknowledgments

- Ollama team for the LLM framework
- ChromaDB for vector storage
- Flask team for the web framework

## 📞 Support

For support:
1. Check existing issues
2. Create a new issue
3. Contact: lexieqin@gmail.com