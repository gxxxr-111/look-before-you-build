# Tiering: how much thinking is this worth?

The tier comes from **the task itself**, not from how technical the user seems.

## Five questions

1. **Reversible?** If it goes wrong, can you get back in one step (git revert, flip a flag, delete the new files)?
2. **Blast radius?** Who is affected by a mistake — just this code, the whole project, the user's data, or a third party?
3. **External dependency?** Does it rely on things you don't control — a third-party site's structure, an API, terms of service, paid quotas, the network setup?
4. **Will it be copied?** Will this decision become the template for later code — directory layout, data format, interface conventions, core abstractions?
5. **Uncertain?** Do you actually not know the standard approach for this kind of problem, or not know what the target environment looks like?

## Deciding

- All five come back "reversible / small / none / no / confident" → **tier 0**
- One or two concerns, none serious → **tier 1**
- Any of the following → **tier 2**
  - Q1: not reversible, or reverting is costly;
  - Q3: yes, and the task's core value rests on that dependency;
  - Q4: yes, and the project is young;
  - Q5: very uncertain;
  - anything on the always-escalate list below.

## Always escalate (tier 1 at minimum, usually tier 2)

- Scraping or automating a third-party site or service (reliability, anti-bot measures, terms of service)
- Authentication, secrets, payments, billing
- Long-lived data formats, database schemas, the shape of a public API
- Long-running or unattended jobs (cron jobs, services, bots)
- **Algorithmic core** problems — games, search, optimization, recommendation (where "forcing it with the wrong method" happens most)
- Deleting, migrating, or bulk-editing user data
- The user explicitly asks for "reliable", "scalable", or "we'll add X later"

## Examples

| Task | Tier | Why |
|---|---|---|
| Change a button label | 0 | Reversible, tiny blast radius |
| Add a CLI flag to an existing script | 0–1 | Reversible; tier 1 if the flag becomes a public contract |
| Add a caching layer | 1 | Real trade-offs, but reversible |
| Reliably fetch transcripts from a video site | 2 | Depends on a third party; official or open-source routes may exist; must be "reliable" |
| Build a game-playing AI | 2 | Algorithmic core with well-known standard approaches |
| Pick the stack for a new project | 2 | Will be copied; hard to reverse |
