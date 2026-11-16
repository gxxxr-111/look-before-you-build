# The six-dimension checklist

You don't need to answer every question. Tier 1: pick the ones that change the decision. Tier 2: reach at least a one-line conclusion per dimension.

## 1. Problem framing: what is actually wanted?

- Restate the request in one sentence with the implied solution stripped out ("write a scraper to grab subtitles" → "get the text of a given video"). The user's wording often narrows the solution space before anyone has looked.
- How is success measured? Turn adjectives into runnable checks:
  - "reliable" → success rate on a fixed sample, how fast a site change is detected, behaviour on failure;
  - "fast" → a concrete latency or throughput target;
  - "easy to use" → how many steps a user needs for a given action.
- What counts as failure? What's the worst case?
- State what is explicitly **out of scope** (non-goals).

## 2. Prior art: don't start from zero

- **Classify the problem**: which known class with mature solutions does this belong to? (games → search + value estimation + pruning, à la AlphaGo/MCTS; text extraction → find a structured source first; scheduling → constraint solving; …)
- Does the target system offer an **official** route? (API, export, open data, official SDK)
- Are there mature open-source tools or libraries? Actively maintained? Suitable licence?
- Is there an existing MCP server, skill, or plugin to use directly?
- Papers, blog posts, other people's war stories?
- End with a choice: use as-is / build on it / borrow the idea / genuinely nothing exists, build from scratch (and say why).

## 3. Access path: take the cheapest, most stable route

When fetching a resource, try in this order — earlier is more stable and uses fewer tokens:

1. Official API / SDK / export feature
2. Machine-readable navigation: sitemap.xml, robots.txt, RSS/Atom, OpenAPI docs, JSON-LD or other structured data in the page, embedded initial state (e.g. `__NEXT_DATA__`)
3. Direct HTTP requests for HTML or the underlying endpoints (watch the browser's network traffic to find the data API)
4. Headless browser automation
5. Screenshots plus visual interaction

Also consider:
- What runs best on this machine? (CLI tools, an existing logged-in browser session, an existing proxy or VPN setup)
- Rate limits, anti-bot measures, login walls, terms of service. List the risky ones for the user to decide on.
- Research follows the same rule: read docs and sitemaps before pages, and don't pour whole HTML pages into context.

## 4. Architecture and extensibility: which decisions are hard to undo?

- List the **hard-to-reverse** decisions in this task (data formats, core abstractions, public interfaces, storage choice) and spend your time there.
- How does the interaction model shape the backend? (Results shown live → streaming or a job queue; batch processing → idempotency and resumability.)
- Where is change most likely? Put a seam there (e.g. a per-site adapter interface) and keep everything else simple.
- Don't design for imagined requirements. Leave extension points only where the user asked or it's highly likely.

## 5. Tooling: use the agent-era toolkit well

- What should go to **subagents**? (Broad searches, parallel research, independent review — the idea is to isolate bulky raw material in a separate context.)
- Does an existing **skill** cover any step? Is there a **missing** skill worth writing later?
- Which **MCP** connections are needed (databases, browser, docs, third-party services)?
- Which rules need **enforcement** rather than reminders? Consider hooks (e.g. run tests or a formatter before commit).
- Post-implementation review: use the existing `/code-review` and `/security-review` rather than duplicating them here.
- Does a long job need to run in the background, in tmux, or on a schedule?

## 6. Human control: keep the user able to follow and decide

- How technical is the user? How deep should the brief go?
- Which decisions must the user make? (Direction, scope, risk acceptance, cost, whether to accept third-party terms.)
- How will the user understand and maintain this later? What documentation helps (README, architecture diagram, one-page plain-language summary)?
- Who is accountable for the result, and does the user understand the risks?
