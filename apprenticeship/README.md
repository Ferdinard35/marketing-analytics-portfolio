<!-- markdownlint-disable MD013 -->
# Apprenticeship workspace

The working area for the 12-week Marketing & Product Analytics apprenticeship. The three `project-*` folders one level up are the portfolio a recruiter sees; this folder is where the learning happens.

| File or folder | What it is |
| --- | --- |
| [roadmap.md](roadmap.md) | The full plan, copied from `analytics-apprenticeship-system.docx` so it reads in VS Code |
| [progress-tracker.md](progress-tracker.md) | Skill statuses, mastery gates and weekly scores, updated at every grading |
| [week-01-funnel-metrics/](week-01-funnel-metrics/README.md) | Week 1. Its answer files hold Claude's worked solutions (2026-11-15), not a graded attempt |
| `_instructor/` | Answer keys and dataset generators. Sealed for any week that has not been graded; Week 1's is open |

## How a week runs

1. **You say "start week N".** Claude builds that week's packet: concepts, exercises, dataset, SQL set and quiz, pitched at how the previous week went.
2. **You do the work** in the week's folder, attempting everything before asking for help.
3. **You say "grade week N"** (or "grade my Day 1" part-way through Week 1). Claude marks it against the sealed key, explains what went wrong before showing its own answers, writes `grades.md` in the week's folder and updates the tracker.
4. The results shape the next packet.

Other things you can say at any point:

- **"busy week"** or **"exam week"**: the week is cut down as Part 15 of the roadmap describes, and graded against the smaller plan.
- **"I missed week N"**: Claude writes a one-week recovery plan that fits inside the normal 8 to 10 hours. Optional material is dropped for good, not carried forward.
- **"explain X"**: for a concept, at any time. For an exercise you have not attempted yet, you get a pointer to the relevant concept, not the answer.

## Where the roadmap's parts ended up

| Roadmap part | Lives in |
| --- | --- |
| Part 4, Week 1 in full | [week-01-funnel-metrics/](week-01-funnel-metrics/README.md) |
| Part 6, glossary | Each week's concepts file, starting with [Week 1's](week-01-funnel-metrics/1-concepts.md) |
| Part 14, tracker | [progress-tracker.md](progress-tracker.md) |
| Part 16, portfolio structure | The repository root |
| Everything else | [roadmap.md](roadmap.md), built into packets week by week |
