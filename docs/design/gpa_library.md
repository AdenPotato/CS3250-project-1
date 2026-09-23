# The gpa_calculator Library

A standalone Python package holding the GPA calculation, built with hatchling and **published to PyPI** so the app installs it with pip. Worth 10 rubric points, and the single riskiest item in the project because it depends on an external service and an account.

---

## Why it is separate

The assignment requires it. The engineering reason is sound anyway: the calculation is pure - enrollments in, a number out - with no Flask, no database and no session, which makes it the one part of the project that is trivial to test and reusable outside it.

**The library must not import from `app`.** It stands alone on PyPI, where `app` does not exist. That is why `GRADE_POINTS` is duplicated rather than imported ([app_protocol.md](../protocol/app_protocol.md#grade_points-lives-in-two-places)).

---

## The interface

```python
def calculate_gpa(enrollments) -> float:
    """Credit-weighted GPA over a list of dictionary-like enrollments."""
```

Each enrollment provides a `grade` (`'A+'` ... `'F'`) and `credits` (an int). The docstring in the baseline says "dictionary-like", and SQLAlchemy `Enrollment` objects are not dictionaries - they use attribute access, and `credits` lives on `enrollment.course`, not on the enrollment.

**Decide the shape and write it down**, because the app has to match it. Two workable options:

- **Dicts, and the route adapts.** `calculate_gpa([{'grade': e.grade, 'credits': e.course.credits} for e in current_user.enrollments])`. Keeps the library free of any assumption about the caller, matches the given docstring, and costs one comprehension in the route. **Recommended.**
- **Duck-typed attributes.** The library reads `e.grade` and `e.credits`, and the app passes objects exposing both. Cleaner call site, but it couples the library to a shape the app has to keep providing.

Pick one, make the docstring say exactly that, and test it that way.

## The algorithm

```
points = sum(GRADE_POINTS[grade] * credits for each graded enrollment)
hours  = sum(credits for each graded enrollment)
gpa    = points / hours
```

Behavior the docstring already commits to:

- An enrollment with **no grade yet** or an **unrecognized grade** is ignored - excluded from both sums, not counted as an F.
- **No graded credits returns 0**, not a `ZeroDivisionError`. The empty list is the first case to handle and the first case to test.
- **A+ is 4.3**, so a result above 4.0 is correct output.

Round for display in the template, not in the library. `calculate_gpa` returns the full float; the page shows `{{ "%.2f"|format(gpa) }}`.

---

## Packaging

`src/pyproject.toml` is the hatchling build config, with placeholders to fill:

```toml
[project]
name = "<your_name>lib"          # must be globally unique on PyPI
version = "0.0.1"
authors = [{ name="...", email="..." }]
description = "..."
readme = "README.md"
requires-python = ">=3.10"
```

- **The name must be unique on PyPI and is permanent.** Check availability at `pypi.org/project/<name>/` before building. Something like `gpa-calculator-cs3250-<team>` is safer than `gpalib`.
- **The distribution name and the import name can differ.** `name = "gpa-calculator-cs3250-team7"` installs a package you still `import gpa_calculator`. Say which is which in the README so the grader can install and import it.
- **Update `[project.urls]`** - the placeholders point at the PyPI sample project, not this repo.
- **`description` and `readme`** are what the PyPI page shows. `src/README.md` currently reads "This is my lib"; make it a real short README with an install line and a usage example.
- **Bump `version` on every upload.** PyPI refuses a re-upload of an existing version, permanently, even after a delete. A typo in `0.0.1` costs you `0.0.2`.

## Publishing

```
pip install build twine
cd src
python -m build                          # writes dist/
twine check dist/*
twine upload --repository testpypi dist/*   # rehearse here first
twine upload dist/*                          # the real one
```

**Rehearse on TestPyPI.** It is a separate account and a separate token, and it is where you find out the name is taken or the metadata is malformed - rather than burning a version number on the real index.

Authentication is an **API token**, not a password: create it at pypi.org -> Account settings -> API tokens, use `__token__` as the username and the `pypi-...` string as the password. Put it in `~/.pypirc` or `TWINE_PASSWORD`. **Never commit it.**

Then verify it round-trips, in a clean environment:

```
python -m venv /tmp/check && source /tmp/check/bin/activate.fish
pip install <your-dist-name>
python -c "from gpa_calculator import calculate_gpa; print(calculate_gpa([{'grade':'A','credits':3}]))"
```

That last command is the proof for the rubric. Screenshot it.

`/publish-lib` runs this sequence.

## Wiring it back into the app

Once published, `routes.py` drops the placeholder import:

```python
from gpa_calculator import calculate_gpa
```

and the distribution name goes in `requirements.txt` so the Docker build installs it from PyPI. That is what makes the package real rather than a file that happens to sit in the repo.

---

## Tests

`tests/test_gpa_calculator.py`. Cheap, and it covers the one thing a grader will hand-check:

| Case | Expect |
|---|---|
| empty list | `0` |
| one 3-credit A | `4.0` |
| 3-credit A + 1-credit F | `3.0` |
| 4-credit A + 1-credit A | `4.0` (weighting does not skew a uniform set) |
| 3-credit A+ | `4.3` (above 4.0 is legal) |
| an enrollment with `grade=None` | ignored, not an F |
| an unrecognized grade like `'S'` | ignored, not a crash |
| every grade ignored | `0`, not a `ZeroDivisionError` |

Work one of these by hand on paper and check the app's displayed GPA against it before the demo.
