# Grain, Joins, and Double-Counted Revenue

**Day 03** · **Beginner** · Phase 01: Field Notes: Data & Measurement

Show how a plausible join inflates revenue, then publish a grain checklist that would have stopped it.

## Concept

Harbor Loop's finance extract has one row per rental. The maintenance extract has many rows per bike, because a bike is serviced several times a month. Join them on `bike_id` and sum `fare_cents` and you will report a fantasy. The number is large, the SQL looks ordinary, and a dashboard will happily chart it. This project builds two tiny tables and the wrong join on purpose, then the right one. You will write a grain checklist that names, for each table, what one row represents and which columns are allowed to be summed. The lesson is not "joins are hard." The lesson is that a metric without a grain is a claim you cannot audit. You will also show a safe pattern: aggregate the many-side to the join key first, then join, then sum.

## Approach

Use sqlite3 in the standard library so the SQL is real and the data is a file you can reopen. Create `rentals` with unique `rental_id` and `service_events` with several rows per `bike_id`. Compute three numbers side by side: the true fare sum, the inflated sum after a direct join, and the sum after pre-aggregation. They must not match by accident; pick fares so the inflation factor is obvious, such as exactly 3x on bikes with three service events. Write the checklist as `GRAIN.md` next to the SQL. Include a question the checklist forces: "If I sum this column after this join, am I still summing one row per rental?"

## Components

| Piece | Role |
| --- | --- |
| SQLite schema | Rentals at rental grain and service events at event grain. |
| Inflated query | The join a hurried analysis would ship. |
| Safe query | Aggregate service events to `bike_id` before joining. |
| Grain checklist | One row's meaning, primary key, and which measures are summable. |

## How it works

1. Create the database in `build_db.py` with a fixed seed so the sums are stable.
2. Run the true fare total from `rentals` alone and store it as the reference.
3. Run the naive join and record the inflated total.
4. Pre-aggregate service events to one row per bike, join, and show the fare total returning to the reference.
5. Write `GRAIN.md` using the actual table names and keys from the schema.
6. Test that inflated > reference and safe == reference.

## Tech stack

- Python 3.11 or newer
- Standard library `sqlite3`
- SQL you can paste into any SQLite shell

## Setup

1. Create `grain-lab/` and add `build_db.py`, `queries.sql`, and `tests/test_sums.py`.
2. Insert about 20 rentals and 30 service events. Give three bikes multiple service rows.
3. Run `python3 build_db.py` then `python3 -m unittest discover -s tests -v`.
4. Open the database with `sqlite3 harbor.db` and run the three fare queries yourself.

## What done looks like

- The test names all three totals and fails if the safe query drifts from the reference.
- `GRAIN.md` states the primary key of each table in a single line.
- You can point to the exact join that multiplies fare rows.
- A sum of service cost, which does live at event grain, is still correct after the safe pattern. Add that assert too.
