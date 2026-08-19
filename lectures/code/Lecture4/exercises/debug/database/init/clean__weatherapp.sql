-- The clean layer: typed, deduplicated, ready to query.

CREATE OR REPLACE VIEW clean__weatherapp AS
WITH ranked AS (
    SELECT
        raw__weatherapp.*,
        ROW_NUMBER() OVER (
            PARTITION BY time_epoch
            ORDER BY ingestion_timestamp DESC
        ) AS rn
    FROM raw__weatherapp
)
SELECT
    location,
    (data::json ->> 'time')::timestamp     AS observed_at,
    (data::json ->> 'temp_c')::numeric     AS temp_c,
    (data::json ->> 'wind_kph')::numeric   AS wind_kph,
    (data::json ->> 'precip_mm')::numeric  AS precip_mm,
    (data::json ->> 'humidity')::int       AS humidity,
    (data::json -> 'condition' -> 'text')  AS condition_text,
    ingestion_timestamp
FROM ranked
WHERE rn = 1;
