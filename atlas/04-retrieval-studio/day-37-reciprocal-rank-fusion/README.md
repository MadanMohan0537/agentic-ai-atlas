# Reciprocal Rank Fusion

**Day 37** · **Intermediate** · Phase 04: Retrieval Studio

Fuse lexical and dense rankings with reciprocal rank fusion you recompute by hand on a toy list.

## Concept

Two rankers disagree, and a product has to return one list. Averaging cosine similarity with a BM25 score mixes units nobody can explain. Reciprocal rank fusion ignores the raw scores and sums one over a constant plus the rank. This project implements that fusion for the dense list and the BM25 list, with the constant k set to 60, and also shows a one-row hand example with k set to 1 so the arithmetic fits on a page. You will fuse the gold questions and compare fused gold rank to each individual ranker. Fusion is not required to win on every question. You will count how often it matches the better of the two and how often it matches the worse. That second count is the cost of fusion, and it belongs in the notes before you make fusion the default.

## Approach

Ranks are 1-based. A chunk present in only one list contributes only that list's term. Do not invent a rank for a missing chunk. Sort the fused scores descending, and break ties by chunk id so the output is deterministic. The hand example uses three chunks and two lists of length two. Compute it in the test, not only in prose. On the real questions, write `fusion.md` with one line per question: dense gold rank, lexical gold rank, fused gold rank. Add a config flag to disable fusion so the earlier rankings remain reproducible.

## Components

| Piece | Role |
| --- | --- |
| Rank normalizer | 1-based ranks, no raw-score mixing. |
| Fusion sum | Sum of 1/(k+rank) over lists that contain the chunk. |
| Hand example | Three chunks, k=1, asserted in a test. |
| Win/loss count | How often fusion matches the better ranker, and how often the worse. |

## How it works

1. Implement fusion and the hand example test.
2. Fuse the saved rankings for each gold question.
3. Compute the three gold ranks.
4. Count better-matches and worse-matches. Ties between the source rankers are excluded from both counts and listed instead.
5. Write the notes, including a question where fusion hurt, if one exists.

## Tech stack

- Python 3.11 or newer
- Standard library only
- Saved rankings from the lexical and dense days

## Setup

1. Create `fusion/` with `rrf.py` and tests.
2. Run fusion on the gold set.
3. If you do not yet have saved rankings, recompute BM25 and the hashing embedder inside this folder and say so.
4. Run tests.

## What done looks like

- The hand example matches the test exactly.
- Ties break by chunk id, and a test swaps input order to prove it.
- The notes include the better-match count and the worse-match count.
- A missing chunk is not assigned a fictional rank.
