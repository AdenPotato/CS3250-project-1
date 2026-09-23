# CS3250 Project 1 - GPA Calculator

A Flask web application that lets a student sign in, record completed courses with letter grades, and see their credit-weighted GPA. Built for CS3250 (Software Development Methods and Tools) under a **Waterfall** process with a fixed rubric and a three-week delivery window.

**Stack (fixed by the assignment - not a choice):** Python 3.10+, Flask, Flask-SQLAlchemy, Flask-WTF, Flask-Login, bcrypt, Jinja2, SQLite. Plus a separate `gpa_calculator` library packaged with hatchling and published to PyPI.

## Where things are

| Path | What |
|---|---|
| [docs/README.md](docs/README.md) | Doc hub - start there. |
| [docs/protocol/process_protocol.md](docs/protocol/process_protocol.md) | The Waterfall phases, team roles, the rubric tracker, the checkpoint. |
| [docs/protocol/core_protocol.md](docs/protocol/core_protocol.md) | Python style, git model, commits, the PR checklist. |
| [docs/protocol/app_protocol.md](docs/protocol/app_protocol.md) | Flask rules: routes, models, forms, templates, the database. |
| [docs/design/](docs/design) | Requirements, use cases, data model, routes, the library, the UI. |
| `src/app/` | The application package: `__init__.py`, `models.py`, `routes.py`, `forms.py`. |
| `src/gpa_calculator/` | The publishable GPA library. |
| `templates/`, `static/` | Jinja templates and `style.css`. |
| `uml/` | PlantUML sources: `use_case.wsd`, `class.wsd`. |

## Rules that bind every session

1. **The rubric is the definition of done.** Every task maps to a rubric line in [process_protocol.md](docs/protocol/process_protocol.md#rubric-tracker). Work that maps to nothing is out of scope until a teammate says otherwise.
2. **Never break a graded artifact to make a change convenient.** The route names, the model fields, and the project layout come from the assignment; changing one needs a stated reason.
3. **Write the test and the manual log entry.** `pytest` for logic, and the [manual test log](docs/testing/test_log.md) for anything a grader will click. See [Testing](docs/protocol/process_protocol.md#testing).
4. **Never commit to `main`.** `main` is protected and is reached only by merging `dev`. See [Branching](docs/protocol/core_protocol.md#branching).
5. **Never commit secrets or the database.** `.venv/`, `instance/prj1.db`, and `__pycache__/` stay out of version control. The `app.secret_key` in the baseline is a placeholder - read it from the environment before delivery.
6. **Ask when the requirement is ambiguous.** The assignment is the source of truth; when it is silent, ask a teammate rather than inventing a requirement.

## Writing style

Plain, specific, lowercase-first prose in docs and comments. No em-dashes - use a hyphen with spaces. Say what the code does and why it is there; skip decoration. Comments cap at three lines; anything longer belongs in a doc under `docs/` with a link.
