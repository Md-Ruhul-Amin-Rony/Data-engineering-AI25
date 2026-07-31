# Example 3 — two services, one command 🐘

A web service that reads from a **Postgres** database it does not contain.
Everything so far has been one container; this is the first time containers have
to find each other.

```text
        ┌────────────────┐          ┌────────────────┐
 you ──▶│  web   :8000   │────────▶ │   db   :5432   │
        │  Flask         │  SQL     │  postgres:16   │
        └────────────────┘          └────────────────┘
                                     database_init.sql
```

## Run it

```bash
cd 03-compose-postgres
docker compose up --build
```

Open port 8000. You should see `Users: user1, user2, user3`.
Stop with `Ctrl+C`, then:

```bash
docker compose ps        # both services
docker compose logs db   # what Postgres did on first boot
docker compose down      # stop and remove containers
docker compose down -v   # ...and delete the volume (the data)
```

## The four ideas in `compose.yaml`

1. **Service names are hostnames.** The connection string says `@db:5432`, not
   `localhost`. Compose gives every service a DNS name on a shared network. Inside
   `web`, `localhost` means *`web` itself*.
2. **Config comes from the environment.** `app.py` never contains a password; it
   reads `DATABASE_URL`. The same image runs against a local db or a managed
   Azure one.
3. **`depends_on` + `condition: service_healthy`.** Plain `depends_on` only waits
   for the container to *start*, not for Postgres to be *ready* — a race you will
   otherwise meet at a really inconvenient moment. The healthcheck fixes it.
4. **Volumes outlive containers.** `pgdata` keeps the rows across `down`/`up`.
   `database_init.sql` is mounted into `/docker-entrypoint-initdb.d/`, which
   Postgres runs **only when the data directory is empty** — so if you change the
   seed SQL, you need `docker compose down -v` before it takes effect. This
   confuses everyone exactly once.

## Then, without looking

1. Delete `Dockerfile` **and** `compose.yaml`.
2. Recreate both from scratch: an image for `web`, plus two services with the
   environment variable, the healthcheck, the volume mount and the port.
3. `docker compose up --build` until `Users: user1, user2, user3` comes back.

## Make it break, then fix it

* Change `@db:5432` to `@localhost:5432` in the compose environment. Run it, read
  the error, and be able to explain it out loud.
* Remove the `depends_on` healthcheck condition and restart repeatedly until the
  app loses the race. `docker compose logs web` will show the connection error.
* `docker compose exec db psql -U postgres -d mydatabase -c "\dt"` then
  `INSERT INTO users (username) VALUES ('mikael');` and reload the page.

## Where this is going

Swap Flask for FastAPI, `database_init.sql` for a CSV load, and you have the
[Compose ingestion exercise](../../lecture-2-compose/README.md) — which is the
same shape as the pipelines you build in the project half of the course.
