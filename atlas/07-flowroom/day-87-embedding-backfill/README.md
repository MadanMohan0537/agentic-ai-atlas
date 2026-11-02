# An Embedding Job that Skips Unchanged Text

**Day 87** · **Advanced** · Phase 07: Flowroom: Analytics and Pipelines

Backfill chunk embeddings keyed by content hash and model id, and skip rows whose hash is already stored.

## Concept

Re-embedding a handbook on every build burns time and, when the model is hosted, money. It also mixes vectors from two models in one column if you are not careful. This project stores embeddings in a table keyed by chunk id, content hash, and model id. The job embeds a chunk only when that triple is missing. A text change changes the hash and produces a new row. The old row stays so you can compare. A model id change produces a new row even if the text is identical. The search path must filter to one model id, and a test expects it to ignore the other model's vector. You will run the job twice and show the second run embedding zero chunks. This is a batch data job. It is not a vector database product pitch.

## Approach

Use the hashing embedder so the job runs offline. The hash is SHA-256 of the chunk text bytes. The job writes a log line per chunk: `embedded` or `skipped`, with the reason. A test changes one character, expects one `embedded` and the rest `skipped`, and expects two rows for that chunk id. The reader function `vectors_for(model_id)` returns only that model. If the caller omits the model id, it raises. Silent mixing is the bug. Keep the log. The skip decision should be testable without re-reading the whole table by eye.

## Components

| Piece | Role |
| --- | --- |
| Embedding table | Chunk id, content hash, model id, vector. |
| Skip rule | Do nothing when the triple already exists. |
| Append-on-change | New hash or new model id adds a row and keeps the old one. |
| Reader filter | Requires a model id and will not mix. |

## How it works

1. Embed a three-chunk handbook with model id `hash-v1`.
2. Run the job again and assert zero embeds.
3. Edit one chunk and assert a single embed and two stored rows for that id.
4. Run with model id `hash-v2` and assert three new rows.
5. Assert a reader call without a model id raises, and a call with `hash-v1` does not return `hash-v2` vectors.

## Tech stack

- Python 3.11 or newer
- SQLite and the hashing embedder
- A job log of embedded versus skipped

## Setup

1. Create `embed-backfill/` with `job.py` and tests.
2. Run the sequence of four job states.
3. Run tests.
4. Record the model id naming rule in the notes: changing the hash function means a new model id.

## What done looks like

- The second run skips every chunk.
- A one-character edit embeds one chunk and retains the previous row.
- Two model ids never appear in one reader result.
- Omitting the model id raises.

## Step ahead

A chunk that disappears from the handbook should not remain searchable forever. Add a tombstone step: after a run, rows whose chunk id is absent from the current source and whose model id is the one you are building are marked `retired` with a timestamp, not deleted. The reader skips retired rows. Fixture a deleted chunk and show that its vector is still in the table and absent from search results. The follow-on is reversible retirement, so you can explain a missing hit, rather than a silent delete.
