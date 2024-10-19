FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app

# CMD celery -A tasks.celery_app worker --loglevel INFO