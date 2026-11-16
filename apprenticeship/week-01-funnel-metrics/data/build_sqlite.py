#!/usr/bin/env python3
"""
Builds cediflow_week1.db (SQLite) from the four Week 1 CSVs in this folder.

You only need this if the .db file is missing or you want a fresh copy:
    python build_sqlite.py

Uses only the Python standard library.
"""
import csv
import os
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, "cediflow_week1.db")

SCHEMA = """
CREATE TABLE campaigns (
    campaign_id   TEXT PRIMARY KEY,
    campaign_name TEXT NOT NULL UNIQUE,
    channel       TEXT NOT NULL,
    start_date    TEXT NOT NULL,              -- ISO date, YYYY-MM-DD
    end_date      TEXT NOT NULL
);
CREATE TABLE campaign_spend (
    spend_date  TEXT    NOT NULL,             -- ISO date
    campaign_id TEXT    NOT NULL REFERENCES campaigns (campaign_id),
    impressions INTEGER NOT NULL,
    clicks      INTEGER NOT NULL,
    spend_ghs   REAL    NOT NULL,
    PRIMARY KEY (spend_date, campaign_id)
);
CREATE TABLE users (
    user_id             INTEGER PRIMARY KEY,
    signup_date         TEXT NOT NULL,        -- ISO date
    campaign_id         TEXT REFERENCES campaigns (campaign_id),   -- NULL = organic
    referred_by_user_id INTEGER REFERENCES users (user_id),        -- NULL unless referred
    region              TEXT NOT NULL,
    device_os           TEXT NOT NULL,
    age_band            TEXT NOT NULL,
    kyc_verified_date   TEXT                  -- ISO date, NULL = not verified
);
CREATE TABLE transactions (
    transaction_id   INTEGER PRIMARY KEY,
    user_id          INTEGER NOT NULL REFERENCES users (user_id),
    transaction_ts   TEXT    NOT NULL,        -- YYYY-MM-DD HH:MM:SS
    transaction_type TEXT    NOT NULL,
    amount_ghs       REAL    NOT NULL,
    fee_ghs          REAL    NOT NULL,
    status           TEXT    NOT NULL
);
CREATE INDEX idx_transactions_user ON transactions (user_id);
CREATE INDEX idx_transactions_ts   ON transactions (transaction_ts);
CREATE INDEX idx_users_signup      ON users (signup_date);
CREATE INDEX idx_users_campaign    ON users (campaign_id);
"""

TABLES = ["campaigns", "campaign_spend", "users", "transactions"]   # parents before children


def rows(table):
    with open(os.path.join(HERE, table + ".csv"), newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)                                    # skip the header row
        for r in reader:
            yield [None if v == "" else v for v in r]   # empty CSV field = NULL


def main():
    if os.path.exists(DB):
        os.remove(DB)
    con = sqlite3.connect(DB)
    try:
        con.execute("PRAGMA foreign_keys = ON")
        con.executescript(SCHEMA)
        for t in TABLES:
            with open(os.path.join(HERE, t + ".csv"), newline="", encoding="utf-8") as f:
                ncols = len(next(csv.reader(f)))
            con.executemany(f"INSERT INTO {t} VALUES ({','.join('?' * ncols)})", rows(t))
        con.commit()
        problems = con.execute("PRAGMA foreign_key_check").fetchall()
        if problems:
            raise SystemExit(f"foreign key problems: {problems[:5]}")
        for t in TABLES:
            print(f"{t:15s} {con.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]:>7,} rows")
        con.execute("VACUUM")
    finally:
        con.close()
    print(f"built {DB}")


if __name__ == "__main__":
    main()
