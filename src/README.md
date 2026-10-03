# GPA-Calculator-CS3250-aden

Credit-weighted GPA calculation from letter grades and credit hours. Built for CS3250 Project 1 - GPA Calculator.

## Install

```bash
pip install GPA-Calculator-CS3250-aden
```

The distribution name is `GPA-Calculator-CS3250-aden`, but the import name is `gpa_calculator`.

## Usage

```python
from gpa_calculator import calculate_gpa

enrollments = [
    {'grade': 'A', 'credits': 3},
    {'grade': 'B+', 'credits': 4},
    {'grade': None, 'credits': 3},   # not graded yet - ignored
]

gpa = calculate_gpa(enrollments)
print(f'{gpa:.2f}')   # 3.60
```

`calculate_gpa(enrollments)` takes a list of dicts, each with a `grade` and a `credits` key, and returns `sum(points * credits) / sum(credits)` over the graded ones.

- Enrollments with no grade, or a grade not on the scale below, are skipped - not counted as an F.
- Returns `0` when there are no graded credits.
- The result is not rounded; round it when you display it.

## Grade scale

| Grade | Points | Grade | Points | Grade | Points |
|---|---|---|---|---|---|
| A+ | 4.3 | B+ | 3.3 | C+ | 2.3 |
| A | 4.0 | B | 3.0 | C | 2.0 |
| A- | 3.7 | B- | 2.7 | C- | 1.7 |
| D+ | 1.3 | D | 1.0 | D- | 0.7 |
| F | 0.0 | | | | |

The table is also available as `gpa_calculator.GRADE_POINTS`. Because A+ is 4.3, a GPA above 4.0 is valid.

## Links

- Source: https://github.com/AdenPotato/CS3250-project-1
- Issues: https://github.com/AdenPotato/CS3250-project-1/issues
