<!-- markdownlint-disable MD013 -->
# Week 1: diagnostic quiz

> **Worked solutions, written by Claude on 2026-11-15 at Ferdinard's request.** These are not a graded attempt and carry no score. The arithmetic in Part B was run in a script, not done from memory.

Ten questions, ten points each. Take it **last**, after the SQL exercises.

- **Time:** 45 to 60 minutes in one sitting.
- **Closed notes.** Do not open the concepts file, your SQL results or the dataset. A calculator is fine.
- **Show your working** on the calculation questions. A wrong answer with the right method earns most of the marks; a bare number earns few.
- Round money to 2 decimal places and percentages to 1.
- Type your answers under each question, then tell me **"grade week 1"**.

Questions 5 to 10 use real figures from the Week 1 dataset. "Active" and "revenue" mean what the data dictionary says they mean: at least one completed transaction, and fees on completed transactions.

## Part A: concepts

### Q1

Define activation in the AARRR framework, and give a fintech example for a product that is **not** a mobile wallet (a savings, lending or investing app, for instance).

**Answer:**

Activation is the first time a new user gets the product's core value. It is defined as one specific, measurable action, usually inside a time limit after sign-up, and it sits between acquisition (they arrived) and retention (they came back).

Example: for a savings app, a user is activated when they make their first deposit into a savings goal within 7 days of signing up. Creating the account, passing KYC or linking a bank account are setup steps on the way there; none of them is the value the product exists to deliver.

### Q2

If LTV:CAC = 1.2:1, is the business sustainable? Why, or why not?

**Answer:**

Not as it stands. For every GHS 1 spent acquiring a customer, the business eventually gets GHS 1.20 back, and that is not enough for four reasons:

- LTV is usually revenue. After the cost of serving the customer, GHS 1.20 of revenue is less than GHS 1 of profit, so each customer loses money.
- The 20 pesewas left over has to cover salaries, technology and compliance. It cannot.
- CAC is paid up front and LTV arrives slowly, so payback takes nearly the customer's whole life. Growing faster burns cash faster.
- LTV is a forecast. A 20% cushion disappears if customers leave slightly sooner than predicted.

It can be tolerable for a while in three cases: the LTV is already margin-based and conservative, the cohorts are young and their LTV is still rising, or the company is deliberately buying market share with investors' money and knows when that stops.

### Q3

What is the difference between churn rate and retention rate?

**Answer:**

They describe the same group from opposite sides. Take the customers you had at the start of a period: churn rate is the share of them you lost during it, retention rate is the share still there at the end. Measured on the same group over the same period they add up to 100%.

Three conditions matter. The denominator is customers at the start, so people who joined during the period are in neither number. "Lost" needs a definition when there is no cancel button (for a wallet: no completed transaction in the month). And the two stop being complements if they are measured on different groups or different periods.

### Q4

A campaign reports a ROAS of 4.0. Good or bad? Assume the business has a 15% gross margin and show the numbers behind your answer: the profit or loss on each GHS 1 of ad spend, and the ROAS at which the campaign would break even.

**Answer:**

It depends on the margin, and at 15% it is bad.

- Per GHS 1.00 of ad spend, revenue = GHS 4.00.
- Gross profit = 4.00 × 0.15 = GHS 0.60.
- After the GHS 1.00 of ad spend: 0.60 − 1.00 = **a loss of GHS 0.40 on every GHS 1 spent**.
- Break-even ROAS = 1 ÷ gross margin = 1 ÷ 0.15 = **6.67**.

So a ROAS of 4.0 loses money here. The same 4.0 at a 50% margin would be comfortably profitable, because break-even would be 2.0.

## Part B: calculations from the dataset

### Q5. Blended and paid CAC

Across its first quarter CediFlow spent **GHS 256,520.45** on marketing. **15,051** people signed up, and **3,297** of them came organically, with no campaign.

1. Blended CAC?
2. Paid CAC?
3. In one or two sentences: why do the two differ, and which would you show an investor who asks "what does a new user cost you?"

**Answer:**

1. Blended CAC = 256,520.45 ÷ 15,051 = **GHS 17.04**.
2. Paid users = 15,051 − 3,297 = 11,754. Paid CAC = 256,520.45 ÷ 11,754 = **GHS 21.82**.
3. Blended spreads the spend over 3,297 users nobody paid for, so it flatters the marketing and improves whenever organic sign-ups grow. I would show the investor both, labelled; if they want only one, paid CAC answers the question they are really asking, which is what buying the next user costs.

### Q6. From clicks to customers

Two campaigns:

| | TT_Spark_CashbackChallenge (TikTok) | META_Lookalike_HighValue (Meta) |
| --- | ---: | ---: |
| Spend (GHS) | 13,900.62 | 31,660.96 |
| Clicks | 32,020 | 29,695 |
| Sign-ups | 1,492 | 1,206 |
| Activated users | 522 | 733 |

1. For each campaign calculate the click-to-sign-up conversion rate, the CAC, the activation rate and the cost per activated user.
2. TikTok's CAC is roughly a third of Meta's. How much of that advantage is left when you measure cost per activated user instead? What does that say about judging a campaign on CAC alone?

**Answer:**

| | TikTok | Meta |
| --- | ---: | ---: |
| Click-to-sign-up = sign-ups ÷ clicks | 1,492 ÷ 32,020 = **4.7%** | 1,206 ÷ 29,695 = **4.1%** |
| CAC = spend ÷ sign-ups | 13,900.62 ÷ 1,492 = **GHS 9.32** | 31,660.96 ÷ 1,206 = **GHS 26.25** |
| Activation rate = activated ÷ sign-ups | 522 ÷ 1,492 = **35.0%** | 733 ÷ 1,206 = **60.8%** |
| Cost per activated user = spend ÷ activated | 13,900.62 ÷ 522 = **GHS 26.63** | 31,660.96 ÷ 733 = **GHS 43.19** |

