# Example 1 — your first image 🥚

The smallest interesting Dockerfile there is: a base image, one file, one command.
No dependencies, no ports, no web server. If this works, Docker works.

Your teacher runs this on screen first. Follow along after.

## Build and run

```bash
cd 01-hello-image
docker build -t hello-de:0.1 .
docker run --rm hello-de:0.1
```

Expected: a few lines of output, then the container exits. That is correct — a
container lives exactly as long as its main process.

## Look at what you just made

```bash
docker images | head          # your image, and its size
docker ps                     # nothing: it already exited
docker ps -a | head           # there it is, "Exited (0)"
docker run hello-de:0.1       # without --rm...
docker ps -a | head           # ...you now collect corpses
docker rm <ID>                # clean up
```

## Then, without looking

1. Delete the `Dockerfile`.
2. Write it again from memory. You need three instructions: `FROM`, `COPY`, `CMD`
   (`WORKDIR` is a good habit too).
3. Rebuild as `hello-de:0.2` and run it.

That rewrite *is* the exercise. Reading a Dockerfile teaches you nothing;
producing one teaches you everything.

## Try to break it

* Change `CMD` to `["python", "nope.py"]` → rebuild, run, read the error.
* Remove the `COPY` line → rebuild, run. Why does it fail with the same error?
* Run `docker run --rm hello-de:0.1 python -c "print(2**16)"` — the `CMD` is a
  default, not a law.
