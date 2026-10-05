---
name: session-start
description: Open a working session - sync dev, read the protocol and design context, report where the project stands against the rubric, propose the next piece of work, and cut the branch once a teammate approves. Use at the start of a session, before any code.
argument-hint: "[rubric row or route name]"
---

# /session-start

The start-of-session checklist, in this order. Nothing is written and no branch is cut until Step 5.

## Step 0 - Sync `dev` (guarded)

Start from the integrated state, so the branch is not cut off yesterday's `dev`.

**Skip this step** if resuming a feature branch or the working tree is dirty (`git status --short` non-empty). Never pull into a feature branch mid-task - say so and continue on the current branch.

If the tree is clean:

```bash
git switch dev
git pull --ff-only
git fetch --prune
```

Then delete local branches whose PRs have merged. **Do not use `git branch --merged`** - it only lists ancestors of the current branch, so anything squashed on merge is silently kept:

```bash
for b in $(git branch --format='%(refname:short)' | grep -vE '^(main|dev)$'); do
  state=$(gh pr list --head "$b" --state all --json state --jq '.[0].state' 2>/dev/null)
  if [ "$state" = "MERGED" ]; then git branch -D "$b"; fi
done
```

`-D` and not `-d`: `-d` refuses anything git cannot see as merged.

If there is no repo or no `dev` branch yet, stop and say so. Both are Planning standing items in [schedule.md](../../../docs/planning/schedule.md#standing-items), and `main` unprotected is **-5 points** sitting there.

## Step 1 - Read the context (in parallel)

Read all five before forming any opinion:

- [docs/changelog.md](../../../docs/changelog.md) - what landed last session and what has to be run after pulling.
- [docs/planning/schedule.md](../../../docs/planning/schedule.md) - the current phase, the dates, the standing items.
- [docs/protocol/process_protocol.md](../../../docs/protocol/process_protocol.md) - the phases, the checkpoint, the rubric tracker.
- [docs/protocol/core_protocol.md](../../../docs/protocol/core_protocol.md) - branching, commits, what has to be true before a push.
- [docs/design/requirements.md](../../../docs/design/requirements.md) - what the app actually has to do.

Act on the changelog's `Heads up:` line before anything else. Most often it is `rm src/instance/prj1.db && python init_db.py` after a model change.

## Step 2 - Report where things stand

Gather and render exactly as [`/project-status`](../project-status/SKILL.md) specifies - phase, rubric, penalties, drift, next. Do not invent a second format; that report is defined once.

Two additions for a session start:

- **After pulling**, say what has to be run before the app will start.
- **If issues are in use**, list the open ones so the rubric view and the board agree:

  ```bash
  gh issue list --state open --limit 50 \
    --json number,title,labels,assignees,milestone,createdAt \
    --jq '.[] | "#\(.number)\t\([.labels[].name] | map(select(test("^P[0-2]$"))) | join(",") // "-")\t\([.assignees[].login] | join(",") // "unassigned")\t\(.milestone.title // "no phase")\t\(.title)"'
  ```

  Sort P0, then P1, then P2, then unlabelled. Flag anything open with no priority label, anything assigned to nobody in the current phase, and anything whose milestone is a phase already closed.

## Step 3 - Propose one pick

End the report with a single proposal. Highest points per hour first, preferring work that unblocks someone else - the data model before the routes, PyPI before delivery week, the diagrams before the checkpoint.

```
Pick:        <rubric row or issue> - <title>
Why now:     <one line - points, phase, or who it unblocks>
Branch:      <name>-<short-slug>
Deliverable: <the concrete artifact> -> <what closes it>
Verified by: <pytest, a test log row, or both>
Shape:       <two or three steps>
```

Then ask for a go, or for a different pick.

This is a recommendation and never an auto-start. If `$ARGUMENTS` names the work, plan around that instead of proposing your own.

## Step 4 - Wait

No branch, no edits, no `gh issue edit` before a teammate answers.

## Step 5 - Read the design docs for the pick, then cut the branch

Read what the pick actually touches, and say which files you read and why:

| The pick is | Read |
|---|---|
| A route | [routes.md](../../../docs/design/routes.md) + [app_protocol.md](../../../docs/protocol/app_protocol.md#routes) |
| A model or `init_db.py` | [data_model.md](../../../docs/design/data_model.md) + [app_protocol.md](../../../docs/protocol/app_protocol.md#models) |
| A form | [app_protocol.md](../../../docs/protocol/app_protocol.md#forms) + the route's row in [routes.md](../../../docs/design/routes.md) |
| A template or the stylesheet | [ui.md](../../../docs/design/ui.md) |
| `gpa_calculator` or PyPI | [gpa_library.md](../../../docs/design/gpa_library.md) |
| A UML diagram | [use_cases.md](../../../docs/design/use_cases.md) and [data_model.md](../../../docs/design/data_model.md) |
| Docker or delivery | [docker.md](../../../docs/deployment/docker.md) |
| Testing | [test_log.md](../../../docs/testing/test_log.md) |

**Confirm the deliverable before any code.** Name it concretely and name what closes it. If it is unclear, or the design doc does not answer a question the work needs answered, stop and run [`/new-design`](../new-design/SKILL.md) or ask a teammate - never guess a requirement (CLAUDE.md rule 6).

Only then:

```bash
gh issue edit <n> --add-assignee @me     # if the work has an issue - claim it before coding
git switch -c <name>-<short-slug>        # off dev
```

Branch naming and the rest of the loop are in [core_protocol.md](../../../docs/protocol/core_protocol.md#branching).

## Notes

- **Phase discipline.** If the pick belongs to a later phase than the current one, say so. Building a route while the data model is unsettled is the exact failure Waterfall is chosen to prevent.
- **The checkpoint gates Construction.** If the phase is Modeling and the checkpoint is not booked, that is the pick, whatever else is on the board.
- **The penalties come first in week one.** `main` protection and the evaluation form are -30 combined and take ten minutes.
