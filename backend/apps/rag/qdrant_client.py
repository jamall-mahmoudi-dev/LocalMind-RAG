"""Thin wrapper around the Qdrant client, configured from Django settings."""
import uuid

from django.conf import settings
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, PointStruct, VectorParams

_client = None


def get_client() -> QdrantClient:
    global _client
    if _client is None:
        _client = QdrantClient(url=settings.QDRANT_URL)
    return _client


def ensure_collection(vector_size: int = 384):
    client = get_client()
    collections = [c.name for c in client.get_collections().collections]
    if settings.QDRANT_COLLECTION not in collections:
        client.create_collection(
            collection_name=settings.QDRANT_COLLECTION,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )


def upsert_chunks(document_id: str, chunks: list[str], vectors: list[list[float]]) -> list[str]:
    """Upsert a batch of chunks for a document. Returns the generated point IDs."""
    client = get_client()
    ensure_collection(vector_size=len(vectors[0]) if vectors else 384)

    points = []
    point_ids = []
    for idx, (text, vector) in enumerate(zip(chunks, vectors)):
        point_id = str(uuid.uuid4())
        point_ids.append(point_id)
        points.append(
            PointStruct(
                id=point_id,
                vector=vector,
                payload={
                    "document_id": str(document_id),
                    "chunk_index": idx,
                    "text": text,
                },
            )
        )

    client.upsert(collection_name=settings.QDRANT_COLLECTION, points=points)
    return point_ids


def delete_document_points(document_id: str):
    """Remove all vectors belonging to a document (e.g. on re-ingest or delete)."""
    from qdrant_client.http.models import Filter, FieldCondition, MatchValue

    client = get_client()
    client.delete(
        collection_name=settings.QDRANT_COLLECTION,
        points_selector=Filter(
            must=[FieldCondition(key="document_id", match=MatchValue(value=str(document_id)))]
        ),
    )


def search(vector: list[float], limit: int = 5):
    client = get_client()
    return client.search(
        collection_name=settings.QDRANT_COLLECTION,
        query_vector=vector,
        limit=limit,
    )
