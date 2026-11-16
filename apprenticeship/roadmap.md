<!-- markdownlint-disable MD001 MD013 MD033 -->
> **Markdown copy of `analytics-apprenticeship-system.docx`**, converted on 2026-11-13 so it can be read in VS Code.
> The Word file is the original. Two things live elsewhere now: the progress tracker in Part 14 is kept up to date in
> [`progress-tracker.md`](progress-tracker.md), and the full Week 1 material is in [`week-01-funnel-metrics/`](week-01-funnel-metrics/README.md).

# Marketing & Product Analytics Apprenticeship System

**12 weeks · 8–10 hrs/week · Fintech-focused · Ferdinard, University of Ghana**

Core skill you’re building: given a messy dataset, answer *what happened, why, what should the business do, and how confident are we.*

## PART 1 — Executive Overview

You already know SQL (intermediate), Python (intermediate), Tableau (beginner-intermediate), stats (basic-intermediate), DB design, Git. This program does NOT re-teach those from zero — it points them at marketing/product problems.

**3 portfolio projects, in order:** 1. Web/Acquisition Analytics (Tableau + SQL + Python) — Weeks 1–4 2. Email/Segmentation/Retention Analytics — Weeks 5–8 3. Capstone: Fintech Growth Analytics — Weeks 9–12

**Grading happens every week** across: Marketing Knowledge, SQL, Statistics, Tableau, Business Thinking, Communication.

**How this document works with me (Claude) going forward:** This file is your master roadmap, tracker, and reference. The full *curriculum content for Week 1* (readings, exercises, SQL sets, quiz) is built out below in Part 4. For Weeks 2–12 I’ve given you the real structure, learning objectives, and sample exercises so you can see the shape of each week — but I’ll generate the **full weekly packet** (complete SQL challenge set, dataset, quiz, grading) at the start of each week when you say “start week N.” This is deliberate, not a cop-out: dumping 12 weeks of dense material on you today would violate your own “don’t overwhelm me” rule, and it lets me calibrate difficulty to how Week 1 actually goes.

## PART 2 — Starting Skill Assessment

| Area | Self-rated | My working assumption |
| --- | --- | --- |
| SQL | Intermediate | Comfortable with JOINs, GROUP BY, subqueries. Window functions (ROW_NUMBER, LAG/LEAD, RANK) — assume exposure but not fluency. Will test Week 1. |
| Python/Pandas | Intermediate | Comfortable with dataframes, cleaning, basic viz. Statistical testing (scipy.stats) — assume new. |
| Tableau | Beginner-intermediate | Can connect data, build basic charts. Calculated fields, parameters, actions, LOD expressions — assume new-to-shaky. |
| Statistics | Basic-intermediate | Mean/median/variance solid. Hypothesis testing, p-values, confidence intervals — assume conceptual gaps. |
| Marketing analytics | Beginner | Everything here is new: funnels, CAC/LTV, attribution, RFM. |
| Business reasoning | Developing | This is the actual bottleneck for internships — most candidates can run a query but can’t say “so what.” |

You’ll confirm/correct this with the Week 1 diagnostic (Part 4).

## PART 3 — 12-Week Roadmap

| Week | Theme | Output |
| --- | --- | --- |
| 1 | Marketing funnel & metrics (AARRR, CAC, LTV, ROI) | Manual + SQL metric calculations |
| 2 | Data sources & data quality | Cleaned messy marketing dataset |
| 3 | GA4 concepts (events, sessions, attribution basics) | Funnel dataset built from GA4-style events |
| 4 | Tableau mastery (calc fields, params, actions, LOD) | **Project 1: Web/Acquisition Dashboard** |
| 5 | Email marketing analytics | Campaign comparison analysis |
| 6 | Customer segmentation (RFM) | Segment build in SQL/Python → Tableau |
| 7 | Cohort analysis | Retention heatmap (SQL window functions) |
| 8 | A/B testing & statistics | **Project 2: Email/Cohort/Retention Dashboard** |
| 9 | Customer Lifetime Value | LTV by channel/segment/cohort |
| 10 | Attribution modeling | First/last/multi-touch comparison |
| 11 | Growth & product analytics | Marketing→product funnel linkage |
| 12 | Capstone + presentation + final exam | **Capstone: Fintech Growth Analytics** |

Month 1 = Weeks 1–4. Month 2 = Weeks 5–8. Month 3 = Weeks 9–12.

