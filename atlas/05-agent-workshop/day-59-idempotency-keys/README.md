# Idempotency Keys on Retried Tools

**Day 59** · **Advanced** · Phase 05: Agent Workshop

Retry a tool that appends a ledger row without appending it twice, using a key the caller supplies.

## Concept

The pure tools from earlier days can be repeated safely. A tool that appends a maintenance ticket cannot. This project adds one effectful tool, `create_ticket`, backed by an in-memory ledger. Each call carries an idempotency key chosen by the agent, not by the tool. The first call with a key appends a row and stores the result. A second call with the same key and the same body returns the stored result and does not append. A second call with the same key and a different body is an error `key-reused-with-different-body`, and the ledger stays as it was. Retries are how you survive a crash after the tool succeeded but before the observation was written. You will simulate that crash by invoking the tool, discarding the observation, and invoking it again. The ledger length must stay one.

## Approach

The ledger is a list and a dict from key to stored result. Body equality is JSON canonical form: sorted keys, no whitespace surprises. Do not use the key as a substitute for identity of the ticket only; store the body hash next to the key. A missing key is a schema error from Day 50's rules, and the tool does not run. This is not a permission system and not an approval chain. The only question is whether a retry duplicates a row. Include a test where two different keys with the same body create two tickets, because idempotency is not deduplication of intent. Write that distinction in `notes.md` so you do not collapse the two ideas later.

## Components

| Piece | Role |
| --- | --- |
| Ledger | Append-only ticket rows in memory. |
| Key store | Maps a key to a body hash and a result. |
| Retry simulation | Two calls, one discarded observation, one row. |
| Conflict error | Same key, different body, no new row. |

## How it works

1. Implement `create_ticket` with required `idempotency_key` and a body.
2. Call it twice with the same key and body. Assert one row.
3. Call it with the same key and a changed summary. Assert the error and an unchanged ledger.
4. Call it with two keys and the same body. Assert two rows.
5. Omit the key and assert the function body does not run.

## Tech stack

- Python 3.11 or newer
- Standard library `json`
- In-memory ledger, no database server

## Setup

1. Create `idempotency/` with `ledger.py` and tests.
2. Run the four cases as a script that prints ledger lengths.
3. Run tests.
4. Write the distinction between retry identity and content dedupe in `notes.md`.

## What done looks like

- A retry with the same key and body does not append a second row.
- The same key with a different body errors and does not append.
- Two keys create two rows even if the bodies match.
- A missing key never reaches the ledger code, and a test covers it.

## Step ahead

The key store lives in the same process as the crash you simulated, so a real crash would forget the key and the retry would duplicate the ticket. Persist the key store to a file before you append the ledger row, and persist the row after. Fixture a crash between the two writes by stopping after the key file is written and before the ledger append, then resume. The follow-on behavior is: resume sees the key with status `pending`, completes the single append, and a later retry returns that row. If resume appends twice, the order of the two writes is wrong.
