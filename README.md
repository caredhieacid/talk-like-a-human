# 像人一样说话（talk-like-a-human）

一个让 AI 说人话的 skill。装上以后，AI 写给人看的文字会更平实、准确，读一遍就懂。适用于 Claude Code 等支持 `SKILL.md` 格式的工具。

它主要管这几件事：

- **黑话和空话**：不写“赋能”“闭环”“抓手”“leverage”“seamless”，直接写具体做了什么。
- **自造词**：不把一句话压成“证据面”“决策压缩”这种只有 AI 自己懂的词。
- **翻译腔**：不写“对……进行了……”、一长串定语、名词堆在一起的句子。
- **为了省字硬删词**：要求简洁时也不删主语和“因为”“所以”，不写成电报。
- **叫法不统一**：大项目里同一个东西只用一个名字，并配了一个检查脚本。
- **不乱编**：不补原文没有的数字、细节和例子，不把“可能”写成“会”。

## 安装

```bash
git clone https://github.com/caredhieacid/talk-like-a-human.git
mkdir -p ~/.claude/skills
ln -s "$PWD/talk-like-a-human/talk-like-a-human" ~/.claude/skills/talk-like-a-human
```

AI 只在觉得需要时才会用 skill。如果想让每条回复都按它来写，在 `~/.claude/CLAUDE.md` 里加一句：

```markdown
写给人看的文字，都按 talk-like-a-human skill 来写。
```

## 仓库里有什么

| 路径 | 内容 |
| --- | --- |
| `talk-like-a-human/SKILL.md` | 主文件：规则、例子和发出前的自查清单 |
| `talk-like-a-human/references/` | 中英文黑话对照表、术语表模板 |
| `talk-like-a-human/scripts/check_terms.py` | 检查项目里叫法是否统一的脚本 |
| `talk-like-a-human/evals/` | 12 个测试用例，其中 4 个专门测“不该改的有没有乱改” |
| `research/` | 两份调研报告：AI 为什么会这样写，以及同类 skill 是怎么做的 |

## 检查叫法是否统一

先按 `talk-like-a-human/references/glossary-template.md` 在项目里写一份术语表，然后运行：

```bash
# 统计每种叫法用了几次、在哪些文件
python3 talk-like-a-human/scripts/check_terms.py --glossary GLOSSARY.md --count docs/ src/

# 找出用了“不要用的叫法”的地方；发现了退出码是 1，可以放进 CI
python3 talk-like-a-human/scripts/check_terms.py --glossary GLOSSARY.md docs/ src/
```

脚本只用 Python 标准库，不用装依赖。

## 测试结果

12 个测试用例，每个分别在用和不用 skill 的情况下各跑一次，用的模型是 Claude Opus 5.5。最近一轮的结果：

| | 用 skill | 不用 skill |
| --- | --- | --- |
| 检查项通过 | 52 / 52 | 43 / 52 |
| 平均用时 | 72 秒 | 37 秒 |
| 平均 token | 约 6.7 万 | 约 5.6 万 |

不用 skill 时，三轮测试里反复出现的问题有：把“4.1 秒降到 1.3 秒”写成“快了约三倍”，把猜测当成事实写进周报，用“原因：…… 需要你确认：……”这种标签加短语代替句子，以及自己估一套原文没有的成本数字。

这份结果仅供参考：每个用例只跑了一次，打分也是由写这个 skill 的 AI 完成的。

## English

A skill that makes AI write plain, clear Chinese and English: no buzzwords, no made-up terms, no translationese, no telegraphic shorthand, one name per thing across a project, and no invented numbers or examples. The rules live in `talk-like-a-human/SKILL.md`; `scripts/check_terms.py` checks a project's docs and code against a glossary.

## 许可

[MIT](LICENSE)
