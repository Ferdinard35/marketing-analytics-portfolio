#!/usr/bin/env python3
"""
Project 1, step 1: clean the raw GA4-style export and build the session table.

    python 01_clean_and_model.py

Reads   ../data/raw/ga4_events_raw.csv      one row per event, as exported
        ../data/raw/ad_spend_raw.csv        one row per campaign per day, from the ad platforms
Writes  ../data/cleaned/sessions.csv        one row per session (the table the analysis and Tableau use)
        ../data/cleaned/ad_spend.csv        de-duplicated cost data with the channel attached
        ../data/cleaned/cleaning_log.json   what was found and what was done about it
        ../data/cediflow_web.db             SQLite database: events, sessions, ad_spend

Every rule below is written down in ../data/data_dictionary.md. Nothing is dropped silently:
each step records how many rows or sessions it touched.
"""
import json
import sqlite3
from pathlib import Path

import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"
RAW, CLEAN = DATA / "raw", DATA / "cleaned"

# Labels that mean the same thing. Left side: as found (after lower-casing). Right side: the standard.
SOURCE_MAP = {"fb": "facebook", "facebook.com": "facebook", "ig": "instagram", "tiktok.com": "tiktok"}
MEDIUM_MAP = {"paidsocial": "paid_social", "paid-social": "paid_social", "ppc": "cpc", "e-mail": "email"}
EMAIL_CAMPAIGNS = ["EM_Weekly_Digest", "EM_Cashback_Announcement"]

SEARCH_SOURCES = {"google", "bing"}
SOCIAL_SOURCES = {"facebook", "instagram", "tiktok", "twitter"}
PLATFORM_CHANNEL = {"Google Ads": "Paid Search", "Meta Ads": "Paid Social", "TikTok Ads": "Paid Social"}

# Bot rules (see the data dictionary for how each was found)
SCANNER = {"country": "United States", "city": "Ashburn", "operating_system": "Linux"}
MAX_SESSIONS_PER_USER_PER_DAY = 20

log = {}


def channel_group(source: str, medium: str) -> str:
    """GA4's default channel grouping, reduced to the rules this property needs."""
    paid = medium in ("cpc", "ppc") or medium.startswith("paid")
    if source == "(direct)" and medium in ("(none)", "(not set)"):
        return "Direct"
    if source in SEARCH_SOURCES and paid:
        return "Paid Search"
    if source in SOCIAL_SOURCES and paid:
        return "Paid Social"
    if medium == "email" or source == "email":
        return "Email"
    if medium == "organic":
        return "Organic Search"
    if source in SOCIAL_SOURCES or medium == "social":
        return "Organic Social"
    if medium == "referral":
        return "Referral"
    return "Unassigned"


def clean_spend() -> pd.DataFrame:
    spend = pd.read_csv(RAW / "ad_spend_raw.csv")
    n_raw, cost_raw = len(spend), spend["cost_ghs"].sum()
    spend = spend.drop_duplicates()
    assert not spend.duplicated(["date", "campaign_name"]).any(), "a campaign has two different rows for one day"
    spend = spend.rename(columns={"campaign_name": "campaign"})
    spend["channel_group"] = spend["platform"].map(PLATFORM_CHANNEL)
    spend["week_start"] = week_start(pd.to_datetime(spend["date"]))
    log["ad_spend"] = {
        "rows_raw": n_raw, "duplicate_rows_removed": n_raw - len(spend), "rows_clean": len(spend),
        "cost_raw_ghs": round(float(cost_raw), 2), "cost_clean_ghs": round(float(spend["cost_ghs"].sum()), 2),
    }
    return spend[["date", "week_start", "platform", "channel_group", "campaign", "impressions", "clicks", "cost_ghs"]]


def week_start(dates: pd.Series) -> pd.Series:
    """The Monday of each date's week, as an ISO date string."""
    return (dates - pd.to_timedelta(dates.dt.weekday, unit="D")).dt.strftime("%Y-%m-%d")


