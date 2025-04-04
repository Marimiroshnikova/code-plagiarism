# Code Plagiarism Detection System

A multi-stage plagiarism detection system combining semantic code analysis with LLM validation.


## Features

- **Repository Cloning**: Automated cloning of GitHub repositories
- **Code Indexing**: File processing and chunking
- **Vector Embeddings**: Using Sentence Transformers models
- **Semantic Search**: ChromaDB vector database
- **LLM Analysis**: GPT-3.5 powered validation
- **Evaluation Suite**: Comparative testing framework
- **Dockerized Services**: Containerized microservices



## System Architecture

```

code-plagiarism-detector/
├── .vscode/
│   ├── settings.json
│   └── extensions.json
├── configs/						# Configuration files
│   ├── repositories.txt			# List of target GitHub repos
│   └── model_config.yaml		# Embedding model settings
├── data/							# Persistent data storage
│   ├── evaluation_results/
│   ├── repositories/			# Cloned GitHub repositories
│   │   ├── examples/
│   │   ├── keras-io/
│   │   └── models/
│   ├── vector_db/				# ChromaDB vector database
│   └── file_index.json			# Processed code file index
├── docker/						# Docker configurations
│   ├── api.Dockerfile
│   ├── embedding.Dockerfile
│   └── indexer.Dockerfile
├── src/							# Source code
│   ├── embedding_service/		# Vector embedding logic
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   ├── model_loader.py
│   │   └── vector_db.py
│   ├── evaluation/				# Evaluation scripts
│   │   ├── __init__.py
│   │   └── evaluator.py
│   ├── plagiarism_api/			# FastAPI endpoints
│   │   ├── __init__.py
│   │   └── main.py
│   ├── repository_indexer/		# Repo cloning & processing
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   ├── cloner.py
│   │   └── file_processor.py
│   └── tests/
│       ├── __pycache__/
│       ├── test_api.py
│       └── test_vector_db.py
├── venv/
├── .dockerignore
├── .env
├── .gitignore
├── docker-compose.yml			# Orchestration config
├── README.md
└── requirements.txt				# Python dependencies


```


## Installation


###Prerequisites

- Docker Desktop
- Python 3.10+
- OpenAI API key


### Setup Instructions

1. **Clone Repository**
   ```bash
   git clone https://github.com/Marimiroshnikova/code-plagiarism.git
   cd code-plagiarism



### Installation

1. Clone repository:
```bash
git clone https://github.com/Marimiroshnikova/code-plagiarism.git
cd code-plagiarism
```

2. Create `.env` file:
```
OPENAI_API_KEY=your_api_key_here
```

###Docker Setup

1. Build and start containers:
```bash
docker-compose up --build
```

2. Services overview:
- **Indexer**: Clones repos (runs first)
- **Embedding Service**: Creates vector DB
- **API**: http://localhost:8080
- **Evaluator**: Runs comparison tests

## Configuration

### Repositories
`configs/repositories.txt`:
```
https://github.com/tensorflow/models
https://github.com/pytorch/examples
https://github.com/keras-team/keras-io
```

### Model Settings
`configs/model_config.py`:
```python
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIM = 384
MAX_FILES = 1000  # Max files to process
CHUNK_SIZE = 5000 # Code chunk size
```

## API Usage

### Check Code Plagiarism
```bash
curl -X POST "http://localhost:8080/check" \
-H "Content-Type: application/json" \
-d '{"code":"import tensorflow as tf\nprint(\"Hello TF\")"}'
```

Sample Response:
```json
{
  "result": "კი",
  "references": [
    "File: models/official/vision/modeling/backbones/resnet.py",
    "File: examples/cpp/autograd/autograd.cpp"
  ]
}
```

## Evaluation

The system compares three approaches:
1. RAG-only (vector similarity)
2. LLM-only (GPT-3.5 analysis)
3. Combined system

Results are saved in CSV format:
```bash
ls data/evaluation_results/
# results_20240515_142356.csv
```

## Troubleshooting

### Common Issues

**Import Errors**
```bash
# Ensure PYTHONPATH is set in Dockerfiles
ENV PYTHONPATH=/app
```

**Docker Build Failures**
```bash
# Clean rebuild:
docker-compose down --volumes --rmi all
docker-compose up --build
```

**API Timeouts**
```ini
# Increase timeout in .env
OPENAI_TIMEOUT=30
```

### View Logs
```bash
docker logs code-plagiarism-api-1
docker logs code-plagiarism-embedding_service-1
```

## Contributing

1. Fork the repository
2. Create feature branch:
```bash
git checkout -b feature/new-algorithm
```
3. Commit changes:
```bash
git commit -m "Add new similarity metric"
```
4. Push to branch:
```bash
git push origin feature/new-algorithm
```
5. Open pull request






