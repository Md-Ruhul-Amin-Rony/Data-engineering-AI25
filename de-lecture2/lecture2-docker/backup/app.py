from fastapi import FastAPI

app = FastAPI(title="Weather API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/latest")
def latest():
    return {"temp_c": 3.4}
