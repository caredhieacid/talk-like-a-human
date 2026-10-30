# 同类 skill 和工具是怎么做的

调研时间：2026-10-24。由调研助手上网查找整理，链接没有逐个核对过。标【原文】的是调研助手打开读过的，标【转述】的是只看到别人的说法。星数是调研当天的数字。

## 一、AI 写作类 skill

**blader/humanizer**（约 6 万星）https://github.com/blader/humanizer 【原文】
- 一个 SKILL.md，26 条规则按强弱排序：前 5 条看到一次就改；标了“weak alone”的，要和别的问题一起出现才改。每条有改前改后的例子，也写了什么时候不改。流程是先写初稿，再问“哪里还像 AI”，然后定稿。不许加原文没有的事实和数字。
- 只管英文；没有作者样本时一律不许用破折号，规定太死。

**op7418/Humanizer-zh**（约 2 万星）https://github.com/op7418/Humanizer-zh 【原文】
- humanizer 的中文版，31 条，每条分“改写前、改写后、保留”三段，补了“的”字叠用、“进行+动词”等中文问题。
- 第一优先是保住信息和确定程度：不把“可能”改成“确定”，不把“计划”改成“已完成”。有 18 条测试和 5 个人工核对的问题。

**MrGeDiao/shuorenhua**（约 2251 星，中文名也叫“说人话”）https://github.com/MrGeDiao/shuorenhua 【原文】
- 中文改稿 skill。2.5 版把词表从运行文件里撤掉，改成默认少改。发版前跑 123 条测试，其中 58 条是不该改的正常文字。
- CHANGELOG 里的教训：原来“换同义词”的做法本身加重了 AI 味（重要→关键→核心轮着换）；连接词密度阈值实测会误伤正常文字，所以不设阈值。
- 作者承认长文里的黑话清理得不够。

**lieflat-less-ai-tone**（约 3960 星）https://github.com/larashero3-dotcom/lieflat-less-ai-tone 【原文】
- 拿 300 篇 AI 文章和 329 篇人写的文章对比，每条规则给出 AI 和人的使用倍数。
- 结果：人比 AI 更常重复同一个名词；AI 用口语连接词只有人的 0.26 倍；“进行……”、被动句、名词化，人用得不比 AI 少。最后只留下 5 种翻译腔，包括“当……时”“这意味着”。
- 提醒：改规则前先看 20 条实际命中。只改清单里有的问题，范围窄。

**其他**【原文】
- stop-slop https://github.com/hardikpandya/stop-slop ：删掉所有副词，不用被动句和破折号，最后打 50 分制的分。规定太绝对。
- avoid-ai-writing https://github.com/conorbronsdon/avoid-ai-writing ：112 个词分三级，按出现密度决定是否提示。说明了 AI 会换同义词绕开词表。
- speak-human-tw https://github.com/Raymondhou0917/speak-human-tw ：动笔前先圈出数字、专名、原话这些不能动的内容。
- obra/the-elements-of-style https://github.com/obra/the-elements-of-style ：SKILL.md 只列规则，原书全文另外放；上下文不够时交给子代理去改。
- anthropics/skills 的 doc-coauthoring https://github.com/anthropics/skills/tree/main/skills/doc-coauthoring ：最后一步让一个不带上下文的新 Claude 回答读者会问的问题，看哪里答错。

## 一（补）、防御性写法类 skill

补充调研：2026-10-30。GitHub 上叫 anti-defensive-writing 或类似名字的仓库至少有 20 个，几乎都是 2026 年 6 到 10 月出现的，大多只管学术论文。

**Kiterlin/anti-defensive-writing**（约 1.5k 星）https://github.com/Kiterlin/anti-defensive-writing 【原文】
- 把防御性写作定义为：作者不讲观点，反复解释“没说什么、没证明什么”，是在跟想象中的批评者谈判。
- 先给每句定性（多余免责、必要范围、方法局限、概念区分、证据限定、重复澄清），删掉多余的，把“不研究什么”改成“研究了什么”。
- 保留影响结论、证据、适用范围和安全、法律后果的限定，只写一次。没有行为测试。

**lennney/stop-that-shit 里的 stss**（仓库约 3.4k 星）https://github.com/lennney/stop-that-shit 【原文】
- 判断方法最干净：每句先问谁会用、改变读者什么、删掉后什么会变假；再选删、收（只留一个精确限定）、挪（放到被限定的那句旁边，挪到脚注不算）、留四种处理。明确说不按关键词判断。
- 我们第 8 条里“删掉、只留一层、挪到旁边、留下并写具体”这四种处理来自这里。

