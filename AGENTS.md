# CS3250 Project 1 - GPA Calculator

A Flask web application that lets a student sign in, record completed courses with letter grades, and see their credit-weighted GPA. Built for CS3250 (Software Development Methods and Tools) under a **Waterfall** process with a fixed rubric and a three-week delivery window.

**Stack (fixed by the assignment - not a choice):** Python 3.10+, Flask, Flask-SQLAlchemy, Flask-WTF, Flask-Login, bcrypt, Jinja2, SQLite. Plus a separate `gpa_calculator` library packaged with hatchling and published to PyPI.

This file is the entry point for every AI coding agent (Codex, Gemini, Cursor, Copilot, Claude Code and others). `CLAUDE.md` imports it, so edit the rules here, not there.

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
| `.agents/skills/` | Workflow skills, one `SKILL.md` per folder. |
| `.agents/agents/` | Role briefs: `app`, `ui`, `release`. |

## Rules that bind every session

1. **The rubric is the definition of done.** Every task maps to a rubric line in [process_protocol.md](docs/protocol/process_protocol.md#rubric-tracker). Work that maps to nothing is out of scope until a teammate says otherwise.
2. **Never break a graded artifact to make a change convenient.** The route names, the model fields, and the project layout come from the assignment; changing one needs a stated reason.
3. **Write the test and the manual log entry.** `pytest` for logic, and the [manual test log](docs/testing/test_log.md) for anything a grader will click. See [Testing](docs/protocol/process_protocol.md#testing).
4. **Never commit to `main`.** `main` is protected and is reached only by merging `dev`. See [Branching](docs/protocol/core_protocol.md#branching).
5. **Never commit secrets or the database.** `.venv/`, `instance/prj1.db`, and `__pycache__/` stay out of version control. The `app.secret_key` in the baseline is a placeholder - read it from the environment before delivery.
6. **Ask when the requirement is ambiguous.** The assignment is the source of truth; when it is silent, ask a teammate rather than inventing a requirement.
7. **AI agents never commit.** No AI agent runs `git commit`, `git push`, or `git merge`, or opens or merges PRs - it edits files and a teammate reviews and commits them. Never add a `Co-Authored-By` trailer or a "Generated with" line for any AI tool to a commit message, PR, or issue, including drafts written for a teammate.

## Skills

Skills live in `.agents/skills/<name>/SKILL.md`. When a skill or doc says `/new-model`, it means "read and follow `.agents/skills/new-model/SKILL.md`". Read the whole skill before starting its first step.

| Skill | Use when |
|---|---|
| `session-start` | Opening a working session, before any code. |
| `project-status` | Reporting where the project stands against the rubric. |
| `new-design` | A requirement is ambiguous, or a change touches model, route and template at once. |
| `new-route` | Replacing a "Work in progress..." stub or adding a page. |
| `new-model` | Changing `User`, `Course` or `Enrollment`. |
| `uml` | Writing or refreshing the PlantUML diagrams. |
| `test-log` | Recording manual test results. |
| `qa-steps` | Writing a QA script for the tester. |
| `new-issue` | Opening a GitHub issue a teammate approved. |
| `publish-lib` | Building and publishing `gpa_calculator` to PyPI. |
| `deliver` | Docker build, delivery checklist, merging `dev` into `main`. |
| `phase` | Moving the Waterfall phase marker once a phase closes. |
| `log-work` | Writing the end-of-day changelog entry. |

## Roles

For focused work, take on the matching brief in `.agents/agents/`: `app.md` for anything under `src/`, `ui.md` for `templates/` and `static/`, `release.md` for Docker, PyPI, requirements and branch protection.

## Guardrails

Claude Code enforces these through `.claude/settings.json`. Other tools must follow them by hand.

- **Never read** `.env` files, `.pypirc`, `*.pem`, `*.key`, or `instance/*.db`.
- **Never run** `git push --force` (or `-f`, `--force-with-lease`), `git push origin main`, or `twine upload`.
- **Ask first** before `gh issue create`, `gh pr create`, `gh pr merge`, creating a branch, `git merge`, `docker build`, `docker run`, `python -m build`, or deleting `src/instance/prj1.db`.
- **Free to run:** `pytest`, `flask --app app run`, `python init_db.py`, `pip install -r requirements*.txt`, and read-only git (`status`, `diff`, `log`, `branch`).

## Running the app

From `src/`:

```bash
python init_db.py                 # create and load the database
flask --app app run --debug       # serve on http://127.0.0.1:5000
```

## Writing style

Plain, specific, lowercase-first prose in docs and comments. No em-dashes - use a hyphen with spaces. Say what the code does and why it is there; skip decoration. Comments cap at three lines; anything longer belongs in a doc under `docs/` with a link.
