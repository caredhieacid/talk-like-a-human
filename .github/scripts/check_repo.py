#!/usr/bin/env python3
"""Checks run on every pull request. Standard library only.

1. SKILL.md has valid frontmatter (Agent Skills format: name and description).
2. Relative links in SKILL.md, the references and both READMEs point to files that exist.
3. Every eval case has prompt.md, case.yaml and at least one grader.
4. check_terms.py still finds a wrong name and passes a clean document.
5. Skill files contain no commands that download or run remote code. Agents read these
   files as instructions, so a line like `curl … | sh` there would be a real risk.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "talk-like-a-human"
errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def check_frontmatter() -> None:
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        fail("SKILL.md: frontmatter missing (must start and end with ---)")
        return
    fields = dict(re.findall(r"^(\w[\w-]*):\s*(.*)$", m.group(1), re.M))
    name = fields.get("name", "")
    desc = fields.get("description", "")
    if name != SKILL.name:
        fail(f"SKILL.md: name is '{name}', expected the folder name '{SKILL.name}'")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) or len(name) > 64:
        fail("SKILL.md: name must be lowercase letters, digits and hyphens, at most 64 characters")
    if not desc:
        fail("SKILL.md: description is empty")
    elif len(desc) > 1024:
        fail(f"SKILL.md: description is {len(desc)} characters; the Agent Skills limit is 1024")


def check_links() -> None:
    files = [SKILL / "SKILL.md", *sorted((SKILL / "references").glob("*.md")), ROOT / "README.md", ROOT / "README.en.md", ROOT / "CONTRIBUTING.md"]
    for f in files:
        if not f.exists():
            continue
        text = re.sub(r"```.*?```", "", f.read_text(encoding="utf-8"), flags=re.S)
        targets = re.findall(r"\]\(([^)\s]+)\)", text) + re.findall(r'(?:src|href)="([^"]+)"', text)
        for t in targets:
            if re.match(r"^(https?:|mailto:|#)", t):
                continue
            path = (f.parent / t.split("#")[0]).resolve()
            if not path.exists():
                fail(f"{f.relative_to(ROOT)}: broken link -> {t}")


def check_evals() -> None:
    cases = [p for p in sorted((SKILL / "evals").iterdir()) if p.is_dir() and p.name != "results"]
    if not cases:
        fail("evals/: no test cases")
    for c in cases:
        for need in ("prompt.md", "case.yaml"):
            if not (c / need).exists():
                fail(f"evals/{c.name}: missing {need}")
        if not list((c / "graders").glob("*.md")):
            fail(f"evals/{c.name}: no graders")


def check_term_checker() -> None:
    script = SKILL / "scripts" / "check_terms.py"
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        (t / "GLOSSARY.md").write_text(
            "| 标准叫法 | 不要用的叫法 | 例外 |\n| --- | --- | --- |\n| 工作区 | 空间、workspace | 存储空间 |\n", encoding="utf-8"
        )
        docs = t / "docs"
        docs.mkdir()
        (docs / "bad.md").write_text("新建一个空间，然后邀请成员。\n", encoding="utf-8")
        (docs / "good.md").write_text("新建一个工作区，存储空间不够时可以扩容。\n", encoding="utf-8")
        run = lambda target: subprocess.run(
            [sys.executable, str(script), "--glossary", str(t / "GLOSSARY.md"), str(target)], capture_output=True, text=True
        )
        bad = run(docs / "bad.md")
        if bad.returncode != 1 or "空间" not in bad.stdout:
            fail(f"check_terms.py: expected exit 1 and a hit on 空间, got exit {bad.returncode}: {bad.stdout.strip()}")
        good = run(docs / "good.md")
        if good.returncode != 0:
            fail(f"check_terms.py: clean document should pass, got exit {good.returncode}: {good.stdout.strip()}")


RISKY = re.compile(r"(curl|wget)[^\n|]*\|\s*(ba|z)?sh|base64\s+(-d|--decode)|\beval\s*\(|Invoke-WebRequest|iex\s*\(", re.I)


def check_risky_commands() -> None:
    for f in sorted(SKILL.rglob("*")):
        if f.is_file() and f.suffix in {".md", ".py", ".sh", ".yaml", ".yml", ".txt"}:
            for n, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                if RISKY.search(line):
                    fail(f"{f.relative_to(ROOT)}:{n}: command that downloads or runs remote code: {line.strip()[:120]}")


for step in (check_frontmatter, check_links, check_evals, check_term_checker, check_risky_commands):
    step()

if errors:
    print("Found problems:")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("All checks passed.")
