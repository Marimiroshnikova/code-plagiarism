FROM python:3.10-slim

WORKDIR /app

ENV PYTHONPATH=/app  

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/src/
COPY configs/ /app/configs/

CMD ["python", "src/embedding_service/vector_db.py"]