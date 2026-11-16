<!-- markdownlint-disable MD013 -->
# Week 1: Marketing Funnel & Metrics

> **2026-11-15: the answer files in this folder hold Claude's worked solutions, written at Ferdinard's request.** The week is not graded and has no score. The instructions below are left as they were, for anyone who wants to attempt the week before reading the solutions.

**By Sunday you can** take a marketing or product number (CAC, LTV, conversion, churn, ROI, ROAS, DAU/MAU), calculate it by hand, calculate it in SQL from raw tables, and say what it means for the business.

**Output this week:** manual and SQL metric calculations. No Tableau, no Python, no Week 2 material.

## Start here: Day 1 (about 90 minutes)

1. Read [1-concepts.md](1-concepts.md). 20 minutes.
2. Do the four exercises in [2-manual-calculations.md](2-manual-calculations.md) by hand. 20 minutes.
3. Write your answer to [3-business-scenario.md](3-business-scenario.md). 150 to 250 words, 30 to 40 minutes.
4. Tell me **"grade my Day 1"**. I mark both and flag any gaps in the concepts before you touch SQL.

Do not open the dataset until step 4 is done. The scenario is worth more if you write it before you have seen any data.

## The rest of the week

This follows the default week in Part 5 of the roadmap. Move the days around to suit your timetable; the order of the work is what matters.

| Day | Work | Time | File |
| --- | --- | --- | --- |
| Mon | Day 1, above | 1.5 hr | files 1, 2, 3 |
| Tue | Load the dataset, read the data dictionary, SQL Q1 and Q2 | 1 to 1.5 hr | [data/data_dictionary.md](data/data_dictionary.md), [4-sql-exercises.md](4-sql-exercises.md) |
| Wed | Benchmarks: find three real-world numbers to hold CediFlow against (details below) | 45 min | none |
| Thu | SQL Q3 and Q4. Q3 is the hard one | 1 to 1.5 hr | [4-sql-exercises.md](4-sql-exercises.md) |
| Fri | Rest, or university work | 0 | |
| Sat | Finish the SQL file: results pasted in, a "so what" line under each. Stretch questions if you have time | 2 hr | [sql/week1_queries.sql](sql/week1_queries.sql) |
| Sun | [5-diagnostic-quiz.md](5-diagnostic-quiz.md), then tell me **"grade week 1"** | 1 hr | file 5 |

**Wednesday's benchmarks.** Skim one industry benchmark source (the roadmap suggests the SaaStr or Bessemer "State of the Cloud" reports) and write down three numbers with where each came from: a typical LTV:CAC, a typical CAC payback period, and a typical churn rate. Most published benchmarks are for subscription software, not wallets, and noticing where they do not transfer is part of the exercise. Nothing to hand in; you will use them when you interpret your results.

**Thursday, optional, 15 minutes.** If you finish early, connect Tableau Public to `data/users.csv` and build one bar chart of sign-ups per month to confirm your Q1 answer by eye. Nothing to hand in. Tableau proper starts in Week 4.

## What you hand in

| Evidence | Where it lives |
| --- | --- |
| Manual calculations, with working | [2-manual-calculations.md](2-manual-calculations.md) |
| Business scenario answer, 150 to 250 words | [3-business-scenario.md](3-business-scenario.md) |
| Your four queries, their results, and a "so what" line for each | [sql/week1_queries.sql](sql/week1_queries.sql) |
| Quiz answers | [5-diagnostic-quiz.md](5-diagnostic-quiz.md) |

Type your answers into those files. I read them from there, write my marking into `grades.md` in this folder, and update [the progress tracker](../progress-tracker.md).

## How Week 1 is graded

| Piece | Points | What I look at |
| --- | ---: | --- |
| Manual calculations | 20 | Right answers, visible working, and the two "explain" parts |
| Business scenario | 20 | The questions you ask and why they matter; clear writing inside the word limit |
| SQL, four core queries | 30 | Correct results, sound logic, readable code |
| Diagnostic quiz | 30 | Ten questions, ten points each, scaled to 30 |
| **Total** | **100** | |

From those I report four of the roadmap's six weekly axes: Marketing Knowledge, SQL, Business Thinking and Communication. Statistics and Tableau are not assessed this week because Week 1 has no work in them.

The two stretch SQL questions carry no points. They tell me how fluent you are with window functions, which the roadmap says Week 1 should find out.

## Ground rules

- **Attempt first.** I will not give you a query, an answer or a hint that amounts to one before you have tried. When I grade, I explain what went wrong before I show my version.
- **Scores are not inflated.** A 60 means 60. The point is to find the gaps while they are cheap to fix.
- **The answer key is sealed.** It is in `apprenticeship/_instructor/`. Opening it before you submit only costs you the diagnostic.

## If the week goes badly

Part 15 of the roadmap applies from the start:

- **Busy university week (4 to 5 hours):** do files 1 and 2, SQL Q1 to Q3, and the quiz. Write the scenario as five bullet points. Skip Wednesday and the stretch questions.
- **Exam week (2 to 3 hours):** read the concepts and do the manual calculations. Everything else waits, with no penalty.

Tell me which kind of week it is and I will grade against that plan, not the full one.
