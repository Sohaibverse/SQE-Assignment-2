# [DEF-03] Nonzero small dues do not block registration

**Status:** Fixed locally in `defect-fixes`; **GitHub Issue not yet created**.  
**Requirements:** FR-04, FR-09  
**Severity:** Functional correctness

## Reproduction (original starter implementation)
```python
from registration import Student, Course, registration_decision, register_course, withdraw_course, check_credit_limit, prerequisites_satisfied
registration_decision(Student("S1",outstanding_dues=1),Course("CS201",3,10))
```

**Expected:** DUES_BLOCK; any positive amount blocks  
**Actual on starter:** REGISTERED; source used > 1000  
**Failing pytest IDs:** BB002, BB003, BB028, BB055, WB017

## Correction and verification
Use outstanding_dues > 0. The final included test suite passes. Source tests are authoritative and were **not** modified to conform to buggy behavior.

**GitHub issue URL:** _Add real link after creating this issue on GitHub._
