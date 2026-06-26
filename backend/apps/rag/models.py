import uuid

from django.db import models


class Document(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        READY = "ready", "Ready"
        FAILED = "failed", "Failed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="documents/")
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    error_message = models.TextField(blank=True, default="")
    chunk_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.status})"


class DocumentChunk(models.Model):
    """
    Local mirror of what's stored in Qdrant — useful for admin browsing,
    re-indexing, and debugging without round-tripping to the vector DB.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(
        Document, related_name="chunks", on_delete=models.CASCADE
    )
    qdrant_point_id = models.UUIDField()
    text = models.TextField()
    chunk_index = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["chunk_index"]
        unique_together = ("document", "chunk_index")

    def __str__(self):
        return f"{self.document.title} #{self.chunk_index}"
