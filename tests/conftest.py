# put src/ on the import path so tests can import gpa_calculator and app without installing them
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool


@pytest.fixture
def client():
    from app import app, db
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.app_context():
        # swap in an in-memory database so tests never touch src/instance/prj1.db
        real_engine = db.engines[None]
        db.engines[None] = create_engine('sqlite://', poolclass=StaticPool)
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.engines[None] = real_engine
