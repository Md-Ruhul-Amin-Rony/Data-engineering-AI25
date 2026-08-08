# Lecture 2.1 — Containerising the weather API 🐳

Companion exercises for **Lecture 2.1 – Containers & Docker** (Data Engineering,
week 33). This is the exercise the lecture and self-study actually build —
not [`lecture-2-docker/`](../lecture-2-docker/README.md), which is a separate,
optional bonus exercise with a different sample app.

Goal by the end: a small FastAPI service, built into an image, running as a
container, reachable on `localhost:8000`.

> **Where do I run this?**
> A GitHub Codespace — the one you already have open, same as every other
> session this week. `docker --version` should print something before you
> start.

---

## 0. Where you'll work 📁

Work in a scratch folder in
your existing Codespace, same pattern as `~/de-lecture1` from the Bash
lecture:

```bash
mkdir ~/lecture2-docker
cd ~/lecture2-docker
```

Everything below happens here.

---

## 1. Run it without Docker first 🧪

You cannot containerise something you have never seen work.

Create `app.py`:

```python
from fastapi import FastAPI

app = FastAPI(title="Weather API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/latest")
def latest():
    return {"temp_c": 18.4}
```

Install and run it — `uv` is already on your Codespace from Day 1, so there's
no need for `pip` or a venv here:

```bash
uv pip install --system fastapi 'uvicorn[standard]'
uvicorn app:app --host 0.0.0.0 --port 8000
```

Open `/health`, `/latest` and `/docs` (click the forwarded-port notification
in your Codespace). Then `Ctrl+C`.

`--host 0.0.0.0` matters even running bare like this. By default `uvicorn`
binds to `127.0.0.1` — "only accept connections that originate from this same
machine." Right now that's not a problem: your browser and the server are
both in the same Codespace, so it still works. But port-forwarding (what
Codespaces does to get `/docs` into your browser, and what `docker run -p`
does for a container) works by having something *outside* connect in — and
`127.0.0.1` refuses exactly that, no matter what port you forward. The fix is
always the same: bind to `0.0.0.0`, "accept connections on any network
interface." Build the habit here, where it's invisible, so it's not a
surprise once it's the actual reason `curl` says connection refused inside a
container.

---

## 2. Write the Dockerfile ✍️

Create `requirements.txt`:

```
fastapi
uvicorn[standard]
```

Then `Dockerfile`, next to `app.py`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.9.7 /uv /usr/local/bin/uv

COPY requirements.txt .
RUN uv pip install --system --no-cache -r requirements.txt

COPY app.py .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

Two lines worth pausing on:

* **`COPY --from=ghcr.io/astral-sh/uv:0.9.7 /uv /usr/local/bin/uv`** — this
  looks like the `COPY` you just used above, but it's a different thing
  entirely. Plain `COPY x y` copies from *your* files (the build context).
  `COPY --from=<image>` copies a file out of *another image* — here, the
  official `uv` distribution image — which is how you get the `uv` binary
  into yours without `apt install` or `curl | sh`.
* **`CMD [..., "--host", "0.0.0.0", ...]`** — bind to `127.0.0.1` inside a
  container and it's reachable only from inside that same container. Very
  private. Very useless.

Build and run it:

```bash
docker build -t weather-api:0.1 .
docker run --rm -p 8000:8000 weather-api:0.1
```

Hit `/health` again. Same response, different machine — that's the whole
lecture in one HTTP request.

---

## 3. Prove the caching claim 🧊

```bash
docker build -t weather-api:0.1 .        # again — everything CACHED, seconds
# now change the temp_c value in app.py, then:
docker build -t weather-api:0.2 .        # only the last layers rebuild
```

Then break it on purpose: move `COPY app.py .` above the `RUN uv pip install`
line, rebuild, and watch it reinstall everything. Put it back.

---

## 4. Config from the outside 🎛️

```bash
docker run --rm -p 8000:8000 -e GREETING="Hej från Stockholm" weather-api:0.1
docker run --rm -p 8080:8000 weather-api:0.1     # same image, different host port
```

The image never changes; the environment does. This is how the same artifact
goes from your Codespace to staging to production.

---

## 5. Look inside a running container 🔍

In one terminal, run the container; in another:

```bash
docker ps
docker exec -it <ID> sh          # slim images have sh, not bash
ls -al /app
exit
docker logs <ID>
```

`docker logs` is the first thing you check when a container "does nothing."
Usually it's a stack trace that's been waiting patiently for you.

---

## 6. Mount a volume 📂

```bash
docker run --rm -p 8000:8000 -v ./data:/app/data weather-api:0.1
```

1. With the container running, shell in: `docker exec -it <ID> sh`
2. From *inside* the container, create a file in the mounted path:
   `echo "hello from inside" > /app/data/note.txt`, then `exit`.
3. Look at `./data/` on your Codespace — the file is there too.
4. `docker stop` and `docker rm` the container. The file is still there —
   proof that data in a mounted volume outlives the container.

---

## 7. Exercises ✅

Core deliberately repeats Sections 1–2 — the point is to see if you can do it
again without the walkthrough open next to you, not to learn something new.
Then is where it gets new: things that were only briefly demoed above, now
for you to do unaided.

**Core** — do these first:

1. Set up the scratch folder, write `app.py`, run it bare with `uv` (Section 1).
2. Write the Dockerfile from scratch — no peeking at Section 2 until you've
   tried.
3. Build it as `weather-api:0.1`, run it, open `/docs`.

**Then** — behave like an engineer:

4. Add a `.dockerignore` (at least `.venv`, `__pycache__/`, `*.pyc`) and
   rebuild — compare `docker images` sizes before/after.
5. Read a setting from an env var (Section 4) — run two containers on
   different ports with different values at the same time.
6. Mount a volume and write a file *from inside the container* — confirm it
   survives `docker stop` + `docker rm` (Section 6).
7. Shell in with `docker exec` and look around (Section 5).

**Before next week:**

8. Activate your Azure for Students account.
9. Activate your Hopsworks account.
10. Repeat the Bash exercises in a fresh Codespace, if Tuesday feels rusty.
11. Add one extra endpoint of your own. Stuck for ideas? `/stations` (a
    couple more fake station IDs) or `/average` (mean of a few hardcoded
    readings) — or anything else you'd rather build.

Ungraded, self-paced — nothing to hand in. Come to Week 2 with something
running, not something perfect.

---

## 8. Debugging cheat sheet 🧰

| Symptom | Usual cause |
| --- | --- |
| `curl: connection refused` | bound to `127.0.0.1`, or missing `-p` |
| container exits immediately | `CMD` is wrong, or the process isn't long-running — read `docker logs` |
| `port is already allocated` | previous container still running: `docker ps` then `docker stop` |
| build is slow every time | `COPY app.py .` before the install step, or no `.dockerignore` |
| `exec: "bash": not found` | slim image: use `sh` |
| edits don't show up | you rebuilt nothing, or you have no volume mounted |
| `Error loading ASGI app` | check the module:attribute in CMD actually matches your file layout |

## Resources

* [Docker docs — build best practices](https://docs.docker.com/build/building/best-practices/)
* [FastAPI in containers](https://fastapi.tiangolo.com/deployment/docker/)
* `docker <command> --help` — still faster than a search engine

---

## Next 👉

More Docker, and version control, next week.
