from django.contrib import admin
from .models import Document, DocumentChunk


class DocumentChunkInline(admin.TabularInline):
    model = DocumentChunk
    extra = 0
    readonly_fields = ("qdrant_point_id", "chunk_index", "created_at")
    fields = ("chunk_index", "text", "qdrant_point_id", "created_at")
    can_delete = False


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "chunk_count", "created_at")
    list_filter = ("status",)
    search_fields = ("title",)
    readonly_fields = ("id", "chunk_count", "error_message", "created_at", "updated_at")
    inlines = [DocumentChunkInline]


@admin.register(DocumentChunk)
class DocumentChunkAdmin(admin.ModelAdmin):
    list_display = ("document", "chunk_index", "qdrant_point_id")
    search_fields = ("text",)
