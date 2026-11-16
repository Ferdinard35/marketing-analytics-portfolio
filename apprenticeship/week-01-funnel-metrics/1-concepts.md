<!-- markdownlint-disable MD013 -->
# Week 1 concepts: the funnel and seven numbers

Read once, about 20 minutes. Then close the file and explain each idea out loud as if you were teaching a friend. The ones you stumble on are the ones to re-read.

The examples use **CediFlow**, a made-up Ghanaian mobile wallet (top up, send money, pay bills, buy airtime). It is the company in this week's dataset. The numbers in the examples are invented for this page and are not taken from the dataset.

## 1. AARRR: the funnel

AARRR splits a user's journey into five stages. Each stage has its own question and its own metric.

| Stage | The question | For a wallet like CediFlow | Typical metric |
| --- | --- | --- | --- |
| **Acquisition** | Did they show up? | Installs the app and creates an account | New sign-ups, CAC |
| **Activation** | Did they get the core value for the first time? | Verifies their identity and completes a first transaction | Activation rate = activated ÷ sign-ups, usually inside a time limit such as 7 days |
| **Retention** | Do they come back? | Transacts again next week or next month | Retention rate, churn rate |
| **Revenue** | Do we earn from them? | Pays fees on transfers, bills and cash-outs | Revenue per user, LTV |
| **Referral** | Do they bring others? | Invites a friend who signs up | Share of sign-ups that were referred |

Two things to hold on to:

- **Acquisition is not activation.** A sign-up who never transacts cost money and earns nothing. Signing up and passing identity checks are steps towards value; activation is the first moment the user actually receives it.
- The stages form a funnel, and every step loses people. The biggest leak tells you what to fix first.

The framework is Dave McClure's "pirate metrics" from 2007. The name comes from saying the letters out loud.

## 2. CAC: customer acquisition cost

**CAC = acquisition spend ÷ new customers acquired**, both measured over the same period.

*Example.* CediFlow spends GHS 36,000 on Meta ads in a month and 1,500 people sign up from them. CAC = 36,000 ÷ 1,500 = **GHS 24**.

Three questions decide what a CAC figure really means:

1. **Who is in the denominator?** Suppose 600 other people signed up that month without seeing an ad. *Paid CAC* is still 36,000 ÷ 1,500 = GHS 24, but *blended CAC* is 36,000 ÷ 2,100 = GHS 17.14. Blended looks better, and it improves whenever organic sign-ups grow, even if the ads themselves are getting worse.
2. **What counts as "acquired"?** If only 900 of the 1,500 ever transact, the *cost per activated customer* is 36,000 ÷ 900 = GHS 40. Same spend, same campaign, a much less comfortable number.
3. **What is in the spend?** Media cost only, or also agency fees, sign-up bonuses and the growth team's salaries (called "fully loaded" CAC)? Know which one you were handed.

## 3. Conversion rate

**Conversion rate = people who took the next step ÷ people who could have.**

The number means nothing until both ends are named: conversion from *what* to *what*? Click to sign-up, sign-up to verified, and verified to first transaction are three different rates.

*Example.* 40,000 ad clicks lead to 1,500 sign-ups, of whom 900 activate.

- Click to sign-up = 1,500 ÷ 40,000 = 3.75%
- Sign-up to activation = 900 ÷ 1,500 = 60%
- Click to activation = 900 ÷ 40,000 = 2.25%, which is 3.75% × 60%. Step rates multiply.

## 4. Churn and retention

Both start from a fixed group: the customers you had at the start of the period.

- **Churn rate = customers from that group lost during the period ÷ customers in the group at the start**
- **Retention rate = customers from that group still there ÷ customers in the group at the start**, which is 1 − churn

*Example.* 4,000 users were active in May, and 3,400 of them were active again in June. Retention = 3,400 ÷ 4,000 = 85%. Churn = 600 ÷ 4,000 = 15%.

