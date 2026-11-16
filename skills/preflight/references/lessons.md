# General lessons

Each lesson answers one question: *What question, had preflight asked it up front, would have saved the most rework?*
This file holds starter lessons shipped with the skill. Your own cross-project lessons go in `~/.claude/preflight/lessons.md` (same format), so updates don't overwrite them; project-specific ones go in that project's `PREFLIGHT.md`.
If a lesson never earns its keep, remove it — keep this list short.

## 1. Ask "what known class of problem is this?" first

- **Origin**: a game-playing project. Over many iterations the agent kept bolting on local rules and never questioned the architecture; things only clicked after borrowing AlphaGo's "learned evaluation + search with pruning" approach.
- **Going forward**: any game, search, optimization, or planning task is tier 2 at minimum, and the problem-classification track must produce a standard solution before code is written. After three failed fix rounds, come back to this question first.

## 2. The user's wording can lock in a solution prematurely

- **Origin**: a request phrased like "write a scraper to grab subtitles" was implemented literally, without first checking for an official caption endpoint or a mature tool.
- **Going forward**: the first step of problem framing is to restate the request with the solution removed.