## PART 4 — Detailed Weekly Curriculum

### WEEK 1 — Marketing Funnel & Metrics (full detail)

#### Concepts to learn

- **AARRR (Pirate Metrics):** Acquisition → Activation → Retention → Revenue → Referral
- **CAC** = Total acquisition spend / New customers acquired
- **LTV** = Avg revenue per customer × Avg customer lifespan (or margin-adjusted)
- **Conversion rate** = Conversions / Total visitors or leads
- **Churn rate** = Customers lost in period / Customers at start of period
- **ROI** = (Revenue − Cost) / Cost. **ROAS** = Revenue / Ad spend (no cost subtracted — know the difference, it’s a common interview trap)
- **Engagement**: DAU/MAU ratio, session frequency

#### Manual calculation exercises (do these before touching SQL)

1. A fintech app spent GHS 50,000 on Google Ads and acquired 2,000 new users last month. What’s CAC?
2. Average customer generates GHS 15/month in fees and stays active for 18 months on average. What’s LTV? Is LTV:CAC healthy? (Rule of thumb: LTV:CAC ≥ 3:1 is healthy — explain why 1:1 is a problem even though it looks “profitable.”)
3. A SaaS product had 1,200 customers at the start of March and lost 84 by end of March. Churn rate?
4. Two campaigns: Campaign A spent GHS 10,000, generated GHS 35,000 revenue. Campaign B spent GHS 3,000, generated GHS 9,500. Compare ROI and ROAS for both. Which is “better” and why does the answer depend on what the business is optimizing for (efficiency vs. absolute revenue)?

#### SQL exercises (write these against the dataset described below)

You’ll get a `transactions`, `users`, `campaigns` schema. Exercises (attempt before I give solutions): 1. Total new users acquired per calendar month. 2. CAC per month (assume a `campaign_spend` table joined by month). 3. Monthly churn rate using a self-join or window function comparing active users this month vs last month. 4. Top 5 campaigns by ROAS.

#### Business scenario

> Marketing reports: “Conversion rate is up 15% this month, great work!” Finance reports: “Revenue per new customer is down 20%.” Both are true. What questions do you ask before deciding whether this quarter was good or bad? (Write 150–250 words. I’ll grade for whether you identify that conversion *volume* and *quality* are different axes, and that you’d want to check channel mix, discounting, and cohort-level revenue before concluding anything.)

#### Diagnostic quiz (10 questions, mixed concept + calculation) — attempt, then I’ll grade

1. Define activation in the AARRR framework with a fintech example.
2. If LTV:CAC = 1.2:1, is the business sustainable? Why/why not?
3. What’s the difference between churn rate and retention rate?
4. ROAS of 4.0 — good or bad? (Trick: depends on margin. If margin is 15%, a 4x ROAS on gross revenue can still lose money.) 5–10: calculation-based, generated from the dataset once you request the Week 1 packet.

#### Dataset for Week 1

I’ll generate a synthetic fintech dataset (`users`, `transactions`, `campaigns`, `campaign_spend`) sized for realistic cohort/funnel analysis (10k+ users, 90 days) when you’re ready to start — say “generate week 1 dataset” and I’ll build it as CSVs + a data dictionary.

#### Week 1 evidence to save

- Written manual calculations
- SQL file with your 4 queries + results
- 150–250 word business scenario answer
- Quiz score

### WEEK 2 — Data Sources & Data Quality

**Learn:** where marketing data actually comes from (CRM, GA4, ad platforms, payment systems) and the data model underneath (events, users, sessions, campaigns, channels, attribution). **Data quality faults to detect:** missing values, duplicate user records, malformed timestamps, inconsistent campaign naming, orphaned foreign keys, outlier transaction amounts, bot/test traffic. **Exercise:** I’ll hand you a deliberately messy CSV (duplicate IDs, bad dates, null campaign names, a few impossible values). Your job: profile it (Python), document every issue found, clean it, and write a short “data quality memo” explaining what you fixed and what you couldn’t fix without more context. **Grading axis added this week:** Data Quality (part of Part 20’s rubric).

### WEEK 3 — GA4 Concepts

