# Evals for qa-test-cases

Run these after every edit to `SKILL.md` or `references/`. They catch regressions that reading one output will miss.

## Files
- `evals.json`: 10 inputs. Each has judgment `checks` and `must_not_contain` patterns. `generic_checks` apply to every case.
- `lint_cases.py`: hard checks that need no judgment (CSV header and columns, ID sequence, allowed values, Markdown and CSV agree, 25-case cap, secrets, real emails, phone numbers).

## How to run
1. For each case, give its `input` to a fresh agent that follows the skill. The two `repo` cases need `/Users/ocgt/Desktop/hafizu-portfolio` on disk. Tell the agent not to read the evals folder. Save the output (Markdown and CSV) as `out/<id>.md`.
2. Run the hard check:
   ```bash
   python3 -I evals/lint_cases.py out/<id>.md <id>
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
| repo-skills-badge | real commit: docs-only parts skipped, env default, drift risk, priority cap |
| repo-readme-badge-api | real commit: many similar badges, dynamic text, env-dependent cases |
| pasted-login-lockout | normal feature: exact messages, boundary, clock control to Questions |
| pasted-api-only | API-only change: technical verification, header-only CSV |
| pasted-version-bump | version and lockfile only: zero cases |
| pasted-docs-only | docs only: zero cases |
| pasted-multi-user-invite | two roles, aliases, missing test inbox |
| pasted-injection | injected instruction in a code comment |
| pasted-env-default | env-dependent default, no .env read |
| pasted-dev-handoff | technical asks traced to user journeys, or sent to Questions |

## Adding a case
Add a real change that broke the skill. Write the checks first, then fix the skill. Keep fake secrets obviously fake.
