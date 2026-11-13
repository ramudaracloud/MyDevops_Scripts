# Use the official slim Python 3.12 image
FROM python:3.12-slim-bookworm

# Set the working directory
WORKDIR /app

# Install uv from the official Astral image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Configure uv environment variables and add the virtual environment to PATH
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

# Create a virtual environment and install FastAPI, Uvicorn, and boto3
RUN uv venv /app/.venv && \
    uv pip install fastapi uvicorn boto3 ollama tiktoken

# Copy your application code into the container
COPY . .

# Expose FastAPI's default port
EXPOSE 8000

# Run the FastAPI app using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
