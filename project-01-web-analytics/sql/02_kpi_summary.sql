-- Executive summary: the quarter in one row.
-- Question: how much traffic did the site get, how much of it signed up, and what did the paid part cost?
--
-- Sessions and spend are summarised separately and then put side by side. Joining the
-- session table to the daily spend table directly would repeat every session once per spend row.
--
-- Engine: SQLite. Tables: sessions, ad_spend.

WITH s AS (
    SELECT COUNT(*)                                                                             AS sessions,
           COUNT(DISTINCT user_pseudo_id)                                                       AS users,
           SUM(signed_up)                                                                       AS signups,
           SUM(engaged_session)                                                                 AS engaged,
           SUM(is_new_user)                                                                     AS new_user_sessions,
           SUM(began_signup)                                                                    AS began,
           SUM(otp_verified)                                                                    AS verified,
           SUM(CASE WHEN channel_group IN ('Paid Search', 'Paid Social') THEN signed_up ELSE 0 END) AS paid_signups
    FROM sessions
),
c AS (
    SELECT SUM(cost_ghs) AS cost_ghs FROM ad_spend
)
SELECT s.sessions,
       s.users,
       s.signups,
       ROUND(100.0 * s.signups / s.sessions, 2)           AS conversion_pct,
       ROUND(100.0 * s.engaged / s.sessions, 2)           AS engaged_rate_pct,
       ROUND(100.0 * s.new_user_sessions / s.sessions, 2) AS new_user_session_pct,
       ROUND(100.0 * s.began / s.sessions, 2)             AS begin_rate_pct,
       ROUND(100.0 * s.verified / s.began, 2)             AS otp_rate_pct,
       ROUND(100.0 * s.signups / s.verified, 2)           AS completion_rate_pct,
       ROUND(c.cost_ghs, 2)                               AS cost_ghs,
       s.paid_signups,
       ROUND(c.cost_ghs / s.paid_signups, 2)              AS cost_per_paid_signup
FROM s
CROSS JOIN c;
