# Minimal multi-stage Dockerfile
FROM python:3.11-slim as builder
WORKDIR /app
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_HOME="/opt/poetry"

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock* /app/
RUN pip install --upgrade pip setuptools wheel
RUN pip install poetry && poetry export -f requirements.txt --without-hashes -o requirements.txt || true
RUN pip install -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . /app

ENV PYTHONUNBUFFERED=1

# Create entrypoint and default CMD will be provided in compose for development
