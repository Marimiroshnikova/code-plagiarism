import os
from sentence_transformers import SentenceTransformer

class EmbeddingModel:
    def __init__(self):
        self.model_path = os.getenv("MODEL_PATH", "/app/models/all-MiniLM-L6-v2")
        
        try:
            self.model = SentenceTransformer(self.model_path)
            print(f"✅ model loaded: {self.model_path}")
            
        except Exception as e:
            print(f"❌ model is not loaded: {str(e)}")
            raise

    def encode(self, text: str):
        return self.model.encode(text)