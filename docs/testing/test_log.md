# Manual Test Log

The Testing phase deliverable, worth 5 rubric points. The assignment asks for manual testing documented in a table, so this file is the graded artifact - the pytest suite is a separate, ungraded safety net ([process_protocol.md](../protocol/process_protocol.md#testing)).

Add rows with `/test-log`.

---

## Results

| Functionality Tested | Date | Time | Tester | Result | Notes |
|---|---|---|---|---|---|
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
| GPA with no enrollments | 2026-10-04 | 12:28 | Elijah Ortiz | passed | Signed up with a new account and opened `/enrollments` with no enrollments. Expected GPA 0.00 and the page displayed GPA: 0.00. |
| #13 create enrollment/update grade (Data Load Verification) | 2026-10-04 | 10:22 | Isabella Eaton | passed | Navigated to `/enrollments/create` after running database setup (`init_db.py`). Inspect the Course dropdown list. Every loaded course (all 8) appears as an option labeled `PREFIX NUMBER - Name` (e.g., `CS 3250 - Software Development Methods and Tools`). |
| #13 create enrollment/update grade (Create Enrollment) | 2026-10-04 | 10:25 | Isabella Eaton | passed | 1. Log in.<br>2. Go to `/enrollments/create`.<br>3. Pick an unenrolled course and select grade `A`.<br>4. Click Submit. Form posts with valid CSRF token; creates a new `Enrollment` row for `current_user`; redirects to `/enrollments` with the new course and grade displayed. |
| #13 create enrollment/update grade (Update Enrollment) | 2026-10-04 | 10:27 | Isabella Eaton | passed | 1. Go to `/enrollments/create`.<br>2. Pick the same course used in TC-ENROLL-02.<br>3. Select grade `B+`.<br>4. Click Submit. Existing record is updated to `B+` without raising an `IntegrityError` / primary key conflict; redirects to `/enrollments` with updated grade `B+`. |
| Delete an enrollment - GPA recomputes | 2026-10-04 | 14:59 | Johnny De La Garza | passed | Branch `14-johnny-r5-gpa-check`, fresh database from `init_db.py`. Signed in as `johnny` and added CS 3250 (4 cr) A, MTH 2140 (2 cr) C, ENG 1010 (3 cr) B on the create page. GPA showed 3.22, matching (16+4+9)/9. Deleted MTH 2140; expected (16+9)/7 = 3.57 and the page showed 3.57. |
| #17 Manual test log | 2026-10-04 | 15:20 | Isabella Eaton | failed | docker was not updated, needed to update docker to showcase correct image with all project updates implemented. |
| #17 Manual test log (retest) | 2026-10-04 | 15:41 | Isabella Eaton | passed | Retest of the 15:20 failure. test log updated, all program requirements met (R1-R5) through manual testing. |
| Sign up with details and created an account successfully | 2026-10-04 | 15:49 | Isabella Eaton | passed | Additional requirements shown in coverage checklist, all passed easily with no error after fixing docker issue, ran in Chrome browser. |
| Sign up with valid details creates the account | 2026-10-04 | 15:49 | Isabella Eaton | passed |  |
| Sign up with a duplicate id is rejected with a message | 2026-10-04 | 15:49 | Isabella Eaton | passed |  |
| Sign up with mismatched passwords is rejected | 2026-10-04 | 15:49 | Isabella Eaton | passed |  |
| Sign in with correct credentials reaches the enrollments page | 2026-10-04 | 15:49 | Isabella Eaton | passed |  |
| Sign in with a wrong password is rejected, and the message does not reveal which field was wrong | 2026-10-04 | 15:51 | Isabella Eaton | passed |  |
| Sign in with an unknown id is rejected the same way | 2026-10-04 | 15:51 | Isabella Eaton | passed |  |
| Sign out ends the session; going back to `/enrollments` redirects to login | 2026-10-04 | 15:51 | Isabella Eaton | passed |  |
| A new account sees the empty state, not a bare table | 2026-10-04 | 15:51 | Isabella Eaton | passed |  |
| After creating enrollments, all of them are listed with prefix, number, name, credits and grade | 2026-10-04 | 15:55 | Isabella Eaton | passed |  |
| Signed in as a second student, only that student's enrollments appear | 2026-10-04 | 15:55 | Isabella Eaton | passed |  |
| GPA shows on the enrollments page to two decimals | 2026-10-04 | 15:56 | Isabella Eaton | passed |  |
| GPA matches a hand calculation for a known set | 2026-10-04 | 15:56 | Isabella Eaton | passed | Notes for R3 view gpa arithmetic: ((grade)x(weight))+((grade)x(weight))....=gpa. weight == number of courses registered/100 = % weight per class (assuming even weight). ((4.0)x(.25))+((3.0)x(.25))+((2.0)x(.25))+((1.0)x(.25))=2.50, matches app result for gpa. For uneven courses the arithmetic is total quality points / total credit hours, where quality points = grade x credit hours. |
| GPA with no enrollments is 0.00, not an error | 2026-10-04 | 15:56 | Isabella Eaton | passed |  |
| Credit weighting is visible: a 4-credit A and a 1-credit F differ from the unweighted average | 2026-10-04 | 16:00 | Isabella Eaton | passed |  |
| An A+ can push the GPA above 4.00 | 2026-10-04 | 16:00 | Isabella Eaton | passed |  |
| Creating an enrollment for a course already held updates the grade instead of erroring | 2026-10-04 | 16:00 | Isabella Eaton | passed |  |
| The list and the GPA both reflect the new grade | 2026-10-04 | 16:00 | Isabella Eaton | passed |  |
| Delete removes the row from the list | 2026-10-04 | 16:00 | Isabella Eaton | passed |  |
| The GPA recomputes after delete | 2026-10-04 | 16:00 | Isabella Eaton | passed |  |
| The course still exists afterwards and can be enrolled in again | 2026-10-04 | 16:00 | Isabella Eaton | passed |  |
| `/enrollments`, `/enrollments/create` and delete all redirect to login when signed out | 2026-10-04 | 16:00 | Isabella Eaton | passed |  |
| Editing the delete URL to another student's course does not delete their enrollment | 2026-10-04 | 16:00 | Isabella Eaton | passed |  |
| Every loaded course appears in the create-enrollment dropdown | 2026-10-04 | 16:02 | Isabella Eaton | passed |  |
| Deployment - `docker build` succeeds from a clean clone | 2026-10-04 | 16:03 | Isabella Eaton | passed |  |
| Deployment - the container runs and the app is reachable on the mapped port | 2026-10-04 | 16:03 | Isabella Eaton | passed |  |
| The database holds a bcrypt hash, not a plaintext password | 2026-10-04 | 16:56 | Claude Code (command line) | passed | Clean export of `dev` at e267217, fresh database, two accounts signed up over HTTP. Read `passwd` back through the `User` model. Expected a bcrypt hash; both were 60 bytes starting `$2b$12$`, neither the typed password. |
| `pip install GPA-Calculator-CS3250-aden` from PyPI in a clean venv | 2026-10-04 | 16:56 | Claude Code (command line) | passed | New empty venv outside the repo, `pip install GPA-Calculator-CS3250-aden`. Expected 0.1.0 to install and `calculate_gpa` to import and run; `pip list` showed 0.1.0, the import resolved to `site-packages/gpa_calculator`, and `calculate_gpa([{'grade':'A','credits':3}])` returned 4.0. |
| Create page links back to the enrollments list | 2026-10-04 | 17:12 | Claude Code (HTTP requests, no browser) | passed | Branch `28-aden-final-validation`, copy of the app laid out as the Docker image is (no `src/gpa_calculator`), fresh database. Signed in and opened `/enrollments/create`. Expected a link to `/enrollments`; the page has "Back to enrollments" pointing there. An earlier run at 16:56 on `dev` found no such link, which is what this fixes. |
| New account's GPA 0.00 is not shown as a low-GPA warning | 2026-10-04 | 17:12 | Claude Code (HTTP requests, no browser) | passed | Same run. A new account's `/enrollments` showed GPA 0.00 without the `low_gpa` class; a second student with CS 1050 A+ and CS 3250 F still showed 2.15 with it. |
| Full R1-R5 pass with the library imported from PyPI | 2026-10-04 | 17:12 | Claude Code (HTTP requests, no browser) | passed | Same run, 43 checks: signup and its rejections, sign in and out, empty state, 8 courses in the dropdown, three enrollments giving 3.22 = (16+9+4)/9, an update giving 3.73 = (16+9+8.6)/9, a delete giving 3.57 = (16+9)/7, a second student's isolation, and a 404 on deleting another student's course. `gpa_calculator` resolved to `site-packages`, not the repo copy. Not run inside a container. |
| Deployment - `docker build --no-cache` on branch `28-aden-final-validation` | 2026-10-04 | 17:21 | Claude Code (command line) | passed | Built from the working tree of the branch, not a fresh clone, with Docker 29.8.2. Expected all 11 steps to finish; the image built and tagged. |
| Deployment - container imports `gpa_calculator` from PyPI | 2026-10-04 | 17:22 | Claude Code (command line) | passed | Ran the image and looked inside the container. Expected no `gpa_calculator` folder under `/app/src` and the import to resolve to the pip install; `/app/src` held only `app`, `init_db.py`, `instance`, `pyproject.toml` and `README.md`, the import resolved to `/usr/local/lib/python3.12/site-packages/gpa_calculator`, and `pip list` showed 0.1.0. |
| Deployment - full R1-R5 pass against the running container | 2026-10-04 | 17:22 | Claude Code (HTTP requests, no browser) | passed | Container mapped to host port 5060. The startup log printed "Loaded 8 courses, 8 in the catalog." The same 43 checks as the 17:12 row all passed, with the same GPA values (3.22, 3.73, 3.57, 4.30), and the container log showed no 500 responses. |

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
- [x] Sign in with an unknown id is rejected the same way |IE 
- [x] Sign out ends the session; going back to `/enrollments` redirects to login 

### R2 - View enrollments

- [x] A new account sees the empty state, not a bare table 
- [x] After creating enrollments, all of them are listed with prefix, number, name, credits and grade 
- [x] Signed in as a second student, only that student's enrollments appear 

### R3 - View GPA

- [x] GPA shows on the enrollments page to two decimals 
- [x] GPA matches a hand calculation for a known set (write the arithmetic in Notes) 
- [x] GPA with no enrollments is 0.00, not an error 
- [x] Credit weighting is visible: a 4-credit A and a 1-credit F differ from the unweighted average 
- [x] An A+ can push the GPA above 4.00 

### R4 - Update a grade

- [x] Creating an enrollment for a course already held updates the grade instead of erroring 
- [x] The list and the GPA both reflect the new grade 

### R5 - Delete an enrollment

- [x] Delete removes the row from the list
- [x] The GPA recomputes after delete
- [x] The course still exists afterwards and can be enrolled in again

### Data load

- [x] `python init_db.py` loads at least 5 courses 
- [x] Running it a second time does not crash 
- [x] Every loaded course appears in the create-enrollment dropdown 

### Security

- [x] `/enrollments`, `/enrollments/create` and delete all redirect to login when signed out 
- [x] Editing the delete URL to another student's course does not delete their enrollment 
- [x] The database holds a bcrypt hash, not a plaintext password (check with `sqlite3` or a viewer)

### Deployment

- [x] `docker build` succeeds from a clean clone 
- [x] The container runs and the app is reachable on the mapped port 
- [x] `pip install <dist-name>` from PyPI works in a clean venv, and `calculate_gpa` imports and runs

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
