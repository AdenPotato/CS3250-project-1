---
name: qa-steps
description: Write a numbered QA script for a branch - every step with an exact action, an exact expected result, and a blank for the result. Use when handing a branch to the tester, or when a QA round found problems and the next round has to be precise about what to re-check.
argument-hint: "[branch or route name]"
---

# /qa-steps

Turn "ready to test" into a script a teammate can work through without designing the test themselves.

**Why this exists.** "Have a click around the enrollments page" puts the work of inventing the test on the person running it, and produces "looks fine", which cannot be acted on and cannot be logged. A numbered script with an exact expected result per step produces "3b failed, the GPA stayed at 3.50 after the delete" - which is a defect report, a reproduction, and a [test log](../../../docs/testing/test_log.md) row at once.

The reviewer's job on a PR is to pull the branch and **run** it, not only to read the diff ([core_protocol.md](../../../docs/protocol/core_protocol.md#pull-requests)). This is what they run.

## When to run it

- A branch is pushed and about to be reviewed.
- A QA round found problems and the next round has to state exactly what to re-check.
- The change is hard to verify from the diff - anything visual, anything with session state, anything computed.

Skip it for a change with no observable surface: a doc edit, a comment, a refactor that changes nothing a browser shows. Those are verified by `pytest` and by reading, and a QA script for them is ceremony.

## Step 1 - Establish where QA happens

**Before writing a single step, say what the tester will be looking at and confirm it is running this branch's code.** Getting this wrong wastes a whole round.

For this project that is nearly always:

```bash
git switch <branch> && git pull
rm -f src/instance/prj1.db        # a model change makes the old database wrong, not stale
cd src && python init_db.py       # reload the catalog
flask --app app run --debug       # http://127.0.0.1:5000
```

Then name, concretely:

- **The database** - freshly loaded, or deliberately carried over. Results are only reproducible from a known state.
- **The accounts** - most scripts need **two** students, because cross-student isolation is the check a single account cannot make. Give the ids and passwords to create.
- **A rebuilt container**, if the change is to the Dockerfile. An image built before the change runs the old code ([docker.md](../../../docs/deployment/docker.md)).

That is the **Preconditions** block. A step that assumes the wrong surface is worse than no step.

## Step 2 - Derive the steps from the diff

Work from what the change did, not from imagination. In this order:

1. **The happy path** - the thing the change was for, in its normal state.
2. **The states the design exists to handle** - the empty state a fresh account sees, invalid input re-rendering with the typed values kept, a duplicate enrollment updating the grade instead of erroring (R4).
3. **The security surface**, on anything student-facing - signed out, does the route redirect to login; signed in as the second student, does editing the delete URL reach the first student's row. It must not ([app_protocol.md](../../../docs/protocol/app_protocol.md#routes)).
4. **The arithmetic**, on anything touching the GPA - checked against a hand calculation, with credit weighting visible and an A+ able to push it above 4.00.
5. **What must not have changed** - the neighbouring behavior this change could plausibly have broken.

Every step traces to something in the diff or to a row in the [coverage checklist](../../../docs/testing/test_log.md#coverage-checklist).

## Step 3 - Write the steps

**Numbering is the contract.** Top-level steps are numbers; sub-steps are letters, used when one step has more than one thing to observe - so "4c failed" means the same thing to both people.

Every step has three parts and none is optional:

- **Do** - one concrete action. Two actions is two steps.
- **Expect** - the exact observable result. Not "the GPA updates" but "the GPA reads `3.25`".
- **Result** - left blank, for the tester.

Rules for a step worth writing:

- **One assertion per sub-step.** "Check the table and the GPA" cannot be failed precisely.
- **Exact values.** "the empty state reads `You have no enrollments yet`", not "a message appears".
- **Say the arithmetic.** For a GPA step, write the sum out: `(4.0*4 + 3.0*3) / 7 = 3.57`. The tester copies it into the test log Notes.
- **Say what the near-miss failure looks like** where there is one. "If the delete returns 200 rather than redirecting, a refresh resubmits it - that is the defect this step catches."
- **Never write a step whose result you already know.** If `pytest` proves it, the test is the check.

## Step 4 - Render it

This goes in the PR description or a comment, not a file. It is per-round; the permanent record is the [test log](../../../docs/testing/test_log.md).

```markdown
## QA script - <branch>

**Preconditions**
- Branch: `<branch>`, pulled
- Database: `rm -f src/instance/prj1.db && cd src && python init_db.py`
- Run: `flask --app app run --debug` -> http://127.0.0.1:5000
- Accounts: create `s001` / `pw001` and `s002` / `pw002`
- Roughly: <minutes>

### 1. <what this group checks>
**Do:** <action>
**Expect:** <exact observable>
**Result:**

### 2. <group with several observations>
**Do:** <action>
- **2a. Expect:** <one observable>
  **Result:**
- **2b. Expect:** <another observable>
  **Result:**

### 3. Regression - <what must not have changed>
...
```

End with:

```markdown
**Report back as:** the step number, what you saw, and a screenshot for anything visual.
A bare "looks good" on a numbered script loses the information the numbering exists to carry.
```

## Step 5 - Close the loop

1. **Every step that ran becomes a test log row** - `passed` or `failed`, with a real timestamp, via [`/test-log`](../test-log/SKILL.md). The script is the working paper; the log is the graded artifact.
2. **A failed row stays.** When it is fixed, add a new row for the retest referencing the failure. Never edit the original.
3. **Quote the step number in the fix** so the change and the observation stay linked.
4. **Re-issue only the affected steps**, plus any regression step the fix could touch. Re-issuing the whole script trains people to skim it.
5. **A step that failed once is a candidate for a pytest.** If it can be asserted automatically, say so and propose it - a QA step that keeps failing is a missing test wearing a disguise.

## What this is not

- **Not a substitute for pytest.** Anything a test can assert belongs in `tests/`. This covers what automation cannot: does the page read right, does the real flow behave.
- **Not a checklist to pad.** Ten precise steps beat forty vague ones.
- **Not a place to hide uncertainty.** If you do not know what a step should produce, say so in the step rather than writing a vague expectation and hoping.
