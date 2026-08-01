"""The command-line interface of the linter."""

from __future__ import annotations

import argparse
import json
import sys

from .engine import Linter, Report
from .rules import load_rules


def _print_text(reports: list[Report], style: str) -> None:
    for report in reports:
        for violation in report.violations:
            print(f"{violation.file}:{violation.line}: [{violation.rule}] {violation.message}")
            print(f"    {violation.sentence}")
    total_sentences = sum(r.sentence_count for r in reports)
    total_violations = sum(len(r.violations) for r in reports)
    rate = 100.0 * total_violations / total_sentences if total_sentences else 0.0
    print(
        f"style {style}: {total_violations} violation(s) in {total_sentences} sentence(s), "
        f"rate {rate:.1f} per 100 sentences"
    )


def _print_json(reports: list[Report], style: str) -> None:
    total_sentences = sum(r.sentence_count for r in reports)
    total_violations = sum(len(r.violations) for r in reports)
    rate = 100.0 * total_violations / total_sentences if total_sentences else 0.0
    print(
        json.dumps(
            {
                "style": style,
                "files": [r.as_dict() for r in reports],
                "total": {
                    "sentences": total_sentences,
                    "violations": total_violations,
                    "rate": round(rate, 2),
                },
            },
            indent=2,
        )
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="style-lint",
        description="Check Markdown files against the writing rules of a style.",
    )
    parser.add_argument("files", nargs="+", help="Markdown files to check")
    parser.add_argument("--rules", required=True, help="path to the rule file")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args(argv)

    rules = load_rules(args.rules)
    linter = Linter(rules)
    reports = [linter.lint_file(f) for f in args.files]
    if args.format == "json":
        _print_json(reports, rules.style)
    else:
        _print_text(reports, rules.style)
    return 1 if any(r.violations for r in reports) else 0


if __name__ == "__main__":
    sys.exit(main())
