#!/usr/bin/env python3
"""Install talk-like-a-human for the AI tools on this machine.

Two things are installed:
1. The skill: a link to talk-like-a-human/ in each tool's skills folder.
2. The always-on rules (talk-like-a-human/core.md, or core.en.md with --lang en):
   written into each tool's global instructions file, which the tool reads in
   every session, so even a one-line chat reply follows them.

The rules sit between two marker lines, so running this again updates them in
place and --uninstall removes exactly what was added. Nothing outside the
markers is changed.

    python3 install.py              # install, or update after git pull
    python3 install.py --dry-run    # only print what would change
    python3 install.py --uninstall
"""
from __future__ import annotations

import argparse
import locale
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKILL = ROOT / "talk-like-a-human"
HOME = Path.home()
START = "<!-- talk-like-a-human:start -->"
END = "<!-- talk-like-a-human:end -->"

# Skills folders. ~/.agents/skills is shared by Codex, Cursor, GitHub Copilot,
# Gemini CLI and others, so it is always used; the rest only if the tool is installed.
SKILL_DIRS = [
    (HOME / ".agents", HOME / ".agents" / "skills", True),
    (HOME / ".claude", HOME / ".claude" / "skills", False),
    (HOME / ".cline", HOME / ".cline" / "skills", False),
    (HOME / ".kiro", HOME / ".kiro" / "skills", False),
]

# Global instructions files, used only if the tool's folder exists.
RULE_FILES = [
    ("Claude Code", HOME / ".claude", HOME / ".claude" / "CLAUDE.md"),
    ("Codex", HOME / ".codex", HOME / ".codex" / "AGENTS.md"),
    ("Gemini CLI", HOME / ".gemini", HOME / ".gemini" / "GEMINI.md"),
]


def default_lang() -> str:
    lang = os.environ.get("LANG") or (locale.getlocale()[0] or "")
    return "zh" if lang.lower().startswith("zh") else "en"


def strip_block(text: str) -> str:
    """Remove our marked block and the blank line written before it."""
    start = text.find(START)
    if start < 0:
        return text
    end = text.find(END, start)
    if end < 0:
        sys.exit(f"Found {START} without {END}. Fix the file by hand, then run again.")
    end += len(END)
    before = text[:start].rstrip("\n")
    after = text[end:].lstrip("\n")
    if before and after:
        return before + "\n\n" + after
    return (before + "\n") if before else after


def link_skill(skills_dir: Path, dry: bool) -> str:
    target = skills_dir / SKILL.name
    if target.is_symlink() or target.exists():
        if target.resolve() == SKILL:
            return f"already linked: {target}"
        return f"skipped, something else is already there: {target}"
    if not dry:
        skills_dir.mkdir(parents=True, exist_ok=True)
        try:
            target.symlink_to(SKILL, target_is_directory=True)
        except OSError:
            # Windows without Developer Mode can't create symlinks; copy instead.
            shutil.copytree(SKILL, target, ignore=shutil.ignore_patterns("evals"))
            return f"copied (run again after git pull to update): {target}"
    return f"{'would link' if dry else 'linked'}: {target} -> {SKILL}"


def unlink_skill(skills_dir: Path, dry: bool) -> str | None:
    target = skills_dir / SKILL.name
    if target.is_symlink() and target.resolve() == SKILL:
        if not dry:
            target.unlink()
        return f"{'would remove link' if dry else 'removed link'}: {target}"
    return None


def write_rules(path: Path, block: str | None, dry: bool) -> str | None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    new = strip_block(old)
    if block:
        new = (new.rstrip("\n") + "\n\n" if new.strip() else "") + f"{START}\n{block.strip()}\n{END}\n"
    if new == old:
        return None
    if not dry:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(new, encoding="utf-8")
    return path


def main() -> None:
    ap = argparse.ArgumentParser(description="Install talk-like-a-human for the AI tools on this machine.")
    ap.add_argument("--lang", choices=["zh", "en"], default=default_lang(), help="language of the always-on rules (default: from your system locale)")
    ap.add_argument("--skill-only", action="store_true", help="link the skill but don't write the always-on rules")
    ap.add_argument("--uninstall", action="store_true", help="remove the links and the always-on rules this script added")
    ap.add_argument("--dry-run", action="store_true", help="print what would change without changing anything")
    args = ap.parse_args()
    dry = args.dry_run
    if dry:
        print("Dry run: nothing will be changed.\n")

    for tool_dir, skills_dir, always in SKILL_DIRS:
        if always or tool_dir.exists():
            msg = unlink_skill(skills_dir, dry) if args.uninstall else link_skill(skills_dir, dry)
            if msg:
                print(msg)

    core = SKILL / ("core.en.md" if args.lang == "en" else "core.md")
    block = None if args.uninstall else core.read_text(encoding="utf-8")
    seen = set()
    for tool, tool_dir, path in RULE_FILES:
        if args.skill_only and not args.uninstall:
            break
        if not tool_dir.exists():
            continue
        real = path.resolve()
        if real in seen:
            print(f"{tool}: {path} is the same file as above")
            continue
        seen.add(real)
        changed = write_rules(real, block, dry)
        if args.uninstall:
            verb = "would remove" if dry else "removed"
            print(f"{tool}: {verb} the always-on rules from {real}" if changed else f"{tool}: nothing to remove in {real}")
        else:
            verb = "would write" if dry else "wrote"
            print(f"{tool}: {verb} the always-on rules to {real}" if changed else f"{tool}: rules already up to date in {real}")

    if not args.uninstall:
        print(
            f"\nOther tools: paste {core.relative_to(ROOT)} into their custom instructions,"
            " for example Cursor's User Rules, or the personalization settings in ChatGPT, Claude or Gemini on the web."
            "\nStart a new session so the tools pick up the changes."
        )


if __name__ == "__main__":
    main()
