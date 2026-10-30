---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

帮我写这次改动的 commit message。

改动说明：购物车页面的价格有时候是旧的。查下来是 Redis 里的价格缓存没有设过期时间，价格表更新后缓存还在。我给缓存加了 10 分钟过期时间，改了 cart/price_cache.py 和 cart/tests/test_price_cache.py，测试跑过了。
