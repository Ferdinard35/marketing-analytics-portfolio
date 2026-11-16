#!/usr/bin/env python3
"""
Project 1, step 3: run every query in ../sql/ and check it against the Python analysis.

    python 03_verify_sql_against_python.py

Each number in the README was calculated twice, once in pandas (02_analysis.py) and once in SQL.
This script runs the SQL against ../data/cediflow_web.db, saves each result to ../sql/results/,
and compares it with the matching table in output/. Exit code 0 only if every table agrees.
"""
import sqlite3
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
SQL, DB = HERE.parent / "sql", HERE.parent / "data" / "cediflow_web.db"
RESULTS = SQL / "results"

# query file -> the pandas table it must reproduce
PAIRS = {
    "02_kpi_summary": "kpi_summary",
    "03_channel_performance": "channel_performance",
    "04_campaign_cost_per_signup": "campaign_performance",
    "05_funnel_by_device": "funnel_by_device",
    "06_landing_pages": "landing_pages",
    "07_cashback_page_by_channel": "cashback_page_by_channel",
    "08_remitters_by_country": "remitters_by_country",
    "09_otp_rate_weekly_by_os": "otp_rate_weekly_by_os",
    "10_region_mix_adjusted": "region_mix_adjusted",
    "11_weekly_trend": "weekly_trend",
}
SESSION_COLS = ["session_key", "session_start", "landing_page", "pageviews", "engagement_time_sec", "engaged_session",
                "began_signup", "otp_verified", "signed_up"]


def same(a: pd.DataFrame, b: pd.DataFrame) -> str:
    """Empty string if the two tables agree; otherwise what differs."""
    if list(a.columns) != list(b.columns):
        return f"columns differ: {list(a.columns)} vs {list(b.columns)}"
    if len(a) != len(b):
        return f"row count {len(a)} vs {len(b)}"
    for col in a.columns:
        x, y = a[col].reset_index(drop=True), b[col].reset_index(drop=True)
        if pd.api.types.is_numeric_dtype(x) and pd.api.types.is_numeric_dtype(y):
            if not (x.isna() == y.isna()).all() or ((x - y).abs() > 0.0101).any():      # both sides are rounded to 2 dp
                return f"column {col} differs"
        elif not (x.astype(str) == y.astype(str)).all():
            return f"column {col} differs"
    return ""


def main() -> None:
    RESULTS.mkdir(exist_ok=True)
    con = sqlite3.connect(DB)
    bad = 0
    print(f"SQLite {sqlite3.sqlite_version}")

    built = pd.read_sql_query((SQL / "01_sessions_from_events.sql").read_text(encoding="utf-8"), con)
    stored = pd.read_sql_query(f"SELECT {', '.join(SESSION_COLS)} FROM sessions ORDER BY session_start, session_key", con)
    why = same(built, stored)
    built.head(20).to_csv(RESULTS / "01_sessions_from_events_first20.csv", index=False, lineterminator="\n")
    print(f"{'FAIL' if why else 'PASS'}  01_sessions_from_events   {len(built):,} sessions rebuilt from events {why}")
    bad += bool(why)

    for query, table in PAIRS.items():
        got = pd.read_sql_query((SQL / f"{query}.sql").read_text(encoding="utf-8"), con)
        got.to_csv(RESULTS / f"{query}.csv", index=False, lineterminator="\n")
        why = same(got, pd.read_csv(HERE / "output" / f"{table}.csv"))
        print(f"{'FAIL' if why else 'PASS'}  {query:27s} {why}")
        bad += bool(why)
    con.close()
    print()
    print("SQL AND PYTHON AGREE ON EVERY TABLE" if not bad else f"{bad} TABLE(S) DISAGREE")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
