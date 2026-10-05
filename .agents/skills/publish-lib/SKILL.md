---
name: publish-lib
description: Build the gpa_calculator package with hatchling and publish it to TestPyPI then PyPI, then verify it installs from a clean venv. Use for the PyPI rubric item and every version bump after it.
---

# /publish-lib

Ship `src/gpa_calculator/` to PyPI. Worth **10 rubric points**, and it depends on an external service, a unique name and an API token - so do it in week two, not delivery week. Full reference: [gpa_library.md](../../../docs/design/gpa_library.md).

## Preflight

Stop on any of these before building:

1. **`calculate_gpa` is implemented** and `pytest tests/test_gpa_calculator.py` passes. Publishing `return 0` wastes a version number.
2. **The library imports nothing from `app`.** `grep -n "from app" src/gpa_calculator/*.py` must be empty - `app` does not exist on PyPI.
3. **`src/pyproject.toml` has no placeholders left** - `name`, `authors`, `description`, and `[project.urls]` all still point at the sample project as shipped.
4. **The name is free.** Check `pypi.org/project/<name>/` returns 404. The name is permanent, so prefer something specific like `gpa-calculator-cs3250-<team>` over `gpalib`.
5. **The version is new.** PyPI refuses a re-upload of an existing version forever, even after a delete. Bump `version` in `pyproject.toml` for every upload.
6. **`src/README.md` is real.** It is the PyPI page. The baseline says "This is my lib" - replace it with an install line and a usage example.

## Build

```
pip install build twine
cd src
rm -rf dist/
python -m build
twine check dist/*
```

`twine check` catches malformed metadata before an upload burns a version.

## Rehearse on TestPyPI

Separate account, separate token, and where you find out something is wrong for free.

```
twine upload --repository testpypi dist/*
pip install --index-url https://test.pypi.org/simple/ --no-deps <dist-name>
```

## Publish

```
twine upload dist/*
```

Authentication is an **API token**, never a password: username `__token__`, password the `pypi-...` string, from pypi.org -> Account settings -> API tokens. Keep it in `~/.pypirc` or `TWINE_PASSWORD`. **Never commit it, never paste it into a file in the repo.**

## Verify the round trip

This is the evidence for the rubric. Do it in a clean environment, not your working one:

```
python -m venv /tmp/pypi-check
source /tmp/pypi-check/bin/activate.fish
pip install <dist-name>
python -c "from gpa_calculator import calculate_gpa; print(calculate_gpa([{'grade':'A','credits':3}]))"
```

Expect `4.0`. **Screenshot it** into `pics/`.

Note that the distribution name and the import name can differ - `pip install gpa-calculator-cs3250-team7` then `import gpa_calculator`. Say which is which in the project README so the grader can follow it.

## Wire it back in

1. Add the **distribution name** to `requirements.txt` so the Docker build installs it from PyPI.
2. In `src/app/routes.py`, replace the commented placeholder import with `from gpa_calculator import calculate_gpa`.
3. Delete the duplicated `GRADE_POINTS` from `src/app/models.py` and import it from the library instead; point `forms.py`'s grade choices at the same source.
4. Run the app and check a GPA still displays.
5. Add test log rows under Deployment, and mark the rubric row `done`.
