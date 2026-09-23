---
name: log-work
description: Write the end-of-day changelog entry - one entry per person per day, what landed, what teammates must run after pulling. Use when wrapping up a working session.
---

# /log-work

Write one entry at the top of [changelog.md](../../../docs/changelog.md). One entry **per person per day**, not per session or per task - a second session the same day adds bullets to that day's entry rather than a new block.

## Gather

- `git log --oneline --author="$(git config user.name)" --since=midnight`
- Which rubric rows moved, and to what status.
- Anything a teammate must do after pulling.

## Preview, then write

**Show the entry exactly as it will appear and write nothing until it is approved.** Ending a session without approval writes nothing; the work lives in the commits.

## Format

```
2026-09-24 17:40 MDT
Aden

## Enrollment list and the GPA on the page

- Implemented list_enrollments against current_user.enrollments, with the empty state (rubric: List of Enrollments -> done)
- calculate_gpa now weights by credit hours; verified 3-credit A + 1-credit F = 3.00 by hand (rubric: GPA calculation -> in progress, not yet wired to the published package)

Heads up:
- Model change - delete src/instance/prj1.db and re-run `python init_db.py` after pulling.
- `pip install -r requirements.txt` - added the published gpa_calculator.
```

In order: a date line from `date "+%Y-%m-%d %H:%M %Z"`, the person, a `##` title summarizing the day, one bullet per piece of work with its rubric effect in parentheses, and a **`Heads up:`** block that is always present.

Common heads-ups, and the one that matters most:

- **`rm src/instance/prj1.db && python init_db.py`** after any model change. There are no migrations; a teammate who pulls without this hits a confusing error.
- `pip install -r requirements.txt` when dependencies moved.
- A rebuild of the Docker image when the Dockerfile changed.

When there is nothing: `Heads up: nothing to run - pull and go.`

Insert at the top, under the file header, above the newest existing entry. Never rewrite the file.
