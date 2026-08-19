-- The clean (silver) layer: a VIEW, not a table.
--
-- Nothing is ever inserted here. This stores a query; Postgres runs it against
-- raw__weatherapp every time you select from it. So it is always current, and
-- changing it costs one CREATE OR REPLACE with no backfill.
--
-- It does two jobs:
--   1. Pull a handful of fields out of the JSON and give them real types.
--   2. Keep only the most recently ingested version of each (location, hour).

CREATE OR REPLACE VIEW clean__weatherapp AS
WITH ranked AS (
    SELECT
        raw__weatherapp.*,
        ROW_NUMBER() OVER (
            PARTITION BY location, time_epoch      -- one winner per place per hour
            ORDER BY ingestion_timestamp DESC,     -- newest ingestion wins
                     raw_id DESC                   -- tie-breaker, so this is deterministic
        ) AS rn
    FROM raw__weatherapp
)
SELECT
    location,
    (data ->> 'time')::timestamp     AS observed_at,
    (data ->> 'temp_c')::numeric     AS temp_c,
    (data ->> 'wind_kph')::numeric   AS wind_kph,
    (data ->> 'precip_mm')::numeric  AS precip_mm,
    (data ->> 'humidity')::int       AS humidity,
    (data -> 'condition' ->> 'text') AS condition_text,
    ingestion_timestamp
FROM ranked
WHERE rn = 1;

-- Note `->>` rather than `->`. Both read a JSON field; `->` returns it as JSON
-- (so a string comes back as "NW", quotes included), `->>` returns it as text.
-- Use `->` only to step *into* nested objects, as with 'condition' above.
