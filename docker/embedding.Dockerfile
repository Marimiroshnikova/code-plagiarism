FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install torch==2.0.1+cpu -f https://download.pytorch.org/whl/torch_stable.html

COPY src/embedding_service/ .
COPY configs/ /app/configs/

CMD ["python", "vector_db.py"]