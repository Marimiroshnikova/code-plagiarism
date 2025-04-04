# cSpell:disable

import csv
import os
from datetime import datetime
from typing import List, Dict
from openai import OpenAI
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from src.embedding_service.vector_db import VectorDB
from src.plagiarism_api.main import app

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.embedding_service.vector_db import VectorDB  
from src.plagiarism_api.main import app

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

TEST_CASES = [
    {"code": "import tensorflow as tf\nmodel = tf.keras.Sequential()", "expected": True},
    {"code": "def unique_hash_123(): return 0x7f3b8d", "expected": False},
    {"code": "for i in range(10): print(i)", "expected": True}
]

class Evaluator:
    def __init__(self, vector_db: VectorDB):
        self.vector_db = vector_db
        self.results = []
        self.api_client = TestClient(app)

    def _query_llm(self, code: str) -> bool:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": f"Is this code plagiarized? Answer only yes/no:\n{code}"
            }],
            temperature=0.0
        )
        return "yes" in response.choices[0].message.content.lower()

    def evaluate(self):
        # RAG-only evaluation
        for case in TEST_CASES:
            result = self.vector_db.query(case["code"])
            is_match = any(score < 0.5 for score in result["scores"])
            self.results.append({
                "method": "RAG-only",
                "test_case": case["code"][:50],
                "expected": case["expected"],
                "actual": is_match
            })
        
        # LLM-only evaluation
        for case in TEST_CASES:
            actual = self._query_llm(case["code"])
            self.results.append({
                "method": "LLM-only", 
                "test_case": case["code"][:50],
                "expected": case["expected"],
                "actual": actual
            })
        
        # Full system evaluation
        for case in TEST_CASES:
            response = self.api_client.post("/check", json={"code": case["code"]})
            self.results.append({
                "method": "Full System",
                "test_case": case["code"][:50],
                "expected": case["expected"],
                "actual": response.json().get("is_plagiarism", False)
            })

    def save_results(self):
        output_dir = Path("data/evaluation_results")
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = output_dir / f"results_{timestamp}.csv"
        
        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["method", "test_case", "expected", "actual"])
            writer.writeheader()
            writer.writerows(self.results)

if __name__ == "__main__":
    db = VectorDB()
    evaluator = Evaluator(db)
    evaluator.evaluate()
    evaluator.save_results()