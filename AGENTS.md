# 给在这个仓库工作的 AI

这个仓库做的是一套写作规则，所以我们自己写的文字也按它来。

- 写任何给人看的文字之前，先读 [`talk-like-a-human/SKILL.md`](talk-like-a-human/SKILL.md) 并照着写，包括 README、规则文件、注释、commit message、PR 描述和给用户的回复。
- 动笔前查 [`GLOSSARY.md`](GLOSSARY.md)，用里面的标准叫法。新概念先加进术语表。
- 改了规则或文档，提交前在仓库根目录运行 `python3 .github/scripts/check_repo.py`。
- 新增规则时，尽量按 [`CONTRIBUTING.md`](CONTRIBUTING.md) 在 `talk-like-a-human/evals/` 里加测试用例。
- `talk-like-a-human/evals/` 里的 prompt 和 `references/` 里的 ❌ 例子故意写得不好，不要“改好”它们。
- commit 和 PR 不加 AI 署名，比如 Co-Authored-By Claude。
