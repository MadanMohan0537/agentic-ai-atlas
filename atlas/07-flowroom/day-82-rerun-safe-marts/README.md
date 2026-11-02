# Rerun-Safe Marts

**Day 82** · **Intermediate** · Phase 07: Flowroom: Analytics and Pipelines

Load raw events into staging and a mart in SQLite so running the job twice does not double the totals.

## Concept

A pipeline that inserts into a reporting table every time it runs will double last week's rentals the moment someone retries a failure. This project creates three layers in SQLite: `raw`, `staging`, and `mart_daily`. Raw is append-only and keyed by an event id. A second load of the same file inserts zero new raw rows. Staging is rebuilt from raw for the dates in the batch, deleting that date range inside the transaction and inserting again. The mart is rebuilt from staging for the same range. You will run the job twice and assert the daily totals match the first run. You will also add one new event and show only that day's total changing. The range delete is the whole trick. A job that only inserts cannot be retried.

## Approach

Use the standard library `sqlite3`. Wrap the rebuild in a transaction. The batch range is an argument, not `select min(date), max(date)` from the whole raw table, because that would rebuild history you did not intend to touch. A test loads a file, loads it again, and checks a count. A second test extends the range and checks that an untouched day still has the same total. Primary keys on event id make the raw insert use `INSERT OR IGNORE`. Document that ignore is acceptable for exact duplicate ids and wrong for two different payloads with the same id. A test sends a conflicting payload and expects a recorded conflict, not a silent ignore. You may handle that second case by comparing a hash before ignore.

## Components

| Piece | Role |
| --- | --- |
| Raw table | Append-only events with a primary key and a payload hash. |
| Staging rebuild | Delete-and-insert for a date range, inside a transaction. |
| Daily mart | Totals rebuilt from staging for the same range. |
| Conflict check | Same id with a different hash is reported, not ignored. |

## How it works

1. Create the three tables.
2. Load a file and record daily totals.
3. Load the same file and assert totals are unchanged and raw row count is unchanged.
4. Load a new event on one date and assert other dates are unchanged.
5. Attempt a conflicting payload and assert it is rejected and counted.

## Tech stack

- Python 3.11 or newer
- Standard library `sqlite3`
- SQL visible in the repository as strings or `.sql` files

## Setup

1. Create `marts/` with `pipeline.py`, `schema.sql`, and tests.
2. Run the pipeline twice.
3. Run tests.
4. Point the notes at the transaction that deletes the range.

## What done looks like

- A rerun does not change totals.
- A new event changes only its date.
- A conflicting duplicate id is not silently ignored.
- The batch date range is an explicit argument.
