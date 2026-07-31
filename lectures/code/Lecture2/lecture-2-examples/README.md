# Lecture 2.1 — Docker examples (the warm-up ladder) 🪜

Three tiny examples, in order. They are **not** the graded exercises — they exist
so that everyone in the room has built and run *something* before we attempt the
FastAPI + Postgres work.

| # | Folder | New thing it teaches | Who runs it |
| --- | --- | --- | --- |
| 1 | `01-hello-image/` | `build → run → ps -a → images` on a one-file image, no deps, no ports | **teacher demos** on screen (~3 min) |
| 2 | `02-flask-hello/` | dependencies + a published port you open in the browser | **you**, at your keyboard (~15 min) |
| 3 | `03-compose-postgres/` | two services, one command, a database with seed data | **you**, if there is time — otherwise read it |

Then the real work: [single-container FastAPI](../lecture-2-docker/README.md)
and [Compose ingestion pipeline](../lecture-2-compose/README.md).

> **Where do I run this?** A GitHub Codespace. Docker and Compose are already
> installed and forwarded ports open with one click. `docker --version` should
> print something before you start.

---

## Why demo #1 instead of letting everyone run it?

Because if Docker is broken in your environment, example 1 is where we find out —
and 20 people debugging simultaneously is not a lecture. Watch it once, then
break things yourself in example 2.

---

## A note on `pip` vs `uv` 📦

From example 2 onward we install dependencies with
[**uv**](https://docs.astral.sh/uv/) instead of `pip`:

```dockerfile
COPY --from=ghcr.io/astral-sh/uv:0.9.7 /uv /usr/local/bin/uv
RUN uv pip install --system --no-cache -r requirements.txt
```

Why bother:

* it is *much* faster, which matters when a rebuild is on the critical path of a
  30-person exercise,
* the resolver is stricter, so "works on my machine" fails at build time instead
  of at 02:00 in production,
* it is the same tool we use for local venvs (`uv venv`, `uv pip install`), so
  there is one story instead of two.

`--system` means "install into the image's Python, not a venv" — inside a
container there is nothing else to isolate from. Example 1 has no dependencies
at all, so it needs neither tool.

The old `pip install --no-cache-dir -r requirements.txt` line still works
everywhere; if you meet it in the wild, it is the same idea, slower.

---

## Housekeeping commands you will use all course

```bash
docker ps            # running containers
docker ps -a         # including the dead ones
docker images        # local images
docker stop <ID>     # polite shutdown
docker rm <ID>       # remove a stopped container
docker rmi <IMAGE>   # remove an image
docker system df     # where did my disk go?
```

Containers you never remove are like the 47 browser tabs you never close: free,
until suddenly not.
