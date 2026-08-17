-- The raw (bronze) layer: whatever the API said, stored verbatim.
--
-- Append-only on purpose. We never update or delete here, so the full
-- ingestion history stays visible and the clean layer can always be rebuilt
-- from it without calling the API again.

CREATE TABLE IF NOT EXISTS raw__weatherapp (
    raw_id              BIGSERIAL PRIMARY KEY,   -- technical key, not from the source
    ingestion_timestamp TIMESTAMPTZ NOT NULL DEFAULT now(),
    location            TEXT        NOT NULL,    -- which place this row describes
    time_epoch          BIGINT      NOT NULL,    -- which forecast hour, from the API
    data                JSONB       NOT NULL     -- the untouched hour object
);

-- (location, time_epoch) is the natural key: one row per place per hour, per
-- ingestion run. Not UNIQUE - re-ingesting the same hour is allowed and
-- expected; the clean layer decides which version wins.
CREATE INDEX IF NOT EXISTS raw__weatherapp_natural_key_idx
    ON raw__weatherapp (location, time_epoch);
