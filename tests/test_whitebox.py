"""White-box structural tests; IDs map to branches and MC/DC in final report.

Test pairs WB009/010 and WB011/012 demonstrate condition independence for
`decision == 'WAITLISTED' and student_id not in course.waitlist`.
"""
from copy import deepcopy
import pytest
from registration import (Student, Course, check_credit_limit,
                          prerequisites_satisfied, registration_decision,
                          register_course, withdraw_course)


def fixture(*, current=10, new=3, dues=0, full=False, enrolled=0,
            capacity=10, already=False, prereq=False, done=True, listed=False):
    s = Student("S42", {"PRE"} if done else set(), current, dues,
                {"CS201"} if already else set())
    c = Course("CS201", new, capacity, capacity if full else enrolled,
               {"PRE"} if prereq else set(), ["S42"] if listed else [])
    return s, c


def test_WB001_due_invalid_guard_true():
    s, c = fixture(dues=-1)
    with pytest.raises(ValueError, match="^Invalid dues$"):
        registration_decision(s, c)


def test_WB002_capacity_invalid_guard_true():
    s, c = fixture(capacity=0)
    with pytest.raises(ValueError, match="^Invalid capacity or enrollment$"):
        registration_decision(s, c)


def test_WB003_bad_enrollment_low_guard():
    s, c = fixture(enrolled=-1)
    with pytest.raises(ValueError, match="^Invalid capacity or enrollment$"):
        registration_decision(s, c)


def test_WB004_bad_enrollment_high_guard():
    s, c = fixture(enrolled=11)
    with pytest.raises(ValueError, match="^Invalid capacity or enrollment$"):
        registration_decision(s, c)


def test_WB005_prereq_empty_short_circuit():
    assert prerequisites_satisfied(set(), set()) is True


def test_WB006_prereq_nonempty_not_met():
    assert prerequisites_satisfied({"A"}, {"A", "B"}) is False


def test_WB007_current_lower_valid_pair():
    assert check_credit_limit(0, 1) is True


def test_WB008_current_lower_invalid_pair():
    with pytest.raises(ValueError, match="^Invalid current credits$"):
        check_credit_limit(-1, 1)


def test_WB009_mcdc_first_operand_true_second_true():
    s, c = fixture(full=True)
    assert register_course(s, c) == "WAITLISTED"
    assert c.waitlist == ["S42"]


def test_WB010_mcdc_first_operand_false_second_not_evaluated():
    s, c = fixture(full=False)
    assert register_course(s, c) == "REGISTERED"
    assert c.waitlist == []


def test_WB011_mcdc_second_operand_false_first_true():
    s, c = fixture(full=True, listed=True)
    initial = deepcopy((s, c))
    assert register_course(s, c) == "WAITLISTED"
    assert (s, c) == initial


def test_WB012_mcdc_second_operand_true_first_true():
    s, c = fixture(full=True, listed=False)
    assert register_course(s, c) == "WAITLISTED"
    assert c.waitlist == ["S42"]


def test_WB013_reach_credit_exactly_max_boundary():
    s, c = fixture(current=15, new=3)
    assert registration_decision(s, c) == "REGISTERED"


def test_WB014_reach_full_capacity_branch():
    s, c = fixture(full=True)
    assert registration_decision(s, c) == "WAITLISTED"


def test_WB015_withdraw_true_branch():
    s, c = fixture(current=10, enrolled=2, already=True)
    assert withdraw_course(s, c) is True
    assert c.enrolled == 1


def test_WB016_withdraw_false_branch():
    s, c = fixture()
    original = deepcopy((s, c))
    assert withdraw_course(s, c) is False
    assert (s, c) == original


def test_WB017_extra_regression_priority_due_vs_duplicate():
    s, c = fixture(dues=1, already=True)
    assert registration_decision(s, c) == "DUES_BLOCK"


def test_WB018_credit_invalid_new_and_valid_current():
    with pytest.raises(ValueError, match="^Invalid course credits$"):
        check_credit_limit(0, 5)
