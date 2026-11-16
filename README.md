# look-before-you-build

**English** | [简体中文](README.zh-CN.md)

> **Status: v0.1, experimental.** Small eval suite, weak auto-triggering. See [What we know so far](#what-we-know-so-far).

A Claude Code skill (`preflight`) that does the **meta-research** coding agents usually skip: deciding how much thinking a task deserves *before* writing code, then doing just that much.

## The problem

Ask an agent to "build a game AI" and it piles up heuristics. Ask it to "write a scraper for subtitles" and it writes a scraper, without checking whether an official caption endpoint or a mature tool already exists. The costly mistakes are rarely bad code. They are:

- **misclassifying the problem**: patching a search problem with hand-tuned rules instead of using minimax/MCTS;
- **missing prior art**: an official API, a standard library, or an existing skill/MCP server;
- **expensive access paths**: launching browser automation before looking at the docs, a sitemap, or structured data;
- **architecture that's hard to undo**: data formats, schemas, public interfaces;
- **losing the human**: a non-engineer can't follow, veto, or own the key decisions.

Code review catches problems *after* code exists. This skill covers the step before, deciding what to build and how, which is where most rework comes from.

## What it does

1. **Tier the task** (0 / 1 / 2) by reversibility, blast radius, external dependencies, and uncertainty. Tier 0 just gets done, with no ceremony.
2. **Research at the depth the tier calls for.** A six-dimension checklist covers problem framing, prior art, access path, architecture, tooling, and human control. For tier 2, three parallel subagents handle problem classification, prior art, and cheap environment scouting.
3. **Write a one-page brief in plain language**, with runnable verification and every key decision (what was chosen, what was rejected, and the cost of changing it later).
4. **Ask first or build first.** Decisions the user can't cheaply undo (third-party ToS, accounts, money, schemas, data migrations, real forks in direction) wait for sign-off. Reversible ones get built and verified, then presented *with* the brief. The test: *if the user disagrees after seeing the result, how much do they lose?*
5. **Step back mid-build** after three failed fix rounds, two rejections, growing special cases, or a broken premise.
6. **Retro.** Each task ends by asking: *what question, asked up front, would have saved the most rework?* Answers go into the project's `PREFLIGHT.md` or your personal lessons file.

Inspired in part by Anthropic's write-up on [how the Claude Code team does code review](https://claude.dev/blog/solving-code-review-at-anthropic/): effort scaled to risk, runnable verification, capped rounds, and incidents fed back into the process. This project is not affiliated with Anthropic.

## Install

As a plugin (recommended):

```
/plugin marketplace add gxxxr-111/look-before-you-build
/plugin install look-before-you-build@look-before-you-build
```

Or copy the skill folder by hand:

```bash
git clone https://github.com/gxxxr-111/look-before-you-build
cp -R look-before-you-build/skills/preflight ~/.claude/skills/preflight
```

### Make it actually trigger

Claude rarely picks this skill up on its own for build requests (see below). Add one line to `~/.claude/CLAUDE.md` or a project's `CLAUDE.md`:

```markdown
Before starting a new project or feature, an integration with an external site/API, a scraper or automation, or a stack/architecture choice — or after the same bug survives three fix attempts — use the preflight skill.
```

## Where your lessons live

| File | Holds | Survives updates |
|---|---|---|
| `skills/preflight/references/lessons.md` | Starter lessons shipped with the skill | Replaced on update |
| `~/.claude/preflight/lessons.md` | Your own cross-project lessons | Yes |
| `<project>/PREFLIGHT.md` | Project-specific pitfalls and checks | Yes |

## What we know so far

Evaluated with Anthropic's skill-creator workflow, one run per configuration, so treat these as early signals and not as proof.

| Case | With skill | Without skill | Notes |
|---|---|---|---|
| `rename-function-tier0` (trivial rename) | 3/3 | 3/3 | No ceremony in either; confirms tier 0 stays lightweight |
| `gomoku-stuck-reframe` (5 failed weight tweaks) | 5/5 | 5/5 | Both reframed to search. Not discriminating yet |
| `transcript-tool-tier2` (Bilibili transcripts at scale) | 6/6 | 3/6 | With the skill it built on an existing tool, wrote offline tests, and stopped before the login/ToS decision |

**Auto-triggering is weak.** On 20 queries (10 that should trigger, 10 near-misses), precision was 100% but recall was 0–17%, and five rounds of rewriting the description didn't beat the original on held-out queries. Use the `CLAUDE.md` line above.

Details: [`evals/RESULTS.md`](evals/RESULTS.md). Harder, more discriminating cases are very welcome.

## Run the evals

```bash
claude plugin eval .
```

Each run starts real agent sessions and costs real tokens (one full suite ran several hundred thousand). Run single cases while you iterate.

## Contributing

Issues and PRs are welcome, especially:
- eval cases where agents without the skill go wrong in a costly way;
- lessons that answer "what question would have saved the most rework?" and apply across projects.

This is a side project, so replies may be slow.

## License

[MIT](LICENSE)
