FROM python:3.11-slim

# Definir variáveis de ambiente para evitar criação de caches desnecessários
ENV PIP_NO_CACHE_DIR=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_HOME="/opt/poetry" \
    PATH="/opt/poetry/bin:$PATH" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl make \
    && rm -rf /var/lib/apt/lists/*

# Instalar Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Definir diretório de trabalho
WORKDIR /app

# Copiar apenas os ficheiros essenciais para instalar dependências
COPY pyproject.toml poetry.lock ./

# Instalar dependências
RUN poetry install --no-root --only main

# Copiar código da aplicação
COPY src src
COPY app.py .

# Expor a porta usada pelo Streamlit
EXPOSE 8509
