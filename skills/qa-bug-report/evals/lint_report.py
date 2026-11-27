#!/usr/bin/env python3
"""Hard checks for a qa-bug-report output.

Usage: python3 -I lint_report.py REPORT_FILE [EVAL_ID]

Checks that need no judgment:
  - no secret-shaped strings (bearer tokens, API keys, session cookies)
  - no real-looking email addresses (only @example.test, @example.com, .org, .net allowed)
  - no phone numbers
  - the eval's own must_not_contain patterns, when EVAL_ID is given
  - sections appear in the required order (when a report is present)

Exit code 0 means all hard checks pass. Judgment checks in evals.json still need a reader.
"""

import json
import re
import sys
from pathlib import Path

SECRET_PATTERNS = [
    (r"Bearer\s+(?!\[REDACTED)[A-Za-z0-9._\-]{8,}", "bearer token"),
    (r"\bsk_(live|test)_[A-Za-z0-9]+", "API key"),
    (r"(?i)\bsession(id)?\s*=\s*(?!\[REDACTED)[A-Za-z0-9._\-]{6,}", "session cookie"),
    (r"(?i)\b(password|passwd|pwd)\s*[:=]\s*(?!\[REDACTED)\S{4,}", "password"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "private key"),
    (r"\bAKIA[0-9A-Z]{16}\b", "AWS key id"),
]

EMAIL = re.compile(r"[A-Za-z0-9._%+\-]+@([A-Za-z0-9\-]+\.)+[A-Za-z]{2,}")
# Only the placeholder domain is safe: qa.user.1@example.test, a@example.com and so on.
SAFE_EMAIL = re.compile(r"@example\.(test|com|org|net)$", re.I)
PHONE = re.compile(r"(?<!\d)(\+?\d{1,3}[\s\-.]?)?(\(?\d{3}\)?[\s\-.]?)\d{3}[\s\-.]?\d{4}(?!\d)")

SECTION_ORDER = [
    "Environment",
    "Severity",
    "Steps to reproduce",
    "Expected result",
    "Actual result",
    "Frequency",
    "Evidence",
    "Questions",
]


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2

    text = Path(sys.argv[1]).read_text(encoding="utf-8")
    failures = []

    for pattern, label in SECRET_PATTERNS:
        if re.search(pattern, text):
            failures.append(f"secret-shaped string found: {label}")

    for m in EMAIL.finditer(text):
        if not SAFE_EMAIL.search(m.group(0)):
            failures.append(f"real-looking email address found: {m.group(0)[:3]}...")

    # Phone check ignores digit runs that are build numbers, versions or counts.
    for m in PHONE.finditer(text):
        digits = re.sub(r"\D", "", m.group(0))
        if len(digits) >= 10:
            failures.append("phone-number-shaped string found")

    if len(sys.argv) >= 3:
        evals = json.loads((Path(__file__).parent / "evals.json").read_text(encoding="utf-8"))
        case = next((c for c in evals["cases"] if c["id"] == sys.argv[2]), None)
        if case is None:
            print(f"unknown eval id: {sys.argv[2]}")
            return 2
        for pattern in case["must_not_contain"]:
            if re.search(pattern, text):
                failures.append(f"forbidden text from eval '{case['id']}' found: /{pattern}/")

    # Order check applies only to text that looks like a report.
    # Match section names only where they start a line (as a heading or a bold field),
    # so a word like "Questions" inside a sentence does not count.
    def heading_pos(name: str) -> int:
        m = re.search(rf"(?im)^[\s>#*\-]*\**{re.escape(name)}\b", text)
        return m.start() if m else -1

    positions = [(s, heading_pos(s)) for s in SECTION_ORDER if heading_pos(s) != -1]
    if len(positions) >= 4:
        idx = [p for _, p in positions]
        if idx != sorted(idx):
            failures.append("sections are out of the required order")

    if failures:
        print("FAIL")
        for f in failures:
            print(f" - {f}")
        return 1
    print("PASS (hard checks only; review judgment checks in evals.json)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
