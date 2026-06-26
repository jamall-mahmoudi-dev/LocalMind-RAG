from rest_framework import serializers
from .models import Document, DocumentChunk


class DocumentChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentChunk
        fields = ["id", "chunk_index", "text", "qdrant_point_id"]


class DocumentSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=False, allow_blank=True, max_length=255)

    class Meta:
        model = Document
        fields = [
            "id",
            "title",
            "file",
            "status",
            "error_message",
            "chunk_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "status", "error_message", "chunk_count"]


class QueryRequestSerializer(serializers.Serializer):
    question = serializers.CharField(allow_blank=False, max_length=2000)
    top_k = serializers.IntegerField(default=5, min_value=1, max_value=20)


class QueryResponseSerializer(serializers.Serializer):
    answer = serializers.CharField()
    sources = serializers.ListField(child=serializers.DictField())
