# Docs

The hub. This page links; the content lives in the leaf docs and is defined once.

**The project:** a Flask web app that lets a student record completed courses with letter grades and see their credit-weighted GPA, plus a `gpa_calculator` library published to PyPI. Built for CS3250 under a Waterfall process on a three-week clock. Repo entry point is [CLAUDE.md](../CLAUDE.md).

---

## Start here

1. **[requirements.md](design/requirements.md)** - what the app must do. Five requirements, the constraints, and what is out of scope.
2. **[process_protocol.md](protocol/process_protocol.md)** - the Waterfall phases, team roles, the testing stance, and the **rubric tracker** that defines done.
3. **[schedule.md](planning/schedule.md)** - the dates, the roles, the current phase, and the standing items worth -30 if missed.
4. **[core_protocol.md](protocol/core_protocol.md)** - environment setup, how to run it, Python style, branching, commits.
5. **[app_protocol.md](protocol/app_protocol.md)** - the Flask rules: routes, models, forms, templates, the database.

## protocol/

| File | Purpose |
|---|---|
| [process_protocol.md](protocol/process_protocol.md) | Waterfall phases, checkpoint, team roles, testing, rubric tracker. |
| [core_protocol.md](protocol/core_protocol.md) | Environment, running the app, Python style, git, commits, PRs. |
| [app_protocol.md](protocol/app_protocol.md) | Layout, the app object, models, routes, forms, templates, the data load. |

## design/

| File | Purpose |
|---|---|
| [requirements.md](design/requirements.md) | The five requirements, constraints, risks, out of scope. |
| [use_cases.md](design/use_cases.md) | Actors and eight use cases, behind `uml/use_case.wsd`. |
| [data_model.md](design/data_model.md) | User, Course, Enrollment, the grade scale, behind `uml/class.wsd`. |
| [routes.md](design/routes.md) | Every route: methods, auth, form, template, and what it does. |
| [gpa_library.md](design/gpa_library.md) | The `gpa_calculator` interface, algorithm, packaging, and PyPI publishing. |
| [ui.md](design/ui.md) | Templates, the stylesheet, and what is worth styling. |

## planning/ · testing/ · deployment/

| File | Purpose |
|---|---|
| [schedule.md](planning/schedule.md) | Schedule table, team roles, current phase, standing items. |
| [testing/test_log.md](testing/test_log.md) | The graded manual test table and the coverage checklist. |
| [deployment/docker.md](deployment/docker.md) | The Dockerfile, build and run, the final delivery checklist. |
| [changelog.md](changelog.md) | Rolling work log, newest first. |

---

## Skills

Slash commands, in `.claude/skills/<name>/SKILL.md`.

| Skill | Purpose |
|---|---|
| `/project-status` | Where the project stands: phase, rubric rows, remaining TODOs in the code. |
| `/phase` | Advance the Waterfall phase once its deliverable is actually done. |
| `/new-route` | Scaffold a route with its form, template and test log rows. |
| `/new-model` | Change a model, reset the database, update the class diagram. |
| `/uml` | Write or refresh the PlantUML use case and class diagrams. |
| `/test-log` | Add manual test result rows from a session of testing. |
| `/publish-lib` | Build `gpa_calculator` and publish it to TestPyPI then PyPI. |
| `/deliver` | Build and run the Docker image and walk the delivery checklist. |
| `/log-work` | End-of-day changelog entry. |

## Agents

| Agent | Owns |
|---|---|
| `app` | `src/app/` and `src/gpa_calculator/` - routes, models, forms, the calculation. |
| `ui` | `templates/` and `static/style.css`. |
| `release` | The Dockerfile, PyPI packaging, branch protection, delivery. |

---

## Tree

```
CLAUDE.md              entry point and the rules that bind every session
docs/
  README.md            this hub
  protocol/            process, core, app
  design/              requirements, use_cases, data_model, routes, gpa_library, ui
  planning/            schedule.md (dates, roles, current phase)
  testing/             test_log.md (the graded manual test table)
  deployment/          docker.md (build, run, final checklist)
  changelog.md         newest-first work log
.claude/
  agents/              app, ui, release
  skills/              9 slash commands
```
