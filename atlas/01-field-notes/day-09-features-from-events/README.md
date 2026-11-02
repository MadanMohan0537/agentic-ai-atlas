# Features from Events Without Peeking

**Day 09** · **Beginner** · Phase 01: Field Notes: Data & Measurement

Build a rider feature table where every aggregate uses only events at or before a cutoff.

## Concept

A model that predicts whether a rider will complete a ride next week is worthless if the features include next week's rides. The leak is usually boring: a "lifetime ride count" computed on the full table, then attached to a row that sits in the middle of that lifetime. This project builds a feature table for Harbor Loop riders. Each row is a rider at a decision cutoff. Features are counts and recency computed only from events at or before that cutoff. The label, if you attach one, uses only events after the cutoff. You will try to cheat on purpose — include a future ride in the count — and show a test that catches it. This is the small version of a point-in-time join. A later pipeline day goes further. Today the table fits in memory and the cutoff is a column you can point to.

## Approach

Events are `rider_id`, `event_time`, `event_type`. Decision rows are `rider_id`, `cutoff`. Sort events and, for each decision, scan events for that rider with `event_time <= cutoff`. Compute `rides_so_far`, `days_since_last_ride`, and `cancels_so_far`. If there is no prior ride, recency is null, not zero. Zero would claim a ride happened today. Attach a label `completed_within_7d` from events in `(cutoff, cutoff + 7 days]`. Write the honest table and a broken table that uses `<= cutoff + 7 days` for the ride count. The test asserts the broken count is greater for at least one rider and the honest function never reads an event after the cutoff.

## Components

| Piece | Role |
| --- | --- |
| Event log | Append-only rider events with timestamps. |
| Decision list | Rider and cutoff pairs, including a rider with no history. |
| Honest aggregator | Features from events at or before the cutoff only. |
| Leak detector | A deliberately wrong aggregator and a test that separates the two. |

## How it works

1. Write a small event log covering three riders and two weeks.
2. Define two cutoffs per rider so the second cutoff can see more history than the first.
3. Compute honest features. Check by hand the first rider's `rides_so_far` at the earlier cutoff.
4. Compute labels strictly after the cutoff.
5. Compute the broken feature and assert it differs from the honest one on the planted future ride.
6. Assert a rider with no prior events has null recency.

## Tech stack

- Python 3.11 or newer
- Standard library `datetime` and `csv`
- No feature-store product and no training yet

## Setup

1. Create `features-from-events/` with `events.csv`, `decisions.csv`, `features.py`, and tests.
2. Run `python3 features.py --mode honest` and inspect `out/features.csv`.
3. Run the tests, including the leak contrast.
4. Add a comment at the cutoff comparison that states whether the cutoff instant itself is included. Pick included, and test an event exactly at the cutoff.

## What done looks like

- An event exactly at the cutoff is included in features and excluded from the label.
- Null recency is preserved for riders with no prior ride.
- The broken aggregator fails the contrast test.
- You can explain the decision grain: one row per rider per cutoff, not one row per rider forever.
