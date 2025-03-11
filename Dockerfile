FROM python:3.11-slim

# Define environment variables to avoid cache issues
ENV PIP_NO_CACHE_DIR=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_HOME="/opt/poetry" \
    PATH="/opt/poetry/bin:$PATH" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl make \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set working directory
WORKDIR /app

# Copy only the essential files for dependency installation
COPY pyproject.toml poetry.lock ./

# Install all dependencies (including dev for testing)
RUN poetry install --no-root --with dev

# Copy the full application source code
COPY src src
COPY app.py .
COPY Makefile .

# Expose the Streamlit app port
EXPOSE 8509

# Default command (can be overridden)
CMD ["make", "app"]