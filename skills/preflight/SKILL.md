---
name: preflight
description: Meta-research before building. Decide how much up-front thinking a task deserves, then — scaled to its risk — classify the problem, look for prior art, scout the target environment cheaply, weigh architecture choices, and produce a one-page brief the user can understand and sign off on. Also use mid-build to step back when repeated fixes keep failing. Use this skill before any new project or feature, integrations with external sites/APIs/data sources, scrapers or automation, stack or architecture choices, "build me a tool that reliably…" requests, or when the same problem has survived several fix attempts — even if the user never says "research" or "design". Applies whatever language the user writes in.
---

# Preflight: meta-research before you build

## Why this step exists

Agents tend to take a request literally and start coding: "get the transcript" becomes "write a scraper", "build a game AI" becomes "pile on heuristics". The expensive mistakes are rarely bad code. They are **misclassifying the problem, missing an existing solution, or locking in an architecture that is hard to undo** — and they get more expensive the later they surface.

Overthinking has a cost too. So the point of this skill is not "think more" but **decide how much thinking the task is worth**, spend accordingly, and keep the human able to follow and veto every key decision.

The approach borrows from how Anthropic's Claude Code team runs code review: scale effort to the risk of the change itself, require something runnable as verification, cap back-and-forth rounds, and feed every incident back into the process. That system covers what happens *after* code is written; deciding *whether* to build something and *how* to structure it is explicitly left to humans. Preflight helps people do that part well.

## Overview

1. **Tier** — decide whether the task is tier 0, 1, or 2.
2. **Research** — investigate at the depth the tier calls for.
3. **Brief and sign-off** — tier 1 gets a short note in chat; tier 2 gets a one-page brief. Whether the brief comes *before* the build (ask first) or *with* it (build first) depends on whether the decisions are reversible.
4. **Mid-build triggers** — when specific warning signs appear, return to step 2.
5. **Retro** — at the end, feed lessons back into the checklist.

## 1. Tier the task

Read `references/tiering.md` and answer its questions quickly. Roughly:

- **Tier 0** — small, easily reverted, nowhere sensitive → just do it; don't mention preflight.
- **Tier 1** — an ordinary feature with some trade-offs, all reversible → run through the six-dimension checklist in a few minutes, explain your approach in three to five sentences, then start.
- **Tier 2** — a new project, an external dependency, a hard-to-reverse decision (data formats, core architecture, public interfaces), or anything on the always-escalate list → full research and a written brief; ask-first decisions get the user's confirmation before you build (see step 3).

Tell the user the tier and one reason, e.g. "This is tier 2 because the whole tool depends on a third-party site's structure." If they want to move it up or down, do what they say.

## 2. Research

First read past lessons: `references/lessons.md` (starter lessons shipped with this skill), the user's personal lessons file `~/.claude/preflight/lessons.md` if it exists, and the project's root `PREFLIGHT.md` if it exists. Then read `references/checklist.md`, which groups the questions into six dimensions: problem framing, prior art, access path, architecture and extensibility, tooling, and human control.

- **Tier 1** — go through it in your head and surface only the one or two points that actually change the decision.
- **Tier 2** — dispatch parallel subagents using the prompt templates in `references/research-agents.md`. Usually three tracks:
  - **Problem classification** — what known class of problem is this, and what is the standard solution?
  - **Prior art** — is there an official API, a mature open-source library, or an existing MCP server / skill to use or borrow from?
  - **Environment scouting** — map the target as cheaply as possible (official docs, sitemap, robots.txt, structured data first; pages later), not by firing up browser automation.

  Subagents keep the bulky raw material in their own context so the main conversation only receives conclusions.

Research has a budget. For tier 2, stop when you can make a recommendation and state its risks; don't aim for exhaustiveness. If research shows the problem is simpler than it looked, drop the tier and say so.

## 3. Brief and sign-off

