# GitHub PR descriptions (templates; NOT actual PRs)

## PR 1 — blackbox-testing -> main
**Title:** test: add requirements-derived black-box tests and CI

**Summary:** Add 62 pytest cases mapped to ECP, BVA, decision-table and state-change checks. Ensure the first test run is preserved even though the starter has legitimate failures. Add GitHub Actions pytest/coverage workflow.

**Test evidence:** On original starter, 18 failed and 44 passed, with 96.49% statement and 92.31% branch coverage.

**Linked issues:** DEF-01 through DEF-05 (link after creating issues). **Reviewer:** _Ask an actual teammate for review and address comments._

## PR 2 — whitebox-testing -> main
**Title:** test: add CFG-basis structural tests and MC/DC evidence

**Summary:** Add WB001–WB018 structural tests, path and compound-condition analysis. Keep starter defects visible, including an unreachable waitlist branch.

**Test evidence:** On original implementation with both suites, legitimate failures remain; see `docs/evidence/pre_fix_all_pytest.txt`.

**Linked issues:** DEF-01 through DEF-05. **Reviewer:** _Ask a different team member, if available._

## PR 3 — defect-fixes -> main
**Title:** fix: conform registration logic to FR-01, FR-03, FR-04, FR-08 and FR-13

**Summary:** Apply five minimal fixes without changing expected test outcomes. Include report, test design sheets, CFGs, evidence, and defect issue drafts.

**Tests:** 80 passed. Statement 100%; branch 100% on registration.py.

**Closes:** Add #issue numbers only when issues exist. **Reviewer:** _Actual teammate review required._

NOTE: This document contains templates, not fabricated GitHub PR references or reviews.
