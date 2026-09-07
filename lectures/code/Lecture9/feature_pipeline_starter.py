"""
Starter for Tuesday's feature-pipeline studio.

Standard project only. Copy this file to your project root as
feature_pipeline.py and work in a pull request.

This is intentionally not complete. The point is to give your group a clear
path from the staging views to feat__daily without starting from a blank file.
"""

from __future__ import annotations

import os

import pandas as pd
import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import execute_values

# These functions already handle the project's time zones, daily aggregation
# and feature calculation. Reuse them rather than copying them.
from model.train import (
    AREA_STATIONS,
    STOCKHOLM,
    build_features,
    daily_price_table,
    daily_weather_table,
)

load_dotenv()

PRICE_AREA = os.environ["PRICE_AREA"]
PARAM_TEMP = "1"
PARAM_WIND = "4"


def load_prices_db(conn, area: str) -> pd.DataFrame:
    """Read staged price intervals in the shape daily_price_table() expects."""
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT starts_at, sek_per_kwh
            FROM stg__elpris
            WHERE price_area = %s
            ORDER BY starts_at
            """,
            (area,),
        )
        rows = cur.fetchall()

    if not rows:
        raise ValueError(f"No price rows in stg__elpris for {area}.")

    df = pd.DataFrame(rows, columns=["starts_at", "SEK_per_kWh"])
    df["ts_utc"] = pd.to_datetime(df["starts_at"], utc=True)
    df["ts_local"] = df["ts_utc"].dt.tz_convert(STOCKHOLM)
    df["date_local"] = df["ts_local"].dt.date
    return df.sort_values("ts_utc").reset_index(drop=True)


def load_weather_db(conn, station: int) -> pd.DataFrame:
    """TODO 1: read and reshape staged weather data."""
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT parameter, observed_at, value
            FROM stg__weather
            WHERE station = %s AND parameter IN (%s, %s)
            ORDER BY observed_at
            """,
            (str(station), PARAM_TEMP, PARAM_WIND),
        )
        rows = cur.fetchall()

    if not rows:
        raise ValueError(f"No weather rows in stg__weather for station {station}.")

    # stg__weather is long: one row for temperature and one for wind.
    # Turn it into a table with temp_c and wind_ms as columns, then add:
    # ts_utc, ts_local and date_local.
    #
    # Hint:
    # long_df = pd.DataFrame(rows, columns=["parameter", "observed_at", "value"])
    # wide = long_df.pivot(index="observed_at", columns="parameter", values="value")
    # wide = wide.rename(columns={PARAM_TEMP: "temp_c", PARAM_WIND: "wind_ms"})
    # wide = wide.reset_index()
    raise NotImplementedError("Complete load_weather_db() first.")


def write_features(conn, area: str, features: pd.DataFrame) -> int:
    """TODO 2: write feature rows to feat__daily with an upsert."""
    # First create and commit db/feat_table.sql.
    #
    # Your natural key should identify one feature row for this team and day:
    # normally (price_area, target_date).
    #
    # Prepare the DataFrame here, then write it with:
    # INSERT ... ON CONFLICT (...) DO UPDATE
    #
    # A second run must update the same rows, not create duplicates.
    raise NotImplementedError("Create the table and complete write_features().")


def refresh_daily_features(conn, area: str) -> int:
    """Build the team's feature table once from the staging views."""
    station, _ = AREA_STATIONS[area]
    prices = load_prices_db(conn, area)
    weather = load_weather_db(conn, station)

    daily_prices = daily_price_table(prices)
    daily_weather = daily_weather_table(weather)
    features = build_features(daily_prices, daily_weather)

    return write_features(conn, area, features)


def main() -> None:
    with psycopg2.connect(os.environ["DATABASE_URL"]) as conn:
        n = refresh_daily_features(conn, PRICE_AREA)
    print(f"wrote {n} rows to feat__daily for {PRICE_AREA}")


if __name__ == "__main__":
    main()
