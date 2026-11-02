# A Second Search When the First Is Empty

**Day 45** · **Advanced** · Phase 04: Retrieval Studio

If the first query abstains for low coverage, rewrite once and search again, with a hard stop at two passes.

## Concept

Day 40 abstained when coverage was low. Some of those abstentions are retrieval misses, not missing facts. A second search with a different query can recover the span. It can also thrash: a loop that rewrites forever, or a second pass that lowers the threshold until something, anything, quotes. This project allows exactly one retry. The first pass searches the original question. If the quoter would abstain for low coverage, a rewriter produces one new query, the system searches again, and the quoter runs with the same threshold as the first pass. The threshold does not move. If the second pass also abstains, the system stops and returns the abstention, plus both queries. Three searches is a bug. You will fixture a question that succeeds only on the retry, and a question that must still abstain because the fact is absent.

## Approach

The retry rewriter is deterministic and template-based, so the test does not need a model. For example, it appends the section name from a small keyword map. The attempt counter is an explicit integer in the response, and a test stubs the search function to count calls. A second retry path that catches a broad exception and tries again is forbidden; if you catch errors, they are not retrieval misses and they do not trigger rewrite. Log both queries even when the first pass succeeds, with the second marked `not-run`. The unanswerable holdout from Day 40 must still abstain, and its log must show two searches, not three.

## Components

| Piece | Role |
| --- | --- |
| Attempt counter | An integer capped at two, returned in the response. |
| Same-threshold retry | The quoter's cutoff is identical on both passes. |
| Retry fixture | A question whose gold chunk appears only after the rewritten query. |
| Absent-fact fixture | Two searches, then abstain, with both queries logged. |

## How it works

1. Wire the first pass to the existing quote-or-abstain path.
2. On low coverage only, rewrite once and search again.
3. Stub the search function and assert the absent-fact question triggers two calls.
4. Build the retry-success fixture by making the original query lexically miss and the rewritten query hit.
5. Write `retries.md` with both fixtures' logs.

## Tech stack

- Python 3.11 or newer
- Template rewriter and the Day 40 quoter
- A call-counting stub in tests

## Setup

1. Create `second-search/` with `retry.py` and tests.
2. Run both fixtures.
3. Add a test that a third search call fails the run if it happens.
4. Confirm the threshold file is read once and reused.

## What done looks like

- The absent-fact fixture performs two searches and abstains.
- The retry-success fixture quotes a span that the first query did not retrieve.
- The threshold value is the same in both attempts' logs.
- A test fails the build if search is called three times on one question.

## Step ahead

The next failure is a retry that succeeds by retrieving a contradictory span. Add a check between the two passes: if both passes would quote and the quotes disagree on a number, abstain with reason `conflict` rather than preferring the second pass because it ran later. Fixture two fee sentences with different amounts and a rewriter that surfaces the second one. The step-ahead behavior is to surface the conflict, not to average the numbers or to pick the more recent file unless the case edition already settled it.
