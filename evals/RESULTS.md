# Eval results (v0.1)

All runs: one run per configuration, skill-creator workflow, graded against the `graders/*.md` criteria in each case. Small samples, so read these as signals.

## Behaviour evals

### Iteration 1 (initial skill)

| Case | With skill | Without skill |
|---|---|---|
| rename-function-tier0 | 3/3 | 3/3 |
| gomoku-stuck-reframe | 4/4 | 4/4 |
| transcript-tool-tier2 | 6/6 | 3/6 |

Finding: in the gomoku case the skill over-escalated, stopping for sign-off even though the user said "just fix it". That led to the ask-first / build-first rule, and grader 05 was added to check that the fix actually gets implemented.

### Iteration 2 (after the build-first rule; only affected cases re-run)

| Case | With skill | Notes |
|---|---|---|
| gomoku-stuck-reframe | 5/5 | Implemented a search-based fix with passing tests, and explained the reframe alongside the result |
| transcript-tool-tier2 | 6/6 | Built on an existing tool with 12 offline tests, then stopped before any real-video run at the login/terms-of-service decision |

Overall pass rate: 100% with the skill vs 83% without. Only the tier-2 case shows a difference; the gomoku case does not, because the baseline already reframes to search.

Cost: about 65–77k tokens per run with the skill, similar to the baseline. The tier-2 run with the skill alone used about 90k.

## Trigger evals (`trigger/queries.json`)

20 queries: 10 should trigger (several in Chinese), 10 near-misses (for example a one-off single-page scrape, or explaining a regex). 60/40 train/test split, 3 runs per query, 5 rounds of description rewriting.

- Precision: 100% throughout (near-misses never triggered it).
- Recall: 0–17%. No rewrite beat the original description on the held-out set; the best was 4/8 test accuracy.
- Likely cause: in headless `claude -p` runs, Claude rarely consults skills for build requests. Recommended workaround: the `CLAUDE.md` line in the README.

## Known gaps

- Need harder cases where the baseline makes a costly mistake (wrong problem class, a missed official API, an irreversible schema choice).
- `transcript-tool-tier2/case.yaml`'s `expected_outcome` predates the build-first rule; the graders are current.
- No multi-run variance yet.
