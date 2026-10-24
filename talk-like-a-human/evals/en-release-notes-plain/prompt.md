---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Turn this changelog into release notes for our customers (they're small business owners, not developers). Keep it short.

- feat: CSV export for invoices (#412)
- fix: tz bug — due dates off by 1 day for users west of UTC
- perf: dashboard initial load 4.1s -> 1.3s
- chore: bump deps
- feat: bulk-archive clients
