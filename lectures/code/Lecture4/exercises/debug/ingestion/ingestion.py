"""Fetch a day of hourly weather for one location and land it in the raw layer."""

import os

import psycopg2
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from psycopg2.extras import Json

load_dotenv()

app = FastAPI()

DB_SETTINGS = {
    "host": "localhost",
    "port": 5432,
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "dbname": os.getenv("POSTGRES_DB"),
}


@app.get("/")
def read_root():
    return {"try": "/ingestion?location=Stockholm&date=2026-08-20"}


@app.get("/ingestion")
def ingestion(location: str, date: str):
    api_url = os.getenv("API_URL")
    api_key = os.getenv("API_KEY")
    if not api_url or not api_key:
        raise HTTPException(500, "API_URL / API_KEY not set - check your .env file")

    response = requests.get(
        api_url, params={"key": api_key, "q": location, "dt": date}, timeout=10
    )
    if not response.ok:
        raise HTTPException(502, f"Weather API returned {response.status_code}: {response.text[:200]}")

    payload = response.json()
    try:
        canonical_location = payload["location"]["name"]
        hours = payload["forecast"]["forecastday"][0]["hour"]
    except (KeyError, IndexError) as exc:
        raise HTTPException(502, f"Unexpected response shape from the weather API (missing {exc})")

    conn = psycopg2.connect(**DB_SETTINGS)
    try:
        with conn, conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO raw__weatherapp (location, time_epoch, data) VALUES (%s, %s, %s)",
                [(canonical_location, hour["time_epoch"], Json(hour)) for hour in hours],
            )
    except Exception as exc:
        raise HTTPException(500, f"Insert into the database failed: {exc}")
    finally:
        conn.close()

    return {
        "status": "ok",
        "location": canonical_location,
        "date": date,
        "rows_inserted": len(hours),
    }
