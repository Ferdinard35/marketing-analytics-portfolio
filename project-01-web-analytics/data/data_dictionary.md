<!-- markdownlint-disable MD013 -->
# Data dictionary: CediFlow web analytics

**CediFlow is a made-up Ghanaian mobile wallet.** Every row here is synthetic, produced by a seeded generator for this project. The data is built to behave like a real GA4 export, faults included, but none of the figures describe a real company.

- **Period:** Monday 30 March to Sunday 28 June 2026, 13 full weeks.
- **Scope:** the public website and its sign-up form. What happens after sign-up (identity checks, first transaction) is not in this data.
- **Time zone:** Ghana is on GMT all year, so the UTC timestamps are local time.
- **Currency:** Ghana cedis (GHS).

## Files

| File | Rows | One row is |
| --- | ---: | --- |
| `raw/ga4_events_raw.csv` | 123,435 | one event, as exported |
| `raw/ad_spend_raw.csv` | 671 | one campaign on one day, as exported from the ad platforms |
| `cleaned/sessions.csv` | 31,167 | one session by a real visitor |
| `cleaned/ad_spend.csv` | 665 | one campaign on one day, de-duplicated |
| `cleaned/cleaning_log.json` | | counts for every cleaning step below |
| `cediflow_web.db` | | SQLite database with `events` (115,859 cleaned rows), `sessions` and `ad_spend`. Built by `python/01_clean_and_model.py`; not committed because of its size |

```text
events   >── sessions      events.session_key = sessions.session_key
sessions >── ad_spend      sessions.campaign = ad_spend.campaign, and sessions.session_date = ad_spend.date
```

`sessions` and `ad_spend` have different grains (a session against a campaign-day). Sum each to the level you need before joining them, or every session is repeated once per spend row.

## `raw/ga4_events_raw.csv`

Column names follow GA4's BigQuery export, flattened to one row per event.

| Column | Type | Meaning |
| --- | --- | --- |
| `event_date` | date | Day of the event |
| `event_timestamp` | integer | Microseconds since 1970-01-01 UTC |
| `event_name` | text | `session_start`, `page_view`, `begin_sign_up`, `otp_verified` or `sign_up` |
| `user_pseudo_id` | text | The browser's client ID. Treat it as an opaque label: one per browser, not per person |
| `ga_session_id` | integer | The second the session started. **Not unique on its own**: two visitors who arrive in the same second share it |
| `ga_session_number` | integer | 1 for a visitor's first ever session, 2 for the next, and so on |
| `page_path` | text | Page the event happened on |
| `source`, `medium`, `campaign` | text | Where the session came from, from the UTM tags on the link. `campaign` is empty when there was none |
| `device_category` | text | `mobile`, `desktop` or `tablet` |
| `operating_system`, `browser` | text | As reported by the browser |
| `country`, `region`, `city` | text | From the IP address. `(not set)` where GA4 could not place it |
| `engagement_time_msec` | integer | On `page_view` rows: milliseconds the page was in focus. Empty when there was none |
| `traffic_type` | text | `internal` for traffic from CediFlow's own office, otherwise empty |

### The sign-up funnel

| Step | Event | What the visitor did |
| --- | --- | --- |
| 1 | `session_start` | Arrived on the site |
| 2 | `begin_sign_up` | Entered a phone number on `/signup` |
| 3 | `otp_verified` | Typed in the code sent by SMS. Needs a Ghanaian number |
| 4 | `sign_up` | Completed the details form on `/signup/details` |

## `raw/ad_spend_raw.csv`

| Column | Type | Meaning |
| --- | --- | --- |
| `date` | date | Day |
| `platform` | text | `Google Ads`, `Meta Ads` or `TikTok Ads` |
| `campaign_name` | text | The campaign, as named in the ad platform |
| `impressions`, `clicks` | integer | As reported by the platform |
| `cost_ghs` | numeric | Media cost for the day |

## `cleaned/sessions.csv`

