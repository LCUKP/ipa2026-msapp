FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --progress-bar off -r requirements.txt

COPY producer.py .
COPY database.py .
COPY scheduler.py .

CMD ["python", "-u", "scheduler.py"]
