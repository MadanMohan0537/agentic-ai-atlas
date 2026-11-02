# Several Queries, One Pool

**Day 44** · **Intermediate** · Phase 04: Retrieval Studio

Fan a question out to several lexical queries, pool the hits, and dedupe by chunk id before fusion.

## Concept

One question can be several retrieval problems. "Can I leave a cargo bike out in the rain overnight, and what does it cost" needs the weather section and the fee table. A single BM25 string tends to pick one. This project splits a compound question into subqueries with a deterministic splitter: conjunctions and question marks you define, not a model. Each subquery searches. The pool is the union of hits, deduped by chunk id, keeping the best rank any subquery gave that id. You will compare gold coverage: the fraction of gold chunks hit by the single query versus the pool. On the compound question you wrote, coverage should go up. On a simple question, the pool should not pull in an unrelated second section just because the splitter was eager. Over-splitting is the failure mode you will fixture.

## Approach

The splitter breaks on " and " only when both sides contain a question cue you list, so a station named "Grand and Pine" does not split. That station name is the over-split fixture if you naively split on every "and". Test it. Each subquery returns a top ten. Dedupe keeps the minimum rank. Gold coverage uses the set of gold chunk ids for questions that have more than one gold span. Write `pool.md` with coverage before and after for each compound question, and the station-name fixture result.

## Components

| Piece | Role |
| --- | --- |
| Guarded splitter | Splits compounds without splitting names that contain 'and'. |
| Per-subquery search | BM25 top ten for each piece. |
| Dedupe | One row per chunk id, best rank kept. |
| Coverage comparison | Gold chunk recall of the single string versus the pool. |

## How it works

1. Write two compound questions with two gold spans each.
2. Add a question or a chunk containing `Grand and Pine` and assert it does not split.
3. Search the full string and the pool.
4. Compute coverage.
5. Document a case where the splitter produced a subquery you wish it had not, if one appears. If none appears, say so.

## Tech stack

- Python 3.11 or newer
- BM25
- Gold offsets from Day 33, extended

## Setup

1. Create `multi-query/` with `split.py` and tests.
2. Run the compound questions.
3. Run the station-name test.
4. Keep the splitter rules in a short comment that matches the test names.

## What done looks like

- `Grand and Pine` remains one query in the test.
- Coverage is reported for the compound questions against both strategies.
- Dedupe keeps a single id with the best rank, and a test constructs a duplicate across subqueries.
- The splitter is deterministic: same string in, same list out.
