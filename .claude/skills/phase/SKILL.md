---
name: phase
description: Advance the Waterfall phase - verify the current phase's deliverable actually exists, then move the marker in schedule.md. Use when a phase closes, not to check status.
---

# /phase

Move the project from one Waterfall phase to the next. A phase closes on a **deliverable that exists**, not on a feeling that the work is mostly done.

## Steps

1. **Read the current phase** from [schedule.md](../../../docs/planning/schedule.md#current-phase).

2. **Verify the deliverable.** Check the artifact, do not ask whether it is finished:

   | Closing | Verify |
   |---|---|
   | Communication | [requirements.md](../../../docs/design/requirements.md) lists the requirements and constraints |
   | Planning | The schedule table has real dates, roles have real names, `main` is protected (`gh api repos/:owner/:repo/branches/main/protection`), `dev` exists |
   | Modeling | `uml/use_case.wsd` and `uml/class.wsd` are non-empty and render, and the **checkpoint has been held** |
   | Construction | Every Construction rubric row is `done`, the app runs end to end, the test log covers all five requirements |
   | Deployment | Fresh-clone Docker build runs, the package installs from PyPI, `dev` is merged to `main` |

3. **Report what is missing.** If the deliverable is not there, stop and list the gaps. Do not advance a phase to make a tracker look better - the checkpoint in particular gates Construction for a reason, and skipping it means finding a wrong data model after the routes are built.

4. **On confirmation, update:**
   - The `<- you are here` marker in `schedule.md`.
   - Any rubric rows the closing phase completed ([the tracker](../../../docs/protocol/process_protocol.md#rubric-tracker)).
   - A changelog note if the day's work is being logged.

5. **Say what the new phase needs** - its deliverable, and the first task toward it.

## Notes

- Phases run in order. Going backwards is legitimate when Construction uncovers a model error; say so plainly and reopen Modeling rather than patching around it.
- Edges may overlap. The library can be built during Modeling because it shares nothing with the UML. Starting routes before the data model is settled is the thing Waterfall exists to prevent.
- Never advance past Modeling without the instructor checkpoint. It is 5 points and a gate.
