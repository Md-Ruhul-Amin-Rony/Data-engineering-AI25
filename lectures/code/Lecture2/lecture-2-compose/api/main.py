# api/main.py — FastAPI + Postgres, loaded from a CSV on startup.
#
# You do not need to change this file. Your job is the Dockerfile and
# compose.yaml that make it run.
import os
from contextlib import asynccontextmanager

import pandas as pd
from fastapi import FastAPI, HTTPException
from sqlalchemy import String, create_engine, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

DATABASE_URL = os.environ.get("DATABASE_URL")
CSV_PATH = os.environ.get("CSV_PATH", "/app/data/customers.csv")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. Pass it in from compose.yaml, not from code."
    )

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


class Base(DeclarativeBase):
    pass


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    first_name: Mapped[str] = mapped_column(String, index=True)
    last_name: Mapped[str] = mapped_column(String)
    country: Mapped[str] = mapped_column(String, index=True)


def load_csv() -> int:
    """Idempotent load: safe to run every time the container starts."""
    Base.metadata.create_all(bind=engine)
    df = pd.read_csv(CSV_PATH)
    with Session(engine) as session:
        existing = session.scalar(select(func.count()).select_from(Customer))
        if existing:
            return existing
        session.add_all(
            Customer(
                id=str(row["customer_id"]),
                first_name=row["first_name"],
                last_name=row["last_name"],
                country=row["country"],
            )
            for _, row in df.iterrows()
        )
        session.commit()
        return len(df)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs once when the container starts, before the first request.
    app.state.rows = load_csv()
    yield


app = FastAPI(title="Customers API", lifespan=lifespan)


@app.get("/")
def read_root():
    return {"service": "customers-api", "rows_loaded": app.state.rows}


@app.get("/health")
def health():
    with engine.connect() as conn:
        conn.exec_driver_sql("SELECT 1")
    return {"status": "ok", "db": "reachable"}


@app.get("/customers")
def read_customers(skip: int = 0, limit: int = 10, country: str | None = None):
    if limit > 100:
        raise HTTPException(status_code=400, detail="limit must be <= 100")
    stmt = select(Customer).offset(skip).limit(limit)
    if country:
        stmt = stmt.where(Customer.country == country)
    with Session(engine) as session:
        return session.scalars(stmt).all()


@app.get("/countries")
def top_countries(limit: int = 5):
    stmt = (
        select(Customer.country, func.count().label("n"))
        .group_by(Customer.country)
        .order_by(func.count().desc())
        .limit(limit)
    )
    with Session(engine) as session:
        return [{"country": c, "customers": n} for c, n in session.execute(stmt)]
