-- Drilldown: did the OTP step break for anyone, and when?
-- Question: is each week's OTP verification rate in line with the four weeks before it, per operating system?
--
-- The window frame "4 PRECEDING to 1 PRECEDING" gives every week its own trailing baseline,
-- which is how an alert on this step would work. A week far below its baseline is a fault,
-- not noise.
--
-- Ghana only: visitors abroad cannot pass OTP at all and are far more often on iOS, so
-- including them would make iOS look permanently worse than it is.
--
-- Engine: SQLite. Table: sessions.

WITH weekly AS (
    SELECT week_start,
           operating_system,
           SUM(began_signup)                                 AS began_signup,
           SUM(otp_verified)                                 AS otp_verified,
           ROUND(100.0 * SUM(otp_verified) / SUM(began_signup), 2) AS otp_rate_pct
    FROM sessions
    WHERE country = 'Ghana'
      AND operating_system IN ('iOS', 'Android')
    GROUP BY week_start, operating_system
),
with_baseline AS (
    SELECT weekly.*,
           ROUND(AVG(otp_rate_pct) OVER (PARTITION BY operating_system
                                         ORDER BY week_start
                                         ROWS BETWEEN 4 PRECEDING AND 1 PRECEDING), 2) AS prev4_avg_rate_pct
    FROM weekly
)
SELECT week_start,
       operating_system,
       began_signup,
       otp_verified,
       otp_rate_pct,
       prev4_avg_rate_pct,
       ROUND(otp_rate_pct - prev4_avg_rate_pct, 2) AS change_vs_prev4_pts
FROM with_baseline
ORDER BY week_start, operating_system;
