-- Drilldown: where do META_Lookalike_Remitters clicks come from?
-- Question: why does this campaign cost more per sign-up than the other Meta prospecting campaign?
--
-- Sign-up needs a Ghanaian phone number for the OTP step, so a visitor abroad can start the
-- form but almost never finish it.
--
-- Engine: SQLite. Table: sessions.

SELECT country,
       COUNT(*)                                           AS sessions,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS session_share_pct,
       SUM(began_signup)                                  AS began_signup,
       SUM(otp_verified)                                  AS otp_verified,
       SUM(signed_up)                                     AS signups,
       ROUND(100.0 * SUM(signed_up) / COUNT(*), 2)        AS conversion_pct
FROM sessions
WHERE campaign = 'META_Lookalike_Remitters'
GROUP BY country
ORDER BY sessions DESC;
