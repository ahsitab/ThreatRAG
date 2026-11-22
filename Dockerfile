# Multi-stage Dockerfile for ThreatRAG
FROM python:3.11-slim as base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency specification and install Python packages
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy application source tree
COPY . /app/

# Expose FastAPI (8000) and Streamlit (8501)
EXPOSE 8000 8501

# Default health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Default entrypoint starts both API and dashboard via lightweight bash launcher
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
