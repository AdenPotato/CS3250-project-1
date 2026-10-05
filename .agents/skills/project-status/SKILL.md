---
name: project-status
description: Report where the project stands - the current Waterfall phase, the rubric tracker with points earned and at risk, the TODO stubs still in the code, and what to do next. Use at the start of a working session or before a checkpoint.
---

# /project-status

Read the state, report it, recommend the next move. **Read-only** - this skill changes nothing.

## Gather

1. **Phase** - the marker in [schedule.md](../../../docs/planning/schedule.md#current-phase).
2. **Rubric** - the table in [process_protocol.md](../../../docs/protocol/process_protocol.md#rubric-tracker). Sum points by status.
3. **Standing items** - the table at the bottom of `schedule.md`, especially the two penalty rows.
4. **Code reality** - do not trust the tracker alone:
   - `grep -rn "TODO\|Work in progress" src/` - unwritten stubs.
   - `grep -c "" src/init_db.py` and check whether `courses` is still empty.
   - Does `calculate_gpa` still `return 0`?
   - Are `uml/class.wsd` and `uml/use_case.wsd` still empty stubs?
   - Is there a Dockerfile?
5. **Git** - `git branch -a`, `git log --oneline -10`, whether `dev` exists and is ahead of `main`.
6. **Test log** - how many rows, how many failures unretested.

## Report

Short. Five sections, no preamble:

**Phase** - which one, and what its deliverable is.

**Rubric** - a compact table of anything not `done`, with points. Then one line: `earned N / at risk M / not started K`.

**Penalties** - state the -5 and -25 explicitly every time until both are cleared. They are the cheapest points in the project and the easiest to forget.

**Drift** - anywhere the tracker says `done` but the code disagrees, or vice versa. Name the file.

**Next** - two or three concrete actions, highest points-per-hour first. Prefer work that unblocks others: the data model before routes, PyPI before delivery week, the diagrams before the checkpoint.

## Judgement

- A rubric row is `done` only when the behavior works in a browser and a test log row records it. "The code is written" is `in progress`.
- Flag the checkpoint if the phase is Modeling and it is not yet scheduled - it gates Construction.
- If the clock is short, say which rubric rows are realistically reachable and which are not. A team that knows it will miss 10 points can choose which 10.
