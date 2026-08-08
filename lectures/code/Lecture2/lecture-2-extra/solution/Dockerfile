# Reference solution — try it yourself first. 🙈
# Note the order: dependencies before source code, so that editing app.py
# does not invalidate the (slower) dependency layer.
FROM python:3.12-slim

# uv instead of pip: same job, far faster, stricter resolver.
COPY --from=ghcr.io/astral-sh/uv:0.9.7 /uv /usr/local/bin/uv

WORKDIR /app

COPY requirements.txt .
RUN uv pip install --system --no-cache -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
