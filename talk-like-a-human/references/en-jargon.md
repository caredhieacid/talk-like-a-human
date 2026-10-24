# English buzzwords and AI tics

These are examples, not a ban list. When you hit one, ask "what do I actually mean?" and write that. Swapping one buzzword for a similar one ("leverage" → "harness") doesn't fix anything.

`scripts/check_terms.py --jargon` only checks the first table. Words in the second table have real uses, so the script leaves them to your judgment.

## Almost always fluff

| Instead of | Usually means | Try |
| --- | --- | --- |
| leverage | use | "use the existing cache" |
| utilize | use | "use" |
| seamless / seamlessly | without extra steps, without breaking | say what doesn't break, or cut it |
| streamline | remove steps, simplify | "cut the signup form from 9 fields to 4" |
| empower | let, help | "lets support staff refund orders" |
| holistic | complete, whole | "covers the whole checkout flow" |
| synergy | things working together | say what works with what |
| delve | look at, explain | "look at" |
| deep dive | a detailed look | "a detailed look at" |
| elevate | improve | "improve" |
| cutting-edge / state-of-the-art / best-in-class | new, best | give the fact: "the fastest of the three we tested" |
| game-changer / game-changing / revolutionary | big improvement | say what changes and by how much |
| actionable insights | findings you can act on | state the finding and the action |
| facilitate | help, make easier | "help" |
| foster | encourage, build | "encourage" |
| tapestry / testament | — | cut it |
| paradigm shift | a big change in approach | "a different approach" |
| navigate the complexities | deal with | "deal with" |
| circle back / touch base | talk again | "talk again on Friday" |
| move the needle | make a measurable difference | give the number |
| low-hanging fruit | easy wins | "easy fixes" |
| double-click on | look more closely | "look more closely at" |
| north star | main goal | "main goal" |
| boil the ocean | try to do everything | "try to fix everything at once" |

## Often overused, check the context

| Overused word | Fine when | Fluffy use → fix |
| --- | --- | --- |
| robust | you say what it survives | "a robust solution" → "retries on timeout and rejects malformed input" |
| ecosystem | you name the parts | "a rich ecosystem" → "plugins for VS Code, JetBrains, and Vim" |
| landscape | — | "the AI landscape" → "the current tools" |
| unlock | a real lock, account, or feature gate | "unlock value" → say the benefit |
| optimize | you say for what and by how much | "optimized the query" → "the query now takes 40ms instead of 900ms" |
| scalable | you give the load | "highly scalable" → "handles 10x today's traffic" |
| solution | — | name the product, fix, or tool |
| functionality | — | "feature" |
| key / crucial / critical | it really is the most important | cut, or say why it matters |
| align | text alignment | "align on the plan" → "agree on the plan" |
| bandwidth | network throughput | "no bandwidth this week" → "no time this week" |
| journey | actual travel | "the user journey" → "the steps a user takes to …" |
| enable | a setting or flag | "enables teams to" → "lets teams" |

## Vague words

These aren't jargon, but they stand in for details the reader needs.

| Vague | The reader asks | Try |
| --- | --- | --- |
| "addressed related issues" | Which issues? | "fixed the login timeout and the avatar upload error" |
| "various improvements" | Which ones? | List them. |
| "a number of users reported" | How many? | "14 users reported" |
| "significantly faster" | By how much? | "page load went from 4s to 1.2s" |
| "in terms of performance, it's better" | — | "it's faster: 900ms → 120ms" |
| "touches several modules" | Which modules? | "changes orders, inventory, and notifications" |

If you don't have the detail, say so ("we haven't measured it yet"). Don't make up a number.

## Metaphors instead of direct statements

A metaphor makes the reader translate it back, and it brings in meanings you didn't choose. When a literal phrase exists, use it.

An analogy that helps a non-expert understand something new is different. Say the plain thing first, then add the analogy ("It's a bit like…"), and make sure it fits.

| Metaphor | Direct |
| --- | --- |
| "the engine of our growth" | "brought in 40% of new users this year" |
| "this module is the heart of the system" | "every request goes through this module" |
| "a safety net" | "if the payment call fails, we retry twice and then email the user" |
| "the secret sauce" | name the thing competitors don't have |

## AI tics

| Pattern | Example | Fix |
| --- | --- | --- |
| Fake contrast | "It's not just a linter — it's a philosophy." | Say what it is. |
| Empty openers | "Great question!", "Certainly!", "Absolutely!", "We're excited to announce…" | Start with the answer or the news itself. |
| Empty closers | "I hope this helps!", "Let me know if you have any other questions." | Stop when you're done. |
| Throat-clearing | "It's worth noting that…", "It's important to understand that…" | Delete it and state the thing. |
| Grand framing | "In today's fast-paced digital landscape…" | Delete it. |
| Restating the question | "You're asking how to X. To X, you…" | Answer directly. |
| Rule of three | "fast, reliable, and scalable" when only one is true | List only what's true. |
| Hedge stacking | "This could potentially help to somewhat improve…" | "This should improve…" |
| Nominalizations | "perform an analysis of", "make a decision", "provide an explanation of" | "analyze", "decide", "explain" |
| Em-dash everywhere | "The fix — which was small — worked — mostly." | Use periods and commas. |
| Headers and bold on short answers | three headers on a five-line reply | Write plain paragraphs. |
| Telegraphic style | "Checked logs. Cache not cleared → stale data. Need confirm." | Write full sentences: "I checked the logs. The cache wasn't being cleared, so users saw stale data. Can you confirm?" Short formats like commit subject lines are fine. |
| Dropped subject or owner | "Fixed. Pending review." | Say who did what and who needs to act: "I fixed the timeout bug. Can you review it?" |
| Missing connectors | "Cache stale, users see old prices." | Say the relation: "Because the cache is stale, users see old prices." |
| Ad-hoc abbreviations | "impl", "cfg", "w/", "b/c", "deps" in prose | Spell them out unless every reader surely knows them. |
| Slash and arrow shorthand | "auth/rate-limit/retry → gateway" | Write the sentence: "Move auth, rate limiting, and retries into the gateway." |
