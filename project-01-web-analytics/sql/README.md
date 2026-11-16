<!-- markdownlint-disable MD013 -->
# SQL

Every number in the project README can be reproduced by a query in this folder. Each file holds one query, with the business question it answers written at the top. The saved output of each is in [results/](results/).

Run on SQLite 3.39 against `../data/cediflow_web.db`. The queries avoid aggregate `FILTER`, so they also run on older SQLite builds.

| Query | Question | Technique worth noting |
| --- | --- | --- |
| [01_sessions_from_events.sql](01_sessions_from_events.sql) | How do raw GA4 events become one row per session? | `ROW_NUMBER()` to find each session's first page view; composite session key |
| [02_kpi_summary.sql](02_kpi_summary.sql) | What happened this quarter, in one row? | Two tables of different grain summarised separately, then cross-joined |
| [03_channel_performance.sql](03_channel_performance.sql) | Is each channel's share of sign-ups in line with its share of sessions? | Shares from a window total, `SUM(...) OVER ()` |
| [04_campaign_cost_per_signup.sql](04_campaign_cost_per_signup.sql) | What does a sign-up cost in each paid campaign? | Aggregate to campaign grain on both sides before joining |
| [05_funnel_by_device.sql](05_funnel_by_device.sql) | Which funnel step loses the most people, and on which device? | Step rates, each with its own denominator |
| [06_landing_pages.sql](06_landing_pages.sql) | Which landing pages start sign-ups and which lose the visitor at once? | GA4's engaged-session definition of bounce |
| [07_cashback_page_by_channel.sql](07_cashback_page_by_channel.sql) | Is `/promo/cashback` a bad page, or does it just get bad traffic? | Conditional aggregation to compare inside each channel |
| [08_remitters_by_country.sql](08_remitters_by_country.sql) | Where do the clicks of one expensive campaign come from? | Share of a filtered total with a window |
| [09_otp_rate_weekly_by_os.sql](09_otp_rate_weekly_by_os.sql) | Did the OTP step break for anyone, and when? | Trailing four-week baseline with a window frame |
| [10_region_mix_adjusted.sql](10_region_mix_adjusted.sql) | Does Ashanti convert better than Greater Accra once channel mix is held equal? | Direct standardisation across four CTEs |
| [11_weekly_trend.sql](11_weekly_trend.sql) | Are sessions, sign-ups and spend moving together? | Week grain on both sides before joining |

## Checked against Python

The same tables are calculated independently in pandas by `../python/02_analysis.py`. `../python/03_verify_sql_against_python.py` runs every query here and compares the two. All eleven agree, and query 01 rebuilds all 31,167 sessions identically to the Python pipeline.
