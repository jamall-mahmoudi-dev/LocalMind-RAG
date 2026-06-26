---

# RAG Stack — Django + React + Qdrant + Ollama

A fully self-hosted Retrieval-Augmented Generation (RAG) system with no external APIs required.

It provides document ingestion, vector search, and LLM-based question answering using a completely local infrastructure.

---

## Architecture

```
                 ┌─────────────┐
   Client  ───▶      Nginx      (reverse proxy / entrypoint)
                 └──────┬──────┘
                        │
        ┌───────────────┼───────────────┐
        ▼                               ▼
 ┌─────────────┐                 ┌─────────────┐
    Frontend                       Backend   
   React (Vite)                    Django    
 └─────────────┘                 └──────┬──────┘
                                         │
                ┌────────────────────────┼────────────────────────┐
                ▼                        ▼                        ▼
         ┌───────────┐            ┌───────────┐            ┌───────────┐
         │  Postgres │            │   Qdrant  │            │  Ollama   │
         │ (RDBMS)   │            │ (VectorDB)│            │  (LLM)    │
         └───────────┘            └───────────┘            └───────────┘
                                         ▲
                                         │
                                  ┌───────────┐
                                  │   Redis   │
                                  │ (Celery)  │
                                  └───────────┘
```

---

## Services Overview

| Service       | Role                                                                    |
| ------------- | ----------------------------------------------------------------------- |
| nginx         | Single entry point, reverse proxy, routing between frontend and backend |
| frontend      | React (Vite) UI application                                             |
| backend       | Django REST API and RAG orchestration layer                             |
| celery-worker | Background processing for document ingestion and embeddings             |
| postgres      | Relational database for metadata storage                                |
| redis         | Message broker for Celery tasks                                         |
| qdrant        | Vector database for embeddings and semantic search                      |
| ollama        | Local LLM inference engine                                              |
| ollama-pull   | One-time job to download the default model                              |

---

## How It Works

1. A user uploads a document via the frontend
2. Backend stores document metadata in PostgreSQL
3. Celery worker extracts text and generates embeddings
4. Embeddings are stored in Qdrant
5. A user submits a question
6. The backend:

   * Embeds the query
   * Searches similar chunks in Qdrant
   * Sends retrieved context to Ollama
7. Ollama generates the final answer

---

## Run Locally

```bash
cp .env.example .env
# configure environment variables (secrets, database credentials, etc.)

docker compose up -d --build
```bash
bahram@bahram:~/rag-stack/proj$ docker compose up -d --build
WARN[0000] /home/bahram/rag-stack/proj/docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion
WARN[0000] /home/bahram/rag-stack/proj/docker-compose.override.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion
[+] up 11/11
 ✔ Network proj_backend-net    Created                                                                                                                              0.2s
 ✔ Network proj_frontend-net   Created                                                                                                                              0.2s
 ✔ Container rag_frontend      Started                                                                                                                             14.4s
 ✔ Container rag_postgres      Started                                                                                                                             13.3s
 ✔ Container rag_qdrant        Started                                                                                                                             12.5s
 ✔ Container rag_nginx         Started                                                                                                                             13.6s
 ✔ Container rag_ollama        Started                                                                                                                             12.9s
 ✔ Container rag_redis         Started                                                                                                                             13.9s
 ✔ Container rag_ollama_pull   Started                                                                                                                             18.1s
 ✔ Container rag_backend       Started                                                                                                                             18.7s
 ✔ Container rag_celery_worker Started  
```

# run migrations
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py createsuperuser
```

---

## Access URLs

* Frontend: [http://localhost/](http://localhost/)
* Backend API: [http://localhost/api/](http://localhost/api/)
* Qdrant (if exposed): [http://localhost:6333/dashboard](http://localhost:6333/dashboard)

---

## Production Notes

* Do not expose Qdrant or Ollama publicly in production
* Keep them in an internal Docker network only
* Use a separate docker-compose override for development settings
* Enable GPU acceleration for Ollama using NVIDIA Container Toolkit if needed
* Add backup services for PostgreSQL and Qdrant volumes
* Consider a CI/CD-specific compose file with health checks

---

## Project Structure

```
.
├── docker-compose.yml
├── .env.example
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── manage.py
│   ├── config/
│   │   ├── settings/
│   │   │   ├── base.py
│   │   │   ├── development.py
│   │   │   └── production.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── celery.py
│   └── apps/rag/
│       ├── views.py
│       ├── qdrant_client.py
│       ├── ollama_client.py
│       └── urls.py
├── frontend/
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── main.jsx
│       └── App.jsx
└── nginx/
    └── nginx.conf
```

---
