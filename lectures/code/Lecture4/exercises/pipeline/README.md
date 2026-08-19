# Weather pipeline — Lecture 4

A minimal data pipeline in three containers: an ingestion API, a Postgres
database, and a web UI to look inside it.

```
weatherapi.com  ──►  ingestion (FastAPI)  ──►  raw__weatherapp   (table, append-only)
                                                     │
                                                     ▼
                                               clean__weatherapp (view, typed + deduplicated)
```

## Run it

```bash
cp .env.example .env        # then paste your weatherapi.com key into .env
docker compose up --build
```

That's the whole setup. Three services start, the database creates its tables
from `database/init/`, and the ingestion service waits until the database is
actually ready before starting.

**Why `--build`?** Compose builds an image only if one doesn't exist yet, so
the first run works without the flag. But it does *not* rebuild just because
you edited a file — on the second run it starts a container from the image it
already has, and your code changes silently don't take effect. `--build`
forces the rebuild. It's cheap here: dependencies live in their own cached
layer, so editing `ingestion.py` rebuilds only the last step.

Three different kinds of staleness, three different fixes — worth keeping
straight:

| You changed... | You need |
|---|---|
| `ingestion.py`, `Dockerfile`, `requirements.txt` | `docker compose up --build` (rebuild the image) |
| `docker-compose.yml`, `.env` | `docker compose up` (recreates containers) |
| `database/init/*.sql`, or the DB credentials | `docker compose down -v` first (wipe the volume) |

## On GitHub Codespaces

Everything works unchanged — the course devcontainer includes the
docker-in-docker feature, so `docker compose` is available inside your
Codespace and the bind mount of `database/init/` resolves normally.

One difference: **don't type `localhost:8080` into your browser's address
bar.** Your Codespace is on a remote machine, not your laptop. Open the
**PORTS** tab in VS Code, find ports 8000 and 8080, and click the globe icon
to open the forwarded `*.app.github.dev` URL instead.

Inside Adminer, the Server field is still `db`. Port forwarding only affects
how *your browser* reaches the containers; the containers reach each other
over the Docker network exactly as they would anywhere else.

The first `docker compose up --build` is slower in a fresh Codespace, since
it has to pull the Postgres, Adminer, and Python images.

Then:

- **Ingest a day:** <http://localhost:8000/ingestion?location=Stockholm&date=2026-08-16>
- **Look at the data:** <http://localhost:8080> (Adminer)
  - System: **PostgreSQL** ← it defaults to MySQL, change it or nothing works
  - Server: **db** ← not `localhost`; Adminer runs inside the Docker network
  - Username / Password / Database: from your `.env`

Stop with `Ctrl-C`, or `docker compose down`. Add `-v` to also wipe the
database and start clean next time.

## What each piece is for

**`raw__weatherapp` is a table.** The API response goes in verbatim, one row
per forecast hour, JSON untouched. It is append-only: ingest the same location
and date twice and you get two sets of rows, both kept. That's deliberate —
raw data you still have is raw data you can re-derive from when your
transformation logic turns out to be wrong, and a weather API will not sell you
last Tuesday back.

**`clean__weatherapp` is a view.** Nothing is ever inserted into it. It stores
a *query*, which Postgres runs against the raw table every time you select from
it. The query pulls six fields out of the JSON with real types, and keeps only
the most recently ingested version of each `(location, hour)` pair. So:

```sql
SELECT count(*) FROM raw__weatherapp;    -- grows with every ingestion
SELECT count(*) FROM clean__weatherapp;  -- one row per place per hour
```

Run an ingestion twice and watch those two numbers diverge. That difference is
the whole point of the layer split.

**Compose ties it together.** One network (created automatically), one volume
for the database's files, one `.env` shared by both services at run time.
Services find each other by service name — that's why the ingestion code
connects to a host called `db`.

## Layout

```
docker-compose.yml            three services, one network, one volume
.env.example                  copy to .env; never commit the real one
database/init/01_raw__*.sql   creates the raw table
database/init/02_clean__*.sql creates the clean view
ingestion/ingestion.py        ~60 lines: fetch, unpack, insert
ingestion/Dockerfile          deps in a cached layer, then the code
ingestion/requirements.txt    five direct dependencies
```

The two SQL files run automatically the first time the database starts, via
`/docker-entrypoint-initdb.d` — a convention of the official Postgres image.
It runs `*.sql` files in filename order, which is what the `01_`/`02_` prefixes
are for, and **only when the data directory is empty**.

## Troubleshooting

**Adminer rejects my credentials.** Check the System dropdown first — it
defaults to MySQL/MariaDB and must say PostgreSQL. Server must be `db`. Only
then suspect the username and password.

**`bind: address already in use`.** Something else on your machine holds that
port. `docker ps` to check for another stack, `lsof -nP -iTCP:8080 -sTCP:LISTEN`
to see what owns it. Or change the left-hand number in the `ports:` mapping —
the left side is your machine, the right side is inside the container, and only
the left one can collide. (The database is already on 5433 on the host for
exactly this reason, while staying 5432 inside the network.)

**I changed `.env` and nothing happened.** Postgres reads `POSTGRES_USER`,
`POSTGRES_PASSWORD` and `POSTGRES_DB` only when it initialises an *empty* data
directory. The volume survives `docker compose down`, so later edits are
ignored and you get `password authentication failed`. Run
`docker compose down -v`, then up again. Same rule applies to the `init/*.sql`
scripts — editing them does nothing until the volume is wiped.

**One of my SQL scripts has an error.** The container exits during startup and
`docker compose logs db` shows the `psql` error. Restarting won't re-run
anything, because the data directory is no longer empty. `down -v` and retry.

**`API_URL / API_KEY not set`.** Your `.env` is missing those lines, or you
never copied `.env.example`.

**The API returns no forecast for my date.** `forecast.json` covers today and
roughly two weeks ahead. Past dates need the `history.json` endpoint, which is
a paid feature on some plans.
