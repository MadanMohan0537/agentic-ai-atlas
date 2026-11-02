# Tumbling Windows on a File

**Day 84** · **Intermediate** · Phase 07: Flowroom: Analytics and Pipelines

Aggregate an event file into fixed five-minute windows and put late events in a side bucket.

## Concept

Streaming systems tumble, and so can a file if you are explicit about watermarks. This project reads dock events ordered by ingest time and assigns each event to a five-minute window on event time. A window closes when you have seen an ingest time more than ten minutes past the window end. Events for a closed window do not update the aggregate. They go to a late bucket with a count. You will fixture an event that arrives in order and one that arrives after its window has closed. The closed aggregate must stay fixed. This is not a distributed stream processor. It is the watermark rule, which is the part people skip when they copy a diagram.

## Approach

Windows are aligned to epoch minutes so two runs agree. The watermark is the max ingest time seen so far minus the allowed lateness. An event is late when its window end is less than or equal to the watermark at the time it is processed. Processing order is ingest order, which the fixture should not make identical to event order. Print the open aggregates and the late count. A test processes a late event and asserts the window sum is unchanged and the late count increased by one. A second test puts an event inside the lateness allowance and asserts the sum increased.

## Components

| Piece | Role |
| --- | --- |
| Aligned windows | Five-minute buckets with a defined origin. |
| Watermark | Max ingest time minus allowed lateness. |
| Aggregate | A count or a sum per window that freezes when the window closes. |
| Late bucket | Events that missed the watermark, counted and stored. |

## How it works

1. Write events whose ingest order differs from event order.
2. Process them one by one, updating the watermark.
3. Close a window and then deliver a late event.
4. Assert the frozen sum and the late count.
5. Assert an event inside the allowance still updates the sum.

## Tech stack

- Python 3.11 or newer
- Standard library only
- A fixture file, not a broker

## Setup

1. Create `windows/` with `events.csv`, `tumble.py`, and tests.
2. Run the processor and write `out/windows.csv` and `out/late.csv`.
3. Run tests.
4. Document the window size and the lateness in one place.

## What done looks like

- Late events do not change a closed window.
- Events inside the lateness allowance do change the open window.
- Window bounds are deterministic across two runs.
- The late file contains the late event id.
