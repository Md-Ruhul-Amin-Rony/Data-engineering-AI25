# Example 2 — an image you can open in a browser 🌐

Same loop as example 1, plus the two things that make it a *service*:
a dependency (`Flask`) and a published port.

Now it is your keyboard, not the projector.

## Build and run

```bash
cd 02-flask-hello
docker build -t flask-hello:0.1 .
docker run --rm -p 8000:8000 flask-hello:0.1
```

Then open it:

* **Codespaces** — click the "Open in Browser" notification for port 8000, or use
  the *Ports* tab.
* **Local** — <http://localhost:8000>

You should see a greeting. Also try `/whoami` and `/health`.
Stop it with `Ctrl+C`.

## The two lines that matter

```dockerfile
COPY --from=ghcr.io/astral-sh/uv:0.9.7 /uv /usr/local/bin/uv
RUN uv pip install --system --no-cache -r requirements.txt
```

We use **uv** rather than `pip`: same job, much faster, stricter resolver, and it
is the same tool you use for local venvs. `--system` installs into the image's
Python — inside a container there is nothing to isolate from.

```dockerfile
CMD ["python", "app.py"]     # app.py binds 0.0.0.0
```

`0.0.0.0`, never `127.0.0.1`. A server bound to localhost *inside* a container is
reachable only from inside that container. Very private, entirely useless.

And `-p 8000:8000` is `host:container`. `EXPOSE` alone publishes nothing — it is
documentation.

## Prove layer caching 🧊

```bash
docker build -t flask-hello:0.1 .     # again: all CACHED, seconds
# edit the greeting string in app.py, then:
docker build -t flask-hello:0.2 .     # only the last layers rebuild
```

Now move `COPY . .` *above* the `uv pip install` line, rebuild, and watch it
reinstall Flask for a one-word text change. Put it back. That is why
`requirements.txt` is copied first.

## Then, without looking

1. Delete the `Dockerfile`.
2. Write a new one from scratch: `FROM`, `WORKDIR`, copy requirements, install,
   copy source, `EXPOSE`, `CMD`.
3. Build and run it. Confirm the page still loads.

## Small extensions

* Uncomment the second route in `app.py`, rebuild, and hit `/new-functionality`.
* Run two containers from the *same* image at once:
  ```bash
  docker run --rm -d -p 8000:8000 -e GREETING="Hej Stockholm" flask-hello:0.1
  docker run --rm -d -p 8080:8000 -e GREETING="Hallå Göteborg" flask-hello:0.1
  docker ps
  ```
  One artifact, two configurations. That is how the same image goes from your
  Codespace to staging to production.
* `docker exec -it <ID> sh`, then `ls -al /app` and `env | grep GREETING`.
  Slim images have `sh`, not `bash`.

## When it does not work

| Symptom | Usual cause |
| --- | --- |
| connection refused | bound to `127.0.0.1`, or you forgot `-p` |
| port is already allocated | an older container is still up — `docker ps`, then `docker stop` |
| container exits instantly | read `docker logs <ID>`; it is a stack trace, patiently waiting |
| edits do not appear | you did not rebuild (no volume is mounted here) |

Next: [example 3 — two services with Compose](../03-compose-postgres/README.md).
