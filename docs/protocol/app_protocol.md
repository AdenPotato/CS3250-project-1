# App Protocol - Flask, SQLAlchemy, forms, templates

How the application itself is built. Shared conventions live in [core_protocol.md](core_protocol.md); what the app has to do lives in [design/requirements.md](../design/requirements.md).

---

## Layout

The assignment fixes this shape. Do not rearrange it - the instructor reads it.

```
src/
  app/
    __init__.py       app object, db, login manager, user_loader
    models.py         User, Course, Enrollment
    routes.py         every view function
    forms.py          Flask-WTF form classes
  gpa_calculator/     the publishable library
  init_db.py          one-time course catalog load
  instance/prj1.db    SQLite database (generated, never committed)
templates/            Jinja templates
static/style.css      the only stylesheet
```

Everything in `src/app/` is small on purpose. If `routes.py` grows past a few hundred lines the answer is shorter handlers, not a new package - splitting into blueprints changes the layout the grader expects.

---

## The app object

`src/app/__init__.py` wires four things in a fixed order: the Flask app, SQLAlchemy, the models, then the login manager and `user_loader`, and finally `routes` at the bottom. That trailing `from app import routes` is not a style mistake - it is what lets `routes.py` import `app` without a circular import. Leave the ordering alone.

Three things in the baseline must change before delivery:

- **`Flask("GPA Calculator Web App")`** uses a display string where Flask expects an import name. Flask cannot resolve that to a package, so it falls back to the working directory when locating `templates/` and `static/` - which are a level above `src/` in this layout. Expect `TemplateNotFound` on the first render. The fix and the alternatives are in [core_protocol.md](core_protocol.md#expect-a-template-path-problem-on-the-first-run); settle it before Construction, because it blocks every route that renders a page.

- **`app.secret_key = 'You will never know!'`** is a placeholder. Read it from the environment with a development fallback:
  ```python
  app.secret_key = os.environ.get('SECRET_KEY', 'dev-only-not-for-delivery')
  ```
  The Dockerfile and the run instructions then pass a real value. A hardcoded key in a public repo is a finding a grader can see.
- **`db.create_all()`** runs at import. That is fine for SQLite here, but it means a model change needs the database deleted and `init_db.py` re-run; it will not migrate an existing file.

---

## Models

Three entities, and the shape is set by the assignment ([data_model.md](../design/data_model.md)).

- **`User`** - `id` (the student's login id, a string primary key), `name`, `about`, `passwd` (a bcrypt hash, stored as `LargeBinary`). Subclasses `UserMixin` so Flask-Login can use it.
- **`Course`** - a **composite primary key** of `prefix` + `number`, plus `name` and `credits`.
- **`Enrollment`** - the association object joining a user to a course and carrying the `grade`. Its primary key is `user_id` + `course_prefix` + `course_number`, with a `ForeignKeyConstraint` pointing the last two at `Course`.

Rules:

- **`Enrollment` is an association object, not a plain join table**, because it carries `grade`. Reach a user's courses through `user.enrollments` (or the `courses` association proxy) - never query the table directly from a route.
- **The composite key on `Course` is load-bearing.** A course is identified by prefix and number together; any query, route parameter or form value that identifies a course carries both.
- **Grades are stored as letter strings** (`'A+'`, `'B-'`), never as numbers. The letter-to-points mapping is `GRADE_POINTS`, and the conversion happens in `gpa_calculator`, not in the model.
- **A model change means a database reset.** Delete `src/instance/prj1.db`, re-run `python init_db.py`, and say so in the PR so teammates do the same.

### `GRADE_POINTS` lives in two places

It is defined in both `src/app/models.py` and `src/gpa_calculator/__init__.py`. That duplication is deliberate: the library must stand alone on PyPI, so it cannot import from the app. The app's copy is the one to delete - once `gpa_calculator` is installed, `models.py` should import it rather than redefine it, and `forms.py` should build its grade choices from the same source. Until the library is published, keep them byte-identical and change both together.

---

## Routes

Every view function in `routes.py`. The full table with methods, auth and templates is in [design/routes.md](../design/routes.md).

- **Handlers are thin.** A handler validates a form, calls into the model or the library, and renders a template. Computation - GPA in particular - belongs in `gpa_calculator`.
- **Anything student-specific is `@login_required`** and scopes its query to `current_user`. A student must never see or delete another student's enrollment; the query filters on `current_user.id`, and it is not enough to hide the link in a template.
- **POST for anything that changes data**, then redirect. Deleting an enrollment is a POST with a CSRF-protected form, never a GET link - a GET delete gets triggered by a browser prefetch.
- **Redirect after a successful POST** (`return redirect(url_for('list_enrollments'))`) so a refresh does not resubmit.
- **`url_for`, never a hardcoded path**, in both Python and templates.

### Authentication

- Hash with bcrypt on signup: `bcrypt.hashpw(passwd.encode(), bcrypt.gensalt())`. Store the bytes in `passwd`.
- Check with `bcrypt.checkpw(attempt.encode(), user.passwd)`. Never compare hashes with `==`.
- Never log, render, or flash a password or a hash.
- On a failed login, say "invalid id or password" - do not reveal which half was wrong.
- `login_user(user)` on success, `logout_user()` on signout.

---

## Forms

Every form is a Flask-WTF `FlaskForm` in `forms.py`. This is not optional: `FlaskForm` is what provides the CSRF token, and `{{ form.hidden_tag() }}` in the template is what renders it. A hand-written `<form>` posting to a route is a security hole and a review rejection.

- **Validate on the server.** `form.validate_on_submit()` gates every POST. HTML5 `required` is a convenience, not a check.
- **Two fields the baseline leaves open:** `SignUpForm.passwd_confirm` needs an `EqualTo('passwd')` validator, and `EnrollmentForm.course` is a `SelectField` with no choices - populate them in the route from the `Course` table, formatting each as `(f'{c.prefix} {c.number}', f'{c.prefix} {c.number} - {c.name}')`.
- **Re-render with errors on failure**, with the user's input preserved, rather than redirecting. `render_template('create_enrollment.html', form=form)` does this for free.
- `DeleteEnrollmentForm` exists solely to carry a CSRF token on the delete button. Keep it.

---

## Templates

Jinja2 in `templates/`, all extending `base.html`.

- **`{% extends 'base.html' %}`** and fill `{% block main %}`. `base.html` takes a `title` variable - pass one from every route.
- **No inline styles and no second stylesheet.** `static/style.css` is the only one; `base.html` already links it.
- **Escape by default.** Jinja autoescapes; never reach for `|safe` on anything a user typed, including `about`.
- **Empty states matter.** A student with no enrollments sees a sentence explaining what to do next, not a bare table header. The grader will create a fresh account.
- **Show the GPA where the enrollments are.** Requirement 3 is satisfied on the enrollments page, formatted to two decimals.

Template-to-route mapping is in [design/routes.md](../design/routes.md); visual conventions are in [design/ui.md](../design/ui.md).

---

## The database load

`init_db.py` seeds the course catalog and is worth 10 rubric points. It must insert **at least 5 courses**, and it must be safe to run twice - check for an existing row before inserting, or the second run raises a primary-key violation mid-demo.

Run it inside the app context (the baseline already opens one) and print what it loaded.
