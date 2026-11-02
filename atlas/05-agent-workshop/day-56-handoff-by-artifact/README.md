# Handoff by Artifact

**Day 56** · **Intermediate** · Phase 05: Agent Workshop

Pass work from a researcher role to a writer role only as a file with required fields, never as a shared transcript.

## Concept

Two roles that share a chat will each assume the other noticed the fee code. This project forbids the shared transcript. The researcher reads the handbook chunks and writes `handoff.json` with required fields: `question`, `quotes` (each an exact substring plus chunk id), and `open_questions`. The writer may read only that file. It produces an answer that quotes only from `quotes`, or it returns `incomplete` if `open_questions` is non-empty. You will run one task where the researcher fills a real quote and an empty open-question list, and one where it sets an open question and leaves quotes empty. The writer must not "helpfully" answer the second task from the handbook, because the writer is not given the handbook path. A test that points the writer at the handbook folder should fail code review in the sense that your writer function's signature does not accept a handbook path.

## Approach

Define the handoff schema and validate it before the writer runs. Extra fields are rejected so the researcher cannot smuggle a draft answer the writer will paste. The writer function signature is `write_answer(handoff: dict) -> dict`. Tests pass a handoff whose quote does not contain a number the researcher hoped to sneak into an extra field. Assert the extra field is rejected at validation, before the writer. For the successful task, assert the answer text contains the quote and the chunk id. For the incomplete task, assert the status is `incomplete` and the answer text is empty.

## Components

| Piece | Role |
| --- | --- |
| Handoff schema | Question, quotes, and open questions. Extra fields rejected. |
| Researcher | A scripted function that fills the handoff from fixture chunks. |
| Writer | Reads only the handoff object. |
| Incomplete path | Non-empty open questions block the answer. |

## How it works

1. Implement validation, including rejection of unknown fields.
2. Run the researcher on a fixture question and write `handoff.json`.
3. Run the writer on that file.
4. Run the open-question fixture and assert `incomplete`.
5. Assert the writer source does not take a handbook directory argument. A small test can inspect the signature with `inspect`.

## Tech stack

- Python 3.11 or newer
- JSON handoff file
- Standard library `inspect` for the signature test

## Setup

1. Create `handoff/` with `schema.py`, `roles.py`, and tests.
2. Run both fixtures.
3. Run tests.
4. Open `handoff.json` and confirm every quote is a substring of the fixture chunk you point at in the test.

## What done looks like

- Unknown handoff fields fail validation.
- The writer signature accepts the handoff and nothing else.
- A non-empty open-question list yields an empty answer and status `incomplete`.
- The successful answer cites a chunk id that is inside the handoff.
