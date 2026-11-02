# Facts with Provenance

**Day 54** · **Intermediate** · Phase 05: Agent Workshop

Store long-term facts only with a source id, and refuse a fact the agent tries to save without one.

## Concept

A memory note that says "the late fee is 14" is a liability if nobody can find the sentence it came from. This project is a long-term store, separate from the sliding window. A fact is admitted only with a `source_id` that exists in a catalog of handbook chunks or tool observations. The store records the fact text, the source id, and a hash of the source text at save time. On read, if the source text has changed, the fact is returned with `stale: true` and is not silently refreshed. An agent tool `remember(text, source_id)` calls this store. A call with an unknown source id is an observation of type `rejected-memory`, and nothing is written. You will try to remember a fee that does not appear in the cited chunk and, in the required design, still accept it only if the source id exists — then add a second check that the fact's numbers appear in the source text. The second check is in scope today. A memory that can attach any sentence to any id is not provenance.

## Approach

The catalog is a JSON file of id to text, built from a few handbook chunks. `remember` verifies the id, verifies that every integer in the fact text occurs in the source text, and only then appends. This will reject some true paraphrases. That is acceptable for this day. Write the limitation down: paraphrases need a later design, and the current rule prefers false rejects over free invention. The stale flag flips when you edit the catalog text without updating the hash. A test edits the catalog and expects `stale: true` on the next read.

## Components

| Piece | Role |
| --- | --- |
| Source catalog | Ids and texts the memory is allowed to cite. |
| Remember tool | Rejects unknown ids and facts whose numbers are not in the source. |
| Hash | SHA-256 of the source text at save time. |
| Stale read | A changed source marks the fact stale instead of rewriting it. |

## How it works

1. Load a tiny catalog with one fee chunk and one unrelated chunk.
2. Remember a fact whose number appears in the fee chunk. Assert it is stored.
3. Attempt a fact with a number that does not appear. Assert rejection and an unchanged store.
4. Edit the catalog, reread, and assert the stale flag.
5. Attempt an unknown source id and assert rejection.

## Tech stack

- Python 3.11 or newer
- Standard library `hashlib` and `json`
- No vector database

## Setup

1. Create `provenance-memory/` with `store.py`, `catalog.json`, and tests.
2. Run the four cases and write `out/memory.json`.
3. Run tests.
4. Write the paraphrase limitation in `notes.md` in two sentences.

## What done looks like

- Unknown source ids write nothing.
- A number that is not in the source blocks the write.
- A changed source marks the fact stale and does not auto-edit the fact text.
- The notes name the paraphrase limitation.
