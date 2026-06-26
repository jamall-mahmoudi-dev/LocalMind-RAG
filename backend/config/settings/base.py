import os
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# ---------------- CORE ----------------
SECRET_KEY = env("DJANGO_SECRET_KEY", default="insecure-dev-key")
DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = env.list(
    "DJANGO_ALLOWED_HOSTS",
    default=["localhost", "127.0.0.1", "0.0.0.0"]
)

# ---------------- APPS ----------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "corsheaders",

    "apps.rag",
]

# ---------------- MIDDLEWARE ----------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # must be on top
    "django.middleware.security.SecurityMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

# ---------------- TEMPLATES ----------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ---------------- DATABASE ----------------
DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default="sqlite:///db.sqlite3"
    )
}

# ---------------- REST ----------------
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

# ---------------- CORS (FIXED FOR YOUR SETUP) ----------------
CORS_ALLOW_ALL_ORIGINS = DEBUG  # dev mode safe

CORS_ALLOWED_ORIGINS = env.list(
    "CORS_ALLOWED_ORIGINS",
    default=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://192.168.157.130:5173",
    ],
)

CORS_ALLOW_CREDENTIALS = True

# ---------------- CSRF (IMPORTANT FOR FRONTEND) ----------------
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://192.168.157.130:5173",
]

# ---------------- INTERNATIONALIZATION ----------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ---------------- STATIC / MEDIA ----------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ---------------- DEFAULT AUTO FIELD ----------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------- RAG STACK SETTINGS ----------------
QDRANT_URL = env("QDRANT_URL", default="http://qdrant:6333")
QDRANT_COLLECTION = env("QDRANT_COLLECTION", default="documents")

OLLAMA_URL = env("OLLAMA_URL", default="http://ollama:11434")
OLLAMA_MODEL = env("OLLAMA_MODEL", default="llama3.1:8b")

# مهم برای جلوگیری از mismatch embedding
OLLAMA_EMBED_MODEL = env("OLLAMA_EMBED_MODEL", default="nomic-embed-text")

# ---------------- CELERY ----------------
CELERY_BROKER_URL = env("REDIS_URL", default="redis://redis:6379/0")
CELERY_RESULT_BACKEND = env("REDIS_URL", default="redis://redis:6379/0")

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

# retry behavior (خیلی مهم برای RAG ingestion)
CELERY_TASK_ACKS_LATE = True
CELERY_TASK_REJECT_ON_WORKER_LOST = True