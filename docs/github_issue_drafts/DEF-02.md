# [DEF-02] Partial completion of prerequisites is wrongly accepted

**Status:** Fixed locally in `defect-fixes`; **GitHub Issue not yet created**.  
**Requirements:** FR-03, FR-06  
**Severity:** Functional correctness

## Reproduction (original starter implementation)
```python
from registration import Student, Course, registration_decision, register_course, withdraw_course, check_credit_limit, prerequisites_satisfied
prerequisites_satisfied({"CS101"},{"CS101","MATH101"})
```

**Expected:** False; ALL required courses must be completed  
**Actual on starter:** True; any intersection counted as completion  
**Failing pytest IDs:** BB006, BB049, WB006

## Correction and verification
Use required.issubset(completed) instead of bool(intersection). The final included test suite passes. Source tests are authoritative and were **not** modified to conform to buggy behavior.

**GitHub issue URL:** _Add real link after creating this issue on GitHub._
