# BM25 Beside Vectors

**Day 36** · **Intermediate** · Phase 04: Retrieval Studio

Rank the same chunks with BM25 and show a query the hashing embedder misses and BM25 hits.

## Concept

Dense scores smear rare strings. A rider asks about the exact fee code `HL-FEE-14`, which appears once in the handbook. A hashing embedder may bury that chunk under generic fee language. BM25, a lexical ranker with term frequency and document length, will not, if the tokenizer keeps the code intact. This project implements BM25 over the same chunks, with a tokenizer that does not throw away identifiers. You will run the gold questions through both rankers and write a disagreement table: questions where the top lexical chunk and the top dense chunk differ. At least one query in the set should be an exact code or a rare proper name you placed in the handbook. If your gold set has no such query, add one now and mark it as added after the first dense run so the history stays honest.

## Approach

Implement the standard BM25 scoring formula with k1 and b as named constants. Compute inverse document frequency from the chunk collection you are searching, and keep that statistic with the index so a later chunk changes idf when you rebuild. Do not import a search engine. The point is the formula and the tokenizer. Tokenizer rules: lowercase, split on whitespace and punctuation, but keep tokens that contain digits. A test passes the fee code through as one token. Compare rankers by top-1 chunk id on each question and by gold rank.

## Components

| Piece | Role |
| --- | --- |
| Tokenizer | Keeps codes with digits as single tokens. |
| BM25 scorer | Term frequency, document length, and idf, with named constants. |
| Disagreement table | Questions where lexical top-1 and dense top-1 differ. |
| Rare-token query | A fee code or proper name planted in the handbook. |

## How it works

1. Tokenize chunks and build document frequencies.
2. Score the gold questions with BM25.
3. Load dense rankings from Day 34 or recompute them with the hashing embedder.
4. Write the disagreement table, including gold rank for both.
5. Assert the fee-code query's gold chunk is in the BM25 top three.

## Tech stack

- Python 3.11 or newer
- Standard library only
- The same chunk files as the dense search

## Setup

1. Create `bm25/` with `bm25.py` and tests.
2. Plant `HL-FEE-14` if the handbook does not already contain a rare code.
3. Run both rankers and write `disagreements.md`.
4. Run the tokenizer test on the fee code.

## What done looks like

- BM25 constants are named and the formula is implemented in one function a test can call.
- The rare-token query hits its gold chunk in the BM25 top three.
- The disagreement table covers every gold question.
- A token with digits is not split into a bare number and letters.
