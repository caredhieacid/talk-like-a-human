---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

You just finished a coding task. Write the final message you'd send to the user. Here are the facts:

- Bug: uploading a PNG larger than 5 MB crashed the app.
- Cause: image resizing ran on the main thread.
- Fix: moved resizing to a background worker. Changed upload.ts and worker.ts.
- Added 2 unit tests; both pass.
- Did not test on Android because no emulator was available.
