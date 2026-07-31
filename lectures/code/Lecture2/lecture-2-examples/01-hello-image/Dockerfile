# Example 1 — three instructions, one image.
# python:3.12-slim is small and current. Never use a base image whose Python
# is out of support (3.9 went EOL in October 2025) — no security fixes.
FROM python:3.12-slim

WORKDIR /app

COPY hello.py .

CMD ["python", "hello.py"]
