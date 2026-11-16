-- ============================================================================
-- Week 1: Marketing Funnel & Metrics
-- Dataset: CediFlow, Q1 2026 (see ../data/data_dictionary.md)
-- Engine used: SQLite (run on 3.39; written to run on the VS Code extension's 3.26 too)
--
-- WORKED SOLUTIONS, written by Claude on 2026-11-15 at Ferdinard's request.
-- Not a graded attempt. Every result below was pasted from a real run against
-- ../data/cediflow_week1.db. PostgreSQL versions of the same queries are in
-- ../../_instructor/week-01/reference_solutions_postgres.sql
--
-- For every question: the query, its result pasted below it as a comment,
-- and a "So what" line saying what the result means for the business.
-- The full question text is in ../4-sql-exercises.md
-- ============================================================================


-- ----------------------------------------------------------------------------
-- Q1. New users acquired per calendar month
-- Columns: signup_month, new_users
-- ----------------------------------------------------------------------------

SELECT strftime('%Y-%m', signup_date) AS signup_month,
       COUNT(*)                       AS new_users
FROM users
GROUP BY 1
ORDER BY 1;

-- Result:
-- signup_month | new_users
-- 2026-01      | 3703
-- 2026-02      | 3884
-- 2026-03      | 7464
--
-- Check: 3703 + 3884 + 7464 = 15051 = SELECT COUNT(*) FROM users.

-- So what:
-- Sign-ups were flat from January to February (+5%) and then almost doubled in
-- March (+92%). Half of all the users CediFlow has ever acquired arrived in the
-- last month, so anything measured "per user" this quarter is dominated by people
-- who have had only a few weeks to do anything. Before celebrating March, find out
-- what drove it (Q2 and Q4) and whether those users transact (S1).


-- ----------------------------------------------------------------------------
-- Q2. CAC per month
-- Columns: month, total_spend_ghs, new_users, paid_new_users, blended_cac, paid_cac
-- ----------------------------------------------------------------------------

-- Each table is aggregated to month grain first and joined afterwards. Joining
-- users to campaign_spend row by row would repeat every user once per spend row.
WITH monthly_spend AS (
    SELECT strftime('%Y-%m', spend_date) AS month,
           SUM(spend_ghs)                AS total_spend_ghs
    FROM campaign_spend
    GROUP BY 1
),
monthly_signups AS (
    SELECT strftime('%Y-%m', signup_date) AS month,
           COUNT(*)                       AS new_users,
           COUNT(campaign_id)             AS paid_new_users   -- NULL campaign_id = organic
    FROM users
    GROUP BY 1
)
SELECT s.month,
       ROUND(sp.total_spend_ghs, 2)                               AS total_spend_ghs,
       s.new_users,
       s.paid_new_users,
       ROUND(sp.total_spend_ghs / s.new_users, 2)                 AS blended_cac,
       ROUND(sp.total_spend_ghs / NULLIF(s.paid_new_users, 0), 2) AS paid_cac
FROM monthly_signups s
JOIN monthly_spend sp ON sp.month = s.month
ORDER BY s.month;

-- Result:
-- month   | total_spend_ghs | new_users | paid_new_users | blended_cac | paid_cac
-- 2026-01 | 82519.32        | 3703      | 2732           | 22.28       | 30.20
-- 2026-02 | 60278.01        | 3884      | 2876           | 15.52       | 20.96
-- 2026-03 | 113723.12       | 7464      | 6146           | 15.24       | 18.50
--
-- Check: 82519.32 + 60278.01 + 113723.12 = 256520.45 = SUM(spend_ghs); new_users matches Q1.

-- So what (which CAC would you report, and to whom?):
-- Paid CAC fell from GHS 30.20 to GHS 18.50 and blended from GHS 22.28 to GHS 15.24,
-- while spend in March was the highest of the quarter. Paid CAC is the one for the
-- marketing team and for budget decisions, because it is what buying one more user
-- costs. Blended CAC is the one for the board's view of overall efficiency, but it
-- improves whenever organic sign-ups grow, so an investor should see both, labelled.
-- A cheaper sign-up is only good news if the March users are worth as much as the
-- January ones, and this query cannot say that.


-- ----------------------------------------------------------------------------
-- Q3. Monthly churn rate (self-join or window function)
-- Columns: month, active_prev_month, churned_users, churn_rate_pct
-- ----------------------------------------------------------------------------

-- Version A: self-join. One row per user per month in which they completed a
-- transaction, joined to the same user's row for the following month.
WITH active AS (
    SELECT DISTINCT user_id,
           strftime('%Y-%m', transaction_ts) AS activity_month
    FROM transactions
    WHERE status = 'completed'
)
SELECT strftime('%Y-%m', date(prev.activity_month || '-01', '+1 month'))                 AS month,
       COUNT(*)                                                                          AS active_prev_month,
       SUM(CASE WHEN cur.user_id IS NULL THEN 1 ELSE 0 END)                              AS churned_users,
       ROUND(100.0 * SUM(CASE WHEN cur.user_id IS NULL THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM active prev
LEFT JOIN active cur
       ON cur.user_id = prev.user_id
      AND cur.activity_month = strftime('%Y-%m', date(prev.activity_month || '-01', '+1 month'))
WHERE prev.activity_month < (SELECT MAX(activity_month) FROM active)   -- the last month has no "next month" yet
GROUP BY 1
ORDER BY 1;

-- Version B: window function. LEAD finds each user's next active month; they
-- churned if there is none, or if it is not the month straight after.
WITH active AS (
    SELECT DISTINCT user_id,
           strftime('%Y-%m', transaction_ts) AS activity_month
    FROM transactions
    WHERE status = 'completed'
),
with_next AS (
    SELECT user_id,
           activity_month,
           strftime('%Y-%m', date(activity_month || '-01', '+1 month'))             AS following_month,
           LEAD(activity_month) OVER (PARTITION BY user_id ORDER BY activity_month) AS next_active_month
    FROM active
)
SELECT following_month AS month,
       COUNT(*)        AS active_prev_month,
       SUM(CASE WHEN next_active_month IS NULL OR next_active_month <> following_month THEN 1 ELSE 0 END) AS churned_users,
       ROUND(100.0 * SUM(CASE WHEN next_active_month IS NULL OR next_active_month <> following_month THEN 1 ELSE 0 END)
             / COUNT(*), 2) AS churn_rate_pct
FROM with_next
WHERE activity_month < (SELECT MAX(activity_month) FROM active)
GROUP BY 1
ORDER BY 1;

-- Result (both versions agree):
-- month   | active_prev_month | churned_users | churn_rate_pct
-- 2026-02 | 1999              | 890           | 44.52
-- 2026-03 | 3476              | 1126          | 32.39
--
-- Check: distinct users with a completed transaction in February = 3476.

-- So what:
-- 44.5% of the users who transacted in January did not transact in February, and
-- 32.4% of February's did not come back in March. Losing a third to a half of
-- active users every month is very high for a wallet. The fall from 44.5% to 32.4%
-- is not proof that retention is improving: February's base already contains the
-- January users who stayed, and they are the ones least likely to leave. With two
-- data points from a 90-day-old business the honest reading is "high, and too early
-- to call a trend". The total active base still grew (1,999 to 3,476 to 6,601)
-- because new sign-ups outran the losses, which is exactly how growth hides churn.


-- ----------------------------------------------------------------------------
-- Q4. Top 5 campaigns by ROAS
-- Columns: campaign_id, campaign_name, channel, spend_ghs, revenue_ghs, roas
-- ----------------------------------------------------------------------------

-- Spend and revenue are each summed to campaign grain before they meet.
-- Revenue is fee_ghs on completed transactions only (data dictionary, rules 1 and 2).
WITH campaign_spend_total AS (
    SELECT campaign_id, SUM(spend_ghs) AS spend_ghs
    FROM campaign_spend
    GROUP BY campaign_id
),
campaign_revenue AS (
    SELECT u.campaign_id, SUM(t.fee_ghs) AS revenue_ghs
    FROM users u
    JOIN transactions t ON t.user_id = u.user_id
    WHERE t.status = 'completed'
      AND u.campaign_id IS NOT NULL
    GROUP BY u.campaign_id
)
SELECT c.campaign_id,
       c.campaign_name,
       c.channel,
       ROUND(s.spend_ghs, 2)                              AS spend_ghs,
       ROUND(COALESCE(r.revenue_ghs, 0), 2)               AS revenue_ghs,
       ROUND(COALESCE(r.revenue_ghs, 0) / s.spend_ghs, 3) AS roas
FROM campaigns c
JOIN campaign_spend_total s ON s.campaign_id = c.campaign_id
LEFT JOIN campaign_revenue r ON r.campaign_id = c.campaign_id
ORDER BY roas DESC
LIMIT 5;

-- Result:
-- campaign_id | campaign_name                     | channel    | spend_ghs | revenue_ghs | roas
-- C01         | GGL_Search_Brand_AlwaysOn         | Google Ads | 8271.69   | 16409.95    | 1.984
-- C05         | META_Retargeting_IncompleteSignup | Meta Ads   | 3440.85   | 3964.20     | 1.152
-- C06         | REF_Give10_Get10                  | Referral   | 8100.00   | 8300.81     | 1.025
-- C04         | META_Prospecting_Launch           | Meta Ads   | 24505.70  | 10899.94    | 0.445
-- C02         | GGL_Search_Generic_SendMoney      | Google Ads | 46932.55  | 18072.44    | 0.385
--
-- Check (C01): SUM(spend_ghs) = 8271.69 and completed-fee revenue from its users = 16409.95.

-- So what (what would you want to know before giving #1 more budget?):
-- Only three of fourteen campaigns have earned their spend back so far, and all
-- three are small (GHS 3,400 to 8,300). Before giving brand search more budget I
-- would want to know three things. How much of its revenue is incremental: people
-- who search for "CediFlow" were already on their way in, and might have signed up
-- with no ad. Whether it can absorb more money at all: it is capped by how many
-- people search for the brand. And whether the ranking is a timing effect: the
-- January campaigns have had three months to earn fees and the March ones a few
-- weeks, so this table favours whatever started first.


-- ============================================================================
-- Stretch questions (optional, not graded)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- S1. Activation funnel by sign-up month
-- Columns: signup_month, signups, kyc_verified, activated_7d, activation_rate_7d_pct
-- ----------------------------------------------------------------------------

WITH first_txn AS (
    SELECT user_id, date(MIN(transaction_ts)) AS first_txn_date
    FROM transactions
    WHERE status = 'completed'
    GROUP BY user_id
)
SELECT strftime('%Y-%m', u.signup_date)                                                    AS signup_month,
       COUNT(*)                                                                            AS signups,
       COUNT(u.kyc_verified_date)                                                          AS kyc_verified,
       SUM(CASE WHEN f.first_txn_date <= date(u.signup_date, '+7 days') THEN 1 ELSE 0 END) AS activated_7d,
       ROUND(100.0 * SUM(CASE WHEN f.first_txn_date <= date(u.signup_date, '+7 days') THEN 1 ELSE 0 END) / COUNT(*), 1) AS activation_rate_7d_pct
FROM users u
LEFT JOIN first_txn f ON f.user_id = u.user_id
GROUP BY 1
ORDER BY 1;

-- Result:
-- signup_month | signups | kyc_verified | activated_7d | activation_rate_7d_pct
-- 2026-01      | 3703    | 3008         | 1925         | 52.0
-- 2026-02      | 3884    | 3103         | 1998         | 51.4
-- 2026-03      | 7464    | 5358         | 3406         | 45.6

-- One reason March looks worse that has nothing to do with user quality:
-- The data stops on 31 March, so anyone who signed up after 24 March has not had
-- their seven days yet and counts as "not activated" by default. Restricting March
-- to sign-ups on or before the 24th gives 2,899 of 6,139 = 47.2%. So about a
-- quarter of the gap to February is the calendar; the rest is real.


-- ----------------------------------------------------------------------------
-- S2. Cheapest campaign in each channel
-- Columns: channel, campaign_name, signups, spend_ghs, cac, cac_rank_in_channel
-- ----------------------------------------------------------------------------

WITH campaign_spend_total AS (
    SELECT campaign_id, SUM(spend_ghs) AS spend_ghs
    FROM campaign_spend
    GROUP BY campaign_id
),
campaign_signups AS (
    SELECT campaign_id, COUNT(*) AS signups
    FROM users
    WHERE campaign_id IS NOT NULL
    GROUP BY campaign_id
)
SELECT c.channel,
       c.campaign_name,
       n.signups,
       ROUND(s.spend_ghs, 2)                                                 AS spend_ghs,
       ROUND(s.spend_ghs / n.signups, 2)                                     AS cac,
       RANK() OVER (PARTITION BY c.channel ORDER BY s.spend_ghs / n.signups) AS cac_rank_in_channel
FROM campaigns c
JOIN campaign_spend_total s ON s.campaign_id = c.campaign_id
JOIN campaign_signups n ON n.campaign_id = c.campaign_id
ORDER BY c.channel, cac_rank_in_channel;

-- Result:
-- channel    | campaign_name                     | signups | spend_ghs | cac    | cac_rank_in_channel
-- Google Ads | GGL_Search_Brand_AlwaysOn         | 942     | 8271.69   | 8.78   | 1
-- Google Ads | GGL_UAC_AppInstalls               | 824     | 24280.34  | 29.47  | 2
-- Google Ads | GGL_Search_Generic_SendMoney      | 1386    | 46932.55  | 33.86  | 3
-- Google Ads | GGL_YouTube_LaunchFilm            | 148     | 16712.04  | 112.92 | 4
-- Influencer | INF_Wave2_FinanceCreators         | 633     | 13200.00  | 20.85  | 1
-- Influencer | INF_Wave1_LifestyleCreators       | 548     | 26000.00  | 47.45  | 2
-- Meta Ads   | META_Retargeting_IncompleteSignup | 449     | 3440.85   | 7.66   | 1
-- Meta Ads   | META_Prospecting_Launch           | 1232    | 24505.70  | 19.89  | 2
-- Meta Ads   | META_Lookalike_HighValue          | 1206    | 31660.96  | 26.25  | 3
-- Meta Ads   | META_IndependenceDay_Promo        | 363     | 10190.35  | 28.07  | 4
-- Referral   | REF_Give10_Get10                  | 497     | 8100.00   | 16.30  | 1
-- Referral   | REF_DoubleBonus_March             | 699     | 18800.00  | 26.90  | 2
-- TikTok Ads | TT_InFeed_StudentPromo            | 1335    | 10525.35  | 7.88   | 1
-- TikTok Ads | TT_Spark_CashbackChallenge        | 1492    | 13900.62  | 9.32   | 2

-- So what:
-- The two TikTok campaigns have the lowest CAC of any prospecting campaign
-- (GHS 7.88 and 9.32), yet neither is in the ROAS top five in Q4. Cheap to sign
-- up is not the same as worth acquiring, so CAC alone should not rank campaigns.
