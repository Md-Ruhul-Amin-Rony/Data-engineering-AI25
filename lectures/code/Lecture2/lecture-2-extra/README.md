# Lecture 2.1 — Docker hands-on (optional bonus) 🐳

> **This is not Thursday's exercise.** The live session and self-study both
> build a different app (`weather-api`) from the slide deck, from scratch, in
> your own repo. This folder is a separate, optional exercise if you want more
> Docker practice afterwards — same ideas, a different sample app (`de-hello`),
> so there's no risk of mixing the two up.

Companion exercises for **Lecture 2.1 – Containers & Docker** (Data Engineering, week 33).
Goal by the end: you can take a Python service you wrote, put it in an image,
run it as a container, and hand someone else a single command that works.

> **Where do I run this?**
> A GitHub Codespace is the safe bet — Docker is already installed and you have
> been using Codespaces since day 1. Local Docker Desktop / WSL 2 works too.
> `docker --version` should print something before you continue.

Files in this folder:

| File | What it is |
| --- | --- |
| `app.py` | a tiny FastAPI service (`/`, `/health`, `/whoami`) |
| `requirements.txt` | pinned dependencies |
| `dockerignore.example` | rename to `.dockerignore` |
| `compose.yaml` | for the advanced exercise |
| `solution/Dockerfile` | look after you have tried 🙈 |

---

## 0. Warm-up: someone else's image 📦

```bash
docker run hello-world              # pull + run + exit
docker run -it --rm python:3.12-slim python -c "print(2**10)"
docker run -it --rm python:3.12-slim bash   # look around, then: exit
```

`-it` gives you a terminal, `--rm` deletes the container when it stops.
Without `--rm` you collect dead containers like browser tabs.

Housekeeping — you will need these all course:

```bash
docker ps                # running containers
docker ps -a             # including stopped ones
docker images            # local images
docker stop <ID>         # polite shutdown
docker rm <ID>           # remove a stopped container
docker rmi <IMAGE>       # remove an image
docker system df         # how much disk have I actually used?
```

> Nothing is running but your disk lost 12 GB? That is Docker. `docker system prune`
> is the answer, and yes, read what it says before you say yes.

---

## 1. Run the service *without* Docker first 🧪

You cannot containerise something you have never seen work.

```bash
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

Open `/`, `/health` and `/whoami` (in a Codespace: click the forwarded-port
notification; locally: <http://localhost:8000/whoami>). Then `Ctrl+C`.

Note what `/whoami` says about hostname and OS. We come back to that.

---

## 2. Write your own Dockerfile ✍️

Create a file called `Dockerfile` (capital D, no extension) next to `app.py`.
You need exactly these instructions, in a sensible order:

```text
FROM        which base image (hint: python:3.12-slim)
WORKDIR     where inside the image we work (/app)
COPY        --from=ghcr.io/astral-sh/uv:0.9.7 /uv /usr/local/bin/uv
COPY        requirements.txt first — layer caching!
RUN         uv pip install --system --no-cache -r requirements.txt
COPY        the rest of the source
EXPOSE      document the port
CMD         how to start uvicorn, binding 0.0.0.0
```

Two traps that cost everyone 20 minutes:

* **`--host 0.0.0.0`.** Bind to `127.0.0.1` inside a container and it is
  reachable only from inside that container. Very private. Very useless.
* **COPY order.** Copy the source before installing dependencies and every
  one-character edit re-installs everything.
* **`uv`, not `pip`.** We install with [uv](https://docs.astral.sh/uv/): same
  job, an order of magnitude faster, and the same tool as your local `uv venv`.
  `--system` = install into the image's Python; a container has nothing to
  isolate from.

Also rename the ignore file, then build and run:

```bash
mv dockerignore.example .dockerignore
docker build -t de-hello:0.1 .
docker run --rm -p 8000:8000 de-hello:0.1
```

Hit `/whoami` again. Different hostname, different OS string, same code — that
is the whole point of the lecture in one HTTP response.

---

## 3. Prove the caching claim 🧊

```bash
docker build -t de-hello:0.1 .        # again — everything CACHED, seconds
# now change the GREETING default string in app.py, then:
docker build -t de-hello:0.2 .        # only the last layers rebuild
```

Then break it on purpose: move `COPY . .` above the `RUN pip install` line,
rebuild, and watch it download the internet again. Put it back.

---

## 4. Config from the outside 🎛️

```bash
docker run --rm -p 8000:8000 -e GREETING="Hej från Stockholm" de-hello:0.1
docker run --rm -p 8080:8000 de-hello:0.1     # same image, different host port
```

The image never changes; the environment does. This is how the same artifact
goes from your Codespace to staging to production.

---

## 5. Look inside a running container 🔍

In one terminal run the container, in another:

```bash
docker ps
docker exec -it <ID> sh          # slim images have sh, not bash
ls -al /app                      # is that really what you copied?
env | grep GREETING
exit
docker logs <ID>                 # what uvicorn printed
docker logs -f <ID>              # follow it live
```

`docker logs` is the first thing you check when a container "does nothing".
Usually it is a stack trace that has been waiting patiently for you.

---

## 6. Exercises ✅

**Core** — must be done before Lecture 2.2:

1. `docker run` the `hello-world` image, then list, stop and remove your
   containers and images.
2. Write your own `Dockerfile` for `app.py` from scratch (no peeking).
3. Build it as `de-hello:0.1` and run it on `http://localhost:8000`.
4. Add a `GET /rows` endpoint that counts the lines of a CSV you copy into the
   image, rebuild, and prove it works.

**Then** — behave like an engineer:

5. Show, with two build outputs, that reordering `COPY` changes what is cached.
6. Run two containers from the same image on ports 8000 and 8080 with different
   `GREETING` values at the same time.
7. Add a `.dockerignore` and compare `docker images` sizes before/after — also
   check the build context size line in the build output.
8. Tag and inspect: `docker image inspect de-hello:0.1 | head -40`. Find the
   `Cmd`, `Env` and `WorkingDir` entries.

**Advanced** — optional, pick one:

9. Use `compose.yaml`: `docker compose up --build`, edit `app.py`, and watch
   `--reload` pick it up through the mounted volume. Explain why the volume is
   needed for that.
10. Add a `HEALTHCHECK` instruction that curls `/health`, then find the
    `healthy` status in `docker ps`.
11. Make it a multi-stage build (builder installs into a venv, final stage
    copies it) and compare image sizes.
12. Run as a non-root user (`RUN useradd -m app` + `USER app`) and make sure it
    still starts. Production will ask you for this eventually.

---

## 7. Debugging cheat sheet 🧰

| Symptom | Usual cause |
| --- | --- |
| `curl: connection refused` | bound to `127.0.0.1`, or missing `-p` |
| container exits immediately | `CMD` is wrong or the process is not long-running — read `docker logs` |
| `port is already allocated` | previous container still running: `docker ps` then `docker stop` |
| build is slow every time | `COPY . .` before the install step, or no `.dockerignore` |
| `exec: "bash": not found` | slim image: use `sh` |
| edits do not show up | you rebuilt nothing, or you have no volume mounted |
| out of disk | `docker system df`, then `docker system prune` |

## Resources

* [Docker docs — build best practices](https://docs.docker.com/build/building/best-practices/)
* [Play with Docker](https://labs.play-with-docker.com/) — a throwaway Docker host in the browser
* [FastAPI in containers](https://fastapi.tiangolo.com/deployment/docker/)
* `docker <command> --help` — still faster than a search engine

---

## Next 👉

More Docker, and version control, next week.
