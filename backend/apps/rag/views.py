from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection

from .models import Document
from .serializers import (
    DocumentSerializer,
    QueryRequestSerializer,
    QueryResponseSerializer,
)
from .text_utils import embed_text
from .qdrant_client import search as qdrant_search
from .ollama_client import generate as ollama_generate
from .tasks import ingest_document


@api_view(["GET"])
def health_check(request):
    """Used by Docker healthcheck / load balancer probes."""
    db_ok = True
    try:
        connection.ensure_connection()
    except Exception:
        db_ok = False
    return Response({"status": "ok" if db_ok else "degraded", "database": db_ok})


class DocumentListCreateView(generics.ListCreateAPIView):
    """
    GET  -> list all uploaded documents and their ingestion status
    POST -> upload a new document and kick off async ingestion
    """

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def perform_create(self, serializer):
        title = serializer.validated_data.get("title") or self.request.data.get("file").name
        document = serializer.save(title=title)
        ingest_document.delay(str(document.id))


class DocumentDetailView(generics.RetrieveDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def perform_destroy(self, instance):
        from .qdrant_client import delete_document_points

        delete_document_points(str(instance.id))
        instance.file.delete(save=False)
        instance.delete()


@api_view(["POST"])
def query(request):
    """
    RAG endpoint:
    1) embed the question
    2) search Qdrant for nearest chunks
    3) ask Ollama to answer using retrieved context
    """
    req = QueryRequestSerializer(data=request.data)
    req.is_valid(raise_exception=True)

    question = req.validated_data["question"]
    top_k = req.validated_data["top_k"]

    vector = embed_text(question)
    hits = qdrant_search(vector, limit=top_k)

    context = "\n---\n".join(h.payload.get("text", "") for h in hits)
    answer = ollama_generate(question, context)

    response = QueryResponseSerializer(
        {"answer": answer, "sources": [h.payload for h in hits]}
    )
    return Response(response.data, status=status.HTTP_200_OK)