**Learn:** GA4 event model (events > parameters), users vs sessions, traffic source/medium/campaign, default channel groupings, conversion events, exploration funnels, why GA4 export data looks the way it does (BigQuery export schema — good to know even without a live property). **Exercise:** Build a GA4-style events table in SQL from a synthetic dataset, then derive session-level and funnel-level metrics from raw events (this is the actual skill GA4 requires — most people just click around the UI and never learn to reconstruct sessions/funnels from raw events, which is what sets analysts apart). **No live website required** — synthetic dataset provided.

### WEEK 4 — Tableau Mastery + Project 1

**Learn:** calculated fields, parameters, LOD expressions (FIXED/INCLUDE/EXCLUDE — this is where most “intermediate” Tableau users are actually weak), dashboard actions (filter/highlight/URL), KPI card design, dashboard vs. report vs. analysis vs. data story (this distinction matters in interviews). **Project 1 spec:** see Part 11.

### WEEK 5 — Email Marketing Analytics

**Metrics:** open rate, CTR, click-to-open rate, conversion rate, bounce rate, unsubscribe rate, revenue per email, revenue per recipient, campaign ROI. **Conflict exercise:** Campaign A — 28% open rate, GHS 4,200 revenue. Campaign B — 19% open rate, GHS 7,800 revenue. Which is “better”? What do you need to know before deciding (list size, send cost, audience segment, offer type)? Write the argument for each side, then your recommendation.

### WEEK 6 — Customer Segmentation (RFM)

**Learn:** Recency/Frequency/Monetary scoring, standard RFM segment labels (Champions, Loyal, At-Risk, Lost, New), behavioral segmentation beyond RFM. **Exercise:** Compute RFM scores in SQL (percentile/NTILE window functions), build segments in Python, visualize segment distribution and revenue concentration in Tableau (expect to find ~20% of customers driving ~80% of revenue — verify this yourself, don’t assume it).

### WEEK 7 — Cohort Analysis

**Learn:** signup cohorts, Day-1/7/30 retention, revenue retention (NRR-style), the difference between user retention and revenue retention (revenue can grow even as users churn — expansion revenue). **SQL focus:** this is where you’ll actually use LAG/LEAD and self-joins for real. Write cohort retention SQL from scratch — I will not hand you the query first. **Visualization:** Tableau retention heatmap (cohort month × period, color = retention %).

### WEEK 8 — A/B Testing & Statistics + Project 2

**Learn:** null/alternative hypothesis, p-values, confidence intervals, statistical vs. practical significance, sample size/power, Type I/II errors. **Core exercise:** Subject Line A (10,000 sent, 22% open) vs B (10,000 sent, 23% open). Run a two-proportion z-test in Python. Is it significant at α=0.05? Even if significant — is a 1pp lift practically worth switching, given implementation cost/risk? You must argue both sides before concluding. **Project 2 spec:** see Part 11.

### WEEK 9 — Customer Lifetime Value

**Learn:** historical vs. predictive LTV, AOV × purchase frequency × lifespan, margin-adjusted LTV, LTV:CAC by channel — the actual number that determines whether a channel should get more or less budget. **Exercise:** Calculate LTV by acquisition channel and by cohort in SQL/Python; visualize in Tableau; identify which channel looks cheap (low CAC) but is actually expensive (low LTV) — this “CAC trap” is a classic fintech growth mistake.

### WEEK 10 — Attribution

**Learn:** first-touch, last-touch, linear multi-touch, why each model tells a different story about the same customer journey, and why none of them is “true.” **Exercise:** Given the same multi-channel customer journeys, compute channel credit under all three models and show how the “best channel” ranking changes. Write the explanation a marketing director would need to hear about why the ranking flipped.

### WEEK 11 — Growth & Product Analytics

**Learn:** connecting acquisition data to product usage data — which channels bring users who actually activate and stick, which features correlate with retention, where in the product funnel users drop off. **Fintech-specific questions to answer with data:** Which acquisition channel brings the highest-LTV customers? Which customer segment goes inactive fastest? Which product events predict 30-day retention?

### WEEK 12 — Capstone + Final Exam

See Parts 12, 19, 20.

## PART 5 — Daily/Weekly Study System

**Default weekly structure (8–10 hrs), adjust freely:**

| Day | Focus | Time |
| --- | --- | --- |
| Mon | Learn new concept (read/watch, take notes as if teaching someone else) | 1 hr |
| Tue | SQL exercises for the week | 1–1.5 hr |
| Wed | Marketing concept / statistics deep-dive | 1 hr |
| Thu | Tableau practice | 1–1.5 hr |
| Fri | Rest / university work | 0 |
| Sat | Project work | 2–3 hr |
| Sun | Review + weekly assessment | 1 hr |

## PART 6 — Marketing Analytics Concepts (reference glossary)

Acquisition, Activation, Retention, Revenue, Referral (AARRR) · CAC · LTV · LTV:CAC · Conversion rate · Churn · Engagement (DAU/MAU) · ROI vs ROAS · RFM segmentation · Campaign performance · Attribution (first/last/multi-touch)

Full worked definitions + fintech examples for each land in the week they’re introduced (Part 4) rather than duplicated here — this section is your quick-lookup index once you’ve learned them.

## PART 7 — SQL Challenge System (progression)

**Level 1 (Week 1–2):** aggregations, date functions, multi-table JOINs for metric calculation (CAC, churn, revenue by period). **Level 2 (Week 3–5):** CTEs for readable multi-step logic, subqueries for cohort/campaign comparisons. **Level 3 (Week 6–7):** window functions — `NTILE()` for RFM scoring, `ROW_NUMBER()`/`RANK()` for top-N-per-group, `LAG()`/`LEAD()` for cohort retention and period-over-period change. **Level 4 (Week 9–11):** combining window functions + CTEs for LTV-by-cohort, attribution credit splitting, funnel step-drop analysis.

Full question sets (5–10 per week) generated with each week’s dataset. Sample Level 3 question type you’ll hit in Week 7:

```sql
-- Given `signups(user_id, signup_month)` and `activity(user_id, activity_month)`,
-- write a query returning retention % for each signup cohort at month 0,1,2,3.
```

You write it; I grade it against a reference solution and explain what’s wrong before showing mine.

## PART 8 — Statistics Challenge System (progression)

**Level 1:** descriptive stats, standard deviation/variance interpretation in a business context (“what does high variance in transaction size tell a fintech risk team?”). **Level 2:** probability, sampling, confidence intervals (“we surveyed 200 of 50,000 users — how much do we trust this?”). **Level 3:** hypothesis testing, p-values, two-proportion/two-sample tests (the A/B testing week). **Level 4:** correlation vs. causation traps, intro to regression (does feature X *predict* retention, or are both driven by a third factor like account age?).

Every problem is anchored to a business decision — never abstract math for its own sake.

## PART 9 — Tableau Skill Progression

| Stage | Skills |
| --- | --- |
| Foundations (Wk1-3, incidental) | Connections, dimensions/measures, basic charts, filters |
| Core (Wk4) | Calculated fields, parameters, LOD expressions, dashboard actions, KPI cards, tooltips |
| Applied (Wk6-7) | Cohort heatmaps, segmentation visuals, drilldowns |
| Advanced (Wk9-12) | Executive dashboard storytelling, multi-dashboard suites, publishing to Tableau Public |

Rule enforced throughout: **every chart must answer a stated question.** If you can’t say what question a chart answers, it gets cut.

## PART 10 — Python Analytics Progression

Pandas for cleaning/EDA (Wk2) → GA4-style event reconstruction (Wk3) → RFM/segmentation logic (Wk6) → cohort retention arrays (Wk7) → `scipy.stats` for hypothesis testing (Wk8) → LTV modeling (Wk9) → attribution modeling (Wk10) → optional logistic regression for churn (capstone, if you choose Option C-style analysis within the fintech capstone).

## PART 11 — Weekly Projects

#### Project 1 (end of Week 4) — Web/Acquisition Analytics Dashboard

**Data:** GA4-style synthetic dataset (traffic, channels, landing pages, conversions, device, geo). **Dashboard sections:** Executive Summary · Acquisition Analysis · Funnel Analysis · User Behavior · Drilldown. **Deliverables:** Tableau dashboard (published to Tableau Public if practical) · dataset · SQL queries · Python cleaning/analysis script · 1-page executive insights report with **3–5 actionable recommendations** · README.

#### Project 2 (end of Week 8) — Email Campaign & Retention Dashboard

**Data:** 10+ synthetic email campaigns + cohort/retention data. **Dashboard sections:** Campaign overview · Campaign comparison · Segment analysis · A/B test results · Cohort retention · Revenue impact. **Deliverables:** dashboard, SQL repo (campaign/RFM/cohort/retention queries), Python analysis (cleaning + stats tests), 2–3 page written report structured as **Finding → Evidence → Interpretation → Recommendation → Limitation**.

