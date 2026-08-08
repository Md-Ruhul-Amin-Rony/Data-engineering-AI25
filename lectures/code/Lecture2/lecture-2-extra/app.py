"""Tiny FastAPI service — the thing we are going to containerise.

Run it locally:   uvicorn app:app --reload --port 8000
Run it in Docker: see README.md
"""

import os
import platform
from datetime import datetime, timezone

from fastapi import FastAPI

app = FastAPI(title="de-hello", version="0.1.0")

# Read at import time on purpose: a container gets its config from the
# environment, not from a file you forgot to copy into the image.
GREETING = os.getenv("GREETING", "Hello from inside the container")


@app.get("/")
def root():
    return {"message": GREETING}


@app.get("/health")
def health():
    """Every service you deploy this course needs one of these."""
    return {"status": "ok"}


@app.get("/whoami")
def whoami():
    """Proof that the container is a different machine than your laptop."""
    return {
        "hostname": platform.node(),
        "python": platform.python_version(),
        "os": platform.platform(),
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


# Exercise 4: add an endpoint below.
#
# @app.get("/rows")
# def rows():
#     # count the lines in data/cities.csv and return {"rows": n}
#     ...
