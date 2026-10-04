'''
tests for the course load in src/init_db.py - the data load cases from docs/testing/test_log.md
'''
import runpy

from app import db
from app.models import Course


def run_init_db():
    runpy.run_module('init_db', run_name='__main__')


def test_loads_at_least_five_complete_courses(client, capsys):
    run_init_db()
    courses = db.session.query(Course).all()
    assert len(courses) >= 5
    for course in courses:
        assert course.prefix and course.number and course.name
        assert isinstance(course.number, str)
        assert course.credits > 0
    assert f'Loaded {len(courses)} courses' in capsys.readouterr().out


def test_second_run_does_not_raise_or_duplicate(client, capsys):
    run_init_db()
    count = db.session.query(Course).count()
    capsys.readouterr()
    run_init_db()
    assert db.session.query(Course).count() == count
    assert 'Loaded 0 courses' in capsys.readouterr().out
