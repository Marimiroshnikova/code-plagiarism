from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    timeout=30
)

print("Connection successful!", client.models.list())