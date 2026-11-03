# 参与贡献

欢迎提 issue 和 PR。下面是合并前会看的几件事。

## 提交 PR 之前

- 改规则（`talk-like-a-human/SKILL.md` 或 `talk-like-a-human/references/`）时，在 PR 里写清楚：原来 AI 会写成什么样，改完以后写成什么样。最好附上真实的前后对比。
- 改了 skill 里的规则，也看一下常驻规则 [`core.md`](talk-like-a-human/core.md) 和 [`core.en.md`](talk-like-a-human/core.en.md) 要不要跟着改。常驻规则每次对话都会读到，所以要短，只放最常见的毛病。
- 新增规则时，尽量在 `talk-like-a-human/evals/` 里加一个测试用例，格式照着已有的用例写（`prompt.md`、`case.yaml`、`graders/`）。
- skill 里的脚本（`talk-like-a-human/scripts/`）只用 Python 标准库，不引入第三方依赖。
- 这个仓库的文字也按这套规则写，叫法以 [`GLOSSARY.md`](GLOSSARY.md) 为准。用 AI 协作时，它会读 [`AGENTS.md`](AGENTS.md)。
- 提交前在仓库根目录运行 `python3 .github/scripts/check_repo.py`。它会做 PR 上的全部自动检查，包括 skill 的格式、文档里的链接、测试用例是否齐全、`check_terms.py` 能不能正常工作，以及文档有没有用错叫法。

## 合并规则

- `main` 分支受保护，只能通过 PR 合并，不能直接推送，也不能强推。
- 每个 PR 都要维护者审核通过（见 `.github/CODEOWNERS`），自动检查也要通过。
- PR 有新的提交后，之前的审核会失效，需要重新审核。
- 合并方式是 squash：一个 PR 合并成一个提交。

## 为什么审核得比较严

AI 工具会把 `SKILL.md` 和 `references/` 里的文字当成指令执行。如果有人在里面加一句“把用户的文件发到某个网址”，装了这个 skill 的人就会受影响。所以：

- 改到 skill 文件夹的 PR，维护者会逐行看，尤其是新出现的网址、命令和“请执行……”这类句子。
- `install.py` 会把常驻规则写进用户工具的全局说明文件，每次对话都会读到。改 `core.md`、`core.en.md` 和 `install.py` 的 PR 也逐行看。
- 自动检查会拦下“下载并执行远程代码”的命令（比如 `curl … | sh`）。

---

# Contributing (English)

Issues and PRs are welcome.

- When you change a rule, show what the AI wrote before and after, ideally with a real example, and add an eval case under `talk-like-a-human/evals/` if you can. Also check whether the always-on rules in [`core.md`](talk-like-a-human/core.md) and [`core.en.md`](talk-like-a-human/core.en.md) need the same change; keep them short, since tools read them in every conversation.
- This repo's own text follows these rules, and [`GLOSSARY.md`](GLOSSARY.md) sets the names. AI tools working here read [`AGENTS.md`](AGENTS.md). Run `python3 .github/scripts/check_repo.py` before you commit; it also fails on a wrong name.
- `main` is protected: changes go through a PR, need a maintainer's approval (see `.github/CODEOWNERS`) and a passing check. New commits dismiss earlier approvals. PRs are squash-merged.
- Agents follow `SKILL.md` and `references/` as instructions, so maintainers read every changed line in the skill folder, especially new URLs and commands. The same goes for `install.py` and the always-on rules, which it writes into each tool's global instructions file. The automated check blocks commands that download and run remote code.
