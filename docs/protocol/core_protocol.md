# Core Protocol - Python, git, commits

The shared development core: how Python is written here, how branches and commits work, and what has to be true before a change is handed to a teammate. Flask specifics live in [app_protocol.md](app_protocol.md); phases, roles and the rubric live in [process_protocol.md](process_protocol.md).

---

## Environment

A virtual environment per clone, never committed.

```
python -m venv .venv
source .venv/bin/activate.fish     # bash/zsh: source .venv/bin/activate
pip install -r requirements.txt
```

`requirements.txt` is the dependency source. It currently pins nothing, which is fine for a three-week project but means two teammates can resolve different versions. If a version difference ever causes a bug, pin the whole file with `pip freeze > requirements.txt` and say so in the changelog.

Dependencies the assignment fixes: `flask`, `flask-wtf`, `flask-sqlalchemy`, `flask-login`, `bcrypt`. Adding anything else needs a reason - the grader runs `pip install -r requirements.txt` and then the Docker build, and every addition is a thing that can fail there.

Development-only additions (`pytest`, `pytest-flask`) go in `requirements-dev.txt` so the runtime image stays thin.

## Running it

```
cd src
flask --app app run --debug        # http://127.0.0.1:5000
python init_db.py                  # load the course catalog (run once, after a model change)
```

The database lands at `src/instance/prj1.db`. It is disposable: delete it and re-run `init_db.py` whenever the model changes. It is never committed.

### Expect a template path problem on the first run

The baseline creates the app as `Flask("GPA Calculator Web App")` rather than `Flask(__name__)`. That string is not an importable module, so Flask cannot locate a package directory for it and falls back to the **current working directory** as the application root. Templates and static files are then looked for under wherever you launched the process.

Meanwhile `templates/` and `static/` sit at the **repo root**, a level above `src/`. So `cd src && flask --app app run` will look for `src/templates/` and raise `TemplateNotFound` on the first page that renders one.

Confirm this on the first run rather than taking it on faith, then fix it once, deliberately, and tell the team which way you went:

| Fix | Cost |
|---|---|
| Pass explicit folders: `Flask(__name__, template_folder='../../templates', static_folder='../../static')` | One line, keeps the assignment's directory tree exactly as specified. **Preferred.** |
| Move `templates/` and `static/` under `src/` | Cleanest Flask layout, but it departs from the tree the assignment prints. |
| Always launch from the repo root with `src` on `PYTHONPATH` | No code change, but every teammate and the Dockerfile must remember it. Fragile. |

Whatever you pick, the Dockerfile has to match it ([docker.md](../deployment/docker.md)). Settle this before Construction gets going - it blocks every template-rendering route, which is nearly all of them.

---

## Python style

The assignment does not mandate a formatter, so the rule is consistency with the baseline files rather than a tool.

- **4-space indent, snake_case** for functions and variables, `PascalCase` for model and form classes, `UPPER_SNAKE` for module constants such as `GRADE_POINTS`.
- **Module docstrings stay.** Every file in `src/` opens with the course header docstring (course, instructor, students, description). Fill in the student names; do not delete the block - it is how the instructor identifies the work.
- **Imports grouped** standard library, third party, then local `app.*` / `gpa_calculator`, each group separated by a blank line. `src/app/__init__.py` is the documented exception: its imports are deliberately ordered by initialization sequence (app, then db, then models, then login manager, then routes) because moving them breaks the circular-import dance Flask's application factory pattern avoids. Leave that file's order alone.
- **Type hints on the library, optional in the app.** `gpa_calculator` is published to PyPI and read by strangers, so its public functions are annotated. Flask route handlers are not required to be.
- **Docstrings on anything published or non-obvious** - every public function in `gpa_calculator`, and any route whose behavior is not clear from its name.
- **No em-dashes** in code, comments, docstrings or docs. Use a hyphen with spaces.

### Comments

Cap at three lines. Say why, not what - the code already says what.

```python
# grade points for the traditional college letter grade scale, A+ included (so GPA can exceed 4.0)
GRADE_POINTS = { ... }
```

Do not copy a requirement or a design decision into a comment; link the doc instead. A comment that restates a doc drifts from it within a week.

---

## Branching

Three kinds of branch, and one of them is off limits.

| Branch | Who | Rule |
|---|---|---|
| `main` | nobody directly | Protected. Reached only by merging `dev` once `dev` is stable. Never commit here. |
| `dev` | everyone, via merge | The integration branch. All work lands here first. |
| `<name>-<short-slug>` | one person | A short-lived local branch off `dev` for one task. Delete it after merge. |

The assignment requires the protected `main` and deducts 5 points if it is missing, so protection is set up in the **Planning** phase, not at the end. GitHub: Settings -> Branches -> add a rule for `main` requiring a pull request before merging.

**The loop:**

1. `git switch dev && git pull`
2. `git switch -c aden-gpa-calc`
3. Work. Commit in small steps.
4. Run the checks below.
5. `git push -u origin aden-gpa-calc`, open a PR into `dev`.
6. A teammate reviews, then merges into `dev`.
7. When `dev` is stable and a phase closes, open `dev` -> `main` and merge it.

**Never rewrite pushed history.** No `push --force` on a shared branch; the repo settings deny it.

### Before you push

- The app starts: `flask --app app run` with no traceback.
- The page you changed loads in a browser and does the thing.
- `pytest` passes, if the change touched `gpa_calculator` or any logic with tests.
- The manual test log has a row for any behavior a grader will click ([test_log.md](../testing/test_log.md)).
- No `.venv/`, no `instance/prj1.db`, no `__pycache__/` in the diff. Check with `git status` before `git add`.

---

## Commits

One logical change per commit, present tense, lowercase, no trailing period.

```
implement calculate_gpa with credit weighting
add enrollment list route and template
load 8 courses in init_db
fix grade dropdown losing selection on validation error
```

Reference an issue when there is one: `implement calculate_gpa with credit weighting (#4)`.

Do not commit commented-out code, a stray `print`, or a `TODO` without a name attached to it. The baseline ships with `# TODO` markers from the instructor; replacing one is the work, so a commit that touches a TODO should remove it.

---

## Pull requests

A PR into `dev` carries:

- **What changed**, in two or three sentences.
- **Which rubric line** it advances ([the tracker](process_protocol.md#rubric-tracker)).
- **How it was tested** - the pytest run, the manual test log rows, or both.
- **A screenshot** for anything visual. The rubric is graded partly on what the instructor sees.

One teammate reviews before merge. The reviewer's job is to pull the branch and run it, not only to read the diff - this project is graded on behavior.
