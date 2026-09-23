# Process Protocol - Waterfall phases, roles, rubric

The assignment picks the process: **Waterfall**, because the requirements are fixed and the scope is small. Phases run in order, each closing on a named deliverable. This doc is the phase map, the role assignment, the testing stance and the rubric tracker.

---

## Phases

| Phase | What happens | Deliverable | Where it lands |
|---|---|---|---|
| **Communication** | Understand the requirements. Done - the assignment states them. | The requirement list | [design/requirements.md](../design/requirements.md) |
| **Planning** | Schedule, team roles, repo setup, protected `main` | Schedule table + role table | [planning/schedule.md](../planning/schedule.md) |
| **Modeling** | Requirements analysis and data model as UML | `uml/use_case.wsd`, `uml/class.wsd` | [design/use_cases.md](../design/use_cases.md), [design/data_model.md](../design/data_model.md) |
| **Construction** | Build and test the app and the library | Working app + test report | [design/routes.md](../design/routes.md), [testing/test_log.md](../testing/test_log.md) |
| **Deployment** | Docker image, PyPI package, `dev` -> `main` | Dockerfile + published package + final push | [deployment/docker.md](../deployment/docker.md), [design/gpa_library.md](../design/gpa_library.md) |

Waterfall means you do not start Construction on a route whose model is not settled. It does **not** mean the phases cannot overlap at the edges - the library can be built while the UML is being drawn, because they share nothing. What it forbids is discovering the data model while writing routes.

**The current phase is recorded in [planning/schedule.md](../planning/schedule.md)** and advanced with `/phase`.

### The checkpoint

Between Modeling and Construction there is a **mandatory instructor checkpoint**, scheduled in advance, in person or online. One representative presents:

- The use case and class diagrams
- A working baseline implementation of the app
- `main` protected, demonstrably
- A draft schedule
- The team role assignments

It is worth 5 points and it gates the phase. Do not let Construction run long before it happens - the point of the checkpoint is to catch a wrong model while it is still cheap.

---

## Team roles

Three to five members. One person may hold more than one role. Names go in [planning/schedule.md](../planning/schedule.md).

| Role | Owns |
|---|---|
| **Manager** | The schedule, the checkpoint booking, the rubric tracker, the team evaluation reminder |
| **Developer** | `src/app/`, `src/gpa_calculator/`, templates |
| **Tester** | The manual test log, the pytest suite, pulling teammates' branches and running them |
| **Documenter** | This `docs/` tree, the README, the UML diagrams, screenshots |

The roles describe accountability, not a wall. Anyone can write code; the developer is who notices when it is not getting written.

**Team and self evaluation is mandatory** and carries a **-25** penalty if skipped. Every member submits the form. The manager chases it. The grade is held until all of them are in.

---

## Testing

The assignment asks for **manual testing documented in a table** and does not ask for automated tests. We do both, because the two catch different things and one of them is nearly free.

### Manual testing - the graded artifact

[testing/test_log.md](../testing/test_log.md) holds the table the rubric wants: functionality, date, time, result. Every requirement gets at least one row, and every bug fix gets a row proving it is fixed. Rows are added by whoever ran the test, with real timestamps - a table filled in at the end from memory is obvious and worth less than an honest short one.

Add a row with `/test-log`.

### pytest - the safety net

Automated tests cover what is tedious to click repeatedly:

- **`gpa_calculator`** - the whole point of the library is one pure function, so it is the easiest thing in the project to test and the most embarrassing thing to get wrong. Cover the empty list, a single course, credit weighting across different credit values, an ungraded enrollment, and an unrecognized grade.
- **Routes** - Flask's test client against an in-memory SQLite database, checking that `@login_required` routes redirect when signed out, and that one student cannot see another's enrollments.

```
pip install -r requirements-dev.txt
pytest
```

Tests live in `tests/`, outside `src/`. They are a net, not a gate: a failing pytest run blocks a merge, but no rule says the test comes first. Write whichever comes naturally, and do not let a missing test stop a route from shipping the day before a checkpoint.

---

## Rubric tracker

The definition of done for the whole project. Keep the status column current; `/project-status` reads it.

| Pts | Item | Phase | Status |
|---|---|---|---|
| +5 | Planning: schedule | Planning | not started |
| +5 | Planning: team roles | Planning | not started |
| +5 | Modeling: use case diagram | Modeling | not started |
| +5 | Modeling: class diagram | Modeling | not started |
| +5 | Checkpoint | Modeling | not started |
| +10 | Courses data load (`init_db.py`, 5+ courses) | Construction | not started |
| +5 | Authentication (signup, login, signout) | Construction | not started |
| +10 | List of enrollments | Construction | not started |
| +10 | Create enrollment | Construction | not started |
| +10 | Delete enrollment | Construction | not started |
| +10 | GPA calculation and display | Construction | not started |
| +10 | GPA PyPI build and deployment | Deployment | not started |
| +5 | Testing (manual test report) | Construction | not started |
| +5 | Deployment (Dockerfile) | Deployment | not started |
| **-25** | **Team/self evaluation not submitted** | any | **outstanding** |
| **-5** | **`main` not protected** | Planning | **outstanding** |

**100 points available, and 30 points of penalty that cost nothing to avoid.** Protect `main` in week one and submit the evaluation form; those two are pure loss otherwise.

Status values: `not started` / `in progress` / `done` / `blocked`.

---

## Day to day

The phases are the plan; the working loop inside Construction is small:

1. Pick the highest-value rubric row that is not done.
2. Branch off `dev` ([core_protocol.md](core_protocol.md#branching)).
3. Build it. Check it against the relevant design doc.
4. Test it - pytest where it applies, a test log row where a grader will click.
5. PR into `dev`, a teammate runs it, merge.
6. Update the rubric row.

At the end of a working day, `/log-work` writes one changelog entry ([changelog.md](../changelog.md)).
