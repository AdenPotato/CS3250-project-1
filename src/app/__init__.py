'''
CS3250 - Software Development Methods and Tools
Instructor: Thyago Mota
Student(s): Aden Lytle, Johnny De La Garza, Isabella Eaton, Elijah Damian-Ortiz
Description: Project 1 - GPA Calculator
'''

from flask import Flask
import os

# templates/ and static/ sit at the repo root, two levels above this package
app = Flask(__name__, template_folder='../../templates', static_folder='../../static')
# the fallback is for local development only - delivery passes SECRET_KEY
app.secret_key = os.environ.get('SECRET_KEY', 'dev-only-not-for-delivery')

# db initialization
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prj1.db'
db.init_app(app)

from app import models
with app.app_context(): 
    db.create_all()

# login manager
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
# where @login_required sends a signed-out visitor
login_manager.login_view = 'login'

from app.models import User

# user_loader callback
@login_manager.user_loader
def load_user(id):
    try: 
        return db.session.query(User).filter(User.id==id).one()
    except: 
        return None

from app import routes