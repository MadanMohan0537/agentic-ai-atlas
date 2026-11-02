# Pins for a Retrieval Set

**Day 73** · **Advanced** · Phase 06: Proof Bench: Evals and Harnesses

Hash the embedder id and the top-k chunk ids for a frozen query set, and fail when a rebuild drifts.

## Concept

A retrieval change can look harmless and swap the chunk your quotes depend on. This project pins a frozen query set: for each query, store the embedder name, the index content hash, and the ordered top-k chunk ids. A later run recomputes the list and fails if the ids differ. The pin file is something you commit. Updating it is a deliberate edit, not a side effect of re-running the index. You will change one handbook sentence that should not affect a specific query and show the pin still matching, then change a sentence inside a pinned chunk and show the diff. The failure output names the query id and the first rank where the ids diverge.

## Approach

Use BM25 or the hashing embedder so the pin is reproducible without a downloaded model. The index content hash is a hash of the chunk texts in id order. If the hash changes and the ids do not, the report says `content-changed-ranking-stable`, which is a warning, not a pass you should ignore, and not an automatic failure. You choose failure only when the ordered ids change. A test builds a two-chunk index, pins it, edits a stopword in an unretrieved chunk, and edits a token in the retrieved chunk. Those two edits must produce different statuses.

## Components

| Piece | Role |
| --- | --- |
| Pin file | Query id, embedder name, index hash, ordered chunk ids. |
| Comparer | First rank of divergence. |
| Content hash | Hash of chunk texts, reported even when ranks match. |
| Deliberate update | A human-edited pin, not a silent rewrite. |

## How it works

1. Build a tiny index and write `pins.json` by an explicit `write-pins` command.
2. Re-run check mode and expect a match.
3. Edit an unretrieved chunk and expect the stable-ranking warning.
4. Edit a retrieved chunk's important token and expect a failure that names the rank.
5. Assert check mode does not overwrite `pins.json`.

## Tech stack

- Python 3.11 or newer
- Hashing embedder or BM25
- JSON pin file

## Setup

1. Create `pins/` with `pin.py`, a mini handbook, and tests.
2. Run write-pins once, then check.
3. Run the two edit tests against copies of the index.
4. Document that updating pins is a separate command.

## What done looks like

- Check mode never writes the pin file.
- A ranking change names the query and the rank.
- A content change with stable ranking is a warning with a distinct status.
- The embedder name is inside the pin file.

## Step ahead

Sometimes the ranking should change, because you added a paragraph on purpose. Add an allow-list file `approved_diffs.json` that names the query id and the expected new top-k. Check mode passes a diff only when it matches an approved entry, and fails if the new ranking matches neither the pin nor an approval. Fixture one approved change and one unapproved change. The follow-on is a reviewable diff, not a habit of rewriting pins whenever the check goes red.
