#!/usr/bin/env python3
"""检查文档和代码里的叫法是否统一，并可顺便标出常见黑话。

用法：
  python3 check_terms.py --glossary GLOSSARY.md docs/ README.md src/
  python3 check_terms.py --glossary GLOSSARY.md --count docs/ src/
  python3 check_terms.py --jargon docs/
  python3 check_terms.py --glossary GLOSSARY.md --jargon .

术语表格式见 ../references/glossary-template.md。
检查模式下，发现“不要用的叫法”时退出码为 1，方便放进 CI；黑话只是提示，不影响退出码。
--count 只统计每种叫法出现的次数和文件，退出码总是 0，适合还没定标准叫法的时候用。
某一行含有 "check-terms: ignore" 时跳过这一行；
"check-terms: off" 和 "check-terms: on" 之间的内容整段跳过。
只用 Python 标准库。
"""

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
JARGON_FILES = [
    SKILL_DIR / "references" / "zh-jargon.md",
    SKILL_DIR / "references" / "en-jargon.md",
]
# 只读取这两种表头开头的表格；“看语境”的表不检查
JARGON_HEADERS = {"黑话", "instead of"}

PREFERRED_HEADERS = {"标准叫法", "use"}
AVOID_HEADERS = {"不要用的叫法", "不要用", "avoid"}
EXCEPTION_HEADERS = {"例外", "exceptions"}

TEXT_SUFFIXES = {
    ".md", ".mdx", ".txt", ".rst", ".adoc", ".html", ".vue", ".svelte",
    ".py", ".js", ".jsx", ".ts", ".tsx", ".go", ".java", ".kt", ".swift",
    ".rb", ".rs", ".php", ".cs", ".c", ".h", ".cpp", ".hpp", ".scala",
    ".sh", ".yaml", ".yml", ".toml", ".json", ".properties", ".sql",
}
PROSE_SUFFIXES = {".md", ".mdx", ".txt", ".rst", ".adoc"}
SKIP_DIRS = {
    ".git", "node_modules", "dist", "build", "out", ".next", "target",
    "vendor", ".venv", "venv", "__pycache__", "coverage",
}
SKIP_FILES = {"package-lock.json", "pnpm-lock.yaml", "yarn.lock", "Cargo.lock", "poetry.lock"}
IGNORE_LINE = "check-terms: ignore"
IGNORE_OFF = "check-terms: off"
IGNORE_ON = "check-terms: on"

SPLIT_RE = re.compile(r"[、,，;；/]")
PAREN_RE = re.compile(r"[（(][^）)]*[）)]")
SEP_ROW_RE = re.compile(r"^\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?$")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
LATIN_RE = re.compile(r"[A-Za-z]")
CJK_RE = re.compile(r"[一-鿿]")


