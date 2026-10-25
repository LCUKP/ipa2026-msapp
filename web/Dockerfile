FROM python

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --progress-bar off -r requirements.txt

COPY app.py .
COPY templates/ templates/
COPY static/ static/

EXPOSE 8080

CMD ["python", "app.py"]
