# VULNERABLE: Uses an old, unsupported Python 3.8 image based on Debian 10 (buster)
FROM python:3.8-slim-buster

# Missing best practices: no non-root user, no multi-stage build, no security updates

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 5000

# Run as root user (vulnerable)
CMD ["python", "-m", "flask", "--app", "app.main", "run", "--host=0.0.0.0"]
