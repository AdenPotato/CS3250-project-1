'''
CS3250 - Software Development Methods and Tools
Instructor: Thyago Mota
Student(s): Aden Lytle, Johnny De La Garza, Isabella Eaton, Elijah Damian-Ortiz
Description: Project 1 - GPA Calculator
'''

from app import app, db
from app.models import User, Course, Enrollment
from app.forms import SignUpForm, LoginForm, EnrollmentForm, DeleteEnrollmentForm
from gpa_calculator import calculate_gpa
from flask import render_template, redirect, url_for, request, abort
from flask_login import login_required, login_user, logout_user, current_user
import bcrypt

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index(): 
    return render_template('index.html', title='GPA Calculator')

@app.route('/users/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        if db.session.get(User, form.id.data):
            form.id.errors.append('That id is already taken.')
        else:
            hashed = bcrypt.hashpw(form.passwd.data.encode(), bcrypt.gensalt())
            user = User(id=form.id.data, name=form.name.data, about=form.about.data, passwd=hashed)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=form)

@app.route('/users/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        user = db.session.get(User, form.id.data)
        if user and bcrypt.checkpw(form.passwd.data.encode(), user.passwd):
            login_user(user)
            return redirect(url_for('list_enrollments'))
        # one message for both failures, so the form cannot be used to find valid ids
        error = 'Invalid id or password.'
    return render_template('login.html', title='Login', form=form, error=error)

@app.route('/users/signout', methods=['GET', 'POST'])
@login_required
def signout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/enrollments')
@login_required
def list_enrollments():
    enrollments = sorted(current_user.enrollments, key=lambda e: (e.course_prefix, e.course_number))

    # make the grade and credit data that calculate_gpa needs
    gpa_data = [
        {
            'grade': enrollment.grade,
            'credits': enrollment.course.credits
        }
        for enrollment in enrollments
    ]

    # calculate the students GPA from their enrollments
    gpa = calculate_gpa(gpa_data)

    # send the enrollments and GPA to the page
    return render_template(
        'enrollments.html',
        title='Enrollments',
        enrollments=enrollments,
        delete_form=DeleteEnrollmentForm(),
        gpa=gpa
    )

@app.route('/enrollments/delete/<course_prefix>/<course_number>', methods=['POST'])
@login_required
def delete_enrollment(course_prefix, course_number):
    form = DeleteEnrollmentForm()
    if not form.validate_on_submit():
        abort(400)
    enrollment = db.session.get(Enrollment, (current_user.id, course_prefix, course_number))
    if enrollment is None:
        abort(404)
    db.session.delete(enrollment)
    db.session.commit()
    return redirect(url_for('list_enrollments'))

@app.route('/enrollments/create', methods=['GET', 'POST'])
@login_required
def create_enrollment():
    form = EnrollmentForm()

    # Populate course choices from the Course table: "PREFIX NUMBER - Name"
    courses = db.session.scalars(db.select(Course).order_by(Course.prefix, Course.number)).all()
    form.course.choices = [(f"{c.prefix}:{c.number}", f"{c.prefix} {c.number} - {c.name}") for c in courses]

    if form.validate_on_submit():
        prefix, number = form.course.data.split(':')

        # Check if current_user already has an enrollment for this course (R4)
        enrollment = db.session.get(Enrollment, (current_user.id, prefix, number))

        if enrollment:
            # Update grade on existing enrollment
            enrollment.grade = form.grade.data
        else:
            # Create a new enrollment
            enrollment = Enrollment(
                user_id=current_user.id,
                course_prefix=prefix,
                course_number=number,
                grade=form.grade.data
            )
            db.session.add(enrollment)

        db.session.commit()
        return redirect(url_for('list_enrollments'))

    return render_template('create_enrollment.html', title='Create Enrollment', form=form)