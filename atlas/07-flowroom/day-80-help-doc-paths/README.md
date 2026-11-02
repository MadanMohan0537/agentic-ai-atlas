# Paths Through the Help Docs

**Day 80** · **Intermediate** · Phase 07: Flowroom: Analytics and Pipelines

Count which help-doc sequences precede a resolved event, and ignore paths that never resolve.

## Concept

Pageview counts flatter articles that people open and abandon. Harbor Loop's help center emits doc views and a `resolved` event when the rider marks the issue done. This project builds paths: ordered doc ids inside a session, ending at the first resolved, or ending unfinished if the session never resolves. You will report the top resolved paths and, separately, the top unfinished paths. A doc that appears in both is not "successful" just because it is popular. You will also refuse to count a path that skips across sessions. The fixture includes one doc that is common in unfinished paths and rare in resolved ones, and the report must not rank it as a success. This is path analysis, not a feature-adoption dashboard and not a model of whether the doc caused the resolution.

## Approach

Start from the session ids you know how to build, or from a fixture that already has session ids so this day stays about paths. Collapse consecutive duplicate doc views. End a path at the first `resolved` inside the session. Docs after resolved are ignored and counted in a `tail` tally so you notice a tagging bug if the tail is large. Rank paths by resolved count with a minimum support of two so a unique path does not become a recommendation. Unfinished paths have their own table and are not used as the denominator of a success rate unless you also print the denominator. Write both tables.

## Components

| Piece | Role |
| --- | --- |
| Session events | Doc views and resolved markers. |
| Path cutter | Stops at the first resolved event. |
| Resolved ranking | Paths with support at least two. |
| Unfinished ranking | A separate table, including the planted dead-end doc. |

## How it works

1. Write a fixture with a dead-end doc and a short path that resolves.
2. Build paths per session.
3. Assert events after resolved do not extend the path.
4. Rank both tables.
5. Assert the dead-end doc is absent from the resolved ranking and present in the unfinished ranking.

## Tech stack

- Python 3.11 or newer
- CSV fixtures
- No visualization library required

## Setup

1. Create `paths/` with `events.csv`, `paths.py`, and tests.
2. Run the report and write `out/resolved.csv` and `out/unfinished.csv`.
3. Run tests.
4. State in the notes that the tables are descriptive, not causal.

## What done looks like

- Resolved and unfinished paths are different files.
- The dead-end doc is not listed as a resolved success.
- Events after the first resolved marker do not change the path, and the tail count is reported.
- A path cannot contain events from two session ids, and a test mixes them to prove the cut.
