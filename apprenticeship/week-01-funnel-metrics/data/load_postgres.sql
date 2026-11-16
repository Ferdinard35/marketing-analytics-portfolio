-- Week 1 dataset -> PostgreSQL
--
-- Creates the database analytics_apprenticeship (if it does not exist yet) and
-- rebuilds the schema week01 inside it. Later weeks get their own schema in the
-- same database (week03, week05, ...).
--
-- Easiest: run load_postgres.ps1, which finds psql and runs this file for you.
-- By hand, from THIS folder (the \copy paths below are relative to where psql starts):
--     psql -U postgres -h localhost -f load_postgres.sql
--
-- Safe to re-run: it drops and rebuilds only the week01 schema, inside one
-- transaction, so a failed run leaves whatever was there before untouched.

\set ON_ERROR_STOP on
\encoding UTF8

SELECT 'CREATE DATABASE analytics_apprenticeship'
WHERE NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'analytics_apprenticeship')\gexec

\connect analytics_apprenticeship

BEGIN;

DROP SCHEMA IF EXISTS week01 CASCADE;
CREATE SCHEMA week01;
SET LOCAL search_path TO week01;

CREATE TABLE campaigns (
    campaign_id   varchar(8) PRIMARY KEY,
    campaign_name text       NOT NULL UNIQUE,
    channel       text       NOT NULL,
    start_date    date       NOT NULL,
    end_date      date       NOT NULL,
    CHECK (end_date >= start_date)
);

CREATE TABLE campaign_spend (
    spend_date  date           NOT NULL,
    campaign_id varchar(8)     NOT NULL REFERENCES campaigns (campaign_id),
    impressions integer        NOT NULL CHECK (impressions >= 0),
    clicks      integer        NOT NULL CHECK (clicks >= 0),
    spend_ghs   numeric(12, 2) NOT NULL CHECK (spend_ghs >= 0),
    PRIMARY KEY (spend_date, campaign_id)
);

CREATE TABLE users (
    user_id             integer    PRIMARY KEY,
    signup_date         date       NOT NULL,
    campaign_id         varchar(8) REFERENCES campaigns (campaign_id),   -- NULL = organic
    referred_by_user_id integer    REFERENCES users (user_id),           -- NULL unless referred
    region              text       NOT NULL,
    device_os           text       NOT NULL CHECK (device_os IN ('Android', 'iOS')),
    age_band            text       NOT NULL,
    kyc_verified_date   date,                                            -- NULL = not verified
    CHECK (kyc_verified_date IS NULL OR kyc_verified_date >= signup_date)
);

CREATE TABLE transactions (
    transaction_id   bigint         PRIMARY KEY,
    user_id          integer        NOT NULL REFERENCES users (user_id),
    transaction_ts   timestamp      NOT NULL,
    transaction_type text           NOT NULL,
    amount_ghs       numeric(12, 2) NOT NULL CHECK (amount_ghs > 0),
    fee_ghs          numeric(10, 2) NOT NULL CHECK (fee_ghs >= 0),
    status           text           NOT NULL CHECK (status IN ('completed', 'failed', 'reversed'))
);

\copy campaigns      FROM 'campaigns.csv'      WITH (FORMAT csv, HEADER true)
\copy campaign_spend FROM 'campaign_spend.csv' WITH (FORMAT csv, HEADER true)
\copy users          FROM 'users.csv'          WITH (FORMAT csv, HEADER true)
\copy transactions   FROM 'transactions.csv'   WITH (FORMAT csv, HEADER true)

CREATE INDEX transactions_user_id_idx ON transactions (user_id);
CREATE INDEX transactions_ts_idx      ON transactions (transaction_ts);
CREATE INDEX users_signup_date_idx    ON users (signup_date);
CREATE INDEX users_campaign_id_idx    ON users (campaign_id);

COMMIT;

-- New sessions on this database see the current week's tables without a schema prefix.
ALTER DATABASE analytics_apprenticeship SET search_path TO week01, public;

ANALYZE week01.campaigns;
ANALYZE week01.campaign_spend;
ANALYZE week01.users;
ANALYZE week01.transactions;

SELECT 'campaigns' AS table_name, count(*) AS row_count FROM week01.campaigns
UNION ALL SELECT 'campaign_spend', count(*) FROM week01.campaign_spend
UNION ALL SELECT 'users', count(*) FROM week01.users
UNION ALL SELECT 'transactions', count(*) FROM week01.transactions;
