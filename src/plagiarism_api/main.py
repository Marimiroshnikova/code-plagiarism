# cSpell:disable

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
import os
from pathlib import Path
from typing import Optional
from embedding_service.vector_db import VectorDB

load_dotenv(Path(__file__).parent.parent.parent / ".env")

app = FastAPI(title="Code Plagiarism Detector")
vdb = VectorDB()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),  
    timeout=20  
)

class CodeRequest(BaseModel):
    code: str

PROMPT_TEMPLATE = """Analyze if this code is plagiarized using these criteria:
1. Code structure similarity
2. Variable/method naming patterns
3. Algorithm implementation uniqueness

User Code Excerpt:
{user_code}

Reference Matches:
{references}

Answer strictly 'yes' or 'no'. If uncertain, respond 'no'."""

@app.post("/check")
async def check_plagiarism(request: CodeRequest):
    try:
        if len(request.code) > 10000:
            raise HTTPException(status_code=400, detail="Code exceeds 10k character limit")
        
        # VectorDB query
        results = vdb.query(request.code[:2000])
        references = [
            f"File: {m['path']}\nCode: {c[:500]}..." 
            for m, c in zip(results["metadata"], results["matches"])
        ][:3]

        # LLM analysis
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{
                "role": "user",
                "content": PROMPT_TEMPLATE.format(
                    user_code=request.code[:2000],
                    references="\n\n".join(references)
                )
                }
            ],
            temperature=0.0,
            max_tokens=2
        )
        
        answer = response.choices[0].message.content.strip().lower()
        return {
            "is_plagiarism": answer == "yes",
            "references": results["metadata"] if answer == "yes" else [],
            "scores": results["scores"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))