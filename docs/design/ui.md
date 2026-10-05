# UI

Jinja templates and the one stylesheet. The assignment ships seven screenshots as **suggestions**, not a specification - match their shape and do not spend Construction time on visual polish that earns nothing.

---

## Templates

| File | Extends | Shows |
|---|---|---|
| `base.html` | - | The shell: `<head>`, the `style.css` link, `{% block main %}`. |
| `index.html` | base | Landing page, links to sign up and sign in. |
| `signup.html` | base | `SignUpForm`. |
| `login.html` | base | `LoginForm`. |
| `enrollments.html` | base | The enrollment table, the GPA, a delete button per row, a link to create. |
| `create_enrollment.html` | base | `EnrollmentForm` - course select, grade select. |

### base.html

The baseline is minimal and takes a `title` variable, so every route passes one. Two things worth adding once, in `base.html`, where every page gets them:

- **A nav strip** - the app name, and either "sign up / sign in" or "enrollments / create / sign out" depending on `current_user.is_authenticated`. Flask-Login makes `current_user` available in templates without passing it.
- **Flash messages**, if the team uses `flash()`. Rendering them in one place is the only reason flashing is cheaper than passing a message to every template.

### Form templates

Every one of them, without exception:

```jinja
<form method="POST">
    {{ form.hidden_tag() }}
    {{ form.field.label }} {{ form.field() }}
    {% for error in form.field.errors %}<span class="error">{{ error }}</span>{% endfor %}
    {{ form.submit() }}
</form>
```

`{{ form.hidden_tag() }}` renders the CSRF token. **A form without it fails validation on every POST**, which presents as a form that silently does nothing - the most common way to lose an afternoon on this project.

Render field errors next to their field. A form that rejects input without saying why reads as broken.

### enrollments.html

The page that carries three rubric lines. It needs:

- A table: prefix, number, course name, credits, grade.
- The **GPA**, visible without scrolling, to two decimals: `{{ "%.2f"|format(gpa) }}`.
- A delete control per row - a POST form, not a link:
  ```jinja
  <form method="POST" action="{{ url_for('delete_enrollment', course_prefix=e.course_prefix, course_number=e.course_number) }}">
      {{ delete_form.hidden_tag() }}
      {{ delete_form.submit() }}
  </form>
  ```
- An **empty state**: with no enrollments, a sentence and a link to the create page. The grader signs up fresh, so this is the first authenticated page they see.

---

## Styling

`static/style.css` is the only stylesheet, already linked by `base.html`. No inline `style=` attributes, no second file, no CSS framework from a CDN - the Docker container may be run without network access.

Enough is enough: readable font, a max content width so text does not span a wide monitor, spacing between form fields, a table with visible row separation, and a distinguishable delete button. That is the whole budget. There are no points for visual design, and there are 10 each for the routes underneath.

Use the class names the templates already imply rather than inventing a system; a flat file of element and one-word class selectors is appropriate at this size.

---

## Accessibility and correctness

Cheap, and the kind of thing that goes wrong invisibly:

- **Every input has a label** - `{{ form.field.label }}` gives it to you.
- **Never `|safe`** on user input. `about` is free text a user typed; autoescaping is the only thing between it and a script tag.
- **The delete button says what it deletes**, or sits in the row it belongs to unambiguously.
- **`<title>` is per page** via the `title` variable, not one name for the whole app.

## Screenshots

The instructor is shown the running app, and PRs with visual changes carry a screenshot ([core_protocol.md](../protocol/core_protocol.md#pull-requests)). Keep the delivery set in `pics/` - signup, login, an empty enrollments page, a populated one showing the GPA, and the create form. They double as checkpoint material and as evidence in the test log.