**EtherealClarity/remove-defensive-writing-skill** https://github.com/EtherealClarity/remove-defensive-writing-skill 【原文】
- 针对 ChatGPT 过度防御的回答。一条好用的检查：说出这句回应的是哪条具体反对意见，说不出来就删。

**Devilyuu/anti-defensive-writing-zh** https://github.com/Devilyuu/anti-defensive-writing-zh 【原文】
- 中文分类最完整，专门有一节防止删过头（比如把“可能提升”改成“提升”），附带核对数字和日期的脚本。

**不建议照搬：** Adkid-Zephyr/anti-defensive-writing-Skill（约 4.5k 星）主张“论文是发布会，只讲最强的优势”，不利材料按“删、缩小主张、换维度”处理，没有“什么时候该保留”的清单，容易变成选择性呈现。

## 一（再补）、去 AI 味 skill 的新进展

补充调研：2026-10-30。

- **blader/humanizer v3**（9 月）：35 条合成 25 条，两条总规则是“每句话都要给读者新东西”和“越少见于认真写作的人的写法，权重越高”。“not X but Y”和单独成行的收束句排在最前；删掉了“轮换近义词”。v3.1 新增“重讲读者已经知道的上下文”。【原文】
- **avoid-ai-writing v3.37–3.38**（10 月）：用人写的文章校准后发现，普通的“not only…but also”“not X but Y”人用得更多，现在只在“It's not just X, it's Y”或三句内连用时才标。【原文】
- **shuorenhua v2.6**（10 月 16 日）：用户说“别吹”时，只降纯程度的夸饰（“完美融合”改成“融合”），能核查的承诺和数字原样保留；正常文本误改 0/58。【原文】
- **lieflat-less-ai-tone V2**（10 月 27 日）：新增 270 对同题材文章对照，推翻了 3 条旧规则：“一二三”序号小标题、“这意味着”式复述、用一句话引出列表，其实人用得更多。“赋能/闭环/抓手”“首先/其次/总之”配对后和人没有差别；“不是 A 而是 B”是最强的信号。【原文】
- **Graphite 的研究**（约 9 万篇对照）：同一家模型相邻两个版本只有约 28–45% 的套路相同；某个新模型的破折号少了 99%，空出来的位置被“this matters”（人的 116 倍）这类新套话占了。说明按词表禁词正在失效。【原文】
- **theclaymethod/unslop** 公开了“不发布”的结论：比不加 skill 找出、修好的问题多，但误伤率没达标。【原文】
- 读者怎么判断“slop”：主要看内容相关性、信息密度和语气，看句法比看词汇准（Shaib 等，2026 年 10 月修订）。专业作家改 AI 文字，改的主要是别扭用词、句子结构、多余解释和陈词滥调，几乎都是“说不清楚”的问题（Chakrabarty 等，CHI 2025）。【原文】

我们第 9 条据此改成：先管句子和结构层面的套路（假对比、点明意义、切得太碎、用冒号卖关子），词表只当参考；不改序号标题和“这意味着”；明确列出实测无用的表面功夫。

## 一（三补）、括号和写代码时的文字

补充调研：2026-10-30。

**括号**

- 没有找到“AI 普遍比人多用括号”的研究，证据反而指向另一边：一项拿 LLM 和《经济学人》文章对比的研究，二手报道说 LLM 的逗号、分号和括号都比人少。https://biznews.com/tech/spot-ai-written-text 【转述】
- 维基百科的 Signs of AI writing 没有把括号列为迹象，括号只作为人写时代替破折号的写法出现。【转述】
- 我们观察到的是另一回事：在聊天回复和工作汇报里，AI 爱把补充说明、免责和改动记录塞进括号，被用户纠正之后尤其明显，比如“（没有使用××）”。这是维护者和我们自己检查回复时看到的，没有测量。【个人】

所以第 10 条不限制括号这个符号，也不写“少用括号”，只管括号里放了什么：把括号盖住读一遍，少了也没影响的删掉，要紧的写成句子。

**写代码时的文字**

