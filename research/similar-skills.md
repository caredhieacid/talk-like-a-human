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

## 二、维基百科 Signs of AI writing【原文】

https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing

- 按内容、用词、格式、写给用户的话、引用等分类，另外单列“无效的迹象”和“过时的迹象”。
- 页面说这些是观察，不是规则；只改表面迹象，会让问题更难发现。
- AI 常用词每年在变：delve 已经少见；2026 年中以后变成 leverage、prioritize 这类词，句子也变短了。
- 破折号已列为过时迹象；“同义词轮换”也已列为过时迹象。“含糊的关联”是现在最常见的迹象之一。

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
