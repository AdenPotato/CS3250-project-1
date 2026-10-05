---
name: new-design
description: Settle a design decision before any code is written - run the one-at-a-time questionnaire, then write the answer into the matching docs/design/ file and propose the build tasks. Use when a requirement is ambiguous or a change touches the model, a route and a template at once.
---

# /new-design

Design in this project is **not** open-ended. The assignment fixes the requirements, the routes and the data model, so a design session settles the decisions the assignment leaves open - and nothing else. No design doc is written until the questionnaire is finished.

## Rules

- Questions are asked **one at a time**, never as a list.
- After each question, say how many remain ("3 questions remaining").
- Wait for an answer before asking the next one.
- If an answer contradicts a design doc or the assignment, say so immediately and stop rather than carrying the contradiction into the file.
- Only after every question is answered and the summary is confirmed is the file written.
- The written file reflects every decision made. No omissions, no decisions invented afterwards.

## Step 1 - Find the requirement and the rubric row

Ask: **what decision is this session settling, and which requirement does it serve?**

Every design decision traces to a requirement in [requirements.md](../../../docs/design/requirements.md) (R1-R5) and to a row in the [rubric tracker](../../../docs/protocol/process_protocol.md#rubric-tracker). Work that maps to neither is out of scope until a teammate says otherwise (AGENTS.md rule 1). Say that plainly and stop - do not design it anyway.

Then read the design docs the decision touches, so already-settled decisions are not reopened:

| The decision is about | Read |
|---|---|
| What the app must do, or whether something is in scope | [requirements.md](../../../docs/design/requirements.md) |
| An actor, a flow, or a new step in one | [use_cases.md](../../../docs/design/use_cases.md) |
| Entities, keys, the grade scale, relationships | [data_model.md](../../../docs/design/data_model.md) |
| A route, its methods, its auth, its form | [routes.md](../../../docs/design/routes.md) |
| The calculation or the published package | [gpa_library.md](../../../docs/design/gpa_library.md) |
| A page, a template block, an empty state | [ui.md](../../../docs/design/ui.md) |

## Step 2 - Build the questionnaire

From the area, list the decisions and edge cases the docs do not already answer. Cover:

- **Scope** - which requirement, which rubric row, and what is explicitly not included.
- **Data model impact** - new or changed fields, whether the composite `(prefix, number)` key is involved, and whether this forces a database reset (`rm src/instance/prj1.db && python init_db.py`).
- **Route impact** - which of the seven routes changes, its methods, whether it is `@login_required`, and whether it redirects after POST.
- **Form and validation** - what is validated server-side, and what the user sees when validation fails.
- **Template impact** - which page, and what the **empty state** says. A grader creates a fresh account, so the empty state is part of the design, not an afterthought.
- **Library impact** - whether `gpa_calculator` changes, and if so what version bump that implies for PyPI ([gpa_library.md](../../../docs/design/gpa_library.md#publishing)). `GRADE_POINTS` lives in two places and both move together until the library is installed.
- **Edge cases** - no enrollments, an unrecognized grade, a duplicate enrollment (R4 makes this an update, not an error), a signed-out visitor, and another student's row reached by editing the URL.
- **Testing** - what a pytest can assert, and what needs a manual [test log](../../../docs/testing/test_log.md) row because a grader will click it.

## Step 3 - Run the questionnaire

One question, then wait.

> **Question 1:** [question]
> *(N questions remaining)*

When the assignment is genuinely silent and no doc answers it, that is a question for a teammate, not a decision to invent (AGENTS.md rule 6). Flag it and carry it into the summary as an open item.

## Step 4 - Confirm

Present every decision as a short list, plus any open items still waiting on a teammate. Ask for confirmation that the list is complete and correct before writing anything.

## Step 5 - Write it into the design docs

**Prefer editing an existing file.** The six docs under [docs/design/](../../../docs/design) cover the whole project, and a decision almost always belongs in one of them - as a new subsection, or an edit to the section that is now wrong.

A **new file** needs a stated reason. If one is added:

- It goes in `docs/design/`, lowercase snake_case, named for its subject.
- It is linked from the design table in [docs/README.md](../../../docs/README.md). A doc nothing links to is a doc nobody reads.

Either way, the content is defined **once**. If the decision changes a statement in another doc, fix that doc in the same change rather than leaving two answers in the tree.

Write it in the project voice: plain, specific, lowercase-first, no em-dashes, no decoration.

## Step 6 - The visible-surface gate

If the decision changes what a page looks like or how a flow reads, it is not finished at the doc:

- **Name the blocks on the page** and the empty state, in prose, before anyone opens a template.
- **Check it against the styling budget** in [ui.md](../../../docs/design/ui.md#styling). There are no points for visual design and 10 each for the routes underneath, so a design that asks for more styling than the budget allows is the design that is wrong.
- **A teammate confirms the page before it is built**, and the PR that builds it carries a screenshot ([core_protocol.md](../../../docs/protocol/core_protocol.md#pull-requests)). Never guess the visual direction.

A model, library or packaging decision with no page behind it skips this step.

## Step 7 - Propose the build tasks

**A design session is not finished when the document is written.** It is finished when the work it implies is tracked, or has been explicitly declined.

Writing "the routes follow from this" in a design doc feels like a handoff and is not one. Nothing is on the board, the rubric tracker does not move, and the work exists only in a file nobody is watching.

So, immediately after the doc is accepted:

1. **List the tasks in dependency order.** It is usually model, then library, then route, then template - each blocked by the one before it, which is the order Waterfall exists to enforce.
2. **Name the rubric row and points** each task moves, and whether it needs a database reset teammates must run after pulling.
3. **Propose them** - title, one-line scope, rubric row - and wait for a teammate's go before running `/new-issue`. Proposing is required; creating is not yours to do alone.
4. **A design that produces no build work says so.** "This settles the question and changes no code" is a valid outcome. Silence is not.

## Finish

- Update the rubric row status if the design closed one ([tracker](../../../docs/protocol/process_protocol.md#rubric-tracker)).
- If the decision changes a route's behavior, fix [routes.md](../../../docs/design/routes.md) now, not after the code disagrees with it.
- Add a changelog bullet at end of day with `/log-work`.
