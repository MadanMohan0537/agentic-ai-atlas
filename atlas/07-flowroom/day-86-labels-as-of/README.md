# Labels Joined as Of

**Day 86** · **Intermediate** · Phase 07: Flowroom: Analytics and Pipelines

Attach a training label to a feature row using only events inside a window that starts after the cutoff.

## Concept

Day 9 built features that do not peek. This project is the join you would actually schedule. Each decision row has a rider and a cutoff. Features are aggregates of events at or before the cutoff. The label is 1 if any `overrun` event occurs in `(cutoff, cutoff + 7 days]`. The SQL or the Python join must not use a label window that overlaps the feature window. You will write the query, explain the inequality, and plant one overrun exactly at the cutoff and one a second after. The first is a feature event, not a positive label. The second is a positive label and not a feature. A sloppy `<=` on both sides double-counts that second. A sloppy pair of `<=` on the cutoff double-counts the first. Tests cover both edges.

## Approach

Prefer SQLite so the predicate is visible in one query with two joins or two subqueries. Name the predicates in comments. The output table contains `rider_id`, `cutoff`, feature columns, and `label`. A rider with no events before the cutoff still gets a row if they are in the decision list, with null features, and can still have a positive label. Dropping them biases the set toward riders you already know. Assert a decision row with only a future overrun survives with null `rides_so_far` and label 1.

## Components

| Piece | Role |
| --- | --- |
| Decision list | Rider and cutoff pairs, including a rider with no history. |
| Feature predicate | Events at or before the cutoff. |
| Label predicate | Events strictly after the cutoff and at or before cutoff plus seven days. |
| Edge fixtures | An event exactly at the cutoff and an event one second later. |

## How it works

1. Load events and decisions into SQLite.
2. Run the feature query and the label query as two named SQL strings.
3. Join them on rider and cutoff.
4. Assert the two edge events land in different columns.
5. Assert the history-free rider remains in the output.

## Tech stack

- Python 3.11 or newer
- SQLite
- SQL files you can read without running Python

## Setup

1. Create `as-of-labels/` with `label.sql`, `features.sql`, `join.py`, and tests.
2. Run the join and inspect `out/training_rows.csv`.
3. Run tests.
4. Add a one-line comment on each inequality.

## What done looks like

- The event at the cutoff affects features and not the label.
- The event one second later affects the label and not the features.
- A decision row with no history is kept.
- The SQL files contain the predicates the tests are about.
