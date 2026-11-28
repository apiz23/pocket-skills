#!/usr/bin/env python3
"""Hard checks for a qa-test-cases output.

Usage: python3 -I lint_cases.py OUTPUT_FILE [EVAL_ID]

The output file holds the Markdown cases and the CSV block. Checks that need no judgment:
  - CSV header is exact (quoted or unquoted) and every row has 10 columns
  - IDs run QA-001, QA-002 ... with no gaps
  - Priority is High, Medium or Low; Basis is Code, Spec or Unclear; Status is 'Not run'
  - Steps and Expected Result are not empty
  - Markdown case headings and CSV rows list the same IDs in the same order
  - at most 25 cases in the set
  - Summary has 'Target for testing' and 'Evidence level'
  - no secret-shaped strings, real-looking emails or phone numbers
  - the eval's own must_not_contain patterns, when EVAL_ID is given

Exit code 0 means all hard checks pass. Judgment checks in evals.json still need a reader.
"""

import csv
import io
import json
import re
import sys
from pathlib import Path

HEADER = "ID,Title,Priority,Platform,Precondition,Test Data,Steps,Expected Result,Basis,Status"
PRIORITIES = {"High", "Medium", "Low"}
BASES = {"Code", "Spec", "Unclear"}

SECRET_PATTERNS = [
    (r"Bearer\s+(?!\[REDACTED)[A-Za-z0-9._\-]{8,}", "bearer token"),
    (r"\bsk_(live|test)_[A-Za-z0-9]+", "API key"),
    (r"(?i)\b(password|passwd|pwd)\s*[:=]\s*(?!\[REDACTED)\S{4,}", "password value"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "private key"),
    (r"\bAKIA[0-9A-Z]{16}\b", "AWS key id"),
]
EMAIL = re.compile(r"[A-Za-z0-9._%+\-]+@([A-Za-z0-9\-]+\.)+[A-Za-z]{2,}")
SAFE_EMAIL = re.compile(r"@example\.(test|com|org|net)$", re.I)
PHONE = re.compile(r"(?<!\d)(\+?\d{1,3}[\s\-.]?)?(\(?\d{3}\)?[\s\-.]?)\d{3}[\s\-.]?\d{4}(?!\d)")


def csv_block(text: str):
    m = re.search(r"```csv\s*\n(.*?)```", text, re.S)
    return m.group(1).strip("\n") if m else None


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2

    text = Path(sys.argv[1]).read_text(encoding="utf-8")
    fails = []

    # Summary markers
    for marker in ("Target for testing", "Evidence level"):
        if marker.lower() not in text.lower():
            fails.append(f"Summary is missing '{marker}'")

    # CSV
    block = csv_block(text)
    rows = []
    if block is None:
        fails.append("no ```csv block found")
    else:
        lines = block.splitlines()
        # Parse the header so a quoted or unquoted header both pass. Both import
        # correctly, and format.md tells the agent to quote every cell.
        header_row = next(csv.reader([lines[0]]), []) if lines else []
        if header_row != HEADER.split(","):
            fails.append("CSV header is not exact")
        else:
            reader = csv.reader(io.StringIO("\n".join(lines[1:])))
            for i, row in enumerate(reader, start=1):
                if not row:
                    continue
                if len(row) != 10:
                    fails.append(f"CSV row {i} has {len(row)} columns, expected 10")
                    continue
                rows.append(row)

    ids = []
    for i, row in enumerate(rows, start=1):
        cid, _title, prio, _plat, _pre, _data, steps, expected, basis, status = row
        ids.append(cid)
        if cid != f"QA-{i:03d}":
            fails.append(f"CSV row {i} has ID {cid}, expected QA-{i:03d}")
        if prio not in PRIORITIES:
            fails.append(f"{cid}: Priority '{prio}' is not High, Medium or Low")
        if basis not in BASES:
            fails.append(f"{cid}: Basis '{basis}' is not Code, Spec or Unclear")
        if status != "Not run":
            fails.append(f"{cid}: Status is '{status}', expected 'Not run'")
        if not steps.strip():
            fails.append(f"{cid}: Steps is empty")
        if not expected.strip():
            fails.append(f"{cid}: Expected Result is empty")

    if len(rows) > 25:
        fails.append(f"{len(rows)} cases in one set, maximum is 25")

    # Markdown headings must match CSV IDs
    md_ids = re.findall(r"(?m)^#{2,4}\s*(QA-\d{3})\b", text)
    if md_ids != ids:
        fails.append(f"Markdown case headings {md_ids} do not match CSV IDs {ids}")

    # Secrets, emails, phones
    for pattern, label in SECRET_PATTERNS:
        if re.search(pattern, text):
            fails.append(f"secret-shaped string found: {label}")
    for m in EMAIL.finditer(text):
        if not SAFE_EMAIL.search(m.group(0)):
            fails.append(f"real-looking email address found: {m.group(0)[:3]}...")
    for m in PHONE.finditer(text):
        if len(re.sub(r"\D", "", m.group(0))) >= 10:
            fails.append("phone-number-shaped string found")

    if len(sys.argv) >= 3:
        evals = json.loads((Path(__file__).parent / "evals.json").read_text(encoding="utf-8"))
        case = next((c for c in evals["cases"] if c["id"] == sys.argv[2]), None)
        if case is None:
            print(f"unknown eval id: {sys.argv[2]}")
            return 2
        for pattern in case["must_not_contain"]:
            if re.search(pattern, text):
                fails.append(f"forbidden text from eval '{case['id']}' found: /{pattern}/")

    if fails:
        print("FAIL")
        for f in fails:
            print(f" - {f}")
        return 1
    print(f"PASS ({len(rows)} cases; hard checks only, review judgment checks in evals.json)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
