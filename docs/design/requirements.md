# Requirements

From the assignment. This is the Communication phase output and the source of truth for scope - a feature that does not trace to a line here is out of scope.

---

## The problem

Students need to track their GPA. The application lets a student register, sign in, enter completed courses with the letter grade earned, see everything they have entered, and see the resulting overall GPA. Grades entered incorrectly can be corrected.

## Objectives

- Track previously completed courses for each student, including their letter grades.
- Calculate and display the student's overall GPA.

## Functional requirements

| # | Requirement | Verified by |
|---|---|---|
| R1 | Users must be able to authenticate themselves. | Sign up, sign in with correct and incorrect credentials, sign out. |
| R2 | Students must be able to view all previously completed courses. | The enrollments page lists every enrollment for the signed-in student, and only theirs. |
| R3 | Students must be able to view their current GPA. | The GPA shows on the enrollments page and matches a hand calculation. |
| R4 | Students must be able to update the letter grade for a course. | Change a grade; the list and the GPA both reflect it. |
| R5 | Students must be able to delete a previously completed course. | Delete an enrollment; it disappears and the GPA recomputes. |

"Students" in R2-R5 means **authenticated users**, and each acts only on their own data.

### A note on R4

The assignment's requirement list says *update* a grade; the rubric funds *create* and *delete* and does not name update. The baseline provides a `create_enrollment` route and a `delete_enrollment` route, and no update route.

Treat this as: **create and delete are the graded path, and update is a requirement to satisfy on top of them.** The cheapest honest reading is that re-creating an enrollment for a course a student already has updates the grade rather than failing - which also fixes a real bug, since the composite primary key would otherwise raise on a duplicate. Build it that way and note it in the test log. If the team prefers an explicit edit route, that satisfies R4 too; it is more work and no more points.

## Constraints

- **Three weeks** to a working delivered version.
- **Three to five** team members.
- **Python, Flask and SQLAlchemy.** Not a preference - the implementation must use them.
- The GPA logic ships as a **separate library, packaged and published to PyPI**, installable with pip.
- Delivery is a **Docker image** the instructor can build and run.

## Risks

- **Limited team experience with the tooling.** The named risk in the assignment. Mitigation: the checkpoint happens early, and the riskiest unfamiliar piece - PyPI publishing - is started before the last week rather than left to the end. A PyPI account and an API token take a day to sort out if something goes wrong, and that is 10 points.
- **The baseline is mostly stubs.** Six routes return "Work in progress...", `init_db.py` inserts nothing, and `calculate_gpa` returns 0. Nothing is partially done; everything is not started.
- **The database does not migrate.** `db.create_all()` builds tables that do not exist and silently ignores a changed column. A model change late in the project means everyone deletes their database.

## Out of scope

Not required, and not to be built without the team agreeing to spend the time:

- Admin users, course creation through the UI, or a course catalog editor. Courses come from `init_db.py`.
- Password reset, email verification, or any email at all.
- Per-term GPA, standing, transcripts, credit totals beyond what the GPA needs.
- A REST API, a JavaScript front end, or any database other than SQLite.
