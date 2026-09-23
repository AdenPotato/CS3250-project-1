# Data Model

The Modeling phase output for structure. Source of truth is `src/app/models.py`; the UML class diagram at `uml/class.wsd` is generated from this and is worth 5 rubric points.

---

## Entities

### User

The student. Authenticates, owns enrollments.

| Field | Type | Notes |
|---|---|---|
| `id` | String, **PK** | The student's login id, chosen at signup. Not an integer. |
| `name` | String | Display name. |
| `about` | String | Free text from the signup form. Rendered escaped. |
| `passwd` | LargeBinary | The **bcrypt hash**, stored as bytes. Never the plaintext. |

Subclasses `UserMixin`, which supplies `is_authenticated`, `get_id()` and the rest of what Flask-Login expects.

### Course

The catalog entry, loaded by `init_db.py`. Students never create one.

| Field | Type | Notes |
|---|---|---|
| `prefix` | String, **PK** | e.g. `CS`. |
| `number` | String, **PK** | e.g. `3250`. A string, not an int - `101A` is a real course number. |
| `name` | String | e.g. `Software Development Methods and Tools`. |
| `credits` | Integer | Credit hours. The weight in the GPA calculation. |

**The primary key is composite: `(prefix, number)`.** Every reference to a course carries both halves - in routes, in form values, in URLs.

### Enrollment

The association object joining a student to a course and carrying the grade earned. This is the table the whole app revolves around.

| Field | Type | Notes |
|---|---|---|
| `user_id` | String, **PK**, FK -> `users.id` | |
| `course_prefix` | String, **PK** | Half of the FK to `courses`. |
| `course_number` | String, **PK** | The other half. |
| `grade` | String | A letter from `GRADE_POINTS`, e.g. `A-`. Nullable in principle; treated as ungraded. |

The foreign key to `Course` is a composite `ForeignKeyConstraint(['course_prefix', 'course_number'], ['courses.prefix', 'courses.number'])`, not two separate column-level FKs - a composite key needs a composite constraint.

Because `(user_id, course_prefix, course_number)` is the primary key, **a student can hold at most one enrollment per course.** That is correct behavior, and it is also why creating an enrollment for a course the student already has must update the existing row rather than insert ([requirements R4](requirements.md#a-note-on-r4)).

---

## Relationships

```
User 1 ────< Enrollment >──── 1 Course
```

- `User.enrollments` <-> `Enrollment.user` (one to many, `back_populates`)
- `Course.enrollments` <-> `Enrollment.course` (one to many, `back_populates`)
- `User.courses` - an **association proxy** over `enrollments`, giving the courses directly
- `Course.students` - the mirror proxy, giving the users

Many-to-many between `User` and `Course`, resolved through `Enrollment` because the relationship carries an attribute (`grade`). That is the textbook reason to use an association object instead of a plain secondary table, and it is worth saying out loud in the class diagram.

**Navigate through the relationships.** `current_user.enrollments` is the way to list a student's courses, and `enrollment.course.credits` is the way to reach credit hours. A route that queries `Enrollment` by hand and then queries `Course` separately is doing SQLAlchemy's job badly.

---

## The grade scale

`GRADE_POINTS` maps letter to quality points:

| | | | |
|---|---|---|---|
| A+ 4.3 | A 4.0 | A- 3.7 | |
| B+ 3.3 | B 3.0 | B- 2.7 | |
| C+ 2.3 | C 2.0 | C- 1.7 | |
| D+ 1.3 | D 1.0 | D- 0.7 | |
| F 0.0 | | | |

A+ is included and is worth 4.3, so **a GPA above 4.0 is possible and is not a bug.** Any test or display that assumes a 4.0 ceiling is wrong.

The scale is defined in `src/gpa_calculator/__init__.py` and duplicated in `src/app/models.py` so the library can stand alone on PyPI. See [app_protocol.md](../protocol/app_protocol.md#grade_points-lives-in-two-places) for which copy wins and when to collapse them.

---

## The class diagram

`uml/class.wsd` is PlantUML and currently empty. It needs three classes with their attributes, the two relationships, and the multiplicities - `User "1" -- "0..*" Enrollment` and `Course "1" -- "0..*" Enrollment`. Mark `Enrollment` as the association class.

Generate or refresh it with `/uml`. Render with the PlantUML extension in VS Code, or `plantuml uml/class.wsd`, and commit the rendered PNG next to the source so the instructor does not have to render it.

---

## Changing the model

`db.create_all()` creates missing tables and **ignores changes to existing ones.** There are no migrations. So:

1. Change `models.py`.
2. Delete `src/instance/prj1.db`.
3. Re-run `python init_db.py`.
4. Say so in the PR body, because every teammate has to do the same.

This is survivable in a three-week project and is the reason to settle the model in the Modeling phase rather than during Construction.
