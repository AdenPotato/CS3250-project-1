# mirrors docs/ into a clone of the GitHub wiki - flat page names, links rewritten.
# how to run it and push the result: docs/README.md#wiki
import os, posixpath, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if len(sys.argv) != 2:
    raise SystemExit('usage: python docs/sync_wiki.py <path to a clone of the wiki repo>')
WIKI = sys.argv[1]
BLOB = 'https://github.com/AdenPotato/CS3250-project-1/blob/dev/'
TREE = 'https://github.com/AdenPotato/CS3250-project-1/tree/dev/'
RAW = 'https://raw.githubusercontent.com/AdenPotato/CS3250-project-1/dev/'

PAGES = {
    'docs/README.md': 'Home',
    'docs/design/requirements.md': 'Requirements',
    'docs/design/use_cases.md': 'Use-Cases',
    'docs/design/data_model.md': 'Data-Model',
    'docs/design/routes.md': 'Routes',
    'docs/design/gpa_library.md': 'GPA-Library',
    'docs/design/ui.md': 'UI',
    'docs/planning/schedule.md': 'Schedule',
    'docs/protocol/process_protocol.md': 'Process-Protocol',
    'docs/protocol/core_protocol.md': 'Core-Protocol',
    'docs/protocol/app_protocol.md': 'App-Protocol',
    'docs/testing/test_log.md': 'Manual-Test-Log',
    'docs/deployment/docker.md': 'Deployment-Docker',
    'docs/changelog.md': 'Changelog',
}
IMG = ('.png', '.jpg', '.jpeg', '.gif', '.svg')
unresolved = []


def rewrite(target, src):
    if re.match(r'[a-z]+:', target) or target.startswith('#'):
        return target
    path, _, anchor = target.partition('#')
    full = posixpath.normpath(posixpath.join(posixpath.dirname(src), path))
    tail = '#' + anchor if anchor else ''
    if full in PAGES:
        return PAGES[full] + tail
    on_disk = os.path.join(REPO, full)
    if not os.path.exists(on_disk):
        unresolved.append((src, target))
    if full.lower().endswith(IMG):
        return RAW + full
    return (TREE if os.path.isdir(on_disk) else BLOB) + full + tail


def convert(src):
    out, fenced, seen_h1 = [], False, False
    for line in open(os.path.join(REPO, src)).read().split('\n'):
        if line.lstrip().startswith('```'):
            fenced = not fenced
        elif not fenced:
            # the wiki prints the page name as the title, so the doc's own h1 would repeat it
            if not seen_h1 and line.startswith('# '):
                seen_h1 = True
                continue
            line = re.sub(r'\]\(([^)\s]+)\)', lambda m: '](' + rewrite(m.group(1), src) + ')', line)
        out.append(line)
    return '\n'.join(out).strip('\n')


for src, page in PAGES.items():
    note = f'> Mirrored from [`{src}`]({BLOB}{src}) in the repository. Edit it there, not here - this page is overwritten on the next sync.\n\n'
    open(os.path.join(WIKI, page + '.md'), 'w').write(note + convert(src) + '\n')

open(os.path.join(WIKI, 'UML-Diagrams.md'), 'w').write(f'''> The sources are [`uml/use_case.wsd`]({BLOB}uml/use_case.wsd) and [`uml/class.wsd`]({BLOB}uml/class.wsd) in the repository. Edit them there and re-render.

## Use case diagram

The requirements analysis. Explained in [Use Cases](Use-Cases).

![use case diagram]({RAW}uml/use_case.png)

## Class diagram

The data model. Explained in [Data Model](Data-Model).

![class diagram]({RAW}uml/class.png)
''')

open(os.path.join(WIKI, '_Sidebar.md'), 'w').write('''**[Home](Home)**

**Design**
- [Requirements](Requirements)
- [Use Cases](Use-Cases)
- [Data Model](Data-Model)
- [UML Diagrams](UML-Diagrams)
- [Routes](Routes)
- [GPA Library](GPA-Library)
- [UI](UI)

**Process**
- [Schedule](Schedule)
- [Process Protocol](Process-Protocol)
- [Core Protocol](Core-Protocol)
- [App Protocol](App-Protocol)

**Delivery**
- [Manual Test Log](Manual-Test-Log)
- [Deployment - Docker](Deployment-Docker)
- [Changelog](Changelog)
''')

open(os.path.join(WIKI, '_Footer.md'), 'w').write(f'Mirrored from [`docs/`]({TREE}docs) in the repository, which is the source of truth.\n')
print('pages:', len(PAGES) + 1, '| unresolved links:', unresolved)
