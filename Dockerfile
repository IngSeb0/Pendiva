FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PENDIVA_HOST=0.0.0.0 \
    PENDIVA_PORT=8000 \
    PENDIVA_LIVE_DB=/app/data/live.sqlite3

WORKDIR /app
COPY src /app/src
RUN mkdir -p /app/data && useradd --system --uid 10001 --create-home appuser \
    && chown -R appuser:appuser /app
USER appuser
EXPOSE 8000
CMD ["python", "-m", "src.live_app"]
