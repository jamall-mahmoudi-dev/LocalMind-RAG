ARG PYTHON_VERSION=3.12-slim

# ---------- base ----------
FROM python:${PYTHON_VERSION} AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ---------- deps ----------
FROM base AS deps
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# ---------- production ----------
FROM deps AS production
RUN addgroup --system django && adduser --system --ingroup django django

COPY . .
RUN mkdir -p /app/staticfiles /app/media \
    && chown -R django:django /app

USER django

EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=5s --retries=5 \
    CMD curl -f http://localhost:8000/api/health/ || exit 1

CMD ["gunicorn", "config.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--timeout", "60", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
