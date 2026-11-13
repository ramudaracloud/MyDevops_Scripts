FROM python:3.12-slim-bookworm

WORKDIR /app

# Added zstd (required by Ollama's install script to extract the binary)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    procps \
    zstd \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install Ollama binary (Make sure /install.sh is included!)
RUN curl -fsSL https://ollama.com | sh

# Set environment variables for uv
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

# Create a virtual environment and install packages
RUN uv venv /app/.venv && \
    uv pip install fastapi uvicorn boto3

EXPOSE 8000 11434

# Create startup script
RUN printf '#!/bin/bash\nollama serve &\nsleep 3\nexec uvicorn main:app --host 0.0.0.0 --port 8000\n' > /entrypoint.sh \
    && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
