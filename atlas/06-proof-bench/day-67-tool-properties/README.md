# Properties of a Tool

**Day 67** · **Advanced** · Phase 06: Proof Bench: Evals and Harnesses

Generate random valid and invalid arguments for a tool and shrink the smallest failing case.

## Concept

Example calls hide the argument combination that breaks a tool. This project writes property tests for `add_minutes` and for `create_ticket`'s pure validation logic. A property is a statement: for any start minute in range and any duration in range, the end minute equals the start plus the duration modulo a day, and a second call with the same inputs returns the same result. Invalid durations outside the schema bounds never reach the function. You will generate random inputs with a seeded generator, and when a property fails you will shrink the input toward a smaller one that still fails. Shrinking is the part example tests do not do. You will plant one bug, such as an off-by-one at midnight, watch the shrinker find a small case, fix the bug, and keep the shrunk case as a regression test.

## Approach

The generator draws integers and strings from explicit ranges. The shrinker for integers moves toward zero or toward the lower bound, halving the distance, and stops when the smaller candidate passes. For strings it deletes characters. The property runner prints the original failing input and the shrunk input. Use a fixed seed so the run that finds the midnight bug is reproducible. Do not pull in a property-testing framework. A few dozen lines are the point. The schema validator from the agent phase is the gate: inputs that fail the schema are counted as `rejected`, not as property failures.

## Components

| Piece | Role |
| --- | --- |
| Generators | Seeded draws for ints and strings inside declared ranges. |
| Properties | Pure statements about tool outputs. |
| Shrinker | Searches for a smaller input that still fails. |
| Regression case | The shrunk input, saved after the bug is fixed. |

## How it works

1. Implement generation and shrinking for integers.
2. Plant the midnight bug and run until a failure shrinks.
3. Save the shrunk case, fix the bug, and show the property passing.
4. Show that out-of-range durations are rejects, not failures.
5. Assert the shrinker does not return a larger input than it started with.

## Tech stack

- Python 3.11 or newer
- Standard library `random`
- Your tool functions under test

## Setup

1. Create `properties/` with `prop.py` and tests.
2. Run the planted bug once and save the transcript of the shrink.
3. Fix the bug and keep the regression case.
4. Run tests on the fixed code.

## What done looks like

- The notes show a failing input and a smaller shrunk input for the planted bug.
- The fixed tool passes the property at the saved seed.
- Schema rejects are counted apart from property failures.
- The shrinker unit test covers a known integer failure.

## Step ahead

Shrinking one argument ignores interactions. Add a shrinker for a pair of integers that tries reducing each coordinate, and fixture a bug that appears only when both the hour is 23 and the duration exceeds 60. Single-coordinate shrinking should be allowed to stop at a pair that still fails, and the notes should show the pair, not a misleading single value. The follow-on is a failure region that is not a corner of one axis.
