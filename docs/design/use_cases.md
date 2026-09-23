# Use Cases

The Modeling phase output for behavior - the requirements analysis behind `uml/use_case.wsd`. Worth 5 rubric points.

---

## Actors

- **Visitor** - an unauthenticated person. Can see the landing page, sign up, and sign in. Nothing else.
- **Student** - an authenticated user. Everything below.

There is no administrator actor. The course catalog is loaded by `init_db.py` outside the application, which is why no use case creates a course.

---

## Use cases

| ID | Use case | Actor | Requirement |
|---|---|---|---|
| UC1 | Sign up | Visitor | R1 |
| UC2 | Sign in | Visitor | R1 |
| UC3 | Sign out | Student | R1 |
| UC4 | View enrollments | Student | R2 |
| UC5 | View GPA | Student | R3 |
| UC6 | Record an enrollment | Student | R2 |
| UC7 | Update a grade | Student | R4 |
| UC8 | Delete an enrollment | Student | R5 |

### UC1 - Sign up

A visitor supplies an id, name, optional about text, and a password entered twice. The system rejects a duplicate id and a password mismatch, hashes the password with bcrypt, creates the user, and takes them to sign in.

**Fails when:** the id is taken, the passwords differ, or a required field is blank. The form re-renders with the message and the entered values intact.

### UC2 - Sign in

A visitor supplies an id and password. The system finds the user, checks the password against the stored hash, and starts a session. On failure it says "invalid id or password" without saying which half was wrong.

### UC3 - Sign out

A student ends the session and returns to the landing page.

### UC4 - View enrollments

A student sees every enrollment they hold: course prefix, number, name, credits and grade, with a delete control on each. A student with none sees a message pointing at the create page rather than an empty table.

**Includes UC5** - the GPA is shown on this page.

### UC5 - View GPA

The student's credit-weighted GPA across all graded enrollments, to two decimals. Zero when nothing is graded yet.

### UC6 - Record an enrollment

A student picks a course from the catalog and a letter grade, and the enrollment is saved. The course list comes from the `Course` table.

**Extends to UC7** - picking a course the student already holds updates that grade rather than failing on the duplicate primary key.

### UC7 - Update a grade

A student corrects a grade entered wrongly. The list and the GPA both reflect it immediately. See [the note on R4](requirements.md#a-note-on-r4) for why this rides on UC6.

### UC8 - Delete an enrollment

A student removes an enrollment. It leaves the list and the GPA recomputes. The `Course` row is untouched - deleting an enrollment never deletes a catalog course.

---

## Rules that cut across all of them

- **UC3-UC8 require authentication.** An unauthenticated request to any of them redirects to sign in. This is `@login_required`, plus a query scoped to `current_user` - the decorator proves who you are, the query is what stops you reaching someone else's row.
- **A student only ever touches their own enrollments.** There is no use case in which one student reads or changes another's data.
- **Anything that changes data is a POST** with a CSRF token from a Flask-WTF form.

---

## The diagram

`uml/use_case.wsd` is PlantUML and currently empty. It needs both actors, the eight use cases, the `<<include>>` from UC4 to UC5, the `<<extend>>` from UC7 to UC6, and a boundary box around the system. Keep `left to right direction` for readability.

Generate or refresh it with `/uml`, render it, and commit the PNG alongside the source.
