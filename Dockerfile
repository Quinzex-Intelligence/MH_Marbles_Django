# Base image
FROM python:3.11-slim

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies (required for many Python packages)
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    python3-dev \
    libjpeg-dev \
    zlib1g-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better caching)
COPY requirements.txt .

# Upgrade pip and install dependencies (verbose for debugging)
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt -v

# Copy project files
COPY . .

# Collect static files (safe fallback)
RUN python manage.py collectstatic --noinput || true

# Expose Django port
EXPOSE 8000

# Start Django using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "config.wsgi:application"]
