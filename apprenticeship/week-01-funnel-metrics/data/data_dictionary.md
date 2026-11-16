<!-- markdownlint-disable MD013 -->
# Week 1 dataset: CediFlow, first quarter after launch

**CediFlow is a made-up Ghanaian mobile wallet** (top up, send money, pay bills, buy airtime, pay merchants, cash out). Every row here is synthetic and was generated for this apprenticeship; any resemblance to a real company is coincidental.

- **Period:** 1 January to 31 March 2026, exactly 90 days. CediFlow launched publicly on 1 January, so this is the whole business so far.
- **What is in the extract:** every user who signed up in that window and every transaction they attempted in it.
- **Currency:** Ghana cedis (GHS).
- **This data is clean on purpose.** No duplicate keys, no orphaned foreign keys, no malformed dates. Messy data is Week 2. An empty field in a CSV means NULL, and every NULL has a business meaning described below.

## Files

| File | Rows | One row is |
| --- | ---: | --- |
| `campaigns.csv` | 14 | a marketing campaign |
| `campaign_spend.csv` | 610 | one campaign on one day |
| `users.csv` | 15,051 | a person who signed up |
| `transactions.csv` | 90,310 | one transaction attempt |
| `cediflow_week1.db` | | the same four tables, already loaded into SQLite |

## How the tables connect

```text
campaigns ──< campaign_spend      one row per campaign per day of its run
campaigns ──< users               users.campaign_id      (NULL = organic)
users     ──< transactions        transactions.user_id
users     ──< users               users.referred_by_user_id -> the user who invited them
```

Check the grain of each table (what one row is) before you join anything.

## `campaigns`

| Column | Type | Meaning |
| --- | --- | --- |
| `campaign_id` | text, primary key | `C01` to `C14`, numbered in order of start date |
| `campaign_name` | text | The marketing team's naming convention is `PLATFORM_Type_Detail`. `GGL` = Google, `META` = Facebook and Instagram, `TT` = TikTok, `INF` = influencer partnerships, `REF` = the refer-a-friend programme |
| `channel` | text | `Google Ads`, `Meta Ads`, `TikTok Ads`, `Influencer` or `Referral` |
| `start_date`, `end_date` | date | First and last day the campaign ran, both inclusive |

## `campaign_spend`

One row for every day of every campaign's run, including days when nothing was spent.

| Column | Type | Meaning |
| --- | --- | --- |
| `spend_date` | date | The day |
| `campaign_id` | text, foreign key | Which campaign |
| `impressions` | integer | Times the ad or post was shown. For `Referral`: invites sent |
| `clicks` | integer | Clicks through to the sign-up page. For `Referral`: invite links opened |
| `spend_ghs` | numeric | Cost booked on that day |

Two kinds of campaign book their cost differently from ordinary ads:

- **Influencer** campaigns are paid as flat fees on the days a creator posts, so most days show `0.00` while clicks keep coming in.
- **Referral** spend is the bonus paid out when a referred person completes a first transaction. It is booked on the day that person signed up.

## `users`

| Column | Type | Meaning |
| --- | --- | --- |
| `user_id` | integer, primary key | Increases with sign-up date |
| `signup_date` | date | Day the account was created |
| `campaign_id` | text, foreign key, nullable | The campaign credited with the sign-up. **NULL = organic**: nobody paid for this user (app-store search, word of mouth, press) |
| `referred_by_user_id` | integer, foreign key to `users`, nullable | Filled only for people who joined through a `Referral` campaign: the existing user whose invite they used |
| `region` | text | One of eight regions of Ghana |
| `device_os` | text | `Android` or `iOS` |
| `age_band` | text | `18-24`, `25-34`, `35-44` or `45+` |
| `kyc_verified_date` | date, nullable | Day identity verification (KYC) was approved. **NULL = not verified** by 31 March. Nobody can transact before they are verified |

## `transactions`

One row per transaction a user started. Transfers a user *received* are not listed, so you cannot rebuild wallet balances from this table.

| Column | Type | Meaning |
| --- | --- | --- |
| `transaction_id` | integer, primary key | Increases with time |
| `user_id` | integer, foreign key | Who started it |
| `transaction_ts` | timestamp | `YYYY-MM-DD HH:MM:SS`, Ghana time (GMT) |
| `transaction_type` | text | `wallet_topup` (money into the wallet from a bank or mobile-money account), `p2p_transfer`, `bill_payment`, `airtime_purchase`, `merchant_payment`, `cash_out` |
| `amount_ghs` | numeric | Value of the transaction. This is the customer's money moving, **not** CediFlow's revenue |
| `fee_ghs` | numeric | What CediFlow earns on the transaction **if it completes**: a customer fee or a partner commission. Top-ups are free, so always `0.00` |
| `status` | text | `completed` = money moved and the fee was earned. `failed` = the attempt did not go through. `reversed` = it went through and was then refunded, fee included |

## Business rules

These definitions are the ones the Week 1 exercises and quiz are graded against.

1. **Revenue** is `fee_ghs` on `completed` transactions. `amount_ghs` is transaction volume, not revenue.
2. `fee_ghs` is filled in on `failed` and `reversed` rows too (it is the fee that applied), but that money was not earned.
3. A user is **active** in a period if they have at least one `completed` transaction in it.
4. A user is **activated** once they have their first `completed` transaction.
5. **Organic** means `campaign_id IS NULL`. No spend is attached to organic users.
6. Attribution is all-or-nothing: each paid user belongs to exactly one campaign, the last one they clicked.

## What this data cannot tell you

- It covers 90 days. People who signed up late in March have had little time to verify, transact or generate fees.
- The only cost in it is marketing spend. There is no cost of serving customers and no margin.
- It is synthetic. The patterns are realistic, but nothing here is a benchmark for a real company.

## Getting it into SQL

Use whichever engine you like. I grade the logic, not the dialect.

### Option A: PostgreSQL (best interview practice)

PostgreSQL 16 is already running on this machine. In a terminal, from this folder:

```powershell
powershell -ExecutionPolicy Bypass -File load_postgres.ps1
```

It asks for the password of your `postgres` user, creates a database called `analytics_apprenticeship` if there isn't one, and builds the schema `week01` inside it. It is safe to run again. Then connect your SQL client to:

| Host | Port | Database | User |
| --- | --- | --- | --- |
| `localhost` | `5432` | `analytics_apprenticeship` | `postgres` |

You can write `users` or `week01.users`; both work.

### Option B: SQLite (nothing to set up)

`cediflow_week1.db` is ready. In VS Code open the Command Palette (`Ctrl+Shift+P`), run **SQLite: Open Database** and pick the file, then **SQLite: New Query**. Two things differ from PostgreSQL:

- Dates are stored as text, so use `strftime('%Y-%m', signup_date)` where PostgreSQL uses `date_trunc` or `to_char`.
- The VS Code extension ships SQLite 3.26. Window functions work; `COUNT(*) FILTER (WHERE ...)` does not, so write `SUM(CASE WHEN ... THEN 1 ELSE 0 END)`.

If the `.db` file ever goes missing, `python build_sqlite.py` rebuilds it from the CSVs.

### After loading

Check the row counts match the table at the top of this page: 14, 610, 15,051 and 90,310.
