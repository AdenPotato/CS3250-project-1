'''
tests for the enrollments list - the R2 cases from docs/testing/test_log.md
'''
import bcrypt

from app import db
from app.models import User, Course, Enrollment


def add_user(id):
    db.session.add(User(id=id, name=id.title(), about='', passwd=bcrypt.hashpw(b'secret', bcrypt.gensalt(4))))
    db.session.commit()


def add_course(prefix, number, name, credits):
    db.session.add(Course(prefix=prefix, number=number, name=name, credits=credits))
    db.session.commit()


def enroll(user_id, prefix, number, grade):
    db.session.add(Enrollment(user_id=user_id, course_prefix=prefix, course_number=number, grade=grade))
    db.session.commit()


def login(client, id):
    return client.post('/users/login', data={'id': id, 'passwd': 'secret'})


def test_new_account_sees_empty_state_not_a_table(client):
    add_user('alice')
    login(client, 'alice')
    response = client.get('/enrollments')
    assert response.status_code == 200
    assert b'You have no enrollments yet.' in response.data
    assert b'href="/enrollments/create"' in response.data
    assert b'<table>' not in response.data


def test_rows_show_prefix_number_name_credits_and_grade(client):
    add_user('alice')
    add_course('CS', '3250', 'Software Development Methods and Tools', 4)
    add_course('MTH', '1410', 'Calculus I', 3)
    enroll('alice', 'MTH', '1410', 'B+')
    enroll('alice', 'CS', '3250', 'A-')
    login(client, 'alice')
    html = client.get('/enrollments').text
    for cell in ('CS', '3250', 'Software Development Methods and Tools', '4', 'A-', 'MTH', '1410', 'Calculus I', '3', 'B+'):
        assert f'<td>{cell}</td>' in html
    assert html.index('<td>CS</td>') < html.index('<td>MTH</td>')
    assert 'You have no enrollments yet.' not in html


def test_each_row_has_a_delete_form_for_its_own_course(client):
    add_user('alice')
    add_course('CS', '3250', 'Software Development Methods and Tools', 4)
    add_course('MTH', '1410', 'Calculus I', 3)
    enroll('alice', 'CS', '3250', 'A')
    enroll('alice', 'MTH', '1410', 'B')
    login(client, 'alice')
    client.application.config['WTF_CSRF_ENABLED'] = True
    html = client.get('/enrollments').text
    assert 'action="/enrollments/delete/CS/3250" method="POST"' in html
    assert 'action="/enrollments/delete/MTH/1410" method="POST"' in html
    assert html.count('name="csrf_token"') == 2


def test_second_student_sees_only_their_own_enrollments(client):
    add_user('alice')
    add_user('bob')
    add_course('CS', '3250', 'Software Development Methods and Tools', 4)
    add_course('MTH', '1410', 'Calculus I', 3)
    enroll('alice', 'CS', '3250', 'A')
    enroll('bob', 'MTH', '1410', 'C')
    login(client, 'bob')
    html = client.get('/enrollments').text
    assert 'Calculus I' in html
    assert 'Software Development Methods and Tools' not in html


def test_user_id_in_the_query_string_is_ignored(client):
    add_user('alice')
    add_user('bob')
    add_course('CS', '3250', 'Software Development Methods and Tools', 4)
    enroll('alice', 'CS', '3250', 'A')
    login(client, 'bob')
    html = client.get('/enrollments?user_id=alice').text
    assert 'Software Development Methods and Tools' not in html


# R5 - delete enrollment

def test_delete_removes_enrollment_and_redirects(client):
    add_user('alice')
    add_course('CS', '3250', 'Software Development Methods and Tools', 4)
    enroll('alice', 'CS', '3250', 'A')
    login(client, 'alice')
    response = client.post('/enrollments/delete/CS/3250')
    assert response.status_code == 302
    assert response.headers['Location'].endswith('/enrollments')
    assert db.session.get(Enrollment, ('alice', 'CS', '3250')) is None



def test_delete_leaves_course_in_catalog(client):
    add_user('alice')
    add_course('CS', '3250', 'Software Development Methods and Tools', 4)
    enroll('alice', 'CS', '3250', 'A')
    login(client, 'alice')
    client.post('/enrollments/delete/CS/3250')
    assert db.session.get(Course, ('CS', '3250')) is not None


def test_student_cannot_delete_another_students_enrollment(client):
    add_user('alice')
    add_user('bob')
    add_course('CS', '3250', 'Software Development Methods and Tools', 4)
    enroll('bob', 'CS', '3250', 'B')
    login(client, 'alice')
    response = client.post('/enrollments/delete/CS/3250')
    assert response.status_code == 404
    assert db.session.get(Enrollment, ('bob', 'CS', '3250')) is not None


def test_delete_missing_enrollment_returns_404(client):
    add_user('alice')
    login(client, 'alice')
    response = client.post('/enrollments/delete/XX/0000')
    assert response.status_code == 404


# small fixes from the final walkthrough (#28)

def test_empty_state_gpa_is_not_flagged_low(client):
    add_user('alice')
    login(client, 'alice')
    html = client.get('/enrollments').text
    assert '0.00' in html
    assert 'low_gpa' not in html


def test_low_gpa_is_still_flagged_with_enrollments(client):
    add_user('alice')
    add_course('CS', '3250', 'Software Development Methods and Tools', 4)
    enroll('alice', 'CS', '3250', 'D')
    login(client, 'alice')
    assert 'class="low_gpa">1.00<' in client.get('/enrollments').text


def test_create_page_links_back_to_the_list(client):
    add_user('alice')
    login(client, 'alice')
    assert 'href="/enrollments"' in client.get('/enrollments/create').text
