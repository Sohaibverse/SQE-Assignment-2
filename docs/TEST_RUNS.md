# Reproducible test evidence

All commands run locally using Python / pytest and the instructor-supplied implementation. Expected values are from `REQUIREMENTS.md`.

| Stage | Source code | Cases | Results | Statement | Branch | Source coverage |
|---|---|---:|---|---:|---:|---:|
| 1: Original + black-box | Initial instructor starter | 62 | 44 pass, 18 fail | 96.49% (55/57) | 92.31% (24/26) | 95.18% |
| 2: Original + black/white | Initial instructor starter | 80 | 53 pass, 27 fail | 96.49% (55/57) | 92.31% (24/26) | 95.18% |
| 3: Corrected + black/white | `defect-fixes` code | 80 | 80 pass | 100% (58/58) | 100% (26/26) | 100% |

Original uncovered source: `registration.py` lines 59 and 71, arcs 58->59 and 70->71. Waitlist branch cannot be triggered in original code because `enrolled > capacity` first raises an exception (FR-15 validation). A waitlisted status is therefore unreachable in original `registration_decision`.

To re-run with the corrected code:
```bash
python -m pip install -r requirements.txt
python -m pytest tests/test_blackbox.py -v --cov=registration --cov-branch --cov-report=term-missing
python -m pytest tests/ -v --cov=registration --cov-branch --cov-report=term-missing
```

Machine-readable coverage JSON and full pytest logs are in `docs/evidence/`. The GitHub Actions workflow records new CI run artifacts after you push branches. Local logs are **not** GitHub Actions screenshots or proof of online CI execution.
