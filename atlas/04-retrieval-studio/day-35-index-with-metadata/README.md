# An Index with Metadata

**Day 35** · **Intermediate** · Phase 04: Retrieval Studio

Persist vectors and filter by handbook version and section before similarity is computed.

## Concept

Brute force hides a product bug: the search space is almost never "every chunk we have ever stored." Harbor Loop's handbook has a version and a section. A question about fees in the 2026 edition must not return the 2024 fee table just because the wording is close. This project persists vectors in a simple on-disk layout — a JSON manifest and a binary or JSON vector file — and applies metadata filters before scoring. You will plant a stale chunk with nearly identical text and a different `edition` field, and show that an unfiltered query ranks it first while a filtered query cannot see it. The index rebuilds from the manifest without leftover ids from a deleted chunk. Deleting a chunk and still returning it is the bug the test is named after.

## Approach

Each record has `chunk_id`, `edition`, `section`, `text`, `vector`, and `source` offsets. Filtering is a predicate over metadata, applied to candidate ids, and only then do you dot. Do not filter after you take top-k. A post-filter can return fewer hits than the user asked for and, worse, can drop the stale chunk only when you remembered to ask. The stale-chunk fixture uses the same words as a current fee chunk with one number changed. Rebuild is a pure function of the records directory: remove a file, rebuild, and assert the id is gone. You do not need a vector database server.

## Components

| Piece | Role |
| --- | --- |
| Record manifest | Ids, metadata, and where the vector lives. |
| Pre-filter | Edition and section predicates applied before scoring. |
| Stale-edition fixture | A near-copy that must lose under the filter. |
| Rebuild | Index contents match the files on disk after a deletion. |

## How it works

1. Write records for the current handbook plus one stale fee chunk.
2. Query fees with no filter and record the top id.
3. Query with `edition=2026` and assert the stale id is absent from the candidate set, not merely absent from a truncated display.
4. Delete a chunk file, rebuild, and assert its id does not return.
5. Test a filter that matches nothing: the result is empty, not an error and not a fall-through to all chunks.

## Tech stack

- Python 3.11 or newer
- JSON or a single SQLite table you create yourself
- The Day 34 embedder

## Setup

1. Create `filtered-index/` with `index.py` and fixtures.
2. Run the unfiltered and filtered queries.
3. Run the deletion test.
4. Document the candidate-count before and after the filter in `notes.md`.

## What done looks like

- The stale chunk wins unfiltered and is invisible when the edition filter is on.
- An empty filter result does not fall back to the full corpus.
- A deleted chunk id is gone after rebuild.
- The notes show candidate counts before and after filtering.
