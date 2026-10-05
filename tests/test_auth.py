'''
tests for signup, login and signout - the R1 cases from docs/testing/test_log.md
'''
import bcrypt

from app import db
from app.models import User


def signup(client, id='alice', passwd='secret', passwd_confirm=None):
    return client.post('/users/signup', data={
        'id': id,
        'name': 'Alice',
        'about': 'a student',
        'passwd': passwd,
        'passwd_confirm': passwd if passwd_confirm is None else passwd_confirm,
    })


def login(client, id='alice', passwd='secret'):
    return client.post('/users/login', data={'id': id, 'passwd': passwd})


def test_signup_creates_user_with_bcrypt_hash(client):
    response = signup(client)
    assert response.status_code == 302
    assert response.headers['Location'] == '/users/login'
    user = db.session.get(User, 'alice')
    assert user.name == 'Alice'
    assert user.passwd != b'secret'
    assert bcrypt.checkpw(b'secret', user.passwd)


def test_signup_duplicate_id_shows_message(client):
    signup(client)
    response = signup(client, passwd='other')
    assert response.status_code == 200
    assert b'That id is already taken.' in response.data
    assert bcrypt.checkpw(b'secret', db.session.get(User, 'alice').passwd)


def test_signup_mismatched_passwords_rejected(client):
    response = signup(client, passwd_confirm='different')
    assert response.status_code == 200
    assert b'Passwords must match.' in response.data
    assert db.session.get(User, 'alice') is None


def test_signup_keeps_typed_values_on_error(client):
    response = signup(client, passwd_confirm='different')
    assert b'value="alice"' in response.data


def test_login_reaches_enrollments(client):
    signup(client)
    response = login(client)
    assert response.status_code == 302
    assert response.headers['Location'] == '/enrollments'
    assert client.get('/enrollments').status_code == 200


def test_wrong_password_and_unknown_id_show_same_message(client):
    signup(client)
    wrong_password = login(client, passwd='nope')
    unknown_id = login(client, id='nobody')
    for response in (wrong_password, unknown_id):
        assert response.status_code == 200
        assert b'Invalid id or password.' in response.data
    assert client.get('/enrollments').status_code == 302


def test_signout_ends_session(client):
    signup(client)
    login(client)
    response = client.get('/users/signout')
    assert response.status_code == 302
    assert response.headers['Location'] == '/index.html'
    assert client.get('/enrollments').status_code == 302


def test_enrollments_redirects_to_login_when_signed_out(client):
    response = client.get('/enrollments')
    assert response.status_code == 302
    assert response.headers['Location'].startswith('/users/login')


def test_post_without_csrf_token_is_rejected(client):
    client.application.config['WTF_CSRF_ENABLED'] = True
    response = signup(client)
    assert response.status_code == 200
    assert db.session.get(User, 'alice') is None
