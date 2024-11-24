#!/bin/bash

# Start Ollama service
echo "Starting Ollama service..."
/bin/ollama serve &

# Wait for Ollama service to be ready
echo "Waiting for Ollama service to be ready..."
while ! nc -z localhost 11434; do
    sleep 1
done
echo "Ollama service is ready"

# Pull required models
echo "Pulling required models..."
/bin/ollama pull mxbai-embed-large
/bin/ollama pull llama3.2

# Start your Python application
echo "Starting QBot application..."
python3 -m src.qbot.main