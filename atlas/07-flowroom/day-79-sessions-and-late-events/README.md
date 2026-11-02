# Sessions and Late Events

**Day 79** · **Intermediate** · Phase 07: Flowroom: Analytics and Pipelines

Build rider sessions from an inactivity gap and show a late event that should extend a closed session.

## Concept

A session is a decision about a gap, not a column in the source. Harbor Loop's app emits `app_open`, `search`, and `rental_complete` with event time and ingest time. Two events from the same rider belong to the same session when the gap is under 30 minutes. A job that closes the day at midnight will miss a 23:50 event that arrives the next morning and should have extended the last session. This project builds sessions from a fixture, writes session ids, and then applies a late event. You will show two outputs: the premature close, and the rebuilt sessions after the late event is included. The late event must change a session end time rather than becoming a new one-event session. Rebuilding from the full log is allowed. Mutating a closed session in place without a rebuild record is not.

## Approach

Sort by rider and event time. Assign session ids with a counter that increments when the gap exceeds the threshold. The threshold is a constant. Late events are applied by concatenating them with the original log and recomputing, then writing a diff of session end times. A test plants a 20-minute-late completion after a search and expects the same session id. A test plants a 2-hour-late event and expects a new session. Use ingest time only to decide lateness relative to a close timestamp, not to order the session. Ordering uses event time. Write both clocks into the output so a reader can see which one you used.

## Components

| Piece | Role |
| --- | --- |
| Event fixture | Rider events with event time and ingest time. |
| Gap rule | A named inactivity threshold. |
| Session builder | Deterministic ids from the sorted log. |
| Late diff | End times before and after the late event is included. |

## How it works

1. Write a log with two riders and a known gap pattern.
2. Build sessions and lock the ids in a test.
3. Add a late in-gap event and recompute.
4. Assert the session count does not increase for that rider.
5. Add a late out-of-gap event and assert the session count increases.

## Tech stack

- Python 3.11 or newer
- Standard library `csv` and `datetime`
- No warehouse server

## Setup

1. Create `sessions/` with `events.csv`, `sessions.py`, and tests.
2. Run the builder twice, before and after the late file.
3. Run tests.
4. Record the threshold and the close timestamp in `notes.md`.

## What done looks like

- In-gap late events extend a session.
- Out-of-gap late events start a new session.
- Ordering uses event time, and a test swaps ingest order to prove it.
- The diff file shows the end-time change rather than overwriting silently.
