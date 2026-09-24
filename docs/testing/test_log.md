# Manual Test Log

The Testing phase deliverable, worth 5 rubric points. The assignment asks for manual testing documented in a table, so this file is the graded artifact - the pytest suite is a separate, ungraded safety net ([process_protocol.md](../protocol/process_protocol.md#testing)).

Add rows with `/test-log`.

---

## Results

| Functionality Tested | Date | Time | Tester | Result | Notes |
|---|---|---|---|---|---|
| | | | | | |

Result is `passed` or `failed`. A `failed` row **stays in the table** - delete nothing. When it is fixed, add a new row for the retest and reference the failure. A log with no failures in it reads as a log nobody actually used.

---

## Coverage checklist

Every requirement needs at least one row before delivery. Tick these off against the table above.

### R1 - Authentication

- [ ] Sign up with valid details creates the account
- [ ] Sign up with a duplicate id is rejected with a message
- [ ] Sign up with mismatched passwords is rejected
- [ ] Sign in with correct credentials reaches the enrollments page
- [ ] Sign in with a wrong password is rejected, and the message does not reveal which field was wrong
- [ ] Sign in with an unknown id is rejected the same way
- [ ] Sign out ends the session; going back to `/enrollments` redirects to login

### R2 - View enrollments

- [ ] A new account sees the empty state, not a bare table
- [ ] After creating enrollments, all of them are listed with prefix, number, name, credits and grade
- [ ] Signed in as a second student, only that student's enrollments appear

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

- [ ] Delete removes the row from the list
- [ ] The GPA recomputes after delete
- [ ] The course still exists afterwards and can be enrolled in again

### Data load

- [ ] `python init_db.py` loads at least 5 courses
- [ ] Running it a second time does not crash
- [ ] Every loaded course appears in the create-enrollment dropdown

### Security

- [ ] `/enrollments`, `/enrollments/create` and delete all redirect to login when signed out
- [ ] Editing the delete URL to another student's course does not delete their enrollment
- [ ] The database holds a bcrypt hash, not a plaintext password (check with `sqlite3` or a viewer)

### Deployment

- [ ] `docker build` succeeds from a clean clone
- [ ] The container runs and the app is reachable on the mapped port
- [ ] `pip install <dist-name>` from PyPI works in a clean venv, and `calculate_gpa` imports and runs

---

## How to test one thing

1. Say what you are testing and what you expect, before you click.
2. Do it in a browser against a freshly loaded database.
3. Record what happened - the result, and in Notes anything a reader would need to reproduce it.
4. `failed` is a finding, not a mistake. File it, fix it, retest, add the new row.

Use a real timestamp taken when you ran it. The instructor has seen tables invented on the last evening.
