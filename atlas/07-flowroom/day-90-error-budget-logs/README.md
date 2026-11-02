# Logs and an Error Budget

**Day 90** · **Advanced** · Phase 07: Flowroom: Analytics and Pipelines

Parse structured logs into typed events and compute an error budget for a single route.

## Concept

Free-text logs do not become a reliability number by being searched. This project defines a log line schema: timestamp, level, route, status, and request id. A parser accepts lines that match and sends the rest to `rejected.log` with a reason. You will compute, for one route, the fraction of requests with status 500 over a day, and compare it to a budget of one percent. A day over budget is a row in `budget_breach.csv`. A day with too few requests, under a minimum you set, is `insufficient`, not a breach and not a success. You will fixture both a breach and a quiet day. This is a log mart for one service. It is not a tracing product and it does not join spans across services yet.

## Approach

Write the parser so a line with an extra field is rejected rather than partially used, or accept extra fields and document which. Pick one. A missing status is a reject. Counts group by route and date. The budget comparison runs only when the request count is at least the minimum. Use integers and a ratio you compute from counts, and store the counts in the output so a reader can recompute the ratio. A test with 1 failure out of 10 requests is a breach if the minimum is 10 and the budget is one percent... that would be 10 percent, which breaches. Also test 0 failures out of 5 as insufficient when the minimum is 10.

## Components

| Piece | Role |
| --- | --- |
| Line parser | Typed fields and a reject file. |
| Route-day counts | Requests and errors from accepted lines only. |
| Minimum sample | Days below it are insufficient. |
| Breach file | Days over the error budget, with counts. |

## How it works

1. Parse a fixture containing one bad line and several good lines.
2. Assert the bad line is in the reject file and not in the counts.
3. Compute two days: one breach and one insufficient sample.
4. Assert the quiet small day is not a breach.
5. Recompute the ratio from the stored counts in a test.

## Tech stack

- Python 3.11 or newer
- Plain text logs and CSV outputs
- No log vendor SDK

## Setup

1. Create `error-budget/` with `app.log`, `parse.py`, and tests.
2. Run the parser and the budget step.
3. Run tests.
4. Write the budget and the minimum sample at the top of the report.

## What done looks like

- Malformed lines are excluded from the ratio.
- A small sample is `insufficient`, not healthy and not a breach.
- A breach row contains the counts needed to recompute the ratio.
- The route filter is explicit, and another route's errors do not enter the ratio.

## Step ahead

A request that fails and is retried under a new request id inflates the error rate. Add an optional `root_request_id` field. When it is present, count unique root ids rather than lines. Fixture three lines that share a root id, two of them errors, and show the line-based rate and the root-based rate side by side. The follow-on does not delete the line-based rate. It shows how a retry policy changes the budget math, and days without root ids keep the line-based definition.
