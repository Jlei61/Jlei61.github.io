#!/usr/bin/env python3
"""Fail the build when a published content page lacks an en/zh partner."""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
LANGUAGES = {"en", "zh"}
FRONT_MATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def front_matter_value(text: str, key: str) -> str | None:
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return None
    value_match = re.search(rf"(?m)^{re.escape(key)}:\s*[\"']?([^\n\"']+)", match.group(1))
    return value_match.group(1).strip() if value_match else None


def main() -> int:
    errors: list[str] = []
    groups: dict[tuple[Path, str], dict[str, Path]] = defaultdict(dict)

    for path in sorted(CONTENT.rglob("*.md")):
        relative = path.relative_to(CONTENT)
        stem_parts = path.stem.rsplit(".", 1)
        if len(stem_parts) != 2 or stem_parts[1] not in LANGUAGES:
            errors.append(f"{relative}: filename must end in .en.md or .zh.md")
            continue
        base, language = stem_parts
        groups[(relative.parent, base)][language] = path

    for (parent, base), variants in sorted(groups.items(), key=lambda item: str(item[0])):
        missing = sorted(LANGUAGES - variants.keys())
        if missing:
            errors.append(f"{parent / base}: missing language variant(s): {', '.join(missing)}")
            continue

        keys = {
            language: front_matter_value(path.read_text(encoding="utf-8"), "translationKey")
            for language, path in variants.items()
        }
        if any(value is None for value in keys.values()):
            errors.append(f"{parent / base}: every variant needs translationKey")
        elif len(set(keys.values())) != 1:
            errors.append(f"{parent / base}: translationKey values do not match: {keys}")

    if errors:
        print("i18n content check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"i18n content check passed: {len(groups)} bilingual page pair(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
