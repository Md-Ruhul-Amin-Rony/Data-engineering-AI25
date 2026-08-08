# Reference solution — try it yourself first. 🙈
FROM python:3.12-slim

WORKDIR /app

# uv instead of pip: same job, far faster, stricter resolver.
# COPY --from=<image> is a different form of COPY — it pulls a file out of
# another image (the official uv distribution), not out of this repo.
COPY --from=ghcr.io/astral-sh/uv:0.9.7 /uv /usr/local/bin/uv

COPY requirements.txt .
RUN uv pip install --system --no-cache -r requirements.txt

COPY app.py .

EXPOSE 8000

# --host 0.0.0.0, not localhost — otherwise the server only answers itself.
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
