# Example 2 — dependencies + a port.
FROM python:3.12-slim

# uv instead of pip: same job, an order of magnitude faster, stricter resolver.
COPY --from=ghcr.io/astral-sh/uv:0.9.7 /uv /usr/local/bin/uv

WORKDIR /app

# Dependencies first, so editing app.py does not reinstall Flask.
COPY requirements.txt .
RUN uv pip install --system --no-cache -r requirements.txt

COPY . .

# Documentation only — publishing still needs -p on docker run.
EXPOSE 8000

CMD ["python", "app.py"]
