# Manual Test Log

The Testing phase deliverable, worth 5 rubric points. The assignment asks for manual testing documented in a table, so this file is the graded artifact - the pytest suite is a separate, ungraded safety net ([process_protocol.md](../protocol/process_protocol.md#testing)).

Add rows with `/test-log`.

---

## Results

| Functionality Tested | Date | Time | Tester | Result | Notes |
|---|---|---|---|---|---|
| | | | | | |
| Deployment - Docker Container Run | 2026-10-02 | 21:15 | Isabella Eaton | failed | Built image and ran container on port 5000. App crashed on GET `/` with `TemplateNotFound: index.html` because templates were missing from `/app/src/app/templates/`. |
| Deployment - Docker Container Run | 2026-10-02 | 21:25 | Isabella Eaton | passed | Updated Dockerfile to copy `templates/` and `static/` to `/app/src/app/`. Re-built with `--no-cache` and verified app loads cleanly at `http://localhost:5000` with signup, CRUD, and GPA calculation working. |
| Sign up with valid details | 2026-10-03 | 15:01 | Claude Code (HTTP requests, no browser) | passed | POST `/users/signup` with id `qa150112`, name, about and matching passwords, CSRF token from the form. Expected a redirect to login; got 302 to `/users/login`, and the account then signed in. |
| Sign up with a duplicate id | 2026-10-03 | 15:01 | Claude Code (HTTP requests, no browser) | passed | Submitted id `qa150112` a second time with a different name and password. Expected the form back with a message; got 200 with "That id is already taken." and the typed id kept in the field. |
| Sign up with mismatched passwords | 2026-10-03 | 15:01 | Claude Code (HTTP requests, no browser) | passed | Id `qa150112b`, confirm password one character off. Expected a rejection; got 200 with "Passwords must match.", and signing in as `qa150112b` afterwards failed, so no account was created. |
| Sign up with a blank form | 2026-10-03 | 15:01 | Claude Code (HTTP requests, no browser) | passed | All fields empty. Expected a required message per field; got 200 with "This field is required." on id, name, password and confirm password. |
| Sign up without a CSRF token | 2026-10-03 | 15:01 | Claude Code (HTTP requests, no browser) | passed | Valid details, no `csrf_token` field. Expected no account; got the form back with 200, and signing in with those details failed. |
| Sign in with correct credentials | 2026-10-03 | 15:01 | Claude Code (HTTP requests, no browser) | passed | Id `qa150112` and its password. Expected the enrollments page; got 302 to `/enrollments`, which then returned 200. |
| Sign in with a wrong password | 2026-10-03 | 15:01 | Claude Code (HTTP requests, no browser) | passed | Id `qa150112`, wrong password. Expected a message that does not say which field was wrong; got 200 with "Invalid id or password.", and `/enrollments` still redirected to login. |
| Sign in with an unknown id | 2026-10-03 | 15:01 | Claude Code (HTTP requests, no browser) | passed | An id that was never signed up. Expected the same message as a wrong password; got 200 with "Invalid id or password." - identical text. |
| Sign out ends the session | 2026-10-03 | 15:01 | Claude Code (HTTP requests, no browser) | passed | GET `/users/signout` while signed in. Expected the landing page and a dead session; got 302 to `/index.html`, then `/enrollments` redirected to `/users/login?next=%2Fenrollments`. A second student signed in from another session stayed signed in. |
| Enrollments page for a new account - empty state | 2026-10-03 | 15:01 | Claude Code (HTTP requests, no browser) | passed | Signed in as the new `qa150112`. Expected a sentence and a link, not a bare table; got 200 with "You have no enrollments yet.", a link to `/enrollments/create`, and no table. No GPA line yet - that is #16. |
| Signed-out access to protected routes | 2026-10-03 | 15:01 | Claude Code (HTTP requests, no browser) | passed | With no session: GET `/enrollments`, GET `/enrollments/create`, POST `/enrollments/delete/CS/3250`, GET `/users/signout`. Expected a redirect to login for each; all four returned 302 to `/users/login?next=...`. |
| Course load on an empty database | 2026-10-03 | 19:59 | Claude Code (command line) | passed | Fresh copy of `src/` with no `instance/` folder, then `python init_db.py`. Expected the tables created and 5 or more courses loaded; it printed "Loaded 8 courses, 8 in the catalog." and exited 0. A query afterwards returned all 8 with prefix, number, name and credits. |
| Course load run a second time | 2026-10-03 | 19:59 | Claude Code (command line) | passed | `python init_db.py` again on the same database. Expected no primary-key error and no duplicates; it printed "Loaded 0 courses, 8 in the catalog." and exited 0. |
| Enrollments page lists every enrollment | 2026-10-03 | 20:00 | Claude Code (HTTP requests, no browser) | passed | Fresh database. Signed up `qa_ana`, gave her MTH 2140 B+, CS 3250 A- and ENG 1010 C. Expected three rows with prefix, number, name, credits and grade; got 200 with CS 3250 / Software Development Methods and Tools / 4 / A-, ENG 1010 / Composing Arguments / 3 / C, MTH 2140 / Computational Matrix Algebra / 2 / B+, sorted by prefix and number, each with a delete form to its own course and a CSRF token, and no empty-state sentence. The enrollments were inserted through the `Enrollment` model, not the create page - that page is still a stub (#13). |
| Second student sees only their own enrollments | 2026-10-03 | 20:00 | Claude Code (HTTP requests, no browser) | passed | Same database, `qa_ben` signed in from a separate session with CS 1050 A and CS 3250 D+ (inserted the same way). Expected two rows and none of `qa_ana`'s; got 200 with exactly CS 1050 A and CS 3250 D+ - his own D+ on the shared course, not her A-. `/enrollments?user_id=qa_ana` returned the same two rows. |
| Delete an enrollment - row removed | 2026-10-03 | 21:50 | Johnny De La Garza | passed | Branch `14-johnny-delete-enrollment`, Firefox. Signed in as `johnny` with CS 3250 and MTH 1410 enrolled. Clicked Delete on CS 3250 and confirmed. Expected a return to the list without that row; got `/enrollments` with only MTH 1410 left. |
| Delete the last enrollment - empty state returns | 2026-10-03 | 21:50 | Johnny De La Garza | passed | Deleted MTH 1410, the only remaining row. Expected the empty state; got "You have no enrollments yet." with no table. |
| Delete leaves the course in the catalog | 2026-10-03 | 21:50 | Johnny De La Garza | passed | After both deletes, queried the Course table. Expected CS 3250 and MTH 1410 to still exist; both were listed. Re-enrolling could not be tried yet because the add-grade page (create enrollment) is not built. |
The 2026-10-03 15:01 rows were run on branch `11-aden-auth-routes` as HTTP requests against the dev server (`flask --app app run`), reading the returned status, redirect and page text. Nothing was looked at in a browser, so the page layout is not covered by them.

The 2026-10-03 19:59 and 20:00 rows were run on branch `10-aden-course-load` against a copy of the app with an empty database, the 20:00 rows the same way as the 15:01 ones. A browser pass over the populated list, with rows made on the create page, is still owed once #13 lands.

Result is `passed` or `failed`. A `failed` row **stays in the table** - delete nothing. When it is fixed, add a new row for the retest and reference the failure. A log with no failures in it reads as a log nobody actually used.

---

## Coverage checklist

Every requirement needs at least one row before delivery. Tick these off against the table above.

### R1 - Authentication

- [x] Sign up with valid details creates the account
- [x] Sign up with a duplicate id is rejected with a message
- [x] Sign up with mismatched passwords is rejected
- [x] Sign in with correct credentials reaches the enrollments page
- [x] Sign in with a wrong password is rejected, and the message does not reveal which field was wrong
- [x] Sign in with an unknown id is rejected the same way
- [x] Sign out ends the session; going back to `/enrollments` redirects to login

### R2 - View enrollments

- [x] A new account sees the empty state, not a bare table
- [x] After creating enrollments, all of them are listed with prefix, number, name, credits and grade
- [x] Signed in as a second student, only that student's enrollments appear

### R3 - View GPA

- [ ] GPA shows on the enrollments page to two decimals
- [ ] GPA matches a hand calculation for a known set (write the arithmetic in Notes)
- [ ] GPA with no enrollments is 0.00, not an error
- [ ] Credit weighting is visible: a 4-credit A and a 1-credit F differ from the unweighted average
- [ ] An A+ can push the GPA above 4.00

### R4 - Update a grade

- [ ] Creating an enrollment for a course already held updates the grade instead of erroring
- [ ] The list and the GPA both reflect the new grade

### R5 - Delete an enrollment

- [x] Delete removes the row from the list
- [ ] The GPA recomputes after delete
- [ ] The course still exists afterwards and can be enrolled in again

### Data load

- [x] `python init_db.py` loads at least 5 courses
- [x] Running it a second time does not crash
- [ ] Every loaded course appears in the create-enrollment dropdown

### Security

- [x] `/enrollments`, `/enrollments/create` and delete all redirect to login when signed out
- [ ] Editing the delete URL to another student's course does not delete their enrollment
- [ ] The database holds a bcrypt hash, not a plaintext password (check with `sqlite3` or a viewer)

### Deployment

- [x] `docker build` succeeds from a clean clone
- [x] The container runs and the app is reachable on the mapped port
- [ ] `pip install <dist-name>` from PyPI works in a clean venv, and `calculate_gpa` imports and runs

---

## How to test one thing

1. Say what you are testing and what you expect, before you click.
2. Do it in a browser against a freshly loaded database.
3. Record what happened - the result, and in Notes anything a reader would need to reproduce it.
4. `failed` is a finding, not a mistake. File it, fix it, retest, add the new row.

Use a real timestamp taken when you ran it. The instructor has seen tables invented on the last evening.

| Date | Test Area | Description | Command / Action | Expected Result | Actual Result | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-10-02 | Deployment | Docker container build & execution | `docker build --no-cache -t gpa-calculator .` && `docker run --rm -p 5000:5000 -e SECRET_KEY=change-me gpa-calculator` | Container builds from `python:3.12-slim`, seeds DB with `init_db.py`, serves Flask on `0.0.0.0:5000`, and supports signup, enrollment CRUD, and GPA calculation | App loaded cleanly at `http://localhost:5000`; sign up, create, delete, and GPA calculations all verified working | **PASS** |
