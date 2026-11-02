# Split Leakage Hunt

**Day 10** · **Beginner** · Phase 01: Field Notes: Data & Measurement

Find riders who landed in both train and test, and rebuild the split so a rider lives in only one side.

## Concept

Harbor Loop trains a small classifier later in this atlas. If you split rows at random, the same rider's Monday trip can train the model and their Tuesday trip can test it. Accuracy will look like learning. It is recognition of a person you already saw. This project hunts that leak. You will implement a bad row-wise split, report the set of rider ids that appear on both sides, and then implement a rider-wise split that makes the intersection empty. You will also check a second leak that groups do not fix by themselves: sorting by time, training on the future, and testing on the past. The artifact is a split report with three numbers: overlap under the bad split, overlap under the rider split, and the earliest test time versus the latest train time under a time split. No model is trained today.

## Approach

Use the rental table at rental grain with `rider_id` and `event_time`. The bad split assigns each row to test with probability 0.3 using a seeded RNG. The good split hashes the rider id into buckets, or assigns whole riders after shuffling rider ids with a seed. Do not use Python's built-in `hash()`, which is salted per process. Use `hashlib` on the rider id so the split is stable. The time split sorts by `event_time` and cuts at 70 percent. Write `report.json` with the three overlap or order statistics. A test builds a tiny log where a row-wise split must overlap and the rider split must not.

## Components

| Piece | Role |
| --- | --- |
| Rental rows | Several rides per rider so a row split can leak. |
| Row split | The leaky baseline, seeded. |
| Rider split | A stable whole-rider assignment. |
| Time split check | Compares the max train time to the min test time. |

## How it works

1. Load rentals and group row indexes by rider id.
2. Run the row split and compute the intersection of rider ids.
3. Run the rider split and assert the intersection is empty.
4. Run the time split and record whether every train time is strictly before every test time.
5. Write the report. If your fixture's row split happens to draw no overlap, add rides until it does, or construct the overlap explicitly in the test.

## Tech stack

- Python 3.11 or newer
- Standard library `hashlib` and `json`
- No scikit-learn split helper, so the grouping stays visible

## Setup

1. Create `split-leakage/` with `rides.csv`, `split.py`, and tests.
2. Include at least eight riders with three rides each.
3. Run `python3 split.py` and read `out/report.json`.
4. Run the unit tests. One test should fail if someone switches the rider split back to a row split.

## What done looks like

- The report shows a non-empty rider overlap for the row split on your fixture.
- The rider split overlap is empty and stable across two process runs.
- The time split's latest train instant is earlier than its earliest test instant.
- You can say which split you would use to estimate performance on a new rider, and why the time split answers a different question.
