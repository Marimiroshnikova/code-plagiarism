FROM python:3.10-slim

RUN apt-get update && apt-get install -y git gcc

WORKDIR /app

ENV PYTHONPATH=/app  

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/src/           
COPY configs/ /app/configs/

CMD ["sh", "-c", "python src/repository_indexer/cloner.py && python src/repository_indexer/file_processor.py"]