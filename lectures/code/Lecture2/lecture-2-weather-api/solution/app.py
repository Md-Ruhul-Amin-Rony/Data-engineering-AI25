"""Reference solution — try it yourself first. 🙈

Run it locally:   uv pip install --system fastapi 'uvicorn[standard]'
                   uvicorn app:app --host 0.0.0.0 --port 8000
Run it in Docker:  see ../README.md
"""

from fastapi import FastAPI

app = FastAPI(title="Weather API")


@app.get("/health")
def health():
    """Every service you deploy this course needs one of these."""
    return {"status": "ok"}


@app.get("/latest")
def latest():
    return {"temp_c": 18.4}


# Exercise 11: add an endpoint of your own below.
#
# @app.get("/stations")
# def stations():
#     return {"stations": ["71420", "98230", "53430"]}