def split_row(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def iter_tables(text):
    """逐个返回 Markdown 表格的 (表头, 数据行)。"""
    lines = text.splitlines()
    i = 0
    while i < len(lines) - 1:
        if lines[i].strip().startswith("|") and SEP_ROW_RE.match(lines[i + 1].strip()):
            header = split_row(lines[i])
            rows = []
            j = i + 2
            while j < len(lines) and lines[j].strip().startswith("|"):
                rows.append(split_row(lines[j]))
                j += 1
            yield header, rows
            i = j
        else:
            i += 1


def split_terms(cell):
    cell = PAREN_RE.sub("", cell).replace("`", "")
    terms = []
    for t in SPLIT_RE.split(cell):
        t = t.strip().strip("\"'“”‘’「」")
        if t and t not in {"-", "—", "无"}:
            terms.append(t)
    return terms


def build_pattern(term):
    """英文按单词边界、忽略大小写匹配，单个词兼容常见词形变化；中文按字面匹配。"""
    if LATIN_RE.search(term) and not CJK_RE.search(term):
        words = term.split()
        if len(words) == 1:
            w = term
            if w.endswith("e"):
                body = re.escape(w[:-1]) + r"(?:e|es|ed|ing)"
            elif w.endswith("y") and len(w) > 2 and w[-2] not in "aeiou":
                body = re.escape(w[:-1]) + r"(?:y|ies|ied)"
            else:
                body = re.escape(w) + r"(?:s|es|ed|ing)?"
        else:
            body = r"\s+".join(re.escape(w) for w in words)
        return re.compile(r"(?<![A-Za-z])" + body + r"(?![A-Za-z])", re.IGNORECASE)
    return re.compile(re.escape(term))


def find_column(keys, names):
    return next((k for k, h in enumerate(keys) if h in names), None)


def load_glossary(path):
    """返回术语表的每一行：{preferred, aliases, exceptions}，后两项是 [(词, 匹配规则)]。"""
    rows = []
    for header, table in iter_tables(path.read_text(encoding="utf-8")):
        keys = [h.lower() for h in header]
        pi = find_column(keys, PREFERRED_HEADERS)
        ai = find_column(keys, AVOID_HEADERS)
        ei = find_column(keys, EXCEPTION_HEADERS)
        if pi is None or ai is None:
            continue
        for cells in table:
            if len(cells) <= max(pi, ai):
                continue
            preferred = split_terms(cells[pi])
            if not preferred:
                continue
            exceptions = split_terms(cells[ei]) if ei is not None and ei < len(cells) else []
            rows.append({
                "preferred": (preferred[0], build_pattern(preferred[0])),
                "aliases": [(a, build_pattern(a)) for a in split_terms(cells[ai])],
                "exceptions": [(e, build_pattern(e)) for e in exceptions],
            })
    return rows


def load_jargon():
    """返回 [(黑话, 建议, 匹配规则)]。"""
    entries = []
    for path in JARGON_FILES:
        if not path.exists():
            continue
        for header, rows in iter_tables(path.read_text(encoding="utf-8")):
            if not header or header[0].lower() not in JARGON_HEADERS:
                continue
            for row in rows:
                if not row:
                    continue
                suggestion = row[-1] if len(row) > 1 else ""
                for term in split_terms(row[0]):
                    entries.append((term, suggestion, build_pattern(term)))
    return entries


def iter_files(paths, excluded):
    for raw in paths:
        p = Path(raw)
        if p.is_file():
            if p.resolve() not in excluded:
                yield p
        elif p.is_dir():
            for f in sorted(p.rglob("*")):
                if not f.is_file() or f.name in SKIP_FILES:
                    continue
                if f.suffix.lower() not in TEXT_SUFFIXES:
                    continue
                if any(part in SKIP_DIRS for part in f.relative_to(p).parts):
                    continue
                resolved = f.resolve()
                # 跳过本技能自己的文件，里面全是反例
                if resolved in excluded or SKILL_DIR in resolved.parents:
                    continue
                yield f
        else:
            print(f"找不到：{raw}", file=sys.stderr)


def iter_lines(path):
    """返回 (行号, 要检查的文本)。跳过标了忽略的行和段落；Markdown 里跳过代码块和行内代码。"""
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return
    prose = path.suffix.lower() in PROSE_SUFFIXES
    in_fence = False
    ignoring = False
    for n, line in enumerate(text.splitlines(), 1):
        if IGNORE_OFF in line:
            ignoring = True
            continue
        if IGNORE_ON in line:
            ignoring = False
            continue
        if ignoring or IGNORE_LINE in line:
            continue
        if prose:
            if line.lstrip().startswith(("```", "~~~")):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            line = INLINE_CODE_RE.sub("", line)
        yield n, line


def overlaps(span, spans):
    return any(span[0] < e and s < span[1] for s, e in spans)


def build_term_list(rows):
    """把所有标准叫法和不要用的叫法摊平，长的排前面：“团队空间”先占位，就不会再把其中的“空间”算一遍。"""
    terms = []
    for idx, row in enumerate(rows):
        terms.append((idx, row["preferred"][0], False, row["preferred"][1]))
        for alias, pattern in row["aliases"]:
            terms.append((idx, alias, True, pattern))
    terms.sort(key=lambda t: len(t[1]), reverse=True)
    return terms


def find_terms(line, rows, terms):
    """返回这一行里出现的叫法：[(行序号, 词, 是否不要用的叫法, 实际匹配到的文字)]。"""
    exception_spans = {
        idx: [m.span() for _, p in row["exceptions"] for m in p.finditer(line)]
        for idx, row in enumerate(rows)
        if row["exceptions"]
    }
    taken = []
    hits = []
    for idx, term, is_alias, pattern in terms:
        for m in pattern.finditer(line):
            span = m.span()
            if overlaps(span, taken):
                continue
            if is_alias and overlaps(span, exception_spans.get(idx, [])):
                continue
            taken.append(span)
            hits.append((idx, term, is_alias, m.group(0)))
    return hits


def print_counts(rows, counts, files):
    for idx, row in enumerate(rows):
        preferred = row["preferred"][0]
        names = [(preferred, "（标准叫法）")] + [(a, "") for a, _ in row["aliases"]]
        print(f"■ {preferred}")
        for name, mark in names:
            n = counts[(idx, name)]
            where = sorted(files[(idx, name)])
            shown = "、".join(where[:3]) + (f" 等 {len(where)} 个文件" if len(where) > 3 else "")
            detail = f"，在 {shown}" if where else ""
            print(f"    {name}{mark}：{n} 次{detail}")


def main():
    parser = argparse.ArgumentParser(description="检查叫法是否统一，并标出常见黑话。")
    parser.add_argument("paths", nargs="*", default=["."], help="要检查的文件或目录，默认当前目录")
    parser.add_argument("--glossary", help="术语表文件，例如 GLOSSARY.md")
    parser.add_argument("--count", action="store_true", help="只统计每种叫法出现的次数和文件，不报错")
    parser.add_argument("--jargon", action="store_true", help="同时标出常见黑话（只是提示）")
    args = parser.parse_args()

    if not args.glossary and not args.jargon:
        parser.error("至少要给 --glossary 或 --jargon 其中一个")
    if args.count and not args.glossary:
        parser.error("--count 需要配合 --glossary 使用")

    rows = []
    excluded = {p.resolve() for p in JARGON_FILES}
    if args.glossary:
        gpath = Path(args.glossary)
        if not gpath.is_file():
            parser.error(f"找不到术语表：{gpath}")
        rows = load_glossary(gpath)
        excluded.add(gpath.resolve())
        if not rows:
            print(f"提示：{gpath} 里没找到表头含“标准叫法”和“不要用的叫法”的表格。", file=sys.stderr)
    terms = build_term_list(rows)
    jargon = load_jargon() if args.jargon else []

    term_hits = 0
    jargon_hits = 0
    counts = defaultdict(int)
    files = defaultdict(set)
    for path in iter_files(args.paths, excluded):
        for n, line in iter_lines(path):
            seen = set()
            for idx, term, is_alias, matched in find_terms(line, rows, terms):
                counts[(idx, term)] += 1
                files[(idx, term)].add(str(path))
                if args.count or not is_alias or term in seen:
                    continue
                seen.add(term)
                print(f"{path}:{n}: 用了「{matched}」，统一用「{rows[idx]['preferred'][0]}」")
                term_hits += 1
            for term, suggestion, pattern in jargon:
                m = pattern.search(line)
                if m:
                    hint = f"，可以试试：{suggestion}" if suggestion else ""
                    print(f"{path}:{n}: 「{m.group(0)}」可能是黑话{hint}")
                    jargon_hits += 1

    if args.count:
        print_counts(rows, counts, files)
        return 0

    summary = []
    if args.glossary:
        summary.append(f"叫法不统一 {term_hits} 处")
    if args.jargon:
        summary.append(f"可能的黑话 {jargon_hits} 处（看上下文判断）")
    print("；".join(summary))
    return 1 if term_hits else 0


if __name__ == "__main__":
    sys.exit(main())
