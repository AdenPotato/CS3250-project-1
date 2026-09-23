---
name: test-log
description: Record manual test results in the graded test table - add rows with real timestamps, keep failures, and check coverage against the five requirements. Use after a session of clicking through the app.
---

# /test-log

Add rows to [test_log.md](../../../docs/testing/test_log.md). This table is the Testing rubric deliverable, so it is written as testing happens, not reconstructed the night before.

## Add rows

For each thing tested, one row:

| Functionality Tested | Date | Time | Tester | Result | Notes |
|---|---|---|---|---|---|

- **Real timestamps.** `date "+%Y-%m-%d %H:%M"`. Do not invent them.
- **Name the functionality specifically** - "Sign in with wrong password", not "Login".
- **`passed` or `failed`.** Nothing else.
- **Notes carry what a reader needs to reproduce** - the input used, the GPA arithmetic you checked by hand, the error text.

## Failures stay

A `failed` row is never edited or deleted. When it is fixed, add a **new** row for the retest and reference the failure in Notes ("retest of the 09-24 14:10 failure"). A log with no failures in it reads as a log nobody used, and it is the first thing an experienced grader notices.

## Check coverage

After adding rows, walk the checklist in [test_log.md](../../../docs/testing/test_log.md#coverage-checklist) and tick what is now covered. Report which requirements still have no rows.

Every one of R1-R5 needs at least one row before delivery, plus the data load, security and deployment sections.

## Test well

- Test against a **freshly loaded database** so results are reproducible.
- Say what you expect before you click. A test you did not predict is an observation.
- The high-value cases are the ones that are tedious by hand and easy to get wrong:
  - GPA checked against arithmetic you did on paper, including credit weighting and an A+ above 4.00.
  - Signed-out access to every `@login_required` route.
  - URL tampering to reach another student's enrollment.
  - A duplicate-course enrollment updating rather than raising.
  - A second run of `init_db.py`.

## Also run pytest

If the change touched `gpa_calculator` or route logic, run `pytest` and say so. Automated coverage is not the graded artifact but a failing suite blocks a merge ([process_protocol.md](../../../docs/protocol/process_protocol.md#testing)).
