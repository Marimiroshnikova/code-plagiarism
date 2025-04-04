from pathlib import Path
from src.embedding_service.vector_db import VectorDB
import unittest

class TestVectorDB(unittest.TestCase):
    def setUp(self):
        self.db = VectorDB()
        self.file_index_path = Path("data/file_index.json")

    def test_embedding_generation(self):
        self.db.generate_embeddings(self.file_index_path)
        self.assertGreater(self.db.collection.count(), 0)

    def test_query_function(self):
        results = self.db.query("import tensorflow as tf")
        self.assertEqual(len(results["matches"]), 5)

if __name__ == "__main__":
    unittest.main()