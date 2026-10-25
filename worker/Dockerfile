FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --progress-bar off -r requirements.txt

COPY consumer.py callback.py router_client.py database.py worker.py ./

CMD ["python", "-u", "worker.py"]
