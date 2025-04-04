from sentence_transformers import SentenceTransformer
from configs.model_config import MODEL_NAME, EMBEDDING_DIM

class EmbeddingModel:
    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)
    
    def encode(self, text: str) -> list:
        return self.model.encode(text).tolist()