## PART 12 — Capstone Project (Week 12)

**You will choose ONE option in Week 9** (not now — deciding this early wastes the “which do I actually find interesting” signal you’ll only have after Weeks 1-8). Recommended default given your fintech goal: **Option A — Fintech Growth Analytics**.

**Option A dataset:** users, accounts, transactions, campaigns, channels, email interactions, product events, signups, conversions, churn, revenue — fully simulated fintech app. **Analysis:** acquisition, activation, conversion, retention, churn, LTV, CAC, campaign performance, segmentation, product engagement.

**Required layers for whichever option you pick:** - **Data:** raw + cleaned dataset + data dictionary - **SQL:** cleaning, KPI calcs, funnel, cohort, segmentation, retention queries - **Python:** cleaning, EDA, stats, optional modeling - **Tableau:** as many dashboards as the story needs (quality over the six-dashboard maximum — don’t pad)

## PART 13 — Mastery Gates

For each core skill, you must demonstrate, in order: **Know → Calculate → Query (SQL) → Analyze → Visualize → Recommend.** A skill is marked **Mastered** only once you’ve produced evidence at every stage — not after watching an explanation. Status options: Not Started, Learning, Practicing, Tested, Passed, Mastered.

## PART 14 — Progress Tracker

| Skill | Status | Score | Evidence | Confidence (1–5) | Next Action |
| --- | --- | --- | --- | --- | --- |
| Marketing funnel (AARRR) | Not Started | — | — | — | Start Week 1 |
| CAC / LTV | Not Started | — | — | — | Start Week 1 |
| Data quality / cleaning | Not Started | — | — | — | — |
| GA4 event model | Not Started | — | — | — | — |
| Tableau calc fields/LOD/actions | Not Started | — | — | — | — |
| Email metrics | Not Started | — | — | — | — |
| RFM segmentation | Not Started | — | — | — | — |
| Cohort/retention SQL | Not Started | — | — | — | — |
| A/B testing & significance | Not Started | — | — | — | — |
| LTV modeling | Not Started | — | — | — | — |
| Attribution modeling | Not Started | — | — | — | — |
| Growth/product analytics | Not Started | — | — | — | — |

Send me your evidence at the end of each week and I’ll update this table and tell you honestly where you’re weak — I won’t inflate scores.

## PART 15 — Student Mode & Recovery Mode

**Modes:** - Normal week: 8–10 hrs - Busy university week: 4–5 hrs → keep SQL + one core concept, drop the polish pass on Tableau - Exam week: 2–3 hrs → concept review only, no new project work, no guilt

**If you miss a week entirely:** 1. I identify the 1–2 essential skills from that week (not everything) 2. Cut optional material permanently — it doesn’t get “made up” later 3. Merge related topics into the next week’s session 4. Protect the project deadline over the concept coverage 5. I give you a revised 1-week recovery plan, capped at your normal 8–10 hr budget — never a catch-up cram week

## PART 16 — GitHub Portfolio Structure

```text
marketing-analytics-portfolio/
├── project-01-web-analytics/
│   ├── data/
│   ├── sql/
│   ├── python/
│   ├── tableau/
│   └── README.md
├── project-02-email-retention/
│   ├── data/
│   ├── sql/
│   ├── python/
│   ├── tableau/
│   └── README.md
└── project-03-capstone-fintech-growth/
    ├── data/
    ├── sql/
    ├── python/
    ├── tableau/
    ├── reports/
    └── README.md
```

Each README: business questions → methodology → key findings → dashboard screenshots/link → recommendations → limitations. This is what a recruiter actually reads before opening anything else.

## PART 17 — Certification Strategy

| Certification | Priority | Cost | Verdict |
| --- | --- | --- | --- |
| Tableau Public portfolio (not a cert, but the actual proof) | — | Free | This *is* your credential — prioritize over any certificate |
| Google Analytics (GA4) certification | Medium | Free | Fast to get, mildly useful as a checkbox, teaches nothing your Week 3 work doesn’t already cover |
| Tableau Desktop Specialist | Optional | ~$100 | Only worth it if a specific job posting asks for it; your portfolio proves more |
| DataCamp Data Analyst track | Low (you already have DataCamp certs) | Subscription | Skip — you have equivalent evidence already; time is better spent on projects |
| HubSpot Analytics cert | Optional | Free | Fine if targeting martech-adjacent roles specifically, low priority for fintech |
| Coursera data science courses | Optional | Varies | Only if a specific gap shows up (e.g., you find regression genuinely shaky) |

