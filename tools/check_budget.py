#!/usr/bin/env python3
"""Check the SKILL.md budget: lines, tokens (words x 1.35) and description length."""
import re
import sys
from pathlib import Path

MAX_LINES, MAX_TOKENS = 500, 5000
TARGET_LINES, MAX_DESCRIPTION = 150, 300


def tokens(text):
    return int(len(text.split()) * 1.35)


def description(text):
    front = re.search(r"^---\n(.*?)\n---", text, re.S)
    if not front:
        return ""
    found = re.search(r"^description:\s*(.+)$", front.group(1), re.M)
    return found.group(1).strip().strip('"') if found else ""


def check(skill_dir):
    skill_dir = Path(skill_dir)
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    lines, used, desc = len(text.splitlines()), tokens(text), description(text)
    errors, warnings = [], []
    if lines > MAX_LINES:
        errors.append(f"SKILL.md has {lines} lines (maximum {MAX_LINES})")
    if used > MAX_TOKENS:
        errors.append(f"SKILL.md has ~{used} tokens (maximum {MAX_TOKENS})")
    if not desc:
        errors.append("description is missing")
    elif len(desc) > MAX_DESCRIPTION:
        errors.append(f"description has {len(desc)} characters (maximum {MAX_DESCRIPTION})")
    if TARGET_LINES < lines <= MAX_LINES:
        warnings.append(f"SKILL.md has {lines} lines (target {TARGET_LINES})")
    costs = {"listing": tokens(desc), "invocation": used}
    for ref in sorted((skill_dir / "references").glob("*.md")):
        costs[f"references/{ref.name}"] = tokens(ref.read_text(encoding="utf-8"))
    return errors, warnings, costs


def markdown_table(costs):
    labels = {"listing": "Listing (description, every turn)", "invocation": "Invocation (SKILL.md)"}
    rows = ["| What | Approx. tokens |", "|---|---|"]
    for key, value in costs.items():
        label = labels.get(key, f"{key} (only when needed)")
        rows.append(f"| {label} | {value} |")
    return "\n".join(rows)


def main(argv):
    if not argv:
        print("usage: check_budget.py <skill_dir> [--markdown]", file=sys.stderr)
        return 2
    errors, warnings, costs = check(argv[0])
    print(markdown_table(costs) if "--markdown" in argv else costs)
    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)
    for error in errors:
        print(f"error: {error}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
