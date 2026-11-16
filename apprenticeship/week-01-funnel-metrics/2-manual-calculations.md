<!-- markdownlint-disable MD013 -->
# Week 1: manual calculations

> **Worked solutions, written by Claude on 2026-11-15 at Ferdinard's request.** These are not a graded attempt and carry no score.

**By hand.** Paper and a basic calculator, no spreadsheet. About 20 minutes.

For each exercise write the formula, the numbers you put into it, and the answer with its unit. Then type your working under the exercise (or send me a photo of the page). Do these before you open the dataset.

## 1. CAC

A fintech app spent GHS 50,000 on Google Ads and acquired 2,000 new users last month. What's CAC?

**Working:**

CAC = acquisition spend ÷ new customers acquired, over the same period

= GHS 50,000 ÷ 2,000 users

= **GHS 25 per new user**

This is a paid CAC for one channel: only Google's spend and only the users Google brought.

## 2. LTV and LTV:CAC

The average customer generates GHS 15/month in fees and stays active for 18 months on average.

1. What's LTV?
2. Using the CAC from exercise 1, is LTV:CAC healthy? (Rule of thumb: LTV:CAC ≥ 3:1 is healthy.)
3. Explain why 1:1 is a problem even though it looks "profitable".

**Working:**

1. LTV = average revenue per customer per month × average lifespan in months = GHS 15 × 18 = **GHS 270 of fee revenue per customer**.
2. LTV:CAC = 270 ÷ 25 = **10.8:1**. That is well above 3:1, so on these numbers it is healthy. Payback is 25 ÷ 15 ≈ 1.7 months. A ratio this high is also a prompt to check two things: whether the 18-month lifespan is a measurement or a hope, and whether the company is spending too little on growth.
3. At 1:1 the company gets back GHS 1 of revenue for every GHS 1 it spends on acquisition. That only looks like breaking even:
   - **Revenue is not profit.** The GHS 1 that comes back still has to pay for serving the customer (payment partner fees, support, fraud losses). After those costs each customer is a loss.
   - **The timing is wrong.** CAC is paid on day one and LTV arrives over 18 months. At 1:1 the cash is tied up for the customer's whole life, so the faster the company grows, the faster it runs out of money.
   - **Nothing is left over** for salaries, technology and compliance.
   - **LTV is a forecast.** If customers leave a little earlier than expected, 1:1 becomes less than 1:1 with no cushion.

## 3. Churn

A SaaS product had 1,200 customers at the start of March and lost 84 by the end of March. Churn rate?

**Working:**

Churn rate = customers lost in the period ÷ customers at the start of the period

= 84 ÷ 1,200

= **7.0% for the month**

Retention is the other side of the same group: 1,116 ÷ 1,200 = 93.0%. It is a monthly rate, and it compounds: the implied lifespan is 1 ÷ 0.07 ≈ 14.3 months, and after a year only 0.93¹² ≈ 42% of the starting customers would be left.

## 4. ROI and ROAS

Two campaigns. Campaign A spent GHS 10,000 and generated GHS 35,000 revenue. Campaign B spent GHS 3,000 and generated GHS 9,500.

1. Calculate ROI and ROAS for both.
2. Which is "better"?
3. Why does the answer depend on what the business is optimizing for (efficiency vs. absolute revenue)?

**Working:**

ROAS = revenue ÷ spend. ROI = (revenue − spend) ÷ spend.

| | Spend (GHS) | Revenue (GHS) | ROAS | ROI | Net return (GHS) |
| --- | ---: | ---: | ---: | ---: | ---: |
| Campaign A | 10,000 | 35,000 | 35,000 ÷ 10,000 = **3.50** | 25,000 ÷ 10,000 = **250.0%** | 25,000 |
| Campaign B | 3,000 | 9,500 | 9,500 ÷ 3,000 = **3.17** | 6,500 ÷ 3,000 = **216.7%** | 6,500 |

1. A: ROAS 3.50, ROI 250.0%. B: ROAS 3.17, ROI 216.7%.
2. **A is better on every measure here.** It has the higher ROAS, the higher ROI, more revenue and more net return. The question hints at a trade-off between efficiency and size, but these numbers do not contain one: A is both the more efficient campaign and the bigger one.
3. The "it depends" only becomes real for the *next* cedi, not the ones already spent:
   - A's 3.5 is an average. The next GHS 1,000 put into A may earn less if A is running out of cheap audience, so a business optimizing for efficiency would want A's marginal return, not its average.
   - A business chasing absolute revenue would ask whether B can take more budget at close to 3.17, because that adds revenue even if it is the less efficient campaign.
   - Neither figure is profit. If the two campaigns sell products with different margins, the ranking could flip.
   - A trade-off would exist if, say, B had returned GHS 12,000: ROAS 4.0 and ROI 300% against A's 3.5 and 250%, while A still brought in more net return (25,000 against 9,000). Then efficiency would say B and absolute return would say A.

## When you're done

Go on to [3-business-scenario.md](3-business-scenario.md). When both are filled in, tell me **"grade my Day 1"**.
