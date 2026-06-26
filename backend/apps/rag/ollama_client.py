"""Thin wrapper around the Ollama HTTP API."""
from django.conf import settings
import ollama


def get_client() -> ollama.Client:
    return ollama.Client(host=settings.OLLAMA_URL)


def generate(prompt: str, context: str = "") -> str:
    client = get_client()
    full_prompt = f"Context:\n{context}\n\nQuestion: {prompt}\nAnswer:"
    response = client.generate(model=settings.OLLAMA_MODEL, prompt=full_prompt)
    return response.get("response", "")
