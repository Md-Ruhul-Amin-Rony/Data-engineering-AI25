-- Runs ONLY when the Postgres data directory is empty (first boot, or after
-- `docker compose down -v`). Change this file and nothing happens until then.

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO users (username) VALUES ('user1'), ('user2'), ('user3');
