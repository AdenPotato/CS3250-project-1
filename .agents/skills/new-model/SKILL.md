---
name: new-model
description: Change a SQLAlchemy model - edit models.py, reset the SQLite database, reload the catalog, and update the class diagram and the data model doc together. Use for any change to User, Course or Enrollment.
---

# /new-model

A model change is not just an edit to `models.py`. There are no migrations here - `db.create_all()` creates missing tables and **silently ignores a changed column** - so every teammate has to reset their database, and two documents have to move with the code.

## Before changing anything

Ask whether it should change at all. `User`, `Course` and `Enrollment` and their fields come from the assignment, and the composite key on `Course` is load-bearing. A change that is convenient for a route is usually the route's problem. State the reason.

If the project is past Modeling, say so - changing the model during Construction is what the checkpoint exists to prevent, and it invalidates the class diagram that was already presented.

## Steps

1. **Edit `src/app/models.py`.** Keep the course header docstring. Composite foreign keys need a `ForeignKeyConstraint`, not two column-level FKs.

2. **Reset the database.**
   ```
   rm -f src/instance/prj1.db
   cd src && python init_db.py
   ```
   Confirm it prints the expected course count and does not raise.

3. **Check what the change broke.** Grep for every use of the changed field:
   ```
   grep -rn "<field>" src/ templates/
   ```
   Routes, forms, templates, and `init_db.py` all touch model fields directly.

4. **Update [data_model.md](../../../docs/design/data_model.md)** - the entity table, the relationships, and anything about the grade scale. The doc and the code are checked against each other at the checkpoint.

5. **Update `uml/class.wsd`** to match, and re-render it (`/uml`). A class diagram that disagrees with `models.py` is worth fewer than 5 points.

6. **Run it.** Start the app, sign up, create an enrollment, check the GPA. A model change breaks things far from where it was made.

7. **Add test log rows** for what you re-verified.

## The PR

Say in the body, in the first line: **"Model change - delete `src/instance/prj1.db` and re-run `python init_db.py` after pulling."** Every teammate's database is now stale, and they will hit a confusing error if they do not read it.
