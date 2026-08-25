FROM python:3.12-slim
WORKDIR /app

# uv instead of pip: same job, far faster, stricter resolver.
COPY --from=ghcr.io/astral-sh/uv /uv /usr/local/bin/uv

# Then break it on purpose: move COPY app.py . above the RUN uv pip install line, rebuild, and watch it reinstall everything. Put it back.
COPY requirements.txt .

RUN uv pip install --system --no-cache -r requirements.txt

COPY app.py .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
