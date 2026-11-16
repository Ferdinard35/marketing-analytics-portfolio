-- Funnel: where do visitors drop out, and does it depend on the device?
-- Question: which step of the sign-up funnel loses the most people, and for whom?
--
-- Each rate is a step rate with its own denominator: the people who reached the step before.
-- NULLIF guards the division for a device with nobody at a step.
--
-- Engine: SQLite. Table: sessions.

SELECT device_category,
       COUNT(*)                                                         AS sessions,
       SUM(began_signup)                                                AS began_signup,
       SUM(otp_verified)                                                AS otp_verified,
       SUM(signed_up)                                                   AS signed_up,
       ROUND(100.0 * SUM(began_signup) / COUNT(*), 2)                   AS begin_rate_pct,
       ROUND(100.0 * SUM(otp_verified) / NULLIF(SUM(began_signup), 0), 2) AS otp_rate_pct,
       ROUND(100.0 * SUM(signed_up) / NULLIF(SUM(otp_verified), 0), 2)  AS completion_rate_pct,
       ROUND(100.0 * SUM(signed_up) / COUNT(*), 2)                      AS conversion_pct
FROM sessions
GROUP BY device_category
ORDER BY sessions DESC;
