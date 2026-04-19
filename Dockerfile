FROM <AWS_ACCOUNT_ID>.dkr.ecr.ap-south-2.amazonaws.com/mhmarbles/python-base:latest

WORKDIR /app

# Copy only requirements first
COPY requirements.txt .

# Cache pip dependencies
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Copy app code
COPY . .

CMD ["gunicorn", "your_project.wsgi:application", "--bind", "0.0.0.0:8000"]
