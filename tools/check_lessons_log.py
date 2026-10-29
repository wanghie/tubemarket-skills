#!/usr/bin/env python3
"""Check the LESSONS LOG block in every SKILL.md of this repo.

Run:   python3 tools/check_lessons_log.py
Exits 1 on ERROR. WARNINGs do not fail the run, but report them to the user.

The master copy of the block lives at:
    skills/skill-forge/references/lessons-log-block.md
Set LESSONS_BLOCK=/path/to/lessons-log-block.md to check another repo against it.
"""
import os, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEADING = "## LESSONS LOG"
MAX_ROWS = 10
MAX_LINES = 300
HEADER = "| Date | Source | WRONG | RIGHT |"
SEP = "|---|---|---|---|"
VALID_SOURCES = {"user", "review", "measured"}
ROW = re.compile(r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|([^|]*)\|")
PLACEHOLDER = "<skill-name>"


def master() -> list[str] | None:
    p = os.environ.get("LESSONS_BLOCK")
    cands = [Path(p).expanduser()] if p else []
    cands.append(ROOT / "skills/skill-forge/references/lessons-log-block.md")
    for c in cands:
        if c.is_file():
            return c.read_text(encoding="utf-8").rstrip("\n").split("\n")
    return None


def main() -> int:
    ref = master()
    errors, warnings, ok = [], [], 0

    if ref:
        # The master block must be self-consistent: its numbers must match its real length.
        frame = len(ref)
        body = MAX_LINES - frame - 1 - MAX_ROWS
        txt = "\n".join(ref)
        if f"takes {frame} frame lines" not in txt or f"under {body} lines" not in txt:
            errors.append(f"lessons-log-block.md: block is {frame} lines but its text says otherwise "
                          f"(must say 'takes {frame} frame lines' and 'under {body} lines')")
    else:
        warnings.append("lessons-log-block.md not found — skipping comparison with the master block")

    for f in sorted(ROOT.glob("skills/*/SKILL.md")):
        name = f.parent.name
        lines = f.read_text(encoding="utf-8").rstrip("\n").split("\n")
        n = len(lines)
        if n >= MAX_LINES:
            warnings.append(f"{name}: {n} lines, over the {MAX_LINES} cap — tell the user, "
                            f"move reference material to references/, never cut the log")
        if HEADING not in lines:
            errors.append(f"{name}: missing '{HEADING}' section")
            continue
        block = lines[lines.index(HEADING):]
        if HEADER not in block or SEP not in block:
            errors.append(f"{name}: log table is not the 4 columns '{HEADER}'")
            continue
        j = block.index(SEP)
        if ref:
            frame_real = [l.replace(name, PLACEHOLDER) for l in block[: j + 1]]
            if frame_real != ref:
                errors.append(f"{name}: log block differs from lessons-log-block.md "
                              f"(paste it again, do not retype)")
        rows = [l for l in block[j + 1:] if l.strip().startswith("|")]
        if len(rows) > MAX_ROWS:
            errors.append(f"{name}: log has {len(rows)} rows, over the cap of {MAX_ROWS}")
        for r in rows:
            m = ROW.match(r)
            if not m:
                errors.append(f"{name}: bad row format, expected '| YYYY-MM-DD | Source | WRONG | RIGHT |'"
                              f" → {r[:60]}")
                continue
            src = m.group(2).strip()
            if src not in VALID_SOURCES:
                errors.append(f"{name}: invalid source '{src}' (allowed: {' · '.join(sorted(VALID_SOURCES))})")
        ok += 1

    for w in warnings:
        print(f"WARNING  {w}")
    for e in errors:
        print(f"ERROR    {e}")
    print(f"\n{ok} skills with a valid LESSONS LOG · {len(errors)} errors · {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
