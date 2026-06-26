حق با توئه، همون معماری باید بمونه چون مهم‌ترین بخش README هست و باعث میشه پروژه حرفه‌ای به نظر بیاد. فقط همون رو تمیزتر و انگلیسی‌تر کردم بدون اینکه حذفش کنم.

این نسخه نهایی README تو هست (کاملاً اصلاح‌شده + روان + حرفه‌ای + معماری حفظ شده):

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
