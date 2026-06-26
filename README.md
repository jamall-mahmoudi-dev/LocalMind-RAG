# RAG Stack — Django + React + Qdrant + Ollama

استک کامل RAG (Retrieval-Augmented Generation) با اجرای کاملاً Self-Hosted (بدون نیاز به API خارجی).

## معماری

```
                 ┌─────────────┐
   Client  ───▶  │    Nginx    │  (reverse proxy / entrypoint)
                 └──────┬──────┘
                        │
        ┌───────────────┼───────────────┐
        ▼                               ▼
 ┌─────────────┐                 ┌─────────────┐
 │   Frontend   │                 │   Backend   │
 │  React (Vite)│                 │   Django    │
 └─────────────┘                 └──────┬──────┘
                                         │
                ┌────────────────────────┼────────────────────────┐
                ▼                        ▼                        ▼
         ┌───────────┐            ┌───────────┐            ┌───────────┐
         │  Postgres │            │   Qdrant  │            │  Ollama   │
         │  (RDBMS)  │            │ (Vector DB)│            │  (LLM)    │
         └───────────┘            └───────────┘            └───────────┘
                                         ▲
                                         │
                                  ┌───────────┐
                                  │   Redis   │
                                  │ (Celery)  │
                                  └───────────┘
```

## سرویس‌ها

| سرویس | نقش |
|---|---|
| `nginx` | تک نقطه‌ی ورودی، روتینگ بین فرانت و بک‌اند، ترمیناسیون TLS |
| `frontend` | React build شده، سرو شده با Nginx داخلی |
| `backend` | Django REST API، orchestration بین Qdrant و Ollama |
| `celery-worker` | پردازش async برای embedding / ingestion اسناد |
| `postgres` | دیتابیس اصلی Django |
| `redis` | broker برای Celery |
| `qdrant` | دیتابیس برداری برای ذخیره‌ی embeddings |
| `ollama` | اجرای مدل‌های زبانی به‌صورت لوکال |
| `ollama-pull` | جاب یک‌باره برای pull مدل پیش‌فرض بعد از healthy شدن Ollama |

## اجرا

```bash
cp .env.example .env
# مقادیر .env را ویرایش کنید (پسوردها، SECRET_KEY و ...)

docker compose up -d --build

# مهاجرت دیتابیس
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py createsuperuser
```

سرویس‌ها در دسترس خواهند بود:
- `http://localhost/` → فرانت‌اند
- `http://localhost/api/` → Django REST API
- `http://localhost:6333/dashboard` → Qdrant dashboard (در صورت باز بودن پورت)

## نکات تولید (Production)

- پورت‌های Qdrant و Ollama را در محیط واقعی پابلیک نکنید؛ فقط در شبکه‌ی داخلی `backend-net` نگه دارید (پورت‌مپینگشان را در `docker-compose.yml` کامنت کنید).
- یک `docker-compose.override.yml` برای محیط dev بسازید که پورت‌ها را باز کند و `DEBUG=True` ست کند.
- برای GPU، بخش `deploy.resources.reservations.devices` سرویس `ollama` را از کامنت خارج کنید (نیاز به `nvidia-container-toolkit` روی هاست).
- برای CI/CD یک `docker-compose.ci.yml` جدا با healthcheckهای سریع‌تر پیشنهاد می‌شود.
- اضافه کردن یک سرویس `backup` برای dump دوره‌ای `postgres-data` و `qdrant-data` توصیه می‌شود.

## ساختار پروژه

```
.
├── docker-compose.yml
├── .env.example
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── manage.py
│   ├── config/
│   │   ├── settings/{base,development,production}.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── celery.py
│   └── apps/rag/
│       ├── views.py        # health + query endpoint
│       ├── qdrant_client.py
│       ├── ollama_client.py
│       └── urls.py
├── frontend/
│   ├── Dockerfile
│   ├── nginx.frontend.conf
│   ├── package.json
│   ├── vite.config.js
│   └── src/{main.jsx, App.jsx}
└── nginx/
    └── nginx.conf
```

## License
MIT
