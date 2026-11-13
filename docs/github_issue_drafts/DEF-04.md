# [DEF-04] Full courses fail to waitlist and mutate enrollment

**Status:** Fixed locally in `defect-fixes`; **GitHub Issue not yet created**.  
**Requirements:** FR-08, FR-12  
**Severity:** Functional correctness

## Reproduction (original starter implementation)
```python
from registration import Student, Course, registration_decision, register_course, withdraw_course, check_credit_limit, prerequisites_satisfied
register_course(Student("S1"),Course("CS201",3,1,enrolled=1))
```

**Expected:** WAITLISTED; append S1 once; leave credits, registrations and enrollment unchanged  
**Actual on starter:** REGISTERED; enrollment became 2 despite capacity 1  
**Failing pytest IDs:** BB011, BB024, BB032, BB053, BB054, WB009, WB014

## Correction and verification
Change availability check to enrolled == capacity; retain waitlist deduplication. The final included test suite passes. Source tests are authoritative and were **not** modified to conform to buggy behavior.

**GitHub issue URL:** _Add real link after creating this issue on GitHub._
