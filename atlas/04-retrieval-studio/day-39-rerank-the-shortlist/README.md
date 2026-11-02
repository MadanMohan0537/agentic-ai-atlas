# Rerank the Shortlist

**Day 39** · **Intermediate** · Phase 04: Retrieval Studio

Rerank the top twenty fused hits with a lexical overlap feature and show when the new order hurts.

## Concept

The first retriever is tuned to recall. A second pass can look harder at fewer chunks. A cross-encoder is the usual choice, and it is also a dependency you may not have. This project defines a reranker interface and ships a local implementation: score each candidate by the fraction of query tokens that appear in the chunk, multiplied by a saturation on chunk length so a long chapter does not win by containing every word somewhere. You may add a model cross-encoder behind the same interface later. You will rerank the top twenty from fusion and compare gold rank before and after. Publish every question the reranker made worse. A reranker without a regression list is how a demo becomes the default and quietly drops the fee-code hit below a chatty paragraph.

## Approach

The shortlist is exactly the fused top twenty, or fewer if the corpus is smaller. The reranker may not look outside that list. That constraint is the product: second-pass cost stays bounded, and a bug cannot "fix" recall by searching the rest of the corpus. Length saturation is a named function, such as token overlap divided by log of chunk length. Test it on two chunks with the same overlap count and different lengths. Write `rerank.md` with improved, unchanged, and regressed question ids. If you add a neural reranker, keep the lexical one as the offline default the tests use.

## Components

| Piece | Role |
| --- | --- |
| Shortlist contract | Rerank only the fused top twenty. |
| Lexical reranker | Query-token overlap with a length saturation. |
| Regression list | Questions whose gold rank got worse. |
| Interface | A function signature a neural reranker could match later. |

## How it works

1. Build fused top-twenty lists for each gold question.
2. Rerank with the lexical scorer.
3. Compute gold rank before and after.
4. Group question ids into improved, unchanged, and regressed.
5. Test that a longer chunk loses to a shorter chunk when overlap counts match.

## Tech stack

- Python 3.11 or newer
- Fusion output from Day 37
- No required neural reranker

## Setup

1. Create `rerank/` with `rerank.py` and tests.
2. Run the gold set.
3. Write the three groups into `rerank.md`.
4. Add a test that a candidate outside the shortlist cannot appear in the reranked output even if you pass it accidentally. The function should ignore or reject it. Pick one behavior and test it.

## What done looks like

- The regression list is present, even if it is empty, and emptiness is explicit.
- The length-saturation test passes.
- The reranker does not introduce chunk ids that were not in the shortlist.
- The notes name the shortlist size.
