# Lecture 2.1 — Docker Compose hands-on 🐘🐳

**This is the hard one.** Do the [single-container exercise](../lecture-2-docker/README.md)
first — this task assumes you can already write a Dockerfile.

Here you build a *two-service* system: a FastAPI service that loads a CSV into a
**Postgres** database on startup and then serves it over HTTP. That is a small
but complete ingestion pipeline — the same shape as the pipelines you will build
in the project part of the course, minus the orchestration.

```text
        ┌──────────────┐            ┌──────────────┐
 you ──▶│  api  :8000  │──────────▶ │   db  :5432  │
        │  FastAPI     │  SQL       │  postgres:16 │
        └──────────────┘            └──────────────┘
              ▲                            │
        data/customers.csv           postgres_data volume
```

Run it in a Codespace (Docker and Compose are already there) or locally with
Docker Desktop. Check: `docker compose version` should print v2.x.

## Files in this folder

| Path | What it is |
| --- | --- |
| `api/main.py` | the service — **do not edit it to make it work** |
| `api/requirements.txt` | pinned dependencies |
| `data/customers.csv` | 120 fake customers to ingest |
| `solution/` | Dockerfile + compose.yaml — after you have tried 🙈 |

---

## 0. Read the code before you build anything 📖

Open `api/main.py` and answer these for yourself:

1. Where does the database URL come from? (It is *not* in the code.)
2. What happens in `lifespan()` and how often does it run?
3. Which endpoints exist?

If you skip this step you will spend 40 minutes debugging a container that is
doing exactly what you told it to.

---

## 1. Your task 🛠️

Create two files:

**`api/Dockerfile`** — builds a Python image that serves the app on port 8000.
The app runs under uvicorn, so it ends with:

```dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**`compose.yaml`** (in this folder) with two services:

* `db` — image `postgres:16-alpine`, with `POSTGRES_USER=user`,
  `POSTGRES_PASSWORD=password`, `POSTGRES_DB=mydatabase`, and a **named volume**
  for `/var/lib/postgresql/data`.
* `api` — built from `./api`, publishing `8000:8000`, with
  `DATABASE_URL=postgresql://user:password@db:5432/mydatabase`, and the `./data`
  folder mounted read-only at `/app/data`.

Then:

```bash
docker compose up --build
```

and check:

```bash
curl localhost:8000/            # {"service":"customers-api","rows_loaded":120}
curl localhost:8000/health
curl "localhost:8000/customers?limit=3"
curl "localhost:8000/customers?country=Sweden&limit=5"
curl localhost:8000/countries
```

> **The one thing to understand here:** the host is `db`, not `localhost`.
> Inside a compose network the *service name* is the DNS name. `localhost` from
> the api container means "the api container", which has no database on it.

---

## 2. Race condition, on purpose 🏁

Start with a plain `depends_on: [db]` and run `docker compose down -v` then
`docker compose up --build` a couple of times. Sooner or later the api crashes
with `could not connect to server`.

`depends_on` only waits for the container to *start*, not for Postgres to be
*ready to accept connections*. Fix it properly:

```yaml
  db:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d mydatabase"]
      interval: 3s
      retries: 10
  api:
    depends_on:
      db:
        condition: service_healthy
```

This exact bug shows up in every real pipeline. Now you have seen it in 30
seconds instead of in production at 02:00.

---

## 3. Poke the database directly 🔎

```bash
docker compose ps
docker compose logs api          # add -f to follow
docker compose exec db psql -U user -d mydatabase -c '\dt'
docker compose exec db psql -U user -d mydatabase \
  -c 'select country, count(*) from customers group by 1 order by 2 desc limit 5;'
```

Prove the volume works:

```bash
docker compose down          # keeps the volume
docker compose up            # rows still there, load is skipped
docker compose down -v       # deletes the volume
docker compose up            # 120 rows ingested again
```

`down` vs `down -v` is the difference between a restart and a data loss
incident. Learn it here.

---

## 4. Exercises ✅

**Core**

1. Get `docker compose up --build` working with both services and all five
   endpoints answering.
2. Make `api` wait for a *healthy* `db` and explain in one sentence why
   `depends_on` alone is not enough.
3. Show with `psql` that the `customers` table really contains 120 rows.
4. Demonstrate the difference between `docker compose down` and `down -v`.

**Then**

5. Remove the `ports:` block from `db` and show that the api still works.
   Why? Which network is involved?
6. Add a `GET /customers/{id}` endpoint, rebuild only the api
   (`docker compose up --build api`), and return `404` for an unknown id.
7. Move the credentials into a `.env` file and reference them
   (`POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}`). Add `.env` to `.gitignore`.
   Hard-coded passwords in compose files are a habit worth never forming.
8. Scale it: `docker compose up --scale api=2` — what breaks, and why is the
   published port the problem?

**Advanced** — pick one

9. Add a third service `adminer` (image `adminer`, port `8080:8080`) and browse
   the database in a UI.
10. Add a `loader` service that runs the ingestion once and exits, so the api
    only serves data. Which service should own schema creation then?
11. Persist a second volume with a `./sql/init.sql` mounted into
    `/docker-entrypoint-initdb.d/` that creates an index on `country`. Verify
    with `explain analyze`.
12. Replace `psycopg2-binary` with `psycopg[binary]` (v3) and adjust the URL to
    `postgresql+psycopg://…`. Note what the error message tells you when you get
    it wrong.

---

## 5. Debugging cheat sheet 🧰

| Symptom | Usual cause |
| --- | --- |
| `could not translate host name "db"` | you used `localhost`, or the service is named something else |
| `connection refused` on startup | Postgres not ready yet — use the healthcheck |
| `password authentication failed` | credentials in `DATABASE_URL` do not match the `db` env vars |
| `FileNotFoundError: /app/data/customers.csv` | the `./data` volume is not mounted (or wrong path) |
| rows keep duplicating | the loader is not idempotent — read `load_csv()` again |
| `port is already allocated` | something else is on 5432/8000: `docker compose down`, or change the host port |
| stale code after an edit | `docker compose up --build`, not just `up` |
| `RuntimeError: DATABASE_URL is not set` | you forgot `environment:` on the api service |

## Resources

* [Compose file reference](https://docs.docker.com/reference/compose-file/)
* [Postgres image docs](https://hub.docker.com/_/postgres) — read the env vars section
* [SQLAlchemy 2.0 ORM quickstart](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)
* `docker compose --help`
