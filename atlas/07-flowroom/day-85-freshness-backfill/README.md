# Freshness and a Backfill

**Day 85** · **Intermediate** · Phase 07: Flowroom: Analytics and Pipelines

Mark a mart table stale when its newest event is too old, then backfill a date without touching the others.

## Concept

A dashboard that refreshes on open will still show Tuesday if the job has been failing since Tuesday. This project writes a freshness check for `mart_daily`: the maximum event date must be at least the as-of date minus one day. If it is older, the check fails with the observed maximum and the expected minimum. It does not fill the gap with zeros. You will then run a backfill for the missing date only, using the range rebuild from the mart day, and show the freshness check passing afterward. A backfill that rebuilds every historical day is a bug in this fixture, and a test counts how many dates were deleted. The allowed count is one.

## Approach

Freshness is a function of the mart and an as-of date, returning a record with `ok`, `observed_max`, and `expected_min`. The job log records which dates were rebuilt. The test runs a pipeline that skipped a date, expects `ok` false, runs the backfill command with that date, and expects `ok` true. It also expects the other dates' totals to be byte-identical, which you can check by storing a hash of the untouched rows before and after. Do not implement alerting to a chat system. Print the record. The product is the check and the narrow backfill.

## Components

| Piece | Role |
| --- | --- |
| Freshness function | Compares max event date to the as-of date. |
| Failure record | Observed max and expected min, no invented zeros. |
| Backfill command | Rebuilds one date range. |
| Untouched-row hash | Proves other dates did not change. |

## How it works

1. Load a mart with a missing latest date.
2. Run freshness and expect failure.
3. Backfill that date only.
4. Hash the other dates before and after and assert equality.
5. Run freshness again and expect success.

## Tech stack

- Python 3.11 or newer
- SQLite mart from the previous pipeline day, or a smaller stand-in
- JSON freshness record

## Setup

1. Create `freshness/` with `fresh.py` and tests.
2. Run the fail, the backfill, and the pass.
3. Run tests.
4. Write the expected lag, one day, as a named constant.

## What done looks like

- A stale mart fails the check and does not gain zero rows from the check itself.
- Backfill rebuilds one date.
- Hashes of untouched dates match.
- The success record still includes the observed max, not only a boolean.
