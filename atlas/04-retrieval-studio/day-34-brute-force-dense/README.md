# Brute-Force Dense Search

**Day 34** · **Intermediate** · Phase 04: Retrieval Studio

Embed chunks with a local bag-of-hashes or a small model and rank them by cosine, exhaustively.

## Concept

Dense retrieval is a sort over similarities. An index is an optimization you add after the ranking is correct. This project embeds every chunk from Day 33 and answers a query by scoring all of them. You have two acceptable embedders. The first is a local hashing embedder: tokenize, hash each token into a fixed number of buckets, and L2-normalize the count vector. It needs no network and it is good enough to test the plumbing. The second is a small local model you already have access to, called from one function with the same output shape. The rest of the pipeline must not care which you used. You will run all ten gold questions, record the rank of the first chunk that overlaps a gold offset, and write the misses in full. A miss is a question whose gold chunk is not in the top five.

## Approach

Put the embedder behind `embed(texts) -> list[list[float]]` with a dimension recorded in the output file. Cosine similarity on normalized vectors is a dot product, and a test should lock that equivalence on a random vector. Search is a loop, not an index library. Save `ranking.json` with query id, top five chunk ids, and the rank of the first gold hit or null. Do not tune the embedder against the ten questions repeatedly. You may look once, change a single preprocess setting such as lowercasing, and then stop. A second change belongs in the notes as an unrun idea. Otherwise the gold set becomes training data.

## Components

| Piece | Role |
| --- | --- |
| Embedder interface | One function, hashing implementation required, model implementation optional. |
| Exhaustive scorer | Dot product against every chunk vector. |
| Gold rank | Rank of the first chunk that overlaps a gold span. |
| Miss list | Questions where the gold chunk is outside the top five. |

## How it works

1. Embed all chunks and store vectors next to chunk ids.
2. Embed each question and rank chunks.
3. Compute gold rank using offset overlap, not string equality of the answer.
4. Write the miss list with the top chunk's text so you can see the near miss.
5. Test that normalized vectors have unit length and that brute-force search returns a known nearest neighbor on a toy set.

## Tech stack

- Python 3.11 or newer
- Standard library hashing embedder
- Optional local embedding model behind the same function

## Setup

1. Create `dense-search/` and copy the chunk and question files.
2. Implement `hashing_embed.py` and `search.py`.
3. Run the ten questions.
4. Run tests, including the toy nearest-neighbor case.

## What done looks like

- Every question has a recorded gold rank or an explicit miss.
- The embedder id and dimension are in the output.
- You changed at most one preprocess setting after seeing results, and the notes name it.
- The toy nearest-neighbor test passes.
