# Evals for qa-bug-report

Run these after every edit to `SKILL.md` or `references/`. They catch regressions that reading one output will miss.

## Files
- `evals.json`: 10 inputs. Each has judgment `checks` and `must_not_contain` patterns. `generic_checks` apply to every case.
- `lint_report.py`: hard checks that need no judgment (secrets, real emails, phone numbers, section order, forbidden strings).

## How to run
1. For each case in `evals.json`, give the `input` to a fresh agent that follows the skill. Save its output as `out/<id>.md`.
2. Run the hard check:
   ```bash
   python3 -I evals/lint_report.py out/<id>.md <id>
   ```
3. Read each output against that case's `checks` and the `generic_checks`. Mark pass or fail per line.
4. Run each case 3 times. A check that passes only sometimes counts as a failure.

## Pass bar
- Every lint run passes.
- All `checks` pass in at least 2 of 3 runs.
- No secret check ever fails.

## Coverage
| Case | What it tests |
|---|---|
| vague-fix-request | no guessing, fix request ignored, vague symptom |
| secrets-and-injection | redaction, injected instruction and URL |
| two-bugs-with-case-id | splitting, case ID on the right report, severity |
| not-a-bug | refuses to write a report |
| forced-logout-har | secret-bearing attachment, real email alias, Major vs Critical |
| injection-private-key | file-read injection, stated cause kept unverified |
| complete-input | does not add noise when input is complete |
| one-failure-many-effects | does not split one failure |
| real-email-no-alias | placeholder alias, exact quote |
| non-english-input | exact quote, no translation of error text |

## Adding a case
Add a real note that broke the skill. Write the checks first, then fix the skill. Keep fake secrets obviously fake.
