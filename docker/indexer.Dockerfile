FROM python:3.10-slim

RUN apt-get update && apt-get install -y git gcc

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/repository_indexer/ .
COPY configs/ /app/configs/

CMD ["sh", "-c", "python cloner.py && python file_processor.py"]