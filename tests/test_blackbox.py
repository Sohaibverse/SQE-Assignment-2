"""Requirements-derived black-box tests (FR-01 through FR-15).

Each canonical BB id is mapped to ECP, BVA and/or decision-table rows in
`docs/blackbox_test_design.xlsx`. Expected results come from REQUIREMENTS.md.
Do not weaken expectations merely because the original SUT is defective.
"""
from copy import deepcopy
import pytest
from registration import (Student, Course, check_credit_limit,
                          prerequisites_satisfied, registration_decision,
                          register_course, withdraw_course)


def scenario(*, credits=10, course_credits=3, dues=0, completed=(),
             registered=(), required=(), capacity=10, enrolled=0,
             waitlist=(), sid="S001"):
    student = Student(sid, set(completed), credits, dues, set(registered))
    course = Course("CS201", course_credits, capacity, enrolled,
                    set(required), list(waitlist))
    return student, course


# Parameter tuple: ID, scenario inputs, expected status or exact ValueError message.
# These are CANONICAL cases - a single execution may serve several design methods.
DECISION_CASES = [
    ("BB001", {}, "REGISTERED"),
    ("BB002", {"dues": 1}, "DUES_BLOCK"),
    ("BB003", {"dues": 1000}, "DUES_BLOCK"),
    ("BB004", {"dues": 1001}, "DUES_BLOCK"),
    ("BB005", {"registered": ["CS201"]}, "ALREADY_REGISTERED"),
    ("BB006", {"required": ["CS101", "MATH101"], "completed": ["CS101"]}, "PREREQUISITES_MISSING"),
    ("BB007", {"required": ["CS101", "MATH101"]}, "PREREQUISITES_MISSING"),
    ("BB008", {"required": ["CS101", "MATH101"], "completed": ["CS101", "MATH101"]}, "REGISTERED"),
    ("BB009", {"credits": 16}, "CREDIT_LIMIT"),
    ("BB010", {"credits": 15}, "REGISTERED"),
    ("BB011", {"enrolled": 10}, "WAITLISTED"),
    ("BB012", {"enrolled": 9}, "REGISTERED"),
    ("BB013", {"credits": 0, "course_credits": 1}, "REGISTERED"),
    ("BB014", {"credits": 18, "course_credits": 1}, "CREDIT_LIMIT"),
    ("BB015", {"credits": 17, "course_credits": 1}, "REGISTERED"),
    ("BB016", {"credits": 14, "course_credits": 4}, "REGISTERED"),
    ("BB017", {"credits": 15, "course_credits": 4}, "CREDIT_LIMIT"),
    ("BB018", {"credits": -1}, "Invalid current credits"),
    ("BB019", {"credits": 19}, "Invalid current credits"),
    ("BB020", {"course_credits": 0}, "Invalid course credits"),
    ("BB021", {"course_credits": 5}, "Invalid course credits"),
    ("BB022", {"capacity": 0}, "Invalid capacity or enrollment"),
    ("BB023", {"capacity": 1, "enrolled": 0}, "REGISTERED"),
    ("BB024", {"capacity": 1, "enrolled": 1}, "WAITLISTED"),
    ("BB025", {"enrolled": -1}, "Invalid capacity or enrollment"),
    ("BB026", {"enrolled": 11}, "Invalid capacity or enrollment"),
    ("BB027", {"dues": -1}, "Invalid dues"),
    ("BB028", {"dues": 1, "registered": ["CS201"], "required": ["X"], "credits": 18, "enrolled": 10}, "DUES_BLOCK"),
    ("BB029", {"registered": ["CS201"], "required": ["X"], "credits": 18, "enrolled": 10}, "ALREADY_REGISTERED"),
    ("BB030", {"required": ["X"], "credits": 18, "enrolled": 10}, "PREREQUISITES_MISSING"),
    ("BB031", {"credits": 18, "enrolled": 10}, "CREDIT_LIMIT"),
    ("BB032", {"credits": 15, "enrolled": 10}, "WAITLISTED"),
    ("BB033", {"dues": -1, "capacity": 0}, "Invalid dues"),
    ("BB034", {"dues": 1, "capacity": 0}, "Invalid capacity or enrollment"),
    ("BB035", {"credits": -1, "course_credits": 0}, "Invalid current credits"),
    ("BB036", {"capacity": -1}, "Invalid capacity or enrollment"),
]


