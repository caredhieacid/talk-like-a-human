---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Tighten this update for the team channel:

> The export job (which was previously timing out) now finishes in 40 seconds (down from about 6 minutes, in our staging environment only). We also updated the retry logic (this wasn't in the original plan, but it seemed like a good idea) and the docs (where applicable). Note that the new S3 bucket (see below) needs to be created before Friday (if possible, though this may vary). The bucket is called exports-prod (ap-southeast-1).
