-- User behaviour: how does each landing page perform?
-- Question: which pages turn a visit into a started sign-up, and which lose the visitor at once?
--
-- Bounce rate here is GA4's: the share of sessions that were NOT engaged
-- (under 10 seconds, one page view, no sign-up).
--
-- Engine: SQLite. Table: sessions.

SELECT landing_page,
       COUNT(*)                                               AS sessions,
       ROUND(100.0 - 100.0 * SUM(engaged_session) / COUNT(*), 2) AS bounce_rate_pct,
       ROUND(100.0 * SUM(began_signup) / COUNT(*), 2)         AS begin_rate_pct,
       SUM(signed_up)                                         AS signups,
       ROUND(100.0 * SUM(signed_up) / COUNT(*), 2)            AS conversion_pct
FROM sessions
GROUP BY landing_page
ORDER BY sessions DESC;
