---
name: new-issue
description: Open a GitHub issue for one piece of rubric work - draft it from the session, name its rubric row, set a priority and phase milestone, then create it with gh. Use when a teammate has approved tracking the work.
argument-hint: "[short description]"
---

# /new-issue

One issue, one piece of work, one rubric row. The [rubric tracker](../../../docs/protocol/process_protocol.md#rubric-tracker) is the definition of done for the project; issues are how the work toward a row gets split up and claimed.

**Teammate-gated.** Only run this once someone has asked for the issue or approved it. Never open one unilaterally, not even a follow-on. If you have spotted work that wants an issue, **propose it - title plus one-line scope - and wait for a go.** A mechanical backstop lives in `.claude/settings.json` (`permissions.ask` prompts before any `gh issue create`).

## Before anything

The repo has to exist and be reachable:

```bash
gh repo view --json nameWithOwner -q .nameWithOwner
```

If that fails, the repo is not set up yet. That is a Planning standing item in [schedule.md](../../../docs/planning/schedule.md#standing-items), and it blocks this skill - say so and stop rather than working around it.

## Step 1 - Draft it, then ask for priority and milestone

Infer the title, body and labels from the session - what was decided, or what was found and needs following up.

**Title** is `<Area>: <short description>`, lowercase after the prefix:

| Prefix | Means | Label |
|---|---|---|
| `Route:` | a view function and what it renders | `route` |
| `Model:` | `models.py`, the schema, `init_db.py` | `model` |
| `Library:` | `src/gpa_calculator/` or its packaging | `library` |
| `UI:` | a template or `static/style.css` | `ui` |
| `Design:` | a decision to settle before code | `design` |
| `Docs:` | anything under `docs/` | `documentation` |
| `Test:` | the test log or the pytest suite | `testing` |
| `Deploy:` | Dockerfile, PyPI upload, delivery | `deployment` |
| `Fix:` | something that is broken | `bug` |

**Body** carries five things and nothing else:

```markdown
**Why** - one or two sentences. Which requirement (R1-R5) this serves.

**Scope** - what is in, and the obvious neighbouring thing that is out.

**Rubric row** - the row from the tracker, with its points. If it maps to no row, it is out of scope until a teammate says otherwise.

**Deliverable** - the concrete artifact that closes this. A route that works in a browser, a diagram that renders, a package that installs.

**How it is verified** - a pytest, a manual test log row, or both. Anything a grader will click needs a row.
```

For an issue touching `src/gpa_calculator/`, add a **version impact** line naming the bump it implies (`MAJOR` / `MINOR` / `PATCH`) and why - judged by what someone installing from PyPI has to change, not by the size of the diff ([gpa_library.md](../../../docs/design/gpa_library.md#publishing)). For an issue touching `models.py`, add a **database reset** line, because there are no migrations.

**Priority** is a plain label. There is no project board:

- **`P0`** - the two penalty rows (`main` unprotected, evaluations unsubmitted) and anything gating a phase, the instructor checkpoint above all. These cost points that are free to keep.
- **`P1`** - rubric points in the **current phase** ([schedule.md](../../../docs/planning/schedule.md#current-phase)), and anything blocking a teammate.
- **`P2`** - everything else, including work in a later phase.

Present the drafted title, body and labels, then ask for the priority and whether a milestone applies. List open milestones if unsure:

```bash
gh api "repos/$(gh repo view --json nameWithOwner -q .nameWithOwner)/milestones" --jq '.[].title'
```

Milestones are the Waterfall phases - `Planning`, `Modeling`, `Construction`, `Deployment` - so phase progress can be read off the board. Do not proceed until the draft and the priority are confirmed.

## Step 2 - Make sure the labels exist

Idempotent; ignore "already exists":

```bash
gh label create P0 --color B60205 --description "highest - penalty rows and phase gates" 2>/dev/null || true
gh label create P1 --color D93F0B --description "rubric points in the current phase" 2>/dev/null || true
gh label create P2 --color FBCA04 --description "everything else" 2>/dev/null || true
```

Create the area label the same way if it is new.

## Step 3 - Create it

```bash
gh issue create \
  --title "<title>" \
  --body "<body>" \
  --label "<area-label>" \
  --label "<P0|P1|P2>"
```

Add `--milestone "<phase>"` when one applies. Keep the issue URL from the output.

## Step 4 - Confirm

```bash
gh issue view <number> --json number,title,labels,milestone \
  --jq '"#\(.number) \(.title)\nlabels: \([.labels[].name] | join(", "))\nmilestone: \(.milestone.title // "none")"'
```

Show the URL and the confirmed labels. If the issue starts now, the branch is `<name>-<short-slug>` off `dev` and the commit references the number: `implement calculate_gpa with credit weighting (#4)` ([core_protocol.md](../../../docs/protocol/core_protocol.md#commits)).

## Constraints

- **One rubric row per issue.** "Enrollments" is three issues - list, create, delete - worth 10 points each, and splitting them is how two people work at once.
- **Do not set parent/child links via the API.** That is a GitHub UI action.
- **Priority lives only on the label.** No project board, no org-level field.
- **Do not open an issue for work already done.** The rubric tracker records that; an issue is for work that has not started.
