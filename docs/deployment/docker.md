# Deployment - Docker

The delivery mechanism. The instructor builds the image and runs the app as a container, so **the build has to succeed from a clean clone on a machine that is not yours.** Worth 5 rubric points.

---

## The Dockerfile

It goes in the repository root, and the repo does not have one yet. Shape:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# dependencies first, so a code change does not reinstall them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY templates/ ./templates/
COPY static/ ./static/

WORKDIR /app/src
ENV FLASK_APP=app
EXPOSE 5000

# seed the catalog, then serve on all interfaces so the port mapping works
CMD ["sh", "-c", "python init_db.py && flask run --host=0.0.0.0 --port=5000"]
```

Things that will bite:

- **`--host=0.0.0.0` is mandatory.** Flask's default binds loopback inside the container, and `-p 5000:5000` then maps to nothing. This is the single most common reason a container "starts fine" and the page never loads.
- **Templates and static live outside `src/`** in this layout, but Flask resolves them relative to the app's root path. Copy them so the tree inside the image matches the repo, and confirm a page actually renders in the container rather than assuming it.
- **`requirements.txt` must list the published `gpa_calculator` distribution** once it is on PyPI, or the import fails at runtime in a way it never does on your machine, where the package is on the path.
- **The database is created inside the container** and dies with it. That is acceptable here - `init_db.py` runs at startup, and the grader signs up fresh. If data should survive a restart, mount a volume over `/app/src/instance`.
- **`.dockerignore`** keeps `.venv/`, `.git/`, `__pycache__/` and `instance/` out of the build context. Without it the build is slow and may copy a local database into the image.
- **Do not bake the secret key in.** Read it from the environment ([app_protocol.md](../protocol/app_protocol.md#the-app-object)) and pass it at run time: `-e SECRET_KEY=...`, with the dev fallback covering the grader who does not.

## Build and run

```
docker build -t gpa-calculator .
docker run --rm -p 5000:5000 -e SECRET_KEY=change-me gpa-calculator
```

Then open `http://localhost:5000`.

`/deliver` runs this and checks the app answers.

---

## Before you call it delivered

Test it the way the instructor will, which is not the way you have been testing it.

1. **Clone fresh, somewhere else.** `git clone <url> /tmp/delivery-check && cd /tmp/delivery-check`. This catches the file you never committed - the most common delivery failure by a wide margin.
2. `docker build -t gpa-calculator .` with no cache: add `--no-cache` at least once.
3. `docker run --rm -p 5000:5000 gpa-calculator`.
4. In a browser: sign up, sign in, create two enrollments, check the GPA against arithmetic you did by hand, update a grade, delete one, sign out.
5. Record it in the [test log](../testing/test_log.md) under Deployment.
6. Screenshot the running container and the app.

## Final delivery checklist

- [ ] Dockerfile and `.dockerignore` committed at the repo root
- [ ] Fresh-clone build succeeds
- [ ] Container runs and every requirement works in it
- [ ] `gpa_calculator` published to PyPI and installed from there by `requirements.txt`
- [ ] README states the repo URL, how to build and run, and the PyPI package name
- [ ] UML diagrams committed as source and rendered images
- [ ] Manual test log complete, failures and their retests included
- [ ] Screenshots in `pics/`
- [ ] `dev` merged into protected `main`
- [ ] All members submitted the team/self evaluation

The last two are worth -30 between them if missed. Check them last and check them twice.
