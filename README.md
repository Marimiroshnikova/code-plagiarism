# cSpell:disable

code-plagiarism-detector/
├── .venv/
├── .vscode/
│   ├── settings.json
│   └── extensions.json
├── configs/
│   ├── repositories.txt
│   └── model_config.yaml
├── data/
│   ├── evaluation_results/
│   ├── repositories/
│   │   ├── examples/
│   │   ├── keras-io/
│   │   └── models/
│   ├── vector_db/
│   └── file_index.json
├── docker/
│   ├── api.Dockerfile
│   ├── embedding.Dockerfile
│   └── indexer.Dockerfile
├── src/
│   ├── embedding_service/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   ├── model_loader.py
│   │   └── vector_db.py
│   ├── evaluation/
│   │   ├── __init__.py
│   │   └── evaluator.py
│   ├── plagiarism_api/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── repository_indexer/
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
├── docker-compose.yml
├── README.md
└── requirements.txt