# The Wrong Manual Version

**Day 42** · **Intermediate** · Phase 04: Retrieval Studio

Bind a question to a handbook edition from the conversation, and block a newer chunk the user did not ask for.

## Concept

Filters are useless if the caller forgets them. A support agent asks about "the fee" while the case file says the rider's membership started under the 2024 handbook. The 2026 fee is more prominent in the index because you rewrote that page last. This project models a small case context: `edition` is a field on the case, not a guess from the question text. Retrieval receives the case and must set the filter from it. You will try to regress: a code path that ignores the case and searches all editions. A test calls that path's function, if you are tempted to keep it, and asserts it is not what `answer_case` uses. The user-visible answer cites the edition. An answer that is numerically right for the wrong year is a wrong answer.

## Approach

Represent a case as JSON with `case_id`, `edition`, and `question`. `answer_case` reads the edition only from the case. It does not parse years out of the question. Include a fixture where the question says "2026" but the case edition is 2024, and assert the filter follows the case. That fixture is the whole lesson: the utterance is not the system of record. Cite `edition` in the output next to the chunk id. Log the filter that was applied so a later review can see it without reading code.

## Components

| Piece | Role |
| --- | --- |
| Case file | Edition as a field, separate from the question text. |
| Bound retriever | Filter comes from the case inside `answer_case`. |
| Hostile fixture | Question mentions a different year than the case. |
| Citation | Chunk id plus the edition that was actually searched. |

## How it works

1. Write three cases, including the hostile year mismatch.
2. Implement `answer_case` and log the filter.
3. Assert the hostile case searches 2024.
4. Add a regression test that a helper named `search_all` is not called by `answer_case`. If you have no such helper, assert the candidate editions are a single value.
5. Write the three answers with their cited editions.

## Tech stack

- Python 3.11 or newer
- The filtered index
- JSON case files

## Setup

1. Create `edition-binding/` with `cases.jsonl` and `answer_case.py`.
2. Run the three cases.
3. Run tests.
4. In the notes, state which object is the system of record for edition.

## What done looks like

- The hostile case cites 2024 and does not cite the 2026 fee chunk.
- The applied filter is in the log.
- A test locks the case field as the source of the filter.
- The notes name the system of record in one sentence.
