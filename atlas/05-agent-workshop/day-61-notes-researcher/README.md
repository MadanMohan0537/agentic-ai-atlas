# A Notes Researcher that Cites

**Day 61** · **Advanced** · Phase 05: Agent Workshop

Answer a question from local markdown notes with the quote-or-abstain rule wired into the tool loop.

## Concept

The retrieval stack can quote, and the agent loop can call tools. This project connects them without loosening either rule. The only retrieval tool is `search_notes(query)`, which returns chunk ids and texts from a notes folder using BM25. The only answer tool is `quote(chunk_id, text)` which succeeds only if text is an exact substring of that chunk. A final answer must be one of those successful quotes or an abstention. A scripted policy handles two questions: one answerable from the notes, one not. The unanswerable question must end in abstain even if a chunk shares several words. You will not add a free-text `finish` tool that bypasses `quote`. If the policy tries, the runner rejects it. The point is to make the citation check a tool result, not a convention the model is asked to respect.

## Approach

Reuse a small BM25 implementation and a handful of notes you write. `quote` looks up the chunk by id from the same index `search_notes` uses, so the policy cannot quote a chunk it invented an id for unless that id exists, and cannot quote text that is not there. The runner's terminal states are `quoted` and `abstained`. Anything else is an error. Log the search results and the quote attempts. A test calls `quote` with a near-miss string that differs by one word and expects failure. Another test omits search and calls `quote` with a real pair, which is allowed if the id exists: search is how the agent discovers ids, not a permission check. Do not confuse the two. Write that down so the citation rule stays about text, not about a ritual of having searched first.

## Components

| Piece | Role |
| --- | --- |
| Notes index | Local markdown chunked and scored with BM25. |
| Search tool | Returns ids and texts. |
| Quote tool | Exact substring check against the indexed chunk. |
| Terminal states | Quoted or abstained, with no free-text finish path. |

## How it works

1. Index four short notes, one of which contains a fee sentence.
2. Run the answerable question and assert the quote tool succeeded.
3. Run the unanswerable question and assert abstention and zero successful quotes.
4. Reject a `finish` tool name.
5. Fail a one-word-off quote in a unit test.

## Tech stack

- Python 3.11 or newer
- BM25 over local markdown
- Scripted policy, model optional and off in tests

## Setup

1. Create `notes-researcher/` with `notes/`, `index.py`, `loop.py`, and tests.
2. Run both questions.
3. Run tests.
4. Write `notes.md` explaining that search is discovery and quote is the check.

## What done looks like

- The answerable run ends `quoted` with a substring of a real chunk.
- The unanswerable run ends `abstained` with no successful quote.
- A free-text finish tool is rejected.
- A one-word-off quote fails.

## Step ahead

A quote can be exact and still be the wrong edition if notes from two years share a sentence frame. Add an `edition` field on each note and a required `edition` argument on `quote` that must match the chunk. Fixture two notes with the same sentence and different editions, and show that quoting the 2024 sentence while asking for 2026 fails. The follow-on keeps the substring check and adds a second predicate the tool enforces, rather than hoping the policy prefers the right file.
