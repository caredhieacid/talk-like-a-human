---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

帮我改一下这几条报错，用户看不懂。这是我们内部运维工具的报错，用的人都是工程师：

1. 操作失败，请稍后重试。（实际原因：上传的 CSV 第 42 行日期格式不对，要 YYYY-MM-DD）
2. Oops! Something went wrong.（实际原因：连不上数据库 db.internal:5432）
3. 系统异常，错误码 E1007。（实际原因：API key 过期了，用户要去设置页重新生成）
