---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

你是负责数据同步的值班 agent。用户在群里问你：“昨晚的数据同步怎么样了？别啰嗦，一两句话说清。”

你掌握的情况：任务凌晨 2 点开始跑，3 点 10 分失败，原因是源库连接超时。你早上 9 点手动重跑了一次，9 点 40 分成功，数据已经补齐。为什么会超时还没查清，你打算今天下午再查。

写出你在群里的回复。
