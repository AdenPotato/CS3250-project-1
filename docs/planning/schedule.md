# Schedule and Team

The Planning phase deliverable. Two tables, worth 5 rubric points each, plus the current-phase marker the rest of the process hangs off.

---

## Current phase

**Planning** <- you are here

Advance it with `/phase`. Phases and their deliverables: [process_protocol.md](../protocol/process_protocol.md#phases).

---

## Schedule

Three weeks, five phases. Fill in the dates - the template ships with `mm/dd/26` placeholders and `99 days`, and leaving them is a visible 5 points.

| Phase | Task | Start | End | Duration | Deliverable |
|---|---|---|---|---|---|
| Modeling | Requirements Analysis | mm/dd/26 | mm/dd/26 | ? days | Use Case Diagram |
| Modeling | Data Model | mm/dd/26 | mm/dd/26 | ? days | Class Diagram |
| Construction | Coding | mm/dd/26 | mm/dd/26 | ? days | Code |
| Construction | Testing | mm/dd/26 | mm/dd/26 | ? days | Test Report |
| Deployment | Delivery | mm/dd/26 | mm/dd/26 | ? days | Final Commit/Push |

### Sequencing advice

The table is the assignment's, and it hides three things worth scheduling explicitly:

- **The checkpoint gates Construction** and has to be booked with the instructor in advance. Put it on the calendar in week one, for early week two. It needs the diagrams *and* a running baseline.
- **PyPI publishing is not a Deployment-week task.** It is 10 points that depend on an account, a unique name, and an API token, any of which can take a day to resolve. Publish `0.0.1` in week two even if `calculate_gpa` is not final - versions are cheap, and the second upload is trivial once the first works.
- **`main` protection and the evaluation form are worth -30 combined** and take ten minutes. Do both in week one.

A realistic shape for three weeks:

| Week | Focus |
|---|---|
| 1 | Planning tables, repo + `main` protection, both UML diagrams, `init_db.py` course load, auth routes |
| 2 | Checkpoint. Enrollment list, create, delete. `gpa_calculator` written, tested, and published to TestPyPI then PyPI |
| 3 | GPA wired into the app, manual test pass, Dockerfile, screenshots, `dev` -> `main`, evaluations |

---

## Team roles

Three to five members. One person may hold more than one role. Role definitions: [process_protocol.md](../protocol/process_protocol.md#team-roles).

| Name | Role(s) | GitHub |
|---|---|---|
| | manager | |
| | developer | |
| | tester | |
| | documenter | |

Every member is a collaborator on the repo, and the repo URL goes in the project README for the instructor.

---

## Standing items

| Item | Owner | Status |
|---|---|---|
| Public GitHub repo created, all members added | manager | not done |
| Repo URL shared with instructor | manager | not done |
| `dev` branch created | manager | not done |
| `main` branch protected (**-5 if not**) | manager | not done |
| Checkpoint scheduled | manager | not done |
| Checkpoint held | manager | not done |
| Team/self evaluation submitted by **all** members (**-25 if not**) | everyone | not done |

The two penalty rows are the cheapest points in the project. Clear them first.
