-- The raw layer: whatever the API said, stored as-is.

CREATE TABLE IF NOT EXISTS raw__weatherapp (
    raw_id              BIGSERIAL PRIMARY KEY,
    ingestion_timestamp TIMESTAMPTZ NOT NULL DEFAULT now(),
    location            TEXT        NOT NULL,
    time_epoch          BIGINT      NOT NULL,
    data                TEXT        NOT NULL
);
