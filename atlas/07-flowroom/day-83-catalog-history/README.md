# Catalog History

**Day 83** · **Intermediate** · Phase 07: Flowroom: Analytics and Pipelines

Store fee-code changes as dated rows so a question about last March does not see today's price.

## Concept

A fee table with one row per code shows the price now. A support question about a rental in March needs the price that was in force in March. This project implements a small slowly changing dimension. Each fee code has rows with `valid_from` and `valid_to`. The current row has a null `valid_to`. When the price changes, you close the open row by setting `valid_to` to the change time and insert a new open row. You never update the price in place. A query function `fee_as_of(code, when)` returns the row whose interval contains `when`. You will change a fee twice and show three answers: before the first change, between the changes, and after the second. A test queries exactly at a boundary and documents whether `valid_from` is inclusive. Pick inclusive start and exclusive end, and test both sides of the boundary.

## Approach

Do this in SQLite or in plain data structures backed by a CSV you can diff. The close-and-insert operation is one function. It rejects a change that would open a second current row. It rejects a `valid_from` earlier than the current row's `valid_from`. Historical rows are immutable: a test that tries to update an old price in SQL should not be part of the API. If you are tempted to add an update method, make it raise. Querying a time before the first row returns `unknown`, not the earliest price.

## Components

| Piece | Role |
| --- | --- |
| Interval rows | `valid_from` inclusive, `valid_to` exclusive, one open row. |
| Change function | Closes the open row and inserts the new price. |
| As-of query | Returns the row containing a timestamp. |
| Boundary tests | Both sides of a change instant. |

## How it works

1. Insert an initial fee.
2. Change it twice at known timestamps.
3. Query three times and lock the three prices.
4. Query exactly at `valid_to` of the first row and expect the second price.
5. Attempt a retroactive edit and expect a rejection.

## Tech stack

- Python 3.11 or newer
- SQLite or CSV with a tiny query function
- Aware timestamps

## Setup

1. Create `catalog-history/` with `fees.py` and tests.
2. Run the two changes and print the three as-of answers.
3. Run tests.
4. Write the inclusivity rule in one line at the top of `fees.py`.

## What done looks like

- Three as-of queries return three prices.
- The boundary instant follows the inclusive-start exclusive-end rule.
- A second open row cannot be inserted for the same code.
- Times before the first version return `unknown`.
