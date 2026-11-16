<!-- markdownlint-disable MD013 -->
# Tableau dashboard: build guide

**Status: the workbook has not been built yet.** The data, the calculations and the numbers to check against are all ready; what is left is assembling them in Tableau Public and publishing. Allow three to four hours the first time.

This is the short reference. The long version, with every click and the reasoning behind each step, is the Word document *How to build the Project 1 Tableau dashboard*.

One dashboard, five sections, each answering a stated question. A chart that does not help answer its section's question does not go in.

## 1. Connect the data

1. Open Tableau Public and connect to `../data/cleaned/sessions.csv` (Text file).
2. Drag `ad_spend.csv` onto the canvas beside it and define the **relationship** (not a join) on two fields: `Campaign = Campaign` and `Session Date = Date`.
3. Change the data type of `User Pseudo Id` to String. Tableau reads it as a decimal number.

A relationship keeps each table at its own grain, so cost is not repeated once per session. A join would multiply it.

On any sheet that shows cost, take `Campaign`, `Channel Group` and the date from `ad_spend`, not from `sessions`. Cost is recorded per campaign per day, so it cannot be split by device, region or landing page.

Check before going further: `sessions.csv` has **31,167** rows, `SUM([Cost Ghs])` is **22,218.16**, and `COUNTD([User Pseudo Id])` is **24,559**.

## 2. Calculated fields

Create these once; every sheet uses them. Every rate is a sum divided by a sum, never an average of row-level rates.

| Name | Formula | Format |
| --- | --- | --- |
| `Sessions` | `COUNTD([Session Key])` | Number, 0 dp |
| `Sign-ups` | `SUM([Signed Up])` | Number, 0 dp |
| `Conversion rate` | `SUM([Signed Up]) / COUNTD([Session Key])` | Percentage, 1 dp |
| `Begin rate` | `SUM([Began Signup]) / COUNTD([Session Key])` | Percentage, 1 dp |
| `OTP rate` | `SUM([Otp Verified]) / SUM([Began Signup])` | Percentage, 1 dp |
| `Completion rate` | `SUM([Signed Up]) / SUM([Otp Verified])` | Percentage, 1 dp |
| `Bounce rate` | `1 - SUM([Engaged Session]) / COUNTD([Session Key])` | Percentage, 1 dp |
| `Cost per sign-up` | `SUM([Cost Ghs]) / SUM([Signed Up])` | Currency GHS, 2 dp |
| `Cost per paid sign-up` | `SUM([Cost Ghs]) / SUM(IF [Channel Group] = "Paid Search" OR [Channel Group] = "Paid Social" THEN [Signed Up] END)` | Currency GHS, 2 dp |
| `Visitor type` | `IF [Is New User] = 1 THEN "New" ELSE "Returning" END` | |
| `In Ghana` | `[Country] = "Ghana"` | |

Level-of-detail expressions:

| Name | Formula | Used for |
| --- | --- | --- |
| `Site conversion rate` | `{ FIXED : SUM([Signed Up]) / COUNTD([Session Key]) }` | A reference line that does not move when a channel is selected |
| `Share of sessions` | `COUNTD([Session Key]) / MIN({ EXCLUDE [Channel Group] : COUNTD([Session Key]) })` | Each channel's share of all sessions |
| `Share of sign-ups` | `SUM([Signed Up]) / MIN({ EXCLUDE [Channel Group] : SUM([Signed Up]) })` | Each channel's share of all sign-ups |

Parameters:

| Name | Values | Drives |
| --- | --- | --- |
| `Metric` | Sessions, Sign-ups, Conversion rate (%), Begin rate (%) | `Selected metric`: a `CASE [Metric]` returning the matching measure, counts wrapped in `FLOAT()` and rates multiplied by 100 so every branch is the same type |
| `Break down by` | Channel, Device, Region, Landing page | `Selected dimension`: a `CASE [Break down by]` returning the matching dimension |

Cost is not offered in `Metric`, because it cannot be broken down by device, region or landing page.

