'''
CS3250 - Software Development Methods and Tools
Instructor: Thyago Mota
Student(s):
Description: Project 1 - GPA Calculator
'''

# grade points for the traditional college letter grade scale, A+ included (so GPA can exceed 4.0)
GRADE_POINTS = {
    'A+': 4.3, 'A': 4.0, 'A-': 3.7,
    'B+': 3.3, 'B': 3.0, 'B-': 2.7,
    'C+': 2.3, 'C': 2.0, 'C-': 1.7,
    'D+': 1.3, 'D': 1.0, 'D-': 0.7,
    'F': 0.0
}

def calculate_gpa(enrollments):
    '''
    Computes the credit-weighted GPA from a list of dictionary-like enrollments.
    Each enrollment is expected to provide a 'grade' key (e.g. 'A+', 'B-', ...)
    and a 'credits' key (the number of credit hours for the course).
    Enrollments with no grade yet, or an unrecognized grade, are ignored.
    Returns 0 when there are no graded credits to average.
    The result is not rounded - round it for display in the caller.
    '''
    points = 0.0
    hours = 0
    for enrollment in enrollments:
        grade = enrollment.get('grade')
        # skipped, not counted as an F - the course is not graded yet
        if grade not in GRADE_POINTS:
            continue
        credits = enrollment['credits']
        points += GRADE_POINTS[grade] * credits
        hours += credits
    if hours == 0:
        return 0
    return points / hours
