# Use a slim Python 3.12 base image
FROM python:3.12-slim-bookworm

# Set working directory
WORKDIR /app

# Install system dependencies and curl/ca-certificates needed for Ollama and uv
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Install uv from the official Astral installer / GHCR
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install Ollama binary
RUN curl -fsSL https://ollama.com | sh

# Set environment variables for uv
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

# Create a virtual environment with uv
RUN uv venv /app/.venv

# Install FastAPI, Uvicorn, and Boto3 into the virtual environment
RUN uv pip install fastapi uvicorn boto3

# Expose FastAPI port (8000) and Ollama port (11434)
EXPOSE 8000 11434

# Create a startup script to run Ollama in the background and Uvicorn/FastAPI in the foreground
RUN echo '#!/bin/bash\n\
ollama serve &\n\
OLLAMA_PID=$!\n\
sleep 3\n\
exec uvicorn main:app --host 0.0.0.0 --port 8000\n' > /entrypoint.sh \
    && chmod +x /entrypoint.sh

# Default command runs the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
