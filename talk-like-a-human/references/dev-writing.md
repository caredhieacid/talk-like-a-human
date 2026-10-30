# 写代码时顺带写的文字

这份文件不用每次都读。写 commit message、PR 描述、注释、报错信息、changelog、审查评论，或者用户说这些文字写得不好时，再来查。

这些文字有两个共同点：读的人没看过这次对话，而且它们会留很久。所以每条都问一句：半年后一个新同事只看到这段文字，他知道发生了什么吗？

项目有自己的规范时，比如 Conventional Commits、PR 模板、错误码格式，照项目的来。下面的内容用来填这些格式里的文字。

依据见仓库里的 `research/similar-skills.md`。

## 代码注释

写看不出来的事：为什么这样做、绕开了哪个坑、改这里要同时注意什么。代码本身能说清的不写。

- ❌ `# 遍历用户列表，逐个发送通知`
- ✅ 不写注释。
- ❌ `// Retry the request 3 times`
- ✅ `// The payment gateway drops requests during deploys, so retry.`

### 不要留下对话和改动的痕迹

注释是写给以后读代码的人的，他们不知道这次改之前是什么样。

- ❌ `// 改成了批量查询，之前是逐个查询`
- ✅ `// 逐个查询在 1 万用户时会超时，所以批量查`
- ❌ `// Updated to use the new API`、`// Fixed bug`、`// NEW:`、`// As requested`
- ❌ `// Removed the legacy handler`（删掉的代码直接删，历史在 git 里）
- ❌ `// 这里不需要加锁（已确认）`（谁确认的、依据是什么？）
- ✅ `// 只有启动时的单线程会调用这里，所以不用加锁`

### Docstring 和接口文档

说函数名看不出来的：参数的单位和范围、返回什么、什么情况下出错、有什么副作用。不要把函数名翻译成一句话。

- ❌ `"""Get user by id."""`，放在 `get_user_by_id` 上
- ✅ `"""Return the user, or None if it was deleted. Raises PermissionError for other tenants' users."""`

## Commit message

标题：说做了什么，只看标题就要知道这次改动的内容。用祈使句或动宾短语，别加句号。
正文：说为什么，也就是之前有什么问题、为什么这样改。怎么改的看 diff 就行，除非做法不显然。

- ❌ `Fix bug`、`Update files`、`优化代码`、`完善逻辑`、`一些调整`
- ❌ `This commit introduces a comprehensive refactor of the caching layer to enhance robustness.`
- ✅ `修复缓存没有过期导致页面显示旧价格`
- ✅ `Stop retrying payment requests that were declined`

```text
Stop retrying payment requests that were declined

Declined cards were retried three times, so customers saw three
failed charges on their statements. Only network errors are retried now.
```

不要做的事：

- 不列改了哪些文件，diff 里都有。
- 不写“这次提交”“This commit”“This PR”。
- 不写没验证过的效果，比如“提升稳定性”。有测量结果就写结果。

## PR 描述

写给审查的人。他们要知道：改了什么、为什么改、怎么确认的、哪些没测、有什么风险。

```markdown
修复登录超时后页面卡住的问题。

token 过期后，页面在等一个不会返回的请求，所以一直转圈。现在请求失败会跳回登录页。

我在 Chrome 上走了一遍过期流程，单元测试 132 个全部通过。Safari 没测。

行为变化：会话默认时长从 30 分钟改成 15 分钟，运营后台也会受影响。
```

- 第一句说结果。一个小改动几行就够，不用“Summary / Changes / Testing / Impact”五个标题，更不用 emoji。
- 行为变化要单独点出来：默认值、接口、报错、数据格式、权限。审查的人最容易漏看这些。
- 只写实际跑过的验证。没跑的写“没测”，并说清是哪些。不写“所有测试通过”，除非真的跑完了全部测试。
- 不写“comprehensive”“robust”“全面提升”。不写“请仔细审查”这种空话，有不放心的地方就直接指出来：“重试逻辑我不确定，请重点看 `retry.py`。”

## 报错信息

用户要知道两件事：出了什么问题，下一步怎么办。带上具体的值，比如哪一行、哪个文件、哪个字段。

- ❌ 操作失败，请稍后重试。
- ✅ 导入失败：第 42 行的日期格式不对，应为 YYYY-MM-DD。
- ❌ `Oops! Something went wrong.`
- ✅ `Can't reach the database at db.internal:5432. Check that it's running and that DB_HOST is correct.`
- ❌ `Invalid input.`
- ✅ `Port must be a number from 1 to 65535. Got "abc".`

- 用错误原因，不用错误代码代替句子。可以同时带上代码，方便搜索。
- 不说“哎呀”“抱歉”，也不怪用户。
- 真的只能等，就说清等什么：`The service is rate-limited. Try again in 60 seconds.`
- 不把内部细节和密钥写进给用户看的报错。

## 日志

写给半夜排查问题的人。写发生了什么事，带上能定位问题的字段。

- ❌ `Processing...`、`Error occurred`、`处理完成`
- ✅ `payment failed order_id=123 gateway=stripe status=402`

不要把密码、token 和个人信息写进日志。

## Changelog 和发布说明

写给用户，写他们能感觉到的变化，不写内部改动。

- ❌ Refactored the authentication module for improved maintainability.
- ✅ 登录过期后会跳回登录页，不再一直转圈。

破坏性变更放最前面，并写清要做什么。

## 审查评论

说清三件事：哪里有问题、会造成什么后果、建议怎么改。分清必须改的和可改可不改的。

- ❌ 这里感觉可以优化一下。
- ✅ 这里每个请求都查一次数据库，列表有 100 项时就是 100 次查询。建议批量查。
- ❌ Maybe consider possibly using a map here?
- ✅ Non-blocking: a map would make this lookup O(1), but the list is short, so either is fine.

只评论代码，不评论人。

## 界面文案

- 按钮写点了以后会发生什么：“删除项目”，不写“确定”。
- 同一个操作在所有地方用同一个词，见 SKILL.md 第 6 条。
- 空状态和错误提示要告诉用户下一步能做什么。

## 任务结束的汇报

开发任务做完时，用户想知道结果，不想看过程。

```text
登录超时修好了。token 过期后页面会跳回登录页，不再一直转圈。

我改了 `auth/session.ts` 的失败处理，并加了一个测试。单元测试全部通过，也在 Chrome 上走了一遍过期流程。Safari 没测。

会话默认时长的改动还没做，要等你确认 15 分钟是否合适。
```

- 第一句说结果。
- 不复述过程：“首先我查看了……然后我发现……接着我修改了……”
- 不列每个改动的文件，除非用户要看。
- 区分做了、验证了、没做。没验证的说出具体是哪些。
- 不用括号补充说明，见 SKILL.md 第 10 条。

## 命名

名字也是写给人看的。

- 用项目里已有的叫法。代码里叫 `workspace`，就不要新建一个 `space`。
- 不用说不清的名字：`data2`、`tmp1`、`handleInfo`、`doProcess`、`Manager2`。
- 改已有的类名、字段名是代码改动，要先问用户。

## 进度消息

任务进行中的短消息，一句话说现在在做什么或发现了什么。不要每一步都报告，也不要预告接下来的所有步骤。
