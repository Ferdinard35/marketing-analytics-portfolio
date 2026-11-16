-- Rebuild the session table from raw events.
--
-- GA4 exports events, not sessions. Everything else in this project is counted per session,
-- so this query is the foundation: one row per session, with where it landed and how far
-- it got through the sign-up funnel. The Python pipeline builds the same table; the two
-- are compared row for row by python/03_verify_sql_against_python.py.
--
-- Two details that are easy to get wrong:
--   * ga_session_id is the second the session started, so different users can share one.
--     The session key is user_pseudo_id + ga_session_id.
--   * The landing page is the page of the FIRST page_view, which needs a window function.
--
-- Engine: SQLite. Table: events (cleaned, one row per event).

WITH first_page AS (
    SELECT session_key,
           page_path,
           ROW_NUMBER() OVER (PARTITION BY session_key ORDER BY event_timestamp) AS rn
    FROM events
    WHERE event_name = 'page_view'
),
per_session AS (
    SELECT session_key,
           MIN(event_ts)                                                    AS session_start,
           SUM(CASE WHEN event_name = 'page_view' THEN 1 ELSE 0 END)        AS pageviews,
           SUM(engagement_time_msec)                                        AS engagement_ms,
           MAX(CASE WHEN event_name = 'begin_sign_up' THEN 1 ELSE 0 END)    AS began_signup,
           MAX(CASE WHEN event_name = 'otp_verified' THEN 1 ELSE 0 END)     AS otp_verified,
           MAX(CASE WHEN event_name = 'sign_up' THEN 1 ELSE 0 END)          AS signed_up
    FROM events
    GROUP BY session_key
)
SELECT p.session_key,
       p.session_start,
       f.page_path AS landing_page,
       p.pageviews,
       -- seconds to one decimal: integer division on whole milliseconds, rounded half up
       (p.engagement_ms + 50) / 100 / 10.0 AS engagement_time_sec,
       -- GA4's engaged session: 10 seconds or more, or 2+ page views, or a key event
       CASE WHEN p.engagement_ms >= 10000 OR p.pageviews >= 2 OR p.signed_up = 1 THEN 1 ELSE 0 END AS engaged_session,
       p.began_signup,
       p.otp_verified,
       p.signed_up
FROM per_session p
JOIN first_page f ON f.session_key = p.session_key AND f.rn = 1
ORDER BY p.session_start, p.session_key;
