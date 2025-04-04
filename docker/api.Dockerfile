FROM python:3.10-slim
WORKDIR /app

ENV PYTHONPATH=/app
COPY src/ /app/src/
COPY configs/ /app/configs/

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "src.plagiarism_api.main:app", "--host", "0.0.0.0", "--port", "8000"]