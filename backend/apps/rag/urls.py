from django.urls import path
from . import views

urlpatterns = [
    path("health/", views.health_check, name="health"),
    path("query/", views.query, name="rag-query"),
    path("documents/", views.DocumentListCreateView.as_view(), name="document-list"),
    path("documents/<uuid:pk>/", views.DocumentDetailView.as_view(), name="document-detail"),
]
