# Use Ubuntu as base image and install Ollama
FROM ubuntu:22.04

# Install Ollama
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://ollama.com/install.sh | sh

# Install Python and other dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .
RUN pip3 install -e .

# Expose ports
EXPOSE 11434 8080

# Create and set up entrypoint script
RUN echo '#!/bin/bash\n\
ollama serve &\n\
echo "Waiting for Ollama service..."\n\
while ! nc -z localhost 11434; do\n\
    sleep 1\n\
done\n\
echo "Ollama service is ready"\n\
echo "Pulling required models..."\n\
ollama pull mxbai-embed-large\n\
ollama pull llama3.2\n\
echo "Starting QBot application..."\n\
python3 -m src.qbot.main' > /entrypoint.sh \
    && chmod +x /entrypoint.sh

CMD ["/bin/bash", "/entrypoint.sh"]