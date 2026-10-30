---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Add comments to this function where they help. I just changed it: it used to query users one by one, but that timed out at 10,000 users, so now it batches in groups of 500. The 500 is the most the CRM API accepts per call. Return the full function.

```python
def sync_users(users, crm):
    results = []
    for i in range(0, len(users), 500):
        batch = users[i:i + 500]
        results.extend(crm.upsert(batch))
    return results
```