@pytest.mark.parametrize("case_id,kwargs,expected", DECISION_CASES, ids=[x[0] for x in DECISION_CASES])
def test_registration_decision(case_id, kwargs, expected):
    s, c = scenario(**kwargs)
    before = deepcopy((s, c))
    if expected.startswith("Invalid"):
        with pytest.raises(ValueError, match=f"^{expected}$"):
            registration_decision(s, c)
    else:
        assert registration_decision(s, c) == expected, case_id
    assert (s, c) == before, f"FR-10: {case_id} changed decision-only state"


@pytest.mark.parametrize("case_id,current,new,expected", [
    ("BB037", 0, 1, True), ("BB038", 14, 4, True),
    ("BB039", 15, 3, True), ("BB040", 16, 3, False),
    ("BB041", 18, 1, False), ("BB042", -1, 1, "Invalid current credits"),
    ("BB043", 19, 1, "Invalid current credits"),
    ("BB044", 0, 0, "Invalid course credits"),
    ("BB045", 0, 5, "Invalid course credits"),
    ("BB046", -1, 0, "Invalid current credits"),
], ids=[f"BB{i:03d}" for i in range(37,47)])
def test_credit_limit(case_id, current, new, expected):
    if isinstance(expected, str):
        with pytest.raises(ValueError, match=f"^{expected}$"):
            check_credit_limit(current, new)
    else:
        assert check_credit_limit(current, new) is expected, case_id


@pytest.mark.parametrize("case_id,completed,required,expected", [
    ("BB047", (), (), True),
    ("BB048", (), ("CS101",), False),
    ("BB049", ("CS101",), ("CS101", "MATH101"), False),
    ("BB050", ("CS101", "MATH101"), ("CS101", "MATH101"), True),
    ("BB051", ("CS101",), ("CS101",), True),
], ids=[f"BB{i:03d}" for i in range(47,52)])
def test_prerequisites(case_id, completed, required, expected):
    assert prerequisites_satisfied(set(completed), set(required)) is expected, case_id


def test_BB052_successful_registration_updates_all_three_fields():
    s, c = scenario(credits=10, enrolled=2)
    assert register_course(s, c) == "REGISTERED"
    assert s.registered_courses == {"CS201"}
    assert s.current_credits == 13
    assert c.enrolled == 3
    assert c.waitlist == []


def test_BB053_waitlist_updates_only_waitlist():
    s, c = scenario(enrolled=10)
    before = (s.current_credits, set(s.registered_courses), c.enrolled)
    assert register_course(s, c) == "WAITLISTED"
    assert c.waitlist == ["S001"]
    assert (s.current_credits, s.registered_courses, c.enrolled) == before


def test_BB054_waitlist_does_not_insert_duplicate_id():
    s, c = scenario(enrolled=10, waitlist=["S001"])
    before = deepcopy((s, c))
    assert register_course(s, c) == "WAITLISTED"
    assert (s, c) == before


@pytest.mark.parametrize("case_id,kwargs,status", [
    ("BB055", {"dues": 1}, "DUES_BLOCK"),
    ("BB056", {"registered": ["CS201"]}, "ALREADY_REGISTERED"),
    ("BB057", {"required": ["X"]}, "PREREQUISITES_MISSING"),
    ("BB058", {"credits": 18}, "CREDIT_LIMIT"),
], ids=[f"BB{i:03d}" for i in range(55,59)])
def test_unsuccessful_registration_preserves_state(case_id, kwargs, status):
    s, c = scenario(**kwargs)
    before = deepcopy((s, c))
    assert register_course(s, c) == status, case_id
    assert (s, c) == before


def test_BB059_withdraw_decrements_course_enrollment():
    s, c = scenario(credits=9, enrolled=4, registered=["CS201"])
    assert withdraw_course(s, c) is True
    assert s.current_credits == 6
    assert s.registered_courses == set()
    assert c.enrolled == 3


def test_BB060_withdraw_not_enrolled_preserves_state():
    s, c = scenario(credits=9, enrolled=4)
    before = deepcopy((s, c))
    assert withdraw_course(s, c) is False
    assert (s, c) == before


def test_BB061_register_then_withdraw_round_trip():
    s, c = scenario(credits=8, enrolled=2)
    baseline = deepcopy((s, c))
    assert register_course(s, c) == "REGISTERED"
    assert withdraw_course(s, c) is True
    assert (s, c) == baseline


def test_BB062_register_invalid_dues_raises_without_changes():
    s, c = scenario(dues=-1)
    baseline = deepcopy((s, c))
    with pytest.raises(ValueError, match="^Invalid dues$"):
        register_course(s, c)
    assert (s, c) == baseline
