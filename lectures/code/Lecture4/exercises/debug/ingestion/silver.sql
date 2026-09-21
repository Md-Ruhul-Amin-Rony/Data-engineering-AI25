-- ---------------------------------------------------------------------------
-- VIEW: silver__features
-- WHY: A view acts like a dynamic table. Instead of copying data, Postgres 
-- recalculates this query automatically every time  train.py asks for data.
-- ---------------------------------------------------------------------------
CREATE OR REPLACE VIEW silver__features AS

-- STEP 1: Handle re-ingested electricity data
-- WHAT: Grabs only the most recently ingested JSON payload for each date.
-- WHY: Our bronze layer is "append-only". If the pipeline runs twice for the 
-- same day, we don't want duplicate data in our model. DISTINCT ON keeps only 
-- the newest row based on ingestion_timestamp.
WITH deduplicated_elpris AS (
    SELECT DISTINCT ON (price_area, price_date)
        price_area,
        data
    FROM raw__elpris
    ORDER BY price_area, price_date, ingestion_timestamp DESC
),

-- STEP 2: Unnest JSON and aggregate 15-minute intervals into 1-hour intervals
-- WHAT: Explodes the JSON array into individual rows, extracts the time and 
-- price, and calculates the hourly average.
-- WHY: The European electricity market recently moved to 15-minute intervals 
-- (96 rows/day), but SMHI weather is hourly (24 rows/day). By grouping and 
-- averaging (AVG), we force the prices back into 24 neat hourly rows so they 
-- can join perfectly with the weather.
hourly_prices AS (
    SELECT 
        price_area,
        date_trunc('hour', (elem->>'time_start')::TIMESTAMPTZ) AS valid_at,
        AVG((elem->>'SEK_per_kWh')::NUMERIC) AS price_sek
    FROM deduplicated_elpris,
    LATERAL jsonb_array_elements(data) AS elem
    GROUP BY price_area, date_trunc('hour', (elem->>'time_start')::TIMESTAMPTZ)
),

-- STEP 3: Handle re-ingested weather data
-- WHAT: Deduplicates weather readings, similar to Step 1.
-- WHY: If SMHI corrects a past weather reading and we re-download it, 
-- we want our model to use the newest, most accurate version. We truncate 
-- the observed_at timestamp to the hour to remove any random minute/second 
-- offsets from SMHI.
deduplicated_weather AS (
    SELECT DISTINCT ON (station, parameter, date_trunc('hour', observed_at))
        station,
        parameter,
        date_trunc('hour', observed_at) AS valid_at,
        (data->>'value')::NUMERIC AS weather_value
    FROM raw__weather
    ORDER BY station, parameter, date_trunc('hour', observed_at), ingestion_timestamp DESC
),

-- STEP 4: Pivot the weather parameters from rows into columns
-- WHAT: Moves parameter 1 and parameter 4 into their own side-by-side columns.
-- WHY: Machine learning models require features to be columns (X1, X2), not 
-- stacked rows. The FILTER clause acts like a pivot table.
hourly_weather AS (
    SELECT 
        valid_at,
        MAX(weather_value) FILTER (WHERE parameter = '1') AS temperature,
        MAX(weather_value) FILTER (WHERE parameter = '4') AS wind_speed
    FROM deduplicated_weather
    GROUP BY valid_at
)

-- STEP 5: The Final Join
-- WHAT: Merges the cleaned hourly prices with the cleaned hourly weather.
-- WHY: A LEFT JOIN is used starting from the prices (our target variable). 
-- This ensures that if SMHI's weather API goes down for a few hours, we don't 
-- completely lose our electricity price data for that day in the final table.
SELECT 
    p.valid_at,
    p.price_area,
    p.price_sek,
    w.temperature,
    w.wind_speed
FROM hourly_prices p
LEFT JOIN hourly_weather w ON p.valid_at = w.valid_at
ORDER BY p.valid_at DESC;