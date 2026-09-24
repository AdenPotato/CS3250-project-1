# Change Log

<!-- Newest entry first. Format rules are at the bottom of this file. -->

---

2026-09-22 14:30 MDT
Aden

## Reshaped the docs and skills around the Flask GPA calculator

- Replaced the Java/Vert.x/React scaffold with one sized for CS3250 Project 1: three protocols (process, core, app) in place of nine, six design docs written against the real models, routes and library, and the planning / testing / deployment docs the rubric actually grades
- Skills cut from 18 to 9 and rewritten for this project: /project-status, /phase, /new-route, /new-model, /uml, /test-log, /publish-lib, /deliver, /log-work. Agents cut from four to three: app, ui, release
- Process is now the assignment's Waterfall - phases, the instructor checkpoint as a gate, team roles, and a rubric tracker carrying the -5 and -25 penalties where they cannot be forgotten
- Testing is manual-first, since that is the graded artifact, with pytest kept as an ungraded net over gpa_calculator and auth scoping

Heads up: nothing to run - pull and go. The project code itself is untouched; this is docs and tooling only.

---

## Changelog format

Rolling log of work, **newest at top** - this format section stays at the bottom. **One entry per person per day**, written at end of day, with one bullet per piece of work. **Max 20 entries** - drop the oldest when exceeded.

Written by [`/log-work`](../.claude/skills/log-work/SKILL.md), which previews the entry and writes nothing until it is approved. Multiple sessions in one day fold into that day's single entry as more bullets; never a second block for the same person and day.

Each entry, in order:

1. A **date line** - `YYYY-MM-DD HH:MM TZ` from `date "+%Y-%m-%d %H:%M %Z"`.
2. The **person** on the next line.
3. A `## Title` - a short summary of the day.
4. **One bullet per piece of work**, each naming the rubric row it moved.
5. A **`Heads up:`** block, always present - what a teammate must run after pulling. Most often `rm src/instance/prj1.db && python init_db.py` after a model change, since there are no migrations. When there is nothing: `Heads up: nothing to run - pull and go.`

Insert new entries at the top, just under the file header. Never rewrite the file in full.
