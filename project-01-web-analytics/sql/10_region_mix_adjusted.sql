-- Drilldown: does Ashanti really convert better than Greater Accra, or is it channel mix?
-- Question: if Ashanti's traffic had the same channel mix as Greater Accra's, would it still convert better?
--
-- Greater Accra receives far more paid social, the lowest-converting channel, so the raw
-- comparison flatters Ashanti. Direct standardisation fixes that: take each region's conversion
-- rate inside every channel and weight it by Greater Accra's share of sessions in that channel.
--
-- Engine: SQLite. Table: sessions.

WITH by_region_channel AS (
    SELECT region,
           channel_group,
           COUNT(*)             AS sessions,
           1.0 * SUM(signed_up) / COUNT(*) AS conversion
    FROM sessions
    WHERE country = 'Ghana'
      AND region IN ('Greater Accra', 'Ashanti')
    GROUP BY region, channel_group
),
accra_mix AS (
    SELECT channel_group,
           1.0 * sessions / SUM(sessions) OVER () AS weight
    FROM by_region_channel
    WHERE region = 'Greater Accra'
),
standardised AS (
    SELECT r.region,
           SUM(r.conversion * m.weight) AS conversion_at_accra_mix
    FROM by_region_channel r
    JOIN accra_mix m ON m.channel_group = r.channel_group
    GROUP BY r.region
),
raw AS (
    SELECT region,
           COUNT(*)                                                                             AS sessions,
           1.0 * SUM(signed_up) / COUNT(*)                                                      AS conversion,
           1.0 * SUM(CASE WHEN channel_group IN ('Paid Search', 'Paid Social') THEN 1 ELSE 0 END) / COUNT(*) AS paid_share
    FROM sessions
    WHERE country = 'Ghana'
      AND region IN ('Greater Accra', 'Ashanti')
    GROUP BY region
)
SELECT raw.region,
       raw.sessions,
       ROUND(100.0 * raw.conversion, 2)            AS conversion_pct,
       ROUND(100.0 * raw.paid_share, 2)            AS paid_share_pct,
       ROUND(100.0 * s.conversion_at_accra_mix, 2) AS conversion_at_accra_mix_pct
FROM raw
JOIN standardised s ON s.region = raw.region
ORDER BY raw.sessions DESC;
