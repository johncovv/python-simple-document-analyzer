# ==============================================================================
# BUILDER STAGE: Install dependencies and build packages
# ==============================================================================
FROM python:3.13-slim AS builder

# Install build dependencies (only needed for compilation)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libxml2-dev \
    libxslt-dev \
    libcairo2-dev \
    libpango1.0-dev \
    libgdk-pixbuf-xlib-2.0-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Poetry (temporarily for dependency installation)
RUN pip install --no-cache-dir poetry

# Copy dependency files
COPY pyproject.toml poetry.lock* ./

# Install Python dependencies and clean up
RUN poetry config virtualenvs.create false \
    && poetry install --only=main --no-interaction --no-ansi --no-root \
    && pip uninstall -y poetry \
    && pip cache purge \
    && rm -rf /root/.cache

# ==============================================================================
# PRODUCTION STAGE: Lightweight runtime image
# ==============================================================================
FROM python:3.13-slim

# Install only runtime dependencies (no build tools)
RUN apt-get update && apt-get install -y \
    libcairo2 \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash app

# Set working directory
WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=app:app . .

# Create necessary directories
RUN mkdir -p temp/analysis && chown -R app:app temp/

# Switch to non-root user
USER app

# Set Python path
ENV PYTHONPATH=/app

# Set unbuffered output for better logging
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Default command
CMD ["python", "main.py"]
