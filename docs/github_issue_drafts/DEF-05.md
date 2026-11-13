# [DEF-05] Withdrawal does not decrement course enrollment

**Status:** Fixed locally in `defect-fixes`; **GitHub Issue not yet created**.  
**Requirements:** FR-13  
**Severity:** Functional correctness

## Reproduction (original starter implementation)
```python
from registration import Student, Course, registration_decision, register_course, withdraw_course, check_credit_limit, prerequisites_satisfied
withdraw_course(Student("S1",current_credits=3,registered_courses={"CS201"}),Course("CS201",3,10,enrolled=1))
```

**Expected:** True; credits=0, registered empty, enrolled=0  
**Actual on starter:** True; credits=0 and registered empty, but enrolled=1  
**Failing pytest IDs:** BB059, BB061, WB015

## Correction and verification
Decrement course.enrolled by one when withdrawal succeeds. The final included test suite passes. Source tests are authoritative and were **not** modified to conform to buggy behavior.

**GitHub issue URL:** _Add real link after creating this issue on GitHub._
