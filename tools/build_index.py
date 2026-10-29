#!/usr/bin/env python3
"""Regenerate the skill index table in README.md from each SKILL.md frontmatter.

Run:  python3 tools/build_index.py
Do not edit the index by hand — edit the SKILL.md description and rerun this.
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
README = ROOT / "README.md"
START, END = "<!-- INDEX:START -->", "<!-- INDEX:END -->"

GROUPS = {
    "Video": ["local-whisper-transcriber", "silence-cutter", "word-captions", "punch-zoom",
              "auto-reframe", "video-shorts-pipeline", "broll-prompt-director"],
    "Research": ["market-research-swarm", "clean-room-teardown", "creator-product-teardown",
                 "creator-product-rnd"],
    "App / Design": ["app-ui-designer", "app-landing-page", "app-ux-teardown",
                     "appstore-screenshot-builder"],
    "Dev / Agents": ["agent-secrets-guard", "skill-forge"],
}


def frontmatter(p: Path) -> dict:
    txt = p.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", txt, re.S)
    if not m:
        return {}
    out, key = {}, None
    for line in m.group(1).split("\n"):
        km = re.match(r"^([a-zA-Z_]+):\s*(.*)$", line)
        if km:
            key = km.group(1)
            out[key] = km.group(2).strip().strip('"').strip("'")
        elif key:
            out[key] += " " + line.strip()
    return out


def group_of(name: str) -> str:
    for label, names in GROUPS.items():
        if name in names:
            return label
    return "Other"


def split_desc(desc: str):
    """Split a description into (what it does, trigger phrases)."""
    raw = re.findall(r'["“‘\']([^"”’\']+)["”’\']', desc)
    triggers, seen = [], set()
    for t in raw:
        t = t.strip().rstrip("\\").strip()
        if t and t not in seen:
            seen.add(t)
            triggers.append(t)
    body = re.split(r'(?:Triggers on|Use when the user says|Kích hoạt|Dùng khi user nói|Dùng khi nói)', desc)[0]
    body = body.strip().rstrip(" .")
    if len(body) > 180:
        body = body[:177].rsplit(" ", 1)[0] + "…"
    return body, ", ".join(f"`{t}`" for t in triggers[:6])


def main() -> int:
    rows = []
    for d in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        sk = d / "SKILL.md"
        if not sk.exists():
            print(f"SKIP (no SKILL.md): {d.name}", file=sys.stderr)
            continue
        fm = frontmatter(sk)
        name = fm.get("name", d.name)
        if name != d.name:
            print(f"NAME MISMATCH: folder {d.name} != name: {name}", file=sys.stderr)
            return 1
        body, triggers = split_desc(fm.get("description", ""))
        rows.append((list(GROUPS).index(group_of(name)) if group_of(name) in GROUPS else 99,
                     group_of(name), name, body, triggers))

    rows.sort()
    lines, current = [], None
    for _, grp, name, body, triggers in rows:
        if grp != current:
            current = grp
            lines += ["", f"### {grp}", "", "| Skill | What it does | Say |", "|---|---|---|"]
        lines.append(f"| [`{name}`](./skills/{name}) | {body} | {triggers} |")
    lines.append("")
    block = "\n".join(lines)

    txt = README.read_text(encoding="utf-8")
    new = re.sub(f"{re.escape(START)}.*?{re.escape(END)}",
                 f"{START}\n{block}\n{END}", txt, flags=re.S)
    README.write_text(new, encoding="utf-8")
    print(f"Index updated: {len(rows)} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
