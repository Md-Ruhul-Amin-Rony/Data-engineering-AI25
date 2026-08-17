# Debugging Challenge: Another Team's Weather Pipeline

This is the same pipeline you built this morning — ingestion API, Postgres, a raw
table and a clean view — but written by someone else, and broken on purpose.

Your job: get it running end to end, and say what you'd change even after it works.

```
GET /ingestion?location=Stockholm&date=<today or later>
        │
        ▼
  ingestion API (FastAPI) ──▶ raw__weatherapp (table, append-only)
                                      │
                                      ▼
                            clean__weatherapp (view)
```

## Before you start

- Put your own weatherapi.com key into `.env` (`API_KEY=`). That's not one of the
  bugs — every copy of this repo needs its own key.
- Work in a group of three. One person drives, the other two read.
- **Keep a log.** For every problem: what you saw, how you found it, what you
  changed. The log matters more than the fixes — we compare logs afterwards.

## The bugs come in three flavours

**Loud** — something refuses to start, and says so. Read the whole error before
searching; most of these announce themselves clearly.

**Quiet** — everything starts, every request returns `200`, and the data is
wrong anyway. You will only find these by *looking at the data*, not the logs.

**Smells** — it works, and you still wouldn't ship it. Nothing to fix to reach
"done", but a reviewer would comment. You practised exactly this on Tuesday.

There is at least one of each. There are more quiet ones than you'll expect.

## Definition of done

1. `docker compose up --build` starts all three services with no manual steps
   beyond editing `.env`.
2. `GET /ingestion?location=Stockholm&date=<today>` returns `200` with
   `rows_inserted` greater than zero.
3. `SELECT * FROM raw__weatherapp` in Adminer shows real rows.
4. `SELECT * FROM clean__weatherapp` shows sensible, correctly typed values —
   look closely at each column, not just the row count.
5. **Ingest a second location** (try Zurich, then Gothenburg). Both must still
   be visible in the clean view afterwards. This one catches a bug that nothing
   else in this list will.
6. You have a written list of at least three things you'd change in code review
   even though they don't break anything.

## Rules

- Don't diff against this morning's working version until you're done. You'll
  learn more finding them; and in a real job there is nothing to diff against.
- Fix in dependency order: containers must start before the app can run, and the
  app must insert before the view has anything to show.
- Don't stop at the first green light. Points 4 and 5 above exist because a
  pipeline that returns `200 OK` and stores the wrong thing is worse than one
  that crashes — the crash tells you.

## Hints (open only if properly stuck)

<details>
<summary>Hint 1 — it never even finishes building</summary>

The failure is in `pip install`, and the error names a program it couldn't
find. That program belongs to Postgres, not to Python.

Compare the database driver line in `requirements.txt` with the one you used
this morning. One character of difference decides whether pip downloads a
ready-built package or tries to compile one from source inside a slim image
that has no compiler.
</details>

<details>
<summary>Hint 2 — the database container starts and then dies</summary>

`docker compose logs db`. The init scripts in `database/init/` run in a specific
order, and it isn't the order you'd like. What decides it?

And once you've fixed it: why doesn't simply restarting help? What has to happen
to the volume before those scripts run again?
</details>

<details>
<summary>Hint 3 — the container is up, the port is mapped, the browser says nothing is there</summary>

`docker compose ps` says running. `docker compose logs ingestion` says uvicorn
started fine. So the process is alive and listening — the question is *where*.
Compare the `CMD` line with the one you used this morning.

Try `docker compose exec ingestion curl localhost:8000` and think about why that
works when your browser doesn't.
</details>

<details>
<summary>Hint 4 — the API responds but ingestion fails</summary>

Read the error text in the HTTP response. Something is trying to reach the
database and not finding it. Inside a container, what does `localhost` mean?
Which name did this morning's version use, and where does that name come from?
</details>

<details>
<summary>Hint 5 — it all works, but is the data right?</summary>

Ingest Stockholm. Then ingest Zurich. Then:

```sql
SELECT count(*) FROM raw__weatherapp;
SELECT count(*) FROM clean__weatherapp;
SELECT location, count(*) FROM clean__weatherapp GROUP BY location;
```

Is every city you ingested still there? If not — what is the view's
`PARTITION BY` actually grouping on, and what does that assume about two cities
in the same time zone?

Also look hard at `condition_text`. Does it look like the others?
</details>

<details>
<summary>Hint 6 — the smells</summary>

Open `requirements.txt` and count the lines. Now open `ingestion.py` and count
the imports. Where did the rest come from, and what does that cost you?

Then: `docker history weatherapp-debug-ingestion`. Is there anything in those
layers that you would not want to publish?
</details>

Good luck. Bring your log to the share-back — one bug each, and how you caught it.