**Bottom line: three strong portfolio projects with clear business reasoning beat every certificate on this list combined for internship screening.** Certs are tiebreakers, not qualifiers.

## PART 18 — Interview Preparation (built out in Month 3)

Sample reasoning questions you’ll practice out loud, not memorize: - Conversion dropped 20% this week. How do you investigate? - CAC increased but revenue also increased — necessarily bad? - Email open rate up, purchases down — what could explain it? - Two channels, different CAC and LTV — which do you prioritize, and what else would you want to know? - A test result is statistically significant but the lift is 0.2% — do you ship it?

Full mock interview sets (SQL live-coding style, Tableau walkthroughs, case questions) delivered in Week 11.

## PART 19 — Final Exam (Week 12)

A — Marketing Metrics (15) · B — SQL (15) · C — Statistics (10) · D — Tableau (10) · E — Business Cases (3 scenarios) · F — Data Quality (3 scenarios) · G — Analytics Interpretation (3 charts/datasets) · H — Capstone Defense (10 questions on your own project). Delivered in full at Week 12.

## PART 20 — Final Readiness Assessment

Scored honestly (no inflation) across: Marketing Analytics, SQL, Statistics, Python, Tableau, Business Thinking, Data Quality, Communication, Portfolio Quality, Interview Readiness → Overall /100.

| Band | Meaning |
| --- | --- |
| 90–100 | Strong junior/internship candidate |
| 80–89 | Internship-ready |
| 70–79 | Promising, needs targeted improvement |
| 60–69 | Foundational |
| &lt;60 | Needs significant development |

## PART 21 — Resource Library (starter set)

| Resource | Topic | Cost | Difficulty | Priority |
| --- | --- | --- | --- | --- |
| Google Analytics 4 official docs (support.google.com/analytics) | GA4 event model | Free | Beginner-Int | High — Week 3 |
| Mixpanel / Amplitude blog (product analytics concepts) | Funnels, retention, product analytics | Free | Int | High — Week 11 |
| Tableau’s own “Sample Superstore” + Tableau Public gallery | Tableau technique reference | Free | All levels | High — throughout |
| Mode Analytics SQL tutorial (window functions section) | Window functions | Free | Int-Adv | High — Week 7 |
| Khan Academy: Statistics & Probability (hypothesis testing unit) | Stats foundations | Free | Beginner-Int | Medium — Week 8 |
| “Trustworthy Online Controlled Experiments” (Kohavi et al.) — at least the intro chapters | A/B testing rigor | Free (drafts online) / paid book | Int-Adv | Medium — Week 8 |
| Kaggle datasets (search “marketing,” “fintech,” “churn”) | Real-world messy data practice | Free | Varies | Medium — supplement to synthetic data |
| SaaStr / Bessemer “State of…” reports | Real CAC/LTV benchmarks for sanity-checking your numbers | Free | N/A | Medium — Weeks 1, 9 |

I’ll add resources inline as each week surfaces a specific gap rather than front-loading a huge list you won’t use.

## PART 22 — DAY 1: What To Actually Do

1. **Read** Part 4, Week 1 concepts section above (AARRR, CAC, LTV, conversion, churn, ROI/ROAS) — 20 min, no video needed, you don’t need a beginner explainer at your level.
2. **Do** the 4 manual calculation exercises in Week 1 by hand (not in a spreadsheet yet) — forces the formulas to stick. ~20 min.
3. **Reply to me** with your answers to the manual calculations and the business scenario question. I’ll grade them and flag any conceptual gaps before you touch SQL.
4. **Say “generate week 1 dataset”** and I’ll build the `users`/`transactions`/`campaigns`/`campaign_spend` synthetic dataset + data dictionary as downloadable CSVs.
5. **Write** the 4 SQL exercises against that dataset — attempt first, don’t ask me for the query. Save your `.sql` file.
6. **Evidence to save today:** written manual calcs, business scenario answer (150–250 words), `.sql` file once the dataset is ready.

Do not start Tableau yet. Do not start Week 2 material. That’s the whole Day 1 — should take under 90 minutes total across the calculations and scenario, leaving room for the SQL once you have the dataset.