For tier 2, fill in `assets/design-brief.md` and save it in the project (default `docs/preflight/<date>-<topic>.md`, or the project's existing docs folder).

Write for a reader who may not be an engineer:
- Plain language; define each technical term in one line the first time it appears.
- For every key decision: what you chose, why, what you rejected, and how hard it would be to change later.
- **Verification must be runnable** — tests, scripts, metrics. If you can't say how to check that it works, the problem isn't understood yet; go back to research.
- End with the decisions the user needs to make, each with your recommendation.

### Ask first or build first?

The point of sign-off is that the user can understand and veto every key decision. It is not to make them wait. A decision they can cheaply undo after seeing working code doesn't need their approval beforehand; one they can't undo does. So sort the decisions in the brief:

**Ask first** — stop before implementing, and end your reply with the decisions — when any key decision:
- commits the user to a risk only they can accept: a third party's terms of service, using their account or credentials, spending money, legal or ethical questions;
- is hard to undo: long-lived data formats, schemas, public interfaces, deleting or migrating data, anything shipped to other people;
- is a genuine fork in direction or scope where the options lead to materially different products and the request doesn't indicate which one the user wants.

**Build first** — when the user asked for action ("just fix it", "build it", "go ahead") and the remaining decisions are reversible (version control, new files, a contained module): pick your recommended option for each, build it, verify it with the runnable checks from the brief, then present the brief *alongside* the result. In that reply:
- lead with what now works and the verification results;
- list each decision you made on their behalf, what you rejected, and how to switch if they'd prefer otherwise;
- keep the brief file in the project.

**Mixed** — build the reversible parts (a probe, the core logic, the tests) and stop right at the first ask-first decision, saying what is done and what is waiting on them.

When unsure which bucket a decision falls in, ask yourself: *if the user disagrees after seeing the result, how much do they lose?* Minutes of rework → build first. Money, an account, data, or trust → ask first.

If the user says "you decide" to an ask-first decision, follow your recommendation, but keep the brief in the project so the reasoning stays traceable.

## 4. Mid-build triggers: when to step back

Stop patching and return to step 2 — telling the user why — when any of these happen:

- The same class of problem has survived **three** fix rounds (Anthropic's review process also asks authors to rethink the approach after three rounds).
- The user has rejected your output twice in a row.
- Fixes increasingly rely on special cases, hard-coding, or "one more condition".
- A premise in the brief turns out to be false (e.g. you assumed an API existed and it doesn't).
- Performance or cost is an order of magnitude worse than expected.

When you step back, the first question is always: *Is this a problem type with a known standard solution that I've been forcing with the wrong method?*

## 5. Retro

When the task (or a major phase) wraps up, spend a minute on:

> What question, had preflight asked it up front, would have saved the most rework?

- Project-specific answers go in the project's root `PREFLIGHT.md` (create it if needed): what failure looks like in this project, pitfalls hit, things to check first next time. Read it at the start of future preflights in this project.
- Answers with general value: tell the user and suggest adding them to their personal lessons file `~/.claude/preflight/lessons.md` (create it in the same format as `references/lessons.md`); write only with the user's agreement. Never edit files inside this skill's own folder — installs and updates overwrite them. If a lesson looks useful to everyone, suggest the user contribute it upstream.

This keeps the checklist getting sharper rather than longer. If a lesson never earns its keep, suggest removing it.

## Don't

- Don't run preflight on tier 0 work — that's exactly the overthinking to avoid.
- Don't dump raw research on the user. They want a recommendation and the reasoning.
- Don't build past an ask-first decision. Reversible work and throwaway feasibility probes are fine; say which is which.
- Don't stop for sign-off on reversible decisions when the user asked you to act. Make the call, build it, verify it, and show your reasoning with the result.
- Don't make value judgments for the user — whether to build it at all, or whether to accept a risk such as violating a site's terms of service. Lay them out and let the user decide.
