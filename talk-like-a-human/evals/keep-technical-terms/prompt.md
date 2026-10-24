---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

这段是写给后端同事的设计说明，帮我改得好读一点，但别改成外行话：

本次对订单服务进行了重构，基于幂等键的设计来实现重复请求的去重。支付回调失败时进入重试队列，最多重试 3 次，3 次仍失败则触发告警并人工介入。该方案已在预发环境进行了压测，P99 延迟由 850ms 降至 210ms。回滚方案：关闭 feature flag order_v2 即可。
