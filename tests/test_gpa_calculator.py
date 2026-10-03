'''
tests for the gpa_calculator library - the cases from docs/design/gpa_library.md#tests
'''
import pytest

from gpa_calculator import GRADE_POINTS, calculate_gpa


def test_empty_list_returns_zero():
    assert calculate_gpa([]) == 0


def test_one_course():
    assert calculate_gpa([{'grade': 'A', 'credits': 3}]) == pytest.approx(4.0)


def test_mixed_credits_are_weighted():
    # (4.0 * 3 + 0.0 * 1) / 4 = 3.0
    enrollments = [{'grade': 'A', 'credits': 3}, {'grade': 'F', 'credits': 1}]
    assert calculate_gpa(enrollments) == pytest.approx(3.0)


def test_uneven_weighting_by_hand():
    # (3.3 * 4 + 2.7 * 3 + 4.0 * 1) / 8 = 25.3 / 8 = 3.1625
    enrollments = [
        {'grade': 'B+', 'credits': 4},
        {'grade': 'B-', 'credits': 3},
        {'grade': 'A', 'credits': 1},
    ]
    assert calculate_gpa(enrollments) == pytest.approx(3.1625)


def test_uniform_grades_ignore_weighting():
    enrollments = [{'grade': 'A', 'credits': 4}, {'grade': 'A', 'credits': 1}]
    assert calculate_gpa(enrollments) == pytest.approx(4.0)


def test_a_plus_goes_above_four():
    assert calculate_gpa([{'grade': 'A+', 'credits': 3}]) == pytest.approx(4.3)


def test_ungraded_enrollment_is_skipped_not_an_f():
    enrollments = [{'grade': 'A', 'credits': 3}, {'grade': None, 'credits': 4}]
    assert calculate_gpa(enrollments) == pytest.approx(4.0)


def test_missing_grade_key_is_skipped():
    enrollments = [{'grade': 'B', 'credits': 3}, {'credits': 4}]
    assert calculate_gpa(enrollments) == pytest.approx(3.0)


def test_unknown_grade_is_skipped_not_a_crash():
    enrollments = [{'grade': 'B', 'credits': 3}, {'grade': 'S', 'credits': 2}]
    assert calculate_gpa(enrollments) == pytest.approx(3.0)


def test_every_grade_ignored_returns_zero():
    enrollments = [{'grade': None, 'credits': 3}, {'grade': 'S', 'credits': 2}]
    assert calculate_gpa(enrollments) == 0


@pytest.mark.parametrize('grade', GRADE_POINTS)
def test_each_grade_maps_to_its_points(grade):
    assert calculate_gpa([{'grade': grade, 'credits': 3}]) == pytest.approx(GRADE_POINTS[grade])


def test_library_does_not_import_app():
    import gpa_calculator
    with open(gpa_calculator.__file__) as f:
        source = f.read()
    assert 'from app' not in source and 'import app' not in source