- Google 工程实践的 CL 描述指南：第一行用祈使句说清做了什么，只看这一行就要懂；正文说为什么，也说做法的缺点；“Fix bug”“Moving code from A to B”“Phase 1”都是反面例子；自动生成的改动也要遵守。https://google.github.io/eng-practices/review/developer/cl-descriptions.html 【原文】
- Google 技术写作课的报错信息一节：好的报错要回答出了什么问题、用户怎么解决；常见毛病是没法操作、含糊、不准确、不说原因、不说下一步。https://developers.google.com/tech-writing/error-messages 【原文】
- Watanabe 等分析了 5 个 AI 编程代理的 PR：各家的描述风格不同，这些差别和审查者的参与度、回复时间、合并结果有关。摘要没有给具体数字。https://arxiv.org/abs/2602.17084 【预印】
- 几个清理“AI 痕迹”的 skill 把两类注释列为优先删除：复述代码的，以及叙述改动的（previously、no longer、updated to）；解释原因的注释保留。https://skillselion.com/skills/spences10/claude-code-toolkit/deslop 【转述】

第 12 条和 `references/dev-writing.md` 据此写成。这一类文字还有一个问题：skill 只在 AI 认出这是写作任务时才加载，写代码的途中常常不加载，所以 README 里给了一段放进 `AGENTS.md` 或 `CLAUDE.md` 的常驻说明。

## 二、维基百科 Signs of AI writing【原文】

https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing

- 按内容、用词、格式、写给用户的话、引用等分类，另外单列“无效的迹象”和“过时的迹象”。
- 页面说这些是观察，不是规则；只改表面迹象，会让问题更难发现。
- AI 常用词每年在变：delve 已经少见；2026 年中以后变成 leverage、prioritize 这类词，句子也变短了。
- 破折号已列为过时迹象；“同义词轮换”也已列为过时迹象。“含糊的关联”是现在最常见的迹象之一。
- 2026 年 10 月版（修订号 1382688615）：强迹象是 Markdown 残留、没填的占位符、“I hope this helps”这类聊天口吻；要成批出现才算的有 AI 词汇（按模型代际变化）、用“serves as”“boasts”回避 is/has、否定式对比、三连排比；2026 年中以后新出现“should be treated as X rather than Y”“does not establish”。无效指标包括语法完美、单独出现的过渡词；“perhaps”“tends to”被列为人写的迹象。中文的近义词轮换实测仍是强信号，和英文不同。

## 三、人写的规范

- GOV.UK https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/style-guides/a-to-z-style-guide/ ：禁用词约 31 个，多数给了替换词。技术术语不算黑话，但第一次出现要解释。【原文】
- plainlanguage 指南（存档）https://github.com/GSA/plainlanguage.gov ：同一个概念只用一个词。复述测试：让读者用自己的话复述，并说读完会怎么做；案例中读者都说看懂了，但对同一个术语各有各的理解。【原文】
- 微软 https://learn.microsoft.com/en-us/style-guide/global-communications/writing-tips ：一个概念一个词；保留 that、who 和冠词；少用句子片段。【原文】
- Google https://developers.google.com/style/jargon ：solution 这类意思太宽的词也算黑话。【原文】
- 阮一峰 https://github.com/ruanyf/document-style-guide ：“其、该、此”必须指代明确；不用生造词。【原文】
- 中文文案排版指北 https://github.com/sparanoid/chinese-copywriting-guidelines ：主要讲排版，有一条“不要使用不地道的缩写”。【原文】
- 少数派《不要逃避解释》https://sspai.com/post/98169 ：讲“相关”“有关”被拿来逃避说清楚。【原文】
- 余光中《怎样改进英式中文》：批评“作出/进行+抽象名词”和“的的不休”。【转述】

## 四、检查工具【原文】

- Vale https://docs.vale.sh/checks/consistency ：替换规则可以写例外；有“两种写法只许出现一种”的检查；可以用注释关掉一段。
- prh https://github.com/prh/prh ：每条规则可以附“输入→期望输出”的例子，加载时自动核对；能排除专名。
- 中文的 lint-md、zhlint、autocorrect：只管排版，不查术语和黑话。
- proselint：把“少误报”当作成败关键。
- antislop 词表 https://github.com/sam-paech/antislop-sampler ：从 AI 写的故事里统计出来，不适合技术文字。

## 五、我们已经比别人多做的

- 管的是 AI 自己写的每一段话，不只是改用户贴来的稿子。
- 专门反对为了省字删词，同类 skill 里很少见。
- 项目级的叫法统一，加上检查脚本和 CI。
- 按读者区分术语和黑话，和 GOV.UK、Google 的做法一致。

## 六、不建议照搬的

- 绝对禁令：禁副词、禁破折号、禁冒号。
- 让模型给自己打分。
- 很长的词表，尤其是从小说里统计出来的。
- 写死的数字阈值。
- 把“进行”、被动句当成 AI 痕迹。它们的问题是读着别扭，不是 AI 味。
