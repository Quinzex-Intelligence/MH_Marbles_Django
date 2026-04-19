FROM python:3.11-slim

WORKDIR /app

# Install system deps (your mysql fix)
RUN apt-get update && apt-get install -y \
    gcc \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first
COPY requirements.txt .

# Cache pip dependencies
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Copy project
COPY . .

CMD ["gunicorn", "your_project.wsgi:application", "--bind", "0.0.0.0:8000"]
