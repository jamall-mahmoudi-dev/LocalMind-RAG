import logging

from celery import shared_task
from django.db import transaction

from .models import Document, DocumentChunk
from .text_utils import chunk_text, embed_batch, extract_text_from_file
from .qdrant_client import upsert_chunks, delete_document_points

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def ingest_document(self, document_id: str):
    """
    Full ingestion pipeline for a single document:
    1. extract text from the uploaded file
    2. split into overlapping chunks
    3. embed each chunk
    4. upsert vectors into Qdrant
    5. mirror chunk metadata in Postgres
    """
    try:
        document = Document.objects.get(id=document_id)
    except Document.DoesNotExist:
        logger.warning("Document %s no longer exists, skipping ingest", document_id)
        return

    document.status = Document.Status.PROCESSING
    document.save(update_fields=["status"])

    try:
        raw_text = extract_text_from_file(document.file.path)
        chunks = chunk_text(raw_text)

        if not chunks:
            document.status = Document.Status.FAILED
            document.error_message = "No extractable text found in file."
            document.save(update_fields=["status", "error_message"])
            return

        # Replace any previously indexed vectors for this document (re-ingest case)
        delete_document_points(document_id)
        DocumentChunk.objects.filter(document=document).delete()

        vectors = embed_batch(chunks)
        point_ids = upsert_chunks(document_id, chunks, vectors)

        with transaction.atomic():
            DocumentChunk.objects.bulk_create(
                [
                    DocumentChunk(
                        document=document,
                        qdrant_point_id=point_id,
                        text=text,
                        chunk_index=idx,
                    )
                    for idx, (text, point_id) in enumerate(zip(chunks, point_ids))
                ]
            )
            document.status = Document.Status.READY
            document.chunk_count = len(chunks)
            document.error_message = ""
            document.save(update_fields=["status", "chunk_count", "error_message"])

        logger.info("Ingested document %s into %d chunks", document_id, len(chunks))

    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to ingest document %s", document_id)
        document.status = Document.Status.FAILED
        document.error_message = str(exc)
        document.save(update_fields=["status", "error_message"])
        raise self.retry(exc=exc)
