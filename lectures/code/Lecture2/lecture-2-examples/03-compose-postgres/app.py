"""Example 3 — Flask reading rows from a Postgres container.

Note what is *not* here: no host, no password, no port. Configuration arrives
through DATABASE_URL, which compose.yaml sets.
"""

import os

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)


@app.route("/")
def index():
    usernames = [u.username for u in db.session.query(User).order_by(User.id)]
    return f"Users: {', '.join(usernames) or '(none — did the seed SQL run?)'}\n"


@app.route("/health")
def health():
    # Healthy means "I can reach my database", not "my process is alive".
    try:
        db.session.execute(text("select 1"))
        return jsonify(status="ok", database="reachable")
    except Exception as exc:  # noqa: BLE001 — we want the reason in the response
        return jsonify(status="degraded", error=str(exc)), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
