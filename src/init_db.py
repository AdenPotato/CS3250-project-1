'''
CS3250 - Software Development Methods and Tools
Instructor: Thyago Mota
Student(s):
Description: Project 1 - GPA Calculator
'''

from app import app, db
from app.models import Course

# the catalog - (prefix, number, name, credits). number is a string, see docs/design/data_model.md
courses = [
    ('CS', '1050', 'Computer Science 1', 4),
    ('CS', '2050', 'Computer Science 2', 4),
    ('CS', '2400', 'Computer Organization and Assembly', 4),
    ('CS', '3250', 'Software Development Methods and Tools', 4),
    ('CS', '3600', 'Operating Systems', 4),
    ('MTH', '1410', 'Calculus I', 4),
    ('MTH', '2140', 'Computational Matrix Algebra', 2),
    ('ENG', '1010', 'Composing Arguments', 3),
]

with app.app_context():
    db.create_all()
    loaded = 0
    for prefix, number, name, credits in courses:
        # skip a course already there, so a second run does not raise on the composite key
        if db.session.get(Course, (prefix, number)) is None:
            db.session.add(Course(prefix=prefix, number=number, name=name, credits=credits))
            loaded += 1
    db.session.commit()
    print(f'Loaded {loaded} courses, {db.session.query(Course).count()} in the catalog.')
