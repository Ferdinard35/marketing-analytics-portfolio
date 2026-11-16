-- Drilldown: is /promo/cashback a bad page, or does it just receive bad traffic?
-- Question: within the same channel, do visitors who land on the cashback page convert worse than
-- visitors who land anywhere else?
--
-- Holding the channel fixed separates the page from the audience. If the page converted badly
-- only because TikTok sends it low-intent visitors, email subscribers landing on it would
-- convert normally. They do not.
--
-- Engine: SQLite. Table: sessions. Channels with fewer than 100 cashback sessions are left out.

SELECT channel_group,
       SUM(CASE WHEN landing_page = '/promo/cashback' THEN 1 ELSE 0 END)                AS cashback_sessions,
       ROUND(100.0 * SUM(CASE WHEN landing_page = '/promo/cashback' THEN signed_up ELSE 0 END)
             / SUM(CASE WHEN landing_page = '/promo/cashback' THEN 1 ELSE 0 END), 2)    AS cashback_conversion_pct,
       SUM(CASE WHEN landing_page <> '/promo/cashback' THEN 1 ELSE 0 END)               AS other_sessions,
       ROUND(100.0 * SUM(CASE WHEN landing_page <> '/promo/cashback' THEN signed_up ELSE 0 END)
             / SUM(CASE WHEN landing_page <> '/promo/cashback' THEN 1 ELSE 0 END), 2)   AS other_conversion_pct
FROM sessions
GROUP BY channel_group
HAVING SUM(CASE WHEN landing_page = '/promo/cashback' THEN 1 ELSE 0 END) >= 100
ORDER BY cashback_sessions DESC;
