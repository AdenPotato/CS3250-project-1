# Schedule and Team

The Planning phase deliverable. Two tables, worth 5 rubric points each, plus the current-phase marker the rest of the process hangs off.

---

## Current phase

**Deployment** <- you are here

Advance it with `/phase`. Phases and their deliverables: [process_protocol.md](../protocol/process_protocol.md#phases).

---

## Schedule

Three weeks, five phases. The graded copy of this table is in the project [README](../../README.md#schedule); keep the two the same.

| Phase | Task | Start | End | Duration | Deliverable |
|---|---|---|---|---|---|
| Modeling | Requirements Analysis | 09/22/26 | 09/26/26 | 4 days | Use Case Diagram |
| Modeling | Data Model | 09/22/26 | 09/26/26 | 4 days | Class Diagram |
| Construction | Coding | 09/25/26 | 09/30/26 | 5 days | Code |
| Construction | Testing | 09/25/26 | 09/30/26 | 5 days | Test Report |
| Deployment | Delivery | 10/01/26 | 10/03/26 | 2 days | Final Commit/Push |

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
| Aden Lytle | manager, developer, tester, documenter | AdenPotato |
| Johnny (Juan) De La Garza | developer, tester | jdelagar |
| Isabella Eaton | tester, documenter | ellaevelynn |
| Elijah Damian-Ortiz | developer, tester | damian-ortiz-elijah |

Every member is a collaborator on the repo, and the repo URL goes in the project README for the instructor.

---

## Standing items

| Item | Owner | Status |
|---|---|---|
| Public GitHub repo created, all members added | manager | done |
| Repo URL shared with instructor | manager | done - in the README |
| `dev` branch created | manager | done |
| `main` branch protected (**-5 if not**) | manager | done - "Protect main" ruleset |
| Checkpoint scheduled | manager | done |
| Checkpoint held | manager | done - 2026-09-29, issue #9 |
| Team/self evaluation submitted by **all** members (**-25 if not**) | everyone | not done |

The two penalty rows are the cheapest points in the project. Clear them first.
