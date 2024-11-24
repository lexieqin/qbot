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