- People who joined *during* June are in neither number. If June had 4,900 active users in total, the base grew, and 15% of May's users still left. Growth can hide churn.
- A wallet has no "cancel" button, so "lost" has to be defined. This week: **active** means at least one completed transaction in the month, and **churned** means active last month and not active this month.
- **Lifespan ≈ 1 ÷ churn rate.** At 15% monthly churn the average customer lasts about 1 ÷ 0.15 ≈ 6.7 months. The shortcut assumes churn stays constant, and it rarely does: brand-new users leave much faster than established ones.

## 5. LTV: lifetime value

**LTV = average revenue per customer per period × average customer lifespan.**

The margin-adjusted version multiplies by gross margin, so it counts only what is left after the direct cost of serving the customer.

*Example.* An active CediFlow customer generates GHS 9 in fees a month and stays for 10 months. LTV = 9 × 10 = **GHS 90** of revenue. At a 40% gross margin, that is GHS 36 of gross profit.

**LTV:CAC** puts the two numbers side by side. With an LTV of GHS 90 and a CAC of GHS 24, LTV:CAC = 3.75:1. The usual rule of thumb, which comes from subscription software, is that **3:1 or better is healthy**. The reason the rule asks for 3 and not 1 lies in three facts about LTV: it is normally counted in revenue and not profit, it arrives slowly over the customer's whole life while CAC is paid on day one, and it is a forecast that can be wrong. Manual exercise 2 asks you to turn those facts into an argument.

A companion number is the **payback period = CAC ÷ monthly revenue (or margin) per customer**. Here that is GHS 24 ÷ GHS 9 ≈ 2.7 months to earn the acquisition cost back.

Make sure LTV and CAC describe the same people. LTV per *active customer* set against CAC per *sign-up* flatters the ratio; use cost per activated customer.

## 6. ROI and ROAS

- **ROAS = revenue ÷ ad spend.** It is a multiple, and nothing is subtracted.
- **ROI = (revenue − cost) ÷ cost.** It is a percentage, and the cost comes off first.

*Example.* A campaign costs GHS 8,000 and brings in GHS 20,000 of revenue. ROAS = 20,000 ÷ 8,000 = 2.5. ROI = (20,000 − 8,000) ÷ 8,000 = 150%.

- When the only cost is the ad spend, **ROI = ROAS − 1**. A ROAS of 1.0 is an ROI of 0%: you got your money back and nothing more. Below 1.0, ROI is negative.
- Neither one is profit, because revenue is not profit. If the gross margin is 40%, that GHS 20,000 leaves GHS 8,000 of gross profit, which is exactly the ad spend, so the campaign only broke even. In general, **break-even ROAS = 1 ÷ gross margin**. Here that is 1 ÷ 0.40 = 2.5.
- In fintech, check what "revenue" means. A customer who sends GHS 1,000 through CediFlow and pays a GHS 10 fee has produced GHS 10 of revenue. The GHS 1,000 is transaction volume.

## 7. Engagement: DAU/MAU

**DAU/MAU = average daily active users ÷ monthly active users.**

*Example.* On an average day of a 30-day month, 1,200 users transact. Over the whole month, 8,000 different users do. DAU/MAU = 1,200 ÷ 8,000 = 15%. Put another way, the average active user shows up on 0.15 × 30 = 4.5 days of the month.

The ratio measures habit, so the right level depends on the product. A chat app can pass 50%. A wallet that people open for bills and transfers a few times a month can be healthy far below that. Compare the ratio with the product's own trend and with what the use case implies. "Active" needs a definition here too. Session frequency, meaning how often a user opens the app, is the same idea measured on app opens.

## Five traps that come up in interviews

1. **ROAS is not ROI, and neither is profit.** Ask for the margin.
2. **Volume is not revenue.** In payments, revenue is the fee.
3. **Every rate has a denominator.** "Conversion is up" and "CAC is down" mean nothing until you know who was counted.
4. **Averages hide mix.** A total can improve because the mix shifted towards a cheaper or weaker group while no individual group improved at all.
5. **New customers have had less time.** Comparing revenue from people who joined three months ago with people who joined last week measures time, not quality.
