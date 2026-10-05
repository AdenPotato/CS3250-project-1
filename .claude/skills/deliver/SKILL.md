---
name: deliver
description: Build and run the Docker image from a clean clone, walk the final delivery checklist, and merge dev into protected main. Use in the Deployment phase and for any change to the Dockerfile.
---

# /deliver

Get the project into the state the instructor receives it in. Reference: [docker.md](../../../docs/deployment/docker.md).

The rule that makes this skill worth running: **build from a fresh clone, not from your working tree.** The uncommitted file is the most common delivery failure and it is invisible from where you are sitting.

## 1. The Dockerfile

If there is none, write it per [docker.md](../../../docs/deployment/docker.md#the-dockerfile). Non-negotiables:

- `--host=0.0.0.0` in the `CMD`. Flask's default binds loopback inside the container and the port mapping then reaches nothing. This is the single most common "it builds but the page never loads".
- `requirements.txt` copied and installed **before** the source, so a code change does not reinstall dependencies.
- `templates/` and `static/` copied - they live outside `src/` in this layout.
- `init_db.py` run at startup so the catalog exists.
- No secret key baked in; read it from the environment.
- A `.dockerignore` covering `.venv/`, `.git/`, `__pycache__/`, `instance/`.

## 2. Build clean

```
git clone <repo-url> /tmp/delivery-check
cd /tmp/delivery-check
docker build --no-cache -t gpa-calculator .
docker run --rm -p 5000:5000 -e SECRET_KEY=delivery-check gpa-calculator
```

A failure here is almost always a missing commit. Fix it by committing the file, not by copying it in.

## 3. Walk every requirement inside the container

At `http://localhost:5000`, as the grader would:

- Sign up a new student, sign in.
- Create two enrollments with different credit values.
- Check the GPA against arithmetic you do by hand.
- Change one grade by re-creating that enrollment.
- Delete one; confirm the GPA recomputes.
- Sign out; confirm `/enrollments` redirects to login.

Record every one of these in [test_log.md](../../../docs/testing/test_log.md).

## 4. The checklist

Walk [the final delivery checklist](../../../docs/deployment/docker.md#final-delivery-checklist) top to bottom and report each item. Do not mark one done without checking it.

Two carry penalties rather than points, and they are worth **-30 combined**:

- **`main` protected** - `gh api repos/:owner/:repo/branches/main/protection`, or check Settings -> Branches.
- **Team/self evaluation submitted by every member.** The grade is held until all of them are in. Remind the team by name.

## 5. Merge to main

Only once `dev` is stable and the checklist is clean:

```
git switch main && git pull
git merge dev
git push
```

`main` is protected, so this goes through a PR. Never commit to `main` directly.

## 6. Report

State what passed, what failed, and what is still outstanding on the checklist. If something is not deliverable, say so plainly rather than marking it done - the point of this skill is to find that out before the instructor does.