On CAC, Meta costs 2.82 times as much as TikTok (TikTok is 64.5% cheaper). On cost per activated user, Meta costs only 1.62 times as much (TikTok is 38.3% cheaper). So roughly 40% of TikTok's apparent advantage disappears one step down the funnel.

CAC counts every sign-up, including the ones who never transact, so it favours campaigns that attract people who sign up and leave. A campaign has to be judged at a stage where the user has shown value, and in the end on the revenue those users bring.

### Q7. Churn and retention by channel

| | Google Ads | TikTok Ads |
| --- | ---: | ---: |
| Users active in February | 1,046 | 154 |
| ...of whom were also active in March | 741 | 50 |

1. February-to-March churn rate and retention rate for each channel.
2. If each churn rate stayed constant, what average customer lifespan in months would it imply?

**Answer:**

| | Google Ads | TikTok Ads |
| --- | ---: | ---: |
| Churned = February actives − still active | 1,046 − 741 = 305 | 154 − 50 = 104 |
| Churn rate | 305 ÷ 1,046 = **29.2%** | 104 ÷ 154 = **67.5%** |
| Retention rate | 741 ÷ 1,046 = **70.8%** | 50 ÷ 154 = **32.5%** |
| Lifespan = 1 ÷ churn | 1 ÷ 0.2916 = **3.4 months** | 1 ÷ 0.6753 = **1.5 months** |

### Q8. ROI and ROAS

Spend over the quarter, and the fee revenue earned so far from the users each channel acquired:

| | Google Ads | Meta Ads |
| --- | ---: | ---: |
| Spend (GHS) | 96,196.62 | 69,797.86 |
| Fee revenue to date (GHS) | 39,605.49 | 24,666.72 |

1. ROAS and ROI for each channel.
2. Both ROIs are negative. Does that mean CediFlow should stop both channels? Name the one extra piece of information that would settle it.

**Answer:**

| | Google Ads | Meta Ads |
| --- | ---: | ---: |
| ROAS = revenue ÷ spend | 39,605.49 ÷ 96,196.62 = **0.41** | 24,666.72 ÷ 69,797.86 = **0.35** |
| ROI = (revenue − spend) ÷ spend | −56,591.13 ÷ 96,196.62 = **−58.8%** | −45,131.14 ÷ 69,797.86 = **−64.7%** |

No. The spend was all paid up front, but the revenue covers at most 90 days of customers who may go on paying fees for much longer; someone acquired in March has had under a month. What settles it is the **expected lifetime value of the users each channel brings** (the same thing seen another way: the payback period, or the retention curve), set against the margin.

### Q9. LTV:CAC by channel

Use the lifespans you calculated in Q7.

| | Google Ads | TikTok Ads |
| --- | ---: | ---: |
| CAC per sign-up (GHS) | 29.15 | 8.64 |
| Cost per activated customer (GHS) | 45.57 | 26.58 |
| Fee revenue per active customer in March (GHS) | 14.71 | 1.80 |

1. LTV per active customer for each channel, treating March's figure as the monthly revenue.
2. LTV:CAC for each, using cost per activated customer.
3. TikTok's CAC per sign-up is less than a third of Google's. Which channel should get the next GHS 10,000, and why?
4. Give one reason these LTV figures could be badly wrong for a business that is 90 days old.

**Answer:**

Using the unrounded lifespans from Q7 (3.43 and 1.48 months):

| | Google Ads | TikTok Ads |
| --- | ---: | ---: |
| LTV = monthly revenue × lifespan | 14.71 × 3.43 = **GHS 50.45** | 1.80 × 1.48 = **GHS 2.67** |
| LTV:CAC = LTV ÷ cost per activated customer | 50.45 ÷ 45.57 = **1.11** | 2.67 ÷ 26.58 = **0.10** |

(With the lifespans rounded to 3.4 and 1.5 the LTVs come out at GHS 50.01 and GHS 2.70; the ratios do not change.)

**Part 3.** Google. Each cedi of acquisition cost there buys about eleven times the lifetime value it buys on TikTok (1.11 against 0.10). TikTok is cheap per sign-up because most of its sign-ups never transact, and the ones who do pay almost nothing in fees. But Google at 1.11:1 is still far short of 3:1, so the answer is "Google before TikTok", not "pour money into Google".

**Part 4.** The churn rate comes from a single pair of months, measured on users who are all new. New users leave much faster than established ones, so 1 ÷ churn understates how long the survivors will stay, and the LTVs with it. (Also valid: revenue per customer is taken from one month; only 154 TikTok users are in the sample; it is revenue, not margin.)

### Q10. Engagement

In March, **6,601** different users made at least one completed transaction. On an average day in March, **1,177** different users did.

1. DAU/MAU?
2. On roughly how many days of March did the average active user transact?
3. Is that healthy for a payments wallet? Say what you would compare it against before deciding.

**Answer:**

1. DAU/MAU = 1,177 ÷ 6,601 = **17.8%**.
2. 0.178 × 31 days ≈ **5.5 days** of the month.
3. It is believable for a wallet. Paying bills, buying airtime and sending money are things people do a few times a month, not every day, so a figure well below a chat app's is expected. Before calling it healthy I would compare it with three things: the product's own trend (monthly actives grew from 1,999 to 3,476 to 6,601, so is the ratio rising with them?), the frequency the use cases imply (how often does a typical customer need to top up, pay a bill or send money?), and the split by cohort and channel, because users who activated late in March pull the ratio down without being less engaged.