## 3. The five sections

### Executive Summary

**Question: how much traffic did the site get, how much of it signed up, and what did the paid part cost?**

- Five KPI cards: `Sessions`, `Sign-ups`, `Conversion rate`, `SUM([Cost Ghs])`, `Cost per paid sign-up`.
- Two line charts, one above the other, not on a shared second axis: `Sign-ups` by `Week Start`, and `Sessions` by `Week Start`.

Check: 31,167 · 2,426 · 7.8% · GHS 22,218 · GHS 25.11. Week of 30 March: 1,594 sessions and 140 sign-ups.

### Acquisition Analysis

**Question: which channels and campaigns bring visitors who sign up, and what does each sign-up cost?**

- Dumbbell: `Share of sessions` and `Share of sign-ups` per `Channel Group` (Measure Values on Columns twice, dual axis: Circle with Measure Names on Color, Line with Measure Names on Path).
- Ranked bars: `Cost per sign-up` by `Campaign` from `ad_spend`, sorted descending.

Check: Paid Social 33.1% of sessions and 18.7% of sign-ups. TT_Spark_CashbackChallenge GHS 101.69; META_Retargeting_SiteVisitors GHS 5.08.

### Funnel Analysis

**Question: where do visitors drop out of the sign-up funnel, and for whom?**

- Funnel bars: `Sessions`, `SUM([Began Signup])`, `SUM([Otp Verified])`, `Sign-ups`.
- Grouped bars: `Begin rate`, `OTP rate`, `Completion rate` by `Device Category` (mobile and desktop; tablet is 3% of sessions).

Check: 31,167 → 5,506 → 3,628 → 2,426. Completion rate 60.6% on mobile, 85.1% on desktop.

### User Behavior

**Question: which landing pages turn a visit into a sign-up, and which lose the visitor at once?**

- Ranked bars: `Conversion rate` by `Landing Page`, with `Sessions` in the tooltip and `MIN([Site conversion rate])` as a reference line. Do not use Tableau's Average Line here: it averages the page rates, which is not the site's rate.
- Table: `Landing Page` × `Sessions`, `Bounce rate`, `Begin rate`, `Conversion rate`.
- Bars: `Conversion rate` by `Visitor type`.

Check: `/promo/cashback` 0.7% conversion and 73.9% bounce. Reference line at 7.8%. New 5.4%, Returning 12.7%.

### Drilldown

**Question: what is behind a number that looks wrong?**

- Line chart: `OTP rate` by `Week Start`, coloured by `Operating System`, filtered to `In Ghana` = True and to iOS and Android.
- Bars: `Selected metric` by `Selected dimension`, driven by the two parameters.
- Bars: `Conversion rate` by `Region`, filtered to `In Ghana` = True.

Check: iOS OTP rate 22.2% in the week of 18 May and 29.5% in the week of 25 May, against about 70% in every other week. Ashanti 10.6%, Greater Accra 7.7%.

## 4. Interactivity

- **One date filter for everything:** `Session Date` as a range, applied to all worksheets using the data source. Add it to context on the landing-page sheet so the `FIXED` reference line follows the dates.
- **Filter action:** selecting a channel in the dumbbell filters the session-based sheets (funnel, step rates, landing pages, visitor type, OTP rate, region, weekly lines) on `Channel Group`. The reference line stays at the site average, which is the point of it. Do not target the cost sheets.
- **Highlight action (optional):** useful only where the same dimension appears in two charts, such as Region in the region bars and in the parameter chart.
- **Tooltips:** every mark shows its numerator and denominator, not just the rate. "0.7% (22 of 3,283 sessions)" is harder to misread than "0.7%".

## 5. Before publishing

- Each KPI and each check value above matches.
- Selecting a channel moves the bars and leaves the reference line where it is.
- Each chart's title is the question it answers or the finding it shows.
- Save to Tableau Public. Anything published there is visible to anyone; this data is synthetic, so that is fine.
- Put the link and a screenshot in the project README, and save the image in this folder.
