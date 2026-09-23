# Routes

Every view function in `src/app/routes.py`, what it does, and what it renders. The rules behind them are in [app_protocol.md](../protocol/app_protocol.md#routes).

---

## The table

| Route | Methods | Auth | Form | Template | Use case |
|---|---|---|---|---|---|
| `/`, `/index`, `/index.html` | GET | - | - | `index.html` | landing |
| `/users/signup` | GET, POST | - | `SignUpForm` | `signup.html` | UC1 |
| `/users/login` | GET, POST | - | `LoginForm` | `login.html` | UC2 |
| `/users/signout` | GET, POST | student | - | redirect | UC3 |
| `/enrollments` | GET | student | `DeleteEnrollmentForm` | `enrollments.html` | UC4, UC5 |
| `/enrollments/create` | GET, POST | student | `EnrollmentForm` | `create_enrollment.html` | UC6, UC7 |
| `/enrollments/delete/<course_prefix>/<course_number>` | POST | student | `DeleteEnrollmentForm` | redirect | UC8 |

The paths come from the baseline. **Do not rename them** - the instructor may navigate directly.

Note the delete route takes **both** halves of the course key, because `(prefix, number)` is the composite primary key.

---

## What each one does

### `index`

Renders the landing page. Pass a `title`. If the visitor is already signed in, linking straight to `/enrollments` is a courtesy, not a requirement.

### `signup`

**GET** renders the form. **POST**, on `validate_on_submit()`:

1. Reject a duplicate `id` with a message on the form - do not let the insert raise.
2. Hash: `bcrypt.hashpw(form.passwd.data.encode(), bcrypt.gensalt())`.
3. Insert the `User`, commit, redirect to `login`.

`passwd_confirm` needs an `EqualTo('passwd')` validator added in `forms.py` - the baseline has the field but not the check.

### `login`

**POST**: look up the user by id, and if found check `bcrypt.checkpw(form.passwd.data.encode(), user.passwd)`. On success `login_user(user)` and redirect to `list_enrollments`. On either failure, re-render with "invalid id or password" - the same message for both, so the form does not become a way to enumerate valid ids.

### `signout`

`logout_user()`, redirect to `index`. Keep `@login_required`.

### `list_enrollments`

The main page, and where two rubric lines are earned at once.

1. Read `current_user.enrollments`. Never query the table filtered by a user id from the request.
2. Compute the GPA by handing the enrollments to `calculate_gpa` from the library.
3. Render the table - prefix, number, course name, credits, grade - plus the GPA to two decimals, plus a `DeleteEnrollmentForm` instance per row for the CSRF token.
4. With no enrollments, render the empty state and a GPA of 0.00.

### `create_enrollment`

**GET**: build the form and populate `form.course.choices` from the `Course` table. The value carries both key halves; `f'{c.prefix} {c.number}'` as the value and `f'{c.prefix} {c.number} - {c.name}'` as the label works.

**POST**, after repopulating the choices (a `SelectField` revalidates against them, so a form built without choices on POST always fails):

1. Split the selected value back into prefix and number.
2. Look for an existing `Enrollment` for `(current_user.id, prefix, number)`. If it exists, set `grade` - this is UC7. If not, insert one.
3. Commit, redirect to `list_enrollments`.

Step 2 is the whole of requirement R4 and it is three lines. Skipping it means a duplicate-course submit raises an `IntegrityError` in front of the grader.

### `delete_enrollment`

POST only. Validate the `DeleteEnrollmentForm` for CSRF, then delete the row matching `(current_user.id, course_prefix, course_number)` - **the user id from the session, never from the URL.** Commit and redirect to `list_enrollments`. A missing row is not an error; redirect anyway.

---

## Conventions

- `url_for` everywhere, in Python and in templates. No hardcoded `/enrollments`.
- Every `render_template` passes `title`; `base.html` uses it.
- Redirect after every successful POST so refresh does not resubmit.
- `flash` a short confirmation on create, update and delete if the team wants one; if so, render messages in `base.html` so every page gets them.

## Where the stubs are

All six non-index routes ship as `return "Work in progress..."`. There is no partial credit in the baseline - each one is written from nothing, and each maps to a rubric line worth 5 to 10 points.
