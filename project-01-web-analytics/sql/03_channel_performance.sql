-- Acquisition: which channels bring traffic, and which bring sign-ups?
-- Question: is each channel's share of sign-ups in line with its share of sessions, and what does a paid sign-up cost?
--
-- Shares use a window total (SUM(...) OVER ()) so the query needs no second pass.
-- Cost exists only for the two paid channels; the LEFT JOIN leaves it NULL for the rest.
--
-- Engine: SQLite. Tables: sessions, ad_spend.

WITH by_channel AS (
    SELECT channel_group,
           COUNT(*)          AS sessions,
           SUM(signed_up)    AS signups,
           SUM(began_signup) AS began
    FROM sessions
    GROUP BY channel_group
),
cost AS (
    SELECT channel_group, SUM(cost_ghs) AS cost_ghs
    FROM ad_spend
    GROUP BY channel_group
)
SELECT b.channel_group,
       b.sessions,
       ROUND(100.0 * b.sessions / SUM(b.sessions) OVER (), 2) AS session_share_pct,
       b.signups,
       ROUND(100.0 * b.signups / SUM(b.signups) OVER (), 2)   AS signup_share_pct,
       ROUND(100.0 * b.began / b.sessions, 2)                 AS begin_rate_pct,
       ROUND(100.0 * b.signups / b.sessions, 2)               AS conversion_pct,
       ROUND(c.cost_ghs, 2)                                   AS cost_ghs,
       ROUND(c.cost_ghs / b.signups, 2)                       AS cost_per_signup
FROM by_channel b
LEFT JOIN cost c ON c.channel_group = b.channel_group
ORDER BY b.sessions DESC;
