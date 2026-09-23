---
name: new-route
description: Implement a Flask route end to end - the view function, its Flask-WTF form, its Jinja template, and the test log rows. Use when replacing one of the "Work in progress..." stubs or adding a page.
---

# /new-route

Build one route through every layer it touches. Take the route name as an argument (`/new-route list_enrollments`); if none is given, pick the highest-value unwritten one from [routes.md](../../../docs/design/routes.md).

## Before writing

Read the route's row in [routes.md](../../../docs/design/routes.md) - methods, auth, form, template, use case. If it is not there, it is not in scope; check [requirements.md](../../../docs/design/requirements.md) and ask before inventing one.

## Build, in this order

1. **The form**, if the route takes input. A `FlaskForm` in `src/app/forms.py` with validators. `SignUpForm.passwd_confirm` needs `EqualTo('passwd')`; `EnrollmentForm.course` gets its choices in the route, not the class.

2. **The view function** in `src/app/routes.py`. Replace the `# TODO` and the `"Work in progress..."` return - do not leave either behind.
   - `@login_required` on anything student-facing.
   - Scope every query to `current_user`, never to an id from the URL.
   - `form.validate_on_submit()` gates the POST branch.
   - Redirect after a successful POST; re-render with errors after a failed one.
   - `url_for`, never a hardcoded path. Pass `title` to every `render_template`.

3. **The template** in `templates/`, extending `base.html`. `{{ form.hidden_tag() }}` in every form, field errors rendered next to their fields, an empty state if the page can be empty. Conventions: [ui.md](../../../docs/design/ui.md).

4. **A pytest**, if the logic is worth it - auth redirect when signed out, and cross-student isolation for anything reading or deleting a row. Skip it for a route that only renders a static page.

## Verify

Run it. `flask --app app run --debug`, then in a browser:

- The happy path.
- Invalid input - does it re-render with a visible error and keep what was typed?
- Signed out - does it redirect to login?
- Another student's data - can you reach it by editing the URL? You should not be able to.

## Finish

- Add rows to [test_log.md](../../../docs/testing/test_log.md) for what you just clicked, with a real timestamp (`/test-log`).
- Update the rubric row in [process_protocol.md](../../../docs/protocol/process_protocol.md#rubric-tracker).
- If the route's behavior differs from [routes.md](../../../docs/design/routes.md), fix the doc in the same change.
- Commit per [core_protocol.md](../../../docs/protocol/core_protocol.md#commits), PR into `dev` with a screenshot.
