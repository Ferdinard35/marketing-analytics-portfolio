<!-- markdownlint-disable MD013 -->
# Week 1: SQL exercises

Four core questions (graded) and two stretch questions (optional). This is Level 1 of the roadmap's SQL progression: aggregations, date functions and multi-table joins used to calculate metrics.

## Before you start

1. Load the dataset and read [data/data_dictionary.md](data/data_dictionary.md) all the way through. The definitions of revenue, active and organic are in its "Business rules" section, and the answers are graded against them.
2. Write your queries in [sql/week1_queries.sql](sql/week1_queries.sql).
3. Attempt everything yourself first. I will not hand you a query.

**For every question you hand in three things:** the query, its result pasted underneath as a comment, and one or two sentences beginning `-- So what:` that say what the result means for CediFlow. The "so what" line is where most candidates fall down, so it is marked.

## Core questions

### Q1. New users per month

Total new users acquired per calendar month.

| Output column | Meaning |
| --- | --- |
| `signup_month` | The calendar month of `signup_date` |
| `new_users` | Number of users who signed up in it |

One row per month, in date order.

### Q2. CAC per month

For each calendar month: what CediFlow spent on marketing, how many users it acquired, and what each one cost.

| Output column | Meaning |
| --- | --- |
| `month` | Calendar month |
| `total_spend_ghs` | All campaign spend booked in that month |
| `new_users` | Everyone who signed up that month |
| `paid_new_users` | Those who signed up through a campaign |
| `blended_cac` | `total_spend_ghs` ÷ `new_users`, to 2 decimal places |
| `paid_cac` | `total_spend_ghs` ÷ `paid_new_users`, to 2 decimal places |

In your "so what", say which of the two CAC figures you would report, and to whom.

### Q3. Monthly churn rate

Compare the users who were active in one month with the users who were active in the month before.

- A user is **active** in a month if they have at least one `completed` transaction in it.
- **Churn rate for month M** = users who were active in month M−1 and are not active in month M ÷ users who were active in month M−1.

| Output column | Meaning |
| --- | --- |
| `month` | Month M |
| `active_prev_month` | Users active in the month before |
| `churned_users` | How many of those are not active in month M |
| `churn_rate_pct` | Churned as a percentage of `active_prev_month`, to 2 decimal places |

January has no previous month, so it gets no row. Use either a self-join or a window function (`LAG` or `LEAD`). If you have time, write it both ways and check that the two agree.

### Q4. Top 5 campaigns by ROAS

ROAS for a campaign, over the whole quarter = fee revenue from the users that campaign acquired ÷ that campaign's total spend.

| Output column | Meaning |
| --- | --- |
| `campaign_id`, `campaign_name`, `channel` | From `campaigns` |
| `spend_ghs` | The campaign's total spend |
| `revenue_ghs` | Fee revenue earned from the users it acquired |
| `roas` | `revenue_ghs` ÷ `spend_ghs`, to 3 decimal places |

Return the five campaigns with the highest ROAS, highest first. In your "so what", say what you would want to know before giving your number one campaign more budget.

## Check your own work

A result that looks plausible can still be wrong. Analysts check against totals they can get another way. Do these before you send anything:

- **Q1:** your monthly counts must add up to `SELECT COUNT(*) FROM users`.
- **Q2:** your monthly spend must add up to `SELECT SUM(spend_ghs) FROM campaign_spend`, and `new_users` must match Q1.
- **Q3:** `active_prev_month` for March must equal the number of distinct users with a completed transaction in February. Get that with a separate one-line query.
- **Q4:** pick one campaign from your top five and get its spend and its revenue with two separate, simple queries. They must match your result exactly.

If a check fails, the bug is nearly always in a join.

## Stretch questions (optional, not graded)

Do these only if the core four are finished. They carry no points; they show me how comfortable you are with conditional aggregation and window functions.

### S1. Activation funnel by sign-up month

| Output column | Meaning |
| --- | --- |
| `signup_month` | Calendar month of sign-up |
| `signups` | Users who signed up in it |
| `kyc_verified` | Those with a `kyc_verified_date` |
| `activated_7d` | Those whose first completed transaction was on or before `signup_date` + 7 days |
| `activation_rate_7d_pct` | `activated_7d` as a percentage of `signups`, to 1 decimal place |

March will look worse than the other two months. Give one reason for that which has nothing to do with the quality of the users.

### S2. Cheapest campaign in each channel

CAC per campaign, ranked inside its channel with `RANK()`, where rank 1 is the cheapest.

| Output column | Meaning |
| --- | --- |
| `channel`, `campaign_name` | From `campaigns` |
| `signups` | Users the campaign acquired |
| `spend_ghs` | The campaign's total spend |
| `cac` | `spend_ghs` ÷ `signups`, to 2 decimal places |
| `cac_rank_in_channel` | Rank by CAC within the channel, cheapest first |

## Dialect notes

The same logic in the two engines you can use this week.

| You need | PostgreSQL | SQLite |
| --- | --- | --- |
| The month of a date | `date_trunc('month', d)` or `to_char(d, 'YYYY-MM')` | `strftime('%Y-%m', d)` |
| One month later | `d + INTERVAL '1 month'` | `date(d, '+1 month')` |
| Seven days later | `d + 7` for a date, `ts + INTERVAL '7 days'` for a timestamp | `date(d, '+7 days')` |
| The date part of a timestamp | `ts::date` | `date(ts)` |
| A conditional count | `COUNT(*) FILTER (WHERE ...)` | `SUM(CASE WHEN ... THEN 1 ELSE 0 END)` |

In both engines, dividing one integer by another gives an integer: `7 / 2` is `3`. Multiply one side by `1.0`, or cast it, before you divide.
