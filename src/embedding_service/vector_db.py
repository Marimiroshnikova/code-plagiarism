# cSpell:disable
import json
import logging
from pathlib import Path
from typing import List, Dict, Union
import chromadb
from chromadb.config import Settings
from src.embedding_service.model_loader import EmbeddingModel

# კონფიგის იმპორტი
from configs.model_config import (
    MODEL_NAME,
    EMBEDDING_DIM,
    MAX_FILES,
    MAX_CHUNKS,
    CHUNK_SIZE
)

class VectorDB:
    def __init__(self):
        self.embedder = EmbeddingModel()
        self.tokenizer = self.embedder.model.tokenizer
        
        self.client = chromadb.PersistentClient(
            path=str(Path(__file__).parent.parent.parent / "data" / "vector_db"),
            settings=Settings(allow_reset=True, anonymized_telemetry=False)
        )
        
        self.collection = self.client.get_or_create_collection(
            name="code_embeddings",
            metadata={"hnsw:space": "cosine"}
        )

    def _chunk_code(self, content: str) -> List[str]:
        return [content[i:i+CHUNK_SIZE] for i in range(0, len(content), CHUNK_SIZE//2)]

    def generate_embeddings(self, file_index_path: Path):
        if not file_index_path.exists():
            raise FileNotFoundError(f"File index not found at {file_index_path}")
        
        with open(file_index_path) as f:
            files = json.load(f)[:MAX_FILES]  

        documents = []
        metadatas = []
        ids = []
        chunk_counter = 0

        for idx, file in enumerate(files):
            chunks = self._chunk_code(file['content'])
            for chunk_idx, chunk in enumerate(chunks):
                if chunk_counter >= MAX_CHUNKS:
                    break
                documents.append(chunk)
                metadatas.append({"path": file['path'], "chunk": chunk_idx})
                ids.append(f"{idx}_{chunk_idx}")
                chunk_counter += 1
            if chunk_counter >= MAX_CHUNKS:
                break

        embeddings = self.embedder.encode(documents)
        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        logging.info(f"Added {chunk_counter}/{MAX_CHUNKS} chunks")

    def query(self, text: str, top_k: int = 5) -> Dict[str, Union[List[str], List[float], List[Dict]]]:
        embedding = self.embedder.encode(text)
        results = self.collection.query(query_embeddings=[embedding], n_results=top_k)
        return {
            "matches": results["documents"][0],
            "scores": results["distances"][0],
            "metadata": results["metadatas"][0]
        }

if __name__ == "__main__":
    db = VectorDB()
    db.generate_embeddings(Path("data/file_index.json"))