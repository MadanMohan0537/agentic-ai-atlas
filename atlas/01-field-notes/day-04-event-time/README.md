# Event Time, Time Zones, and Late Arrivals

**Day 04** · **Beginner** · Phase 01: Field Notes: Data & Measurement

Bucket rentals by event time in one zone, and show a late event landing in yesterday's bucket.

## Concept

A rental has three clocks: when the ride happened (`event_time`), when the dock emitted the record (`ingest_time`), and the zone those strings were written in. Harbor Loop's docks write local time without an offset. The warehouse job runs in UTC. A ride at 23:30 local can look like "tomorrow" or "yesterday" depending on which clock you truncate. Late arrivals make it worse: Monday's job closes Sunday, then a Sunday ride appears on Tuesday. This project picks one definition — local event time in `America/New_York`, converted to UTC for storage, bucketed by the local calendar date — and writes a test where a late event moves a closed day's count. You are practicing time literacy, not building a stream processor. The artifact is a small function and three fixtures that would have started an argument in a real standup.

## Approach

Store every instant as timezone-aware UTC in the data model. Parse naive local strings with an explicit zone using the standard library `zoneinfo`. Never truncate a UTC timestamp and call it a local day. Implement `local_day(event_time_utc) -> date` and `apply_arrival(daily_counts, event, arrived_at, closed_through)`. If the event's local day is already closed, record it as a late adjustment rather than silently rewriting history. Use a winter date and a summer date so a daylight-saving transition is at least one fixture, even if you only assert the offset you expect.

## Components

| Piece | Role |
| --- | --- |
| Clock model | Aware UTC instants plus the named local zone. |
| Day bucketer | Converts event time to a local calendar date. |
| Late-arrival rule | Closed days receive an adjustment record, not a quiet rewrite. |
| Fixtures | Evening boundary, DST date, and an event that arrives after close. |

## How it works

1. Parse a naive local string and attach `America/New_York`.
2. Convert to UTC and store both the UTC instant and the source zone name.
3. Bucket by converting back to local and taking the date. Assert 23:30 local stays on that local date.
4. Close a day, then apply an event whose local day is already closed.
5. Check that the closed total is unchanged and an adjustment row exists with the rental id.

## Tech stack

- Python 3.11 or newer
- Standard library `datetime` and `zoneinfo`
- No pandas offsets and no third-party timezone library

## Setup

1. Create `event-time/` with `clocks.py` and `tests/test_clocks.py`.
2. Hard-code three events in the test file so the cases stay visible.
3. Run `python3 -m unittest discover -s tests -v`.
4. Add a one-line comment above the bucketer naming the zone. If the zone is missing, the function should raise rather than assume UTC.

## What done looks like

- A 23:30 America/New_York event buckets to that local date in both January and July.
- Naive timestamps are rejected, or accepted only through a function that requires a zone argument.
- A late event for a closed day produces an adjustment and does not change the closed total.
- You can explain, without notes, which clock a rides-per-day chart is using.
