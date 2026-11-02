# Field Study: A Handbook Agent Under a Harness

**Day 100** · **Advanced** · Phase 08: Frontier Lab

Answer handbook questions with retrieval, a budget, and a cassette, and attach an evidence note to the run.

## Concept

The last project uses pieces you already built, on one handbook, without turning them into a platform. A scripted agent may search notes, quote a span, and stop. It has a tool budget of four. Search is served from a cassette recorded by a fake transport or by a local function treated as a cassette: the replay run performs no new indexing side effects beyond reading files. The output for each question is an evidence note: the queries, the chunk ids returned, the quote or the abstention, the budget remaining, and the cassette key. A question with no supporting span abstains inside the budget. A question that would need a fifth search stops partial and says which checklist item was left. You will run the set twice and show the evidence notes matching. That match is the close of the atlas: a result someone else can replay.

## Approach

Keep the agent scripted so the replay is exact. The evidence note is JSON, one object per question, written to `out/evidence.jsonl`. The second run compares hashes of that file to the first. A mismatch fails. Do not call a hosted model in the required path. If you add one later, record it as a third run that is allowed to differ, and do not overwrite the scripted evidence. The abstention and the partial budget stop must both appear in the question set, so the field study shows a limit and not only successes. The cassette miss path should be tested with one extra question you deliberately leave unrecorded, and that question's note says `cassette-miss` rather than inventing a chunk.

## Components

| Piece | Role |
| --- | --- |
| Scripted handbook agent | Search and quote under a tool budget. |
| Cassette | Recorded search results keyed by query. |
| Evidence note | Queries, ids, quote or abstain, budget remaining, cassette key. |
| Replay check | A second run's evidence hash matches the first. |

## How it works

1. Record cassettes for the answerable questions and the abstention question.
2. Run the agent and write evidence notes.
3. Include one question that exhausts the budget and one unrecorded query.
4. Run again and compare hashes.
5. Assert the unrecorded query does not produce a quote.

## Tech stack

- Python 3.11 or newer
- Your notes index, quote check, budget, and cassette
- JSONL evidence

## Setup

1. Create `field-study/` with `agent.py`, `cassettes/`, `questions.jsonl`, and tests.
2. Run record, then two replays.
3. Run tests for abstain, budget stop, cassette miss, and hash match.
4. Read one evidence note from top to bottom and confirm every id is in the cassette or explained by a miss.

## What done looks like

- Two scripted runs produce the same evidence hash.
- At least one question abstains and one stops on the budget.
- A cassette miss does not invent a chunk.
- Every successful quote is an exact substring of a retrieved chunk in the note.

## Step ahead

Swap the scripted quoter for a second scripted quoter that is wrong on one question, and show the evidence hash changing while the cassette file's hash stays the same. The follow-on is a diff that localizes the change to the answer, not to retrieval. Write the two hashes and the question id that moved. If you cannot tell which question moved without re-reading every note, add a per-question hash to the evidence file and repeat the swap. The atlas ends when a change points at the component that moved.
