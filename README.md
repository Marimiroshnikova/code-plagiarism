Here's a refined and properly formatted README.md:

```markdown
# Code Plagiarism Detection System

A multi-stage plagiarism detection system combining semantic code analysis with LLM validation.

## Features

- **Repository Cloning**: Automated cloning of GitHub repositories
- **Code Indexing**: File processing and chunking
- **Vector Embeddings**: Using Sentence Transformers models
- **Semantic Search**: ChromaDB vector database
- **LLM Analysis**: GPT-3.5 powered validation
- **Evaluation Suite**: Comparative testing framework
- **Dockerized Services**: Containerized microservices architecture

## System Architecture

```
code-plagiarism-detector/
├── configs/                      # Configuration files
│   ├── repositories.txt          # List of target GitHub repos
│   └── model_config.yaml         # Embedding model settings
├── data/                         # Persistent data storage
│   ├── evaluation_results/       # Test comparison results
│   ├── repositories/             # Cloned GitHub repositories
│   ├── vector_db/                # ChromaDB vector database
│   └── file_index.json           # Processed code file index
├── docker/                       # Docker configurations
│   ├── api.Dockerfile
│   ├── embedding.Dockerfile
│   └── indexer.Dockerfile
├── src/                          # Application source code
│   ├── embedding_service/        # Vector embedding logic
│   ├── evaluation/               # Evaluation scripts
│   ├── plagiarism_api/           # FastAPI endpoints
│   ├── repository_indexer/       # Repo cloning & processing
│   └── tests/                    # Test cases
├── .env                          # Environment variables
├── docker-compose.yml            # Container orchestration
└── requirements.txt              # Python dependencies
```

## Installation

### Prerequisites

- Docker Desktop 4.15+
- Python 3.10+ (for local development)
- OpenAI API key
- Git LFS installed

### Quick Start

1. Clone repository and download models:
```bash
git clone https://github.com/Marimiroshnikova/code-plagiarism.git
cd code-plagiarism
git lfs install
git clone https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
```

2. Configure environment:
```bash
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

3. Start services:
```bash
docker-compose up --build
```

## Service Architecture

| Service              | Description                                  | Port  |
|----------------------|----------------------------------------------|-------|
| Indexer              | Clones & processes repositories             | -     |
| Embedding Service    | Generates vector embeddings                 | -     |
| API                  | REST interface for plagiarism checks        | 8080  |
| Evaluator            | Runs comparative performance tests          | -     |

## Configuration

### Repository List
Edit `configs/repositories.txt`:
```
https://github.com/tensorflow/models
https://github.com/pytorch/examples
https://github.com/keras-team/keras-io
```

### Model Configuration
`configs/model_config.yaml`:
```yaml
embedding_model:
  name: "all-MiniLM-L6-v2"
  dimensions: 384
  max_files: 1000
  chunk_size: 5000
```

## API Documentation

### Check Code Similarity
```bash
curl -X POST "http://localhost:8080/check" \
  -H "Content-Type: application/json" \
  -d '{"code":"import tensorflow as tf\nprint(\"Hello TF\")"}'
```

**Response:**
```json
{
  "similarity_score": 0.92,
  "matches": [
    {
      "file": "models/official/vision/modeling/backbones/resnet.py",
      "confidence": 0.89
    }
  ]
}
```

## Evaluation Framework

The system compares three detection approaches:

1. Vector Search Only
2. LLM Analysis Only
3. Combined Hybrid Approach

Run evaluations:
```bash
docker exec -it code-plagiarism-evaluator-1 python evaluation/evaluator.py
```

Results are saved as CSV:
```
data/evaluation_results/results_20240515_142356.csv
```

## Troubleshooting Guide

### Common Issues

**Model Download Failures**
```bash
# Verify LFS installation
git lfs install
git lfs pull
```

**Docker Build Errors**
```bash
# Full clean rebuild:
docker-compose down --volumes --rmi all
docker-compose up --build
```

**API Connection Issues**
```bash
# Check service status
docker ps -a
# View logs
docker logs code-plagiarism-api-1
```

### Performance Tuning

Increase API timeout in `.env`:
```ini
REQUEST_TIMEOUT=30
MAX_RESPONSE_SIZE=1048576
```

## Contributing

1. Create feature branch:
```bash
git checkout -b feature/improved-algorithm
```

2. Test changes:
```bash
docker-compose up --build --force-recreate
```

3. Submit pull request with:
- Implementation details
- Test results
- Documentation updates

---
