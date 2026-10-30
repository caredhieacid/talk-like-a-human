---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Write the PR description for this change.

Notes: the page hung forever after the session token expired, because it waited on a request that never returned. Now a failed request redirects to login. I also changed the default session length from 30 minutes to 15 minutes. I ran the unit tests (132 passed) and walked through the expiry flow in Chrome. Haven't tried Safari. The mobile app uses a different login endpoint, so it isn't affected.
