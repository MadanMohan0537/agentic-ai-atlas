# Rewrite, Then Keep the Original

**Day 38** · **Intermediate** · Phase 04: Retrieval Studio

Rewrite a vague question into a handbook query and search both, because the rewrite can drop the only specific token.

## Concept

Users ask "what's the deal with rain," and a rewrite step turns that into "weather closure policy." Sometimes the rewrite helps. Sometimes the user said `HL-FEE-14` in a messy sentence and the rewrite, aiming for clean prose, drops the code. This project adds a query rewriter with two backends: a deterministic template rewriter you write for the handbook's known topics, and an optional model rewriter behind the same interface. Search runs on the original query and the rewritten query. You will log both strings. A fixture query contains a rare code plus vague wording. The template rewriter must preserve unknown alphanumeric codes. You will also show a hostile template that deletes tokens it does not recognize, and a test that fails that template. Keeping the original query in the fusion set is the mitigation you will measure, not a slogan.

## Approach

The template rewriter maps a few keywords to handbook phrases and appends any token that matches a code pattern, rather than replacing the whole string. Search both queries with BM25, fuse the two lists with the Day 37 function, and compare gold rank to searching the original alone. The hostile rewriter is a one-liner that keeps only whitelisted words. It exists to make the failure mode obvious in a test. If you connect a model, it must be optional and the test suite must pass with the template only. Log a JSON line per question with `original`, `rewritten`, and both rankings' top ids.

## Components

| Piece | Role |
| --- | --- |
| Template rewriter | Keyword expansion that preserves code-like tokens. |
| Hostile rewriter | A whitelist rewriter the test expects to drop the code. |
| Dual search | Original and rewrite, fused. |
| Query log | Both strings and the top ids, per question. |

## How it works

1. Implement the template rewriter and the code-preserving rule.
2. Implement the hostile rewriter and test it against a sentence containing `HL-FEE-14`.
3. Run dual search on the gold questions plus the messy code question.
4. Compare fused dual-search gold rank to original-only gold rank.
5. Write `rewrites.md` with one case the rewrite improved and one it would have damaged if you had dropped the original.

## Tech stack

- Python 3.11 or newer
- BM25 and fusion from earlier days
- Optional model rewriter behind a flag defaulting to off

## Setup

1. Create `rewrite/` with `rewrite.py` and tests.
2. Run the messy code query with the template rewriter and with the hostile one.
3. Run the gold set with dual search.
4. Confirm tests pass with no network and no API key.

## What done looks like

- The hostile rewriter drops the code, and the test asserts that drop.
- The template rewriter keeps the code, and the test asserts that keep.
- The log contains both query strings for every question.
- The notes include a case where dropping the original would have lost the gold chunk.