| Column | Type | Meaning |
| --- | --- | --- |
| `session_key` | text, unique | `user_pseudo_id` + `-` + `ga_session_id` |
| `user_pseudo_id` | text | Client ID |
| `session_number` | integer | `ga_session_number` |
| `is_new_user` | 0/1 | 1 when `session_number` is 1 |
| `session_start` | timestamp | `YYYY-MM-DD HH:MM:SS`, time of the first event |
| `session_date` | date | Date of `session_start` |
| `week_start` | date | The Monday of that week |
| `hour` | integer | Hour of `session_start`, 0 to 23 |
| `channel_group` | text | GA4's default channel grouping: `Paid Search`, `Paid Social`, `Organic Search`, `Organic Social`, `Direct`, `Email` or `Referral` |
| `source`, `medium` | text | Standardised labels |
| `campaign` | text | Standardised name. `(none)` where no campaign applies; `(unattributed)` for a paid click that arrived without a campaign tag |
| `landing_page` | text | `page_path` of the session's first `page_view` |
| `device_category`, `operating_system`, `browser` | text | From the session's first event |
| `country`, `region`, `city` | text | From the session's first event |
| `pageviews` | integer | Number of `page_view` events |
| `engagement_time_sec` | numeric | Total engagement time, to one decimal |
| `engaged_session` | 0/1 | GA4's definition: 10 seconds or more of engagement, or 2 or more page views, or a sign-up |
| `began_signup`, `otp_verified`, `signed_up` | 0/1 | Whether the session reached each funnel step |

## `cleaned/ad_spend.csv`

`date`, `week_start`, `platform`, `channel_group` (`Paid Search` for Google Ads, `Paid Social` for Meta and TikTok), `campaign`, `impressions`, `clicks`, `cost_ghs`. One row per campaign per day.

## What was wrong with the raw data, and what was done

Each rule is applied in `python/01_clean_and_model.py`, in this order. The counts are from `cleaned/cleaning_log.json`.

| # | Problem | How it shows up | Rule | Effect |
| --- | --- | --- | --- | --- |
| 1 | Events fired twice | Rows identical in every column | Keep one | 1,818 rows removed, 36 of them `sign_up` events |
| 2 | Events with no session | `ga_session_id` empty | Drop: they cannot be assigned to a session | 400 rows removed, all `page_view` |
| 3 | Session id shared between visitors | 33,267 distinct `ga_session_id` but 33,369 distinct visitor-and-id pairs | Key sessions on `user_pseudo_id` + `ga_session_id` | 102 sessions that would otherwise have been merged into another visitor's |
| 4 | Inconsistent traffic labels | `fb`, `Facebook`, `facebook.com`; `ppc`, `CPC`; `paidsocial`, `paid-social`; campaign names in lower case or with a trailing space | Lower-case and trim, then map each variant to one standard label | Distinct values: source 20 to 12, medium 14 to 7, campaign 31 to 11 |
| 5 | Paid clicks with no campaign tag | `campaign` empty on a paid medium | Keep in the channel, label the campaign `(unattributed)` | 406 sessions (2.6% of paid sessions) carrying 25 sign-ups |
| 6 | Staff testing the sign-up form | `traffic_type = internal` | Remove the sessions | 221 sessions and **123 sign-ups** that were never customers |
| 7 | A scanner bot | United States, Ashburn, Linux desktop, one page, zero engagement; 65% of these sessions asked for pages that do not exist (`/wp-login.php`, `/.env`, `/admin`, `/xmlrpc.php`) | Remove sessions matching that signature | 973 sessions |
| 8 | An uptime monitor | One client ID with 48 sessions a day for 21 days, every one a single view of `/` | Remove every session from any client with more than 20 sessions in one day | 1,008 sessions from 1 client |
| 9 | Unknown geography | `region` and `city` are `(not set)` | Keep, and report as `(not set)` | 1,143 sessions (3.7%) |
| 10 | Cost rows exported twice | Rows identical in every column | Keep one | 6 rows removed; spend GHS 22,457.27 corrected to GHS 22,218.16 |

**Why it matters.** Counting `sign_up` events in the raw file gives 2,585; the real figure is 2,426, so the raw count is 6.6% too high. The two bots and the QA traffic were all recorded as Direct: removing them takes Direct from 7,436 sessions converting at 10.95% to 5,234 sessions converting at 13.20%.

## Metric definitions

| Metric | Definition |
| --- | --- |
| Sessions | Rows in `sessions` |
| Sign-ups | Sessions with `signed_up = 1` |
| Conversion rate | Sign-ups ÷ sessions |
| Begin rate | Sessions that started the form ÷ sessions |
| OTP rate | Sessions that verified their phone ÷ sessions that started the form |
| Completion rate | Sign-ups ÷ sessions that verified their phone |
| Bounce rate | 1 − engaged sessions ÷ sessions |
| Cost per sign-up | Ad cost ÷ sign-ups from sessions attributed to the same campaign or channel |

Attribution is last-click: a sign-up is credited to the source of the session in which it happened.

## What this data cannot tell you

- **Whether a sign-up became a customer.** There is no transaction or revenue data, so cost per sign-up is the deepest measure available.
- **Why visitors leave a step.** The export has step events, not field-level form events or error messages.
- **What a visitor did on earlier visits from other devices.** The ID is per browser.
- **What ads cost by country.** Spend is by campaign and day only.
