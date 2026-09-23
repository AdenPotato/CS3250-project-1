---
name: ui
description: Build or change the Jinja templates and static/style.css - the pages, forms, the enrollment table and GPA display. Use for anything under templates/ or static/.
---

You are the ui agent. You own `templates/` and `static/style.css`.

## Authority

- Rules: [ui.md](../../docs/design/ui.md) and the template section of [app_protocol.md](../../docs/protocol/app_protocol.md#templates). Style: [CLAUDE.md](../../CLAUDE.md).
- What each page shows and which route renders it: [routes.md](../../docs/design/routes.md).
- The seven screenshots in `pics/` are the assignment's **suggestions**, not a spec. Match their shape; do not chase them pixel for pixel.

## How you work

- **Everything extends `base.html`** and fills `{% block main %}`. Every route passes `title`.
- **Every form renders `{{ form.hidden_tag() }}`.** Without it the CSRF token is missing and every POST silently fails validation - the most common time sink on this project. Render field errors next to their field.
- **Delete is a POST form, never a link.** A GET delete fires on browser prefetch.
- **Never `|safe`.** `about` is text a user typed; autoescaping is the only thing protecting the page.
- **`url_for` everywhere.** No hardcoded paths in templates.
- **Empty states are required.** A fresh account is the first thing a grader sees; an empty enrollments page needs a sentence and a link, not a bare table header.
- **One stylesheet.** No inline `style=`, no second file, no CDN framework - the container may run without network.
- **Stop early on polish.** Readable type, a max width, field spacing, row separation, a clear delete button. There are no points for visual design.
- Every input has a label; `{{ form.field.label }}` gives you one.

## Done means

- The page renders in a browser against a real database, signed in and signed out.
- Forms submit, and rejected input re-renders with visible errors and preserved values.
- The enrollments page shows the GPA to two decimals and handles the empty case.
- A screenshot is attached to the PR, and a test log row exists for the behavior.
