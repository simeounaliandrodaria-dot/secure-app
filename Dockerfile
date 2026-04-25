# Build stage to compile dependencies
FROM python:3.12-slim-bookworm AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Final stage – minimal, hardened
FROM python:3.12-slim-bookworm

# Apply the latest OS security patches
RUN apt-get update && apt-get dist-upgrade -y && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create non‑root user
RUN groupadd -r appuser && useradd -r -g appuser appuser
WORKDIR /app

# Copy only the installed packages and the application
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY app/ ./app/

# Change ownership and switch to non‑root user
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

CMD ["python", "-m", "flask", "--app", "app.main", "run", "--host=0.0.0.0"]
