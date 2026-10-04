'''
CS3250 - Software Development Methods and Tools
Instructor: Thyago Mota
Student(s): Aden Lytle, Johnny De La Garza, Isabella Eaton, Elijah Damian-Ortiz
Description: Project 1 - GPA Calculator
'''

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField, validators
from wtforms.validators import DataRequired, EqualTo, Length

class SignUpForm(FlaskForm):
    id = StringField('Id', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    about = TextAreaField('About')
    # bcrypt rejects passwords over 72 bytes, so the form stops them first
    passwd = PasswordField('Password', validators=[DataRequired(), Length(max=72)])
    passwd_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('passwd', message='Passwords must match.')])
    submit = SubmitField('Confirm')

class LoginForm(FlaskForm):
    id = StringField('Id', validators=[DataRequired()])
    passwd = PasswordField('Password', validators=[DataRequired(), Length(max=72)])
    submit = SubmitField('Confirm')

GRADE_CHOICES = [
    'A+', 'A', 'A-',
    'B+', 'B', 'B-',
    'C+', 'C', 'C-',
    'D+', 'D', 'D-',
    'F'
]

class EnrollmentForm(FlaskForm):
    course = SelectField('Course', validators=[DataRequired()])
    grade = SelectField('Grade', choices=GRADE_CHOICES, validators=[DataRequired()])
    submit = SubmitField('Confirm')

class DeleteEnrollmentForm(FlaskForm):
    submit = SubmitField('Delete')

