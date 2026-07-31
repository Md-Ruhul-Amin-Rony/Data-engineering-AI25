"""Example 2 — a Flask service small enough to read in one breath."""

import os
import platform
import socket

from flask import Flask, jsonify

app = Flask(__name__)

GREETING = os.environ.get("GREETING", "Hello from a container")


@app.route("/")
def hello():
    return f"{GREETING} — served by {socket.gethostname()} 🐳\n"


@app.route("/health")
def health():
    # Boring on purpose. Orchestrators (and your HEALTHCHECK) poll this.
    return jsonify(status="ok")


@app.route("/whoami")
def whoami():
    return jsonify(
        hostname=socket.gethostname(),
        python=platform.python_version(),
        os=platform.platform(),
        greeting=GREETING,
    )


# Uncomment, rebuild, and hit /new-functionality.
# @app.route("/new-functionality")
# def new_functionality():
#     return "This is the new functionality!\n"


if __name__ == "__main__":
    # 0.0.0.0, not 127.0.0.1 — see the README.
    app.run(host="0.0.0.0", port=8000)
