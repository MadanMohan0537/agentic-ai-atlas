# One Definition of Active

**Day 06** · **Beginner** · Phase 01: Field Notes: Data & Measurement

Write a metric dictionary entry for an active rider and compute it two ways that must agree.

## Concept

"Active riders" is where Harbor Loop's weekly review goes to argue. Marketing means anyone who opened the app. Operations means anyone who completed a ride. Finance means anyone who generated a fare. All three numbers are real, and none of them is "the" active count until you pick one and show the formula. This project writes a metric dictionary entry with a name, an owner, a grain, an inclusion rule, an exclusion rule, and a worked example. Then you implement that rule twice: once as a Python function over event rows, and once as SQL over the same rows in sqlite. The two implementations must return the same rider ids on a shared fixture. A second, deliberately different definition lives in the dictionary as a rejected alternative, so you can see the trap without shipping it.

## Approach

Choose the operations definition and make it sharp. An active rider in a week is a `rider_id` with at least one rental whose local event day falls in that week and whose status is `completed`. Cancelled rentals do not count. Riders with only an app-open event do not count. Put the week boundary in the dictionary using the local-day rule from Day 4, described in prose even if you simplify the fixture to dates. Implement `active_riders(events, week_start, week_end) -> set[str]` and the equivalent SQL. Test equality of the sets, not of the counts alone, so a swapped rider cannot hide.

## Components

| Piece | Role |
| --- | --- |
| Dictionary entry | Name, owner, grain, inclusion, exclusion, and a worked example. |
| Rejected alternative | The marketing definition, marked as not the metric. |
| Python implementation | Set of rider ids over in-memory events. |
| SQL implementation | The same rule in sqlite against the same rows. |

## How it works

1. Write `metrics/active_rider.md` before writing code. If the code is easier to write than the entry, the entry is still vague.
2. Load a fixture with completed rides, cancelled rides, and app opens.
3. Compute the Python set and the SQL set for one named week.
4. Assert the sets are equal and that a cancelled-only rider is absent.
5. Add a one-row change that flips a rental to completed and show the set gaining that rider.

## Tech stack

- Python 3.11 or newer
- Standard library `sqlite3`
- Markdown for the dictionary entry

## Setup

1. Create `metric-dictionary/` with `metrics/active_rider.md`, `active.py`, `active.sql`, and a test module.
2. Keep the fixture under 30 events so you can audit it by eye.
3. Run the tests. Then change the SQL on purpose so a cancelled ride counts, and watch the test fail.
4. Revert that change. The failed run is the demonstration, not the final state.

## What done looks like

- Python and SQL return the same set of rider ids on the fixture.
- The dictionary names an owner and a grain. The owner is a role, not the word everyone.
- The rejected marketing definition is present and is not what the code computes.
- A cancelled-only rider is excluded, and a test says so.