def main() -> None:
    CLEAN.mkdir(exist_ok=True)
    spend = clean_spend()
    paid_campaigns = sorted(spend["campaign"].unique())
    campaign_map = {c.lower(): c for c in paid_campaigns + EMAIL_CAMPAIGNS}

    # ------------------------------------------------------------------ load
    ev = pd.read_csv(RAW / "ga4_events_raw.csv", dtype=str, keep_default_na=False)
    log["events_raw_rows"] = len(ev)

    # ------------------------------------------------------------------ 1. exact duplicate events
    before = len(ev)
    signups_before = int((ev["event_name"] == "sign_up").sum())
    ev = ev.drop_duplicates()
    log["duplicate_events_removed"] = before - len(ev)
    log["duplicate_sign_up_events_removed"] = signups_before - int((ev["event_name"] == "sign_up").sum())

    # ------------------------------------------------------------------ 2. events with no session id
    no_session = ev["ga_session_id"] == ""
    log["events_without_session_id_removed"] = int(no_session.sum())
    ev = ev[~no_session].copy()

    # ------------------------------------------------------------------ 3. session key
    # ga_session_id is the second the session started, so two users can share one. The key needs both.
    ev["session_key"] = ev["user_pseudo_id"] + "-" + ev["ga_session_id"]
    log["distinct_ga_session_id"] = int(ev["ga_session_id"].nunique())
    log["distinct_session_key"] = int(ev["session_key"].nunique())

    # ------------------------------------------------------------------ 4. standardise traffic labels
    labels_before = {c: int(ev[c].nunique()) for c in ("source", "medium", "campaign")}
    src = ev["source"].str.strip().str.lower()
    med = ev["medium"].str.strip().str.lower()
    camp = ev["campaign"].str.strip()
    new_src, new_med = src.replace(SOURCE_MAP), med.replace(MEDIUM_MAP)
    new_camp = camp.str.lower().map(campaign_map).fillna(camp)
    unknown = sorted(set(new_camp.unique()) - set(campaign_map.values()) - {""})
    assert not unknown, f"campaign labels with no standard form: {unknown}"
    log["label_rows_changed"] = {"source": int((new_src != ev["source"]).sum()), "medium": int((new_med != ev["medium"]).sum()),
                                 "campaign": int((new_camp != ev["campaign"]).sum())}
    ev["source"], ev["medium"], ev["campaign"] = new_src, new_med, new_camp
    log["distinct_labels"] = {c: {"before": labels_before[c], "after": int(ev[c].nunique())} for c in labels_before}

    # ------------------------------------------------------------------ 5. types
    ev["event_timestamp"] = ev["event_timestamp"].astype("int64")
    ev["ga_session_number"] = ev["ga_session_number"].astype(int)
    ev["engagement_time_msec"] = pd.to_numeric(ev["engagement_time_msec"]).fillna(0).astype(int)
    ev["event_ts"] = pd.to_datetime(ev["event_timestamp"], unit="us")           # Ghana is on GMT, so UTC is local time
    ev = ev.sort_values(["session_key", "event_timestamp"], kind="stable").reset_index(drop=True)

    # ------------------------------------------------------------------ 6. sessionise
    for name in ("page_view", "begin_sign_up", "otp_verified", "sign_up"):
        ev["is_" + name] = (ev["event_name"] == name).astype(int)
    ev["is_internal"] = (ev["traffic_type"] == "internal").astype(int)
    g = ev.groupby("session_key", sort=False)
    first = g.first()
    counts = g[["is_page_view", "is_begin_sign_up", "is_otp_verified", "is_sign_up", "is_internal"]].sum()
    sessions = pd.DataFrame({
        "user_pseudo_id": first["user_pseudo_id"],
        "session_number": first["ga_session_number"],
        "session_start": g["event_ts"].min(),
        "source": first["source"], "medium": first["medium"], "campaign": first["campaign"],
        "device_category": first["device_category"], "operating_system": first["operating_system"],
        "browser": first["browser"], "country": first["country"], "region": first["region"], "city": first["city"],
        "pageviews": counts["is_page_view"],
        "engagement_ms": g["engagement_time_msec"].sum(),
        "began_signup": (counts["is_begin_sign_up"] > 0).astype(int),      # reached the step at least once
        "otp_verified": (counts["is_otp_verified"] > 0).astype(int),
        "signed_up": (counts["is_sign_up"] > 0).astype(int),
        "internal": counts["is_internal"] > 0,
    })
    landing = ev[ev["event_name"] == "page_view"].groupby("session_key", sort=False)["page_path"].first()
    sessions["landing_page"] = landing.reindex(sessions.index)
    assert sessions["landing_page"].notna().all(), "a session has no page_view"
    sessions["session_date"] = sessions["session_start"].dt.strftime("%Y-%m-%d")
    sessions["week_start"] = week_start(sessions["session_start"].dt.normalize())
    sessions["hour"] = sessions["session_start"].dt.hour
    sessions["is_new_user"] = (sessions["session_number"] == 1).astype(int)
    # GA4's definition of an engaged session: 10 seconds or more, or 2+ page views, or a key event
    sessions["engaged_session"] = ((sessions["engagement_ms"] >= 10_000) | (sessions["pageviews"] >= 2)
                                   | (sessions["signed_up"] == 1)).astype(int)
    # seconds to one decimal, rounded half up on whole milliseconds so SQL and Python cannot disagree
    sessions["engagement_time_sec"] = ((sessions["engagement_ms"] + 50) // 100) / 10
    sessions = sessions.drop(columns="engagement_ms")
    sessions["channel_group"] = [channel_group(s, m) for s, m in zip(sessions["source"], sessions["medium"])]
    assert (sessions["channel_group"] != "Unassigned").all(), "a source/medium pair matched no channel rule"

    # a paid click that arrived without a campaign tag stays in its channel, labelled as unattributed
    paid = sessions["channel_group"].isin(["Paid Search", "Paid Social"])
    log["paid_sessions_missing_campaign"] = int((paid & (sessions["campaign"] == "")).sum())
    sessions.loc[paid & (sessions["campaign"] == ""), "campaign"] = "(unattributed)"
    sessions.loc[sessions["campaign"] == "", "campaign"] = "(none)"
    log["sessions_before_filters"] = len(sessions)
    log["signups_before_filters"] = int(sessions["signed_up"].sum())

    # ------------------------------------------------------------------ 7. traffic that is not customers
    per_day = sessions.groupby(["user_pseudo_id", "session_date"]).size()
    hyperactive = set(per_day[per_day > MAX_SESSIONS_PER_USER_PER_DAY].index.get_level_values(0))
    monitor = sessions["user_pseudo_id"].isin(hyperactive)
    scanner = ((sessions["country"] == SCANNER["country"]) & (sessions["city"] == SCANNER["city"])
               & (sessions["operating_system"] == SCANNER["operating_system"])
               & (sessions["engagement_time_sec"] == 0) & (sessions["pageviews"] <= 1))
    internal = sessions["internal"]
    assert not (monitor & scanner).any() and not (internal & (monitor | scanner)).any()
    direct_before = sessions[sessions["channel_group"] == "Direct"]
    log["removed"] = {
        name: {"sessions": int(mask.sum()), "sign_ups": int(sessions.loc[mask, "signed_up"].sum())}
        for name, mask in (("internal_qa", internal), ("scanner_bot", scanner), ("uptime_monitor", monitor))
    }
    log["scanner_probe_path_share_pct"] = round(100 * float(sessions.loc[scanner, "landing_page"].isin(
        ["/wp-login.php", "/.env", "/admin", "/xmlrpc.php"]).mean()), 1)
    log["uptime_monitor_client_ids"] = len(hyperactive)
    keep = ~(monitor | scanner | internal)
    log["conversion_before_filters_pct"] = round(100 * float(sessions["signed_up"].mean()), 2)
    sessions = sessions[keep].drop(columns="internal")
    ev = ev[ev["session_key"].isin(sessions.index)].copy()
    direct_after = sessions[sessions["channel_group"] == "Direct"]
    log["direct_channel"] = {
        "sessions_before": len(direct_before), "sessions_after": len(direct_after),
        "conversion_before_pct": round(100 * float(direct_before["signed_up"].mean()), 2),
        "conversion_after_pct": round(100 * float(direct_after["signed_up"].mean()), 2),
    }

    # ------------------------------------------------------------------ 8. checks on the result
    broken = int(((sessions["otp_verified"] > sessions["began_signup"]) | (sessions["signed_up"] > sessions["otp_verified"])).sum())
    assert broken == 0, f"{broken} sessions reach a later funnel step without the earlier one"
    assert sessions["session_date"].between("2026-03-30", "2026-06-28").all()
    not_set = sessions["region"] == "(not set)"
    log["sessions_region_not_set"] = int(not_set.sum())
    log["sessions_clean"] = len(sessions)
    log["users_clean"] = int(sessions["user_pseudo_id"].nunique())
    log["signups_clean"] = int(sessions["signed_up"].sum())
    log["conversion_clean_pct"] = round(100 * float(sessions["signed_up"].mean()), 2)
    log["events_clean_rows"] = len(ev)

    # ------------------------------------------------------------------ write
    cols = ["session_key", "user_pseudo_id", "session_number", "is_new_user", "session_start", "session_date", "week_start",
            "hour", "channel_group", "source", "medium", "campaign", "landing_page", "device_category", "operating_system",
            "browser", "country", "region", "city", "pageviews", "engagement_time_sec", "engaged_session",
            "began_signup", "otp_verified", "signed_up"]
    sessions = sessions.reset_index().sort_values(["session_start", "session_key"])[cols]
    sessions["session_start"] = sessions["session_start"].dt.strftime("%Y-%m-%d %H:%M:%S")
    sessions.to_csv(CLEAN / "sessions.csv", index=False, lineterminator="\n")
    spend.to_csv(CLEAN / "ad_spend.csv", index=False, lineterminator="\n")

    ev_out = ev[["session_key", "event_timestamp", "event_ts", "event_name", "user_pseudo_id", "ga_session_id",
                 "ga_session_number", "page_path", "source", "medium", "campaign", "device_category", "operating_system",
                 "browser", "country", "region", "city", "engagement_time_msec"]].copy()
    ev_out["event_ts"] = ev_out["event_ts"].dt.strftime("%Y-%m-%d %H:%M:%S")
    ev_out["event_date"] = ev_out["event_ts"].str[:10]
    db = DATA / "cediflow_web.db"
    db.unlink(missing_ok=True)
    with sqlite3.connect(db) as con:
        ev_out.to_sql("events", con, index=False)
        sessions.to_sql("sessions", con, index=False)
        spend.to_sql("ad_spend", con, index=False)
        con.executescript("""
            CREATE INDEX idx_events_session ON events (session_key, event_timestamp);
            CREATE UNIQUE INDEX idx_sessions_key ON sessions (session_key);
            CREATE INDEX idx_sessions_date ON sessions (session_date);
            CREATE UNIQUE INDEX idx_spend ON ad_spend (date, campaign);
        """)
    con.close()

    (CLEAN / "cleaning_log.json").write_text(json.dumps(log, indent=2) + "\n", encoding="ascii")
    print(json.dumps(log, indent=2))


if __name__ == "__main__":
    main()
