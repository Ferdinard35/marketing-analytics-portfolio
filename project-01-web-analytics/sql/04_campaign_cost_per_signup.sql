-- Acquisition: what does a sign-up cost, campaign by campaign?
-- Question: which paid campaigns earn their budget, on a last-click basis?
--
-- ad_spend has one row per campaign per day and sessions has one row per session, so each is
-- summed to campaign grain before the join. Paid sessions that arrived without a campaign tag
-- are labelled '(unattributed)' and match no campaign here, so cost per sign-up is slightly
-- overstated for every campaign.
--
-- Engine: SQLite. Tables: sessions, ad_spend.

WITH cost AS (
    SELECT campaign,
           platform,
           SUM(clicks)   AS clicks,
           SUM(cost_ghs) AS cost_ghs
    FROM ad_spend
    GROUP BY campaign, platform
),
traffic AS (
    SELECT campaign,
           COUNT(*)       AS sessions,
           SUM(signed_up) AS signups
    FROM sessions
    GROUP BY campaign
)
SELECT c.campaign,
       c.platform,
       c.clicks,
       ROUND(c.cost_ghs, 2)                     AS cost_ghs,
       ROUND(c.cost_ghs / c.clicks, 2)          AS cpc_ghs,
       t.sessions,
       t.signups,
       ROUND(100.0 * t.signups / t.sessions, 2) AS conversion_pct,
       ROUND(c.cost_ghs / t.signups, 2)         AS cost_per_signup
FROM cost c
JOIN traffic t ON t.campaign = c.campaign
ORDER BY c.cost_ghs / t.signups DESC;
