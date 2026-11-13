# [DEF-01] Credit total of exactly 18 is incorrectly rejected

**Status:** Fixed locally in `defect-fixes`; **GitHub Issue not yet created**.  
**Requirements:** FR-01, FR-07  
**Severity:** Functional correctness

## Reproduction (original starter implementation)
```python
from registration import Student, Course, registration_decision, register_course, withdraw_course, check_credit_limit, prerequisites_satisfied
check_credit_limit(15,3)
```

**Expected:** True; total 18 is eligible  
**Actual on starter:** False; source used strict < 18  
**Failing pytest IDs:** BB010, BB015, BB016, BB038, BB039, WB013

## Correction and verification
Replace strict < with <= in check_credit_limit (registration.py). The final included test suite passes. Source tests are authoritative and were **not** modified to conform to buggy behavior.

**GitHub issue URL:** _Add real link after creating this issue on GitHub._
