-- Executive summary: the weekly trend.
-- Question: are sessions, sign-ups and spend moving together week by week?
--
-- Sessions and spend are each summed to week grain before the join.
--
-- Engine: SQLite. Tables: sessions, ad_spend.

WITH traffic AS (
    SELECT week_start,
           COUNT(*)       AS sessions,
           SUM(signed_up) AS signups
    FROM sessions
    GROUP BY week_start
),
cost AS (
    SELECT week_start, SUM(cost_ghs) AS cost_ghs
    FROM ad_spend
    GROUP BY week_start
)
SELECT t.week_start,
       t.sessions,
       t.signups,
       ROUND(100.0 * t.signups / t.sessions, 2) AS conversion_pct,
       ROUND(c.cost_ghs, 2)                     AS cost_ghs
FROM traffic t
LEFT JOIN cost c ON c.week_start = t.week_start
ORDER BY t.week_start;
