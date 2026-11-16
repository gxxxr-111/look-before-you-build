# Tier 2 research: subagent prompt templates

Dispatch the tracks in parallel (in the same turn); each returns conclusions only, never raw page content. Trim or merge to fit the task — for a narrow question, two tracks or even one is enough.

Every prompt should include: a one-sentence restatement of the task (solution stripped out), the constraints the user has given, the expected return format, and a budget.

## A. Problem classification

```
Task: <one-sentence restatement, no solution implied>
Constraints: <language, runtime environment, cost, time, etc.>

Work out which known class of problem this belongs to.
1. Give the 1–3 closest problem types and the standard solution for each (algorithm, architectural pattern, or engineering practice).
2. For each, name a well-known success story or reference implementation.
3. Point out where the "intuitive" approach would get stuck.
Return: a conclusion of no more than ~200 words plus reference links. Don't paste long excerpts.
Budget: if ~10 searches don't produce a clear answer, say plainly that you found no standard solution and list the directions you tried.
```

## B. Prior art

```
Task: <one-sentence restatement>
Constraints: <...>

Survey existing solutions we could use directly or borrow from, in priority order:
1. Official routes offered by the target system (API, SDK, export, open data);
2. Mature open-source tools or libraries: name, last release date, licence, whether it covers our need;
3. Existing MCP servers, Claude Code skills, or plugins;
4. Other people's war stories (known pitfalls, bans, approaches that stopped working).
Return: a table (option / coverage / maintenance / risk) plus your recommendation (use as-is / adapt / borrow the idea / build from scratch) with a one-line reason.
Note: evaluate third-party skills or plugins only; do not install them.
```

## C. Environment scouting

```
Target: <site / system / codebase>
Resource to locate: <...>

Map the target as cheaply as possible. Try in order and stop as soon as you have enough:
1. Official docs and developer pages;
2. robots.txt, sitemap.xml, RSS, OpenAPI docs;
3. Structured data in one sample page (JSON-LD, embedded initial state) and the data endpoints it calls;
4. Only if all of the above fail, say whether browser automation is needed.
Don't read whole HTML pages into context; use curl + grep and look only at the relevant fragments.
Return: where the resource lives, the most stable access path, prerequisites (login, rate limits, region), and relevant terms-of-service restrictions.
```

## After the results come back

- Cross-check: does B have an implementation of A's standard solution? Does C's environment support it?
- Where conclusions conflict or a key fact has a single source, mark it "unverified" in the brief.
- If the problem turns out simpler than expected (e.g. an official API gets it in one call), drop the tier and tell the user.
