import uuid
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Document",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=255)),
                ("file", models.FileField(upload_to="documents/")),
                ("status", models.CharField(choices=[("pending", "Pending"), ("processing", "Processing"), ("ready", "Ready"), ("failed", "Failed")], default="pending", max_length=20)),
                ("error_message", models.TextField(blank=True, default="")),
                ("chunk_count", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="DocumentChunk",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("qdrant_point_id", models.UUIDField()),
                ("text", models.TextField()),
                ("chunk_index", models.PositiveIntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("document", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="chunks", to="rag.document")),
            ],
            options={"ordering": ["chunk_index"], "unique_together": {("document", "chunk_index")}},
        ),
    ]
