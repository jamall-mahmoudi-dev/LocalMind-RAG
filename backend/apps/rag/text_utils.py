"""Helpers for splitting raw text into overlapping chunks and embedding them."""
from functools import lru_cache

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDING_DIM = 384


@lru_cache(maxsize=1)
def get_embedding_model():
    """Lazily load the sentence-transformers model once per process."""
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(EMBEDDING_MODEL_NAME)


def embed_text(text: str) -> list[float]:
    model = get_embedding_model()
    return model.encode(text).tolist()


def embed_batch(texts: list[str]) -> list[list[float]]:
    model = get_embedding_model()
    return model.encode(texts).tolist()


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> list[str]:
    """
    Naive but dependable sliding-window chunker, operating on characters.
    Good enough as a baseline; swap for a token-aware splitter
    (e.g. langchain's RecursiveCharacterTextSplitter) if needed.
    """
    text = text.strip()
    if not text:
        return []

    chunks = []
    start = 0
    length = len(text)

    while start < length:
        end = min(start + chunk_size, length)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == length:
            break
        start = end - overlap

    return chunks


def extract_text_from_file(file_path: str) -> str:
    """Extract raw text from a PDF or plain-text file."""
    if file_path.lower().endswith(".pdf"):
        from pypdf import PdfReader

        reader = PdfReader(file_path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()
