# Row Contracts for a Messy Extract

**Day 01** · **Beginner** · Phase 01: Field Notes: Data & Measurement

Accept or reject each rental row with a reason code instead of silently coercing bad fields.

## Concept

A weekly extract looks finished until you sum it. Harbor Loop Bikes, a fictional municipal operator, sends `rentals.csv` with a blank header, a dollar sign inside a duration field, a rental id that appears twice, and a station code that is not on the official list. A notebook that only prints the shape will train on whatever survived coercion. This project builds a row contract. The grain is one row per rental id. A validator either accepts the row or writes a reason code, the source line number, and the raw text. The useful artifact is the rejection report, not a smoother chart. You should be able to tell an analyst which policy removed each row and how many rentals remain. Silent drops are the bug you are hunting. If a later day cannot explain its training set, it will be because this contract was skipped.

## Approach

Declare the contract in a Python dictionary: required columns, python types, numeric ranges, and the set of allowed station codes. Read with the `csv` module so nothing is coerced for you. Run checks in a fixed order — structure, then type, then domain, then uniqueness — and keep the first failing reason so the counts stay interpretable. Generate the fixture yourself, with a known count of each fault, and assert those counts in a test. Write `rentals_clean.csv` and `rejects.csv`. Do not "fix" bad values inside the loader. A repair is a separate decision and belongs in the rejection note, not in an invisible fillna.

## Components

| Piece | Role |
| --- | --- |
| Fixture writer | Creates a 40-row CSV with a counted set of planted faults. |
| Contract spec | Required fields, types, ranges, and the station allow-list. |
| Validator | Pure function from a raw row to accept or a single reason code. |
| Rejection report | Counts by reason plus three example line numbers each. |

## How it works

1. Write the fixture so every fault is intentional and the expected reject counts are known.
2. Parse with `csv.DictReader`. If the field count disagrees with the header, reject the line as `bad-structure` before type checks.
3. Coerce only after a successful type check. A `$` in a numeric field is `bad-type`, not a number you strip quietly.
4. Reject unknown station codes and out-of-range durations with their own reason codes.
5. Track rental ids you have already accepted. A duplicate fails even when every other field is valid.
6. Write the clean file and the reject file, then assert the reason histogram matches the fixture plan.

## Tech stack

- Python 3.11 or newer
- Standard library: `csv`, `pathlib`, `unittest`
- No third-party dataframe library on this day

## Setup

1. Create a folder `row-contracts/` and a virtual environment with `python3 -m venv .venv`, then activate it. You will not install packages.
2. Add `fixtures/build_rentals.py` that writes `fixtures/rentals.csv` and a sibling `expected_rejects.json` mapping reason codes to counts.
3. Add `contract.py` with the station allow-list (eight codes is enough) and `validate_row(row, seen_ids) -> str | None`.
4. Add `load.py` that reads the CSV, writes `out/rentals_clean.csv` and `out/rejects.csv`, and prints the histogram.
5. Add `tests/test_contract.py` and run `python3 -m unittest discover -s tests -v`.

## What done looks like

- Every planted fault appears under the reason code you named, with the right count.
- The clean file has unique rental ids, no currency symbols, and only allow-listed stations.
- A test fails if the loader skips a malformed line without recording a reason.
- You can state the grain in one sentence and point to the line of code that enforces it.
