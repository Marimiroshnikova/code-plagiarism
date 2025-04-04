from sentence_transformers import SentenceTransformer
import yaml

class EmbeddingModel:
    def __init__(self):
        with open("configs/model_config.yaml") as f:
            config = yaml.safe_load(f)
        self.model = SentenceTransformer(config["model_name"])
        
    def encode(self, text: str) -> list:
        return self.model.encode(text).tolist()