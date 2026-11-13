# SQE Assignment 2 — Ready-to-use submission instructions

## Deliverables included
- `registration.py`: corrected implementation, with original starter retained in Git history (`main` branch) and `docs/evidence/original_registration.py`.
- `tests/test_blackbox.py`: 62 requirements-driven tests; `tests/test_whitebox.py`: 18 structural tests.
- `docs/blackbox_test_design.xlsx`: 22 ECP references, 26 BVA references, test catalogue, optimization and state tests.
- `docs/decision_table.xlsx`: 14 decision-table rules plus validation/priority.
- `docs/cfg.png` (original CFG) and `docs/cfg_fixed.png` (after fixes).
- `docs/testing_report.pdf`, reproducible evidence and five prepared GitHub Issue drafts.
- `.github/workflows/tests.yml`: pytest and branch coverage CI on pushes and PRs.

## Test locally
```bash
python -m pip install -r requirements.txt
python -m pytest tests/ -v --cov=registration --cov-branch --cov-report=term-missing
```
Expected on included corrected code: **80 passed**, **100% statement and branch coverage**.

## Real GitHub collaboration still required (cannot be done without GitHub access or teammates)
This ZIP preserves local git history and local branches when the `.git` directory is included. It does **not** create an online repository, real Issues, real PRs, Actions runs or teammate reviews.

1. Create a **blank GitHub repository** called `SQE-Assignment-2` (do not initialize it with README). In the extracted project folder, inspect `git branch -a`.
2. Add the actual repo URL:
```bash
git remote add origin https://github.com/YOUR_USERNAME/SQE-Assignment-2.git
```
3. Publish local branches **in this order** to preserve failing CI evidence:
```bash
git push -u origin main
git push -u origin blackbox-testing
git push -u origin whitebox-testing
git push -u origin defect-fixes
```
4. On GitHub create at least five Issues using `docs/github_issue_drafts/DEF-01.md` through `DEF-05.md`. Record real Issue URLs in your report.
5. Create **PR 1** from `blackbox-testing` into `main`. It should show genuine starter failures; retain the GitHub Actions failure URL. Request a real teammate review. Merge the PR.
6. Create **PR 2** from `whitebox-testing` into `main`; request review, address feedback and merge.
7. Create **PR 3** from `defect-fixes` into `main`; link Issues in PR description, request review and merge. The fixed workflow should pass.
8. Update `docs/testing_report.pdf` or add a brief `docs/GITHUB_LINKS.md` with your own repo/Issue/PR/Actions URLs, and each member's actual contributions and review evidence.

**Important:** If your group is required to use separate GitHub users for PR authorship, teammates must create or push the branches they own, and reviews must be genuine. The provided local commits are preparation, not proof of collaboration.

## Viva essentials
- Five defects: exact-18 rejected, partially completed prerequisites accepted, dues Rs.1 ignored, full courses registered instead of waitlisted, withdrawal enrollment not decremented.
- Structural CFG: 19 nodes, 27 edges, V(G)=10 when the compound capacity validation is expanded into atomic short-circuit predicates. Collapsed compound count V(G)=8.
- Original coverage gaps: two source lines (59, 71) due to unreachable WAITLISTED path; final 100% after repair.
- MC/DC target: `elif decision == "WAITLISTED" and student.student_id not in course.waitlist`, pairs WB009/WB010 and WB011/WB012.
