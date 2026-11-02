# A Flake Budget

**Day 77** · **Advanced** · Phase 06: Proof Bench: Evals and Harnesses

Repeat a scripted eval many times, separate harness flake from decoder flake, and fail when the pass rate wanders too far.

## Concept

A pass rate from one run is a coin flip if the decoder is stochastic. This project runs the same case set N times under two adapters. The stable adapter returns a fixed JSON answer and must produce a pass rate of 1.0 or 0.0 on every repeat, with zero variance. The shaky adapter flips a seeded coin inside the answer and produces a pass rate you can recompute. The harness records every repeat's pass bit, the mean, and the range. A flake budget says the stable adapter's range must be zero, and the shaky adapter's range must stay inside a band you set after computing the expected binomial spread for the seed. You are not building a release gate for a product and you are not estimating a confidence interval for a launch. You are measuring whether your harness itself invents noise.

## Approach

N is 30 so the file stays small and the binomial expectation is easy to write down. The seed is fixed. The stable adapter ignores the seed's random draws. The shaky one uses `random.Random(seed)` and you document the expected number of passes. A bug that reads the system clock inside the stable path should fail the range check. Do not use the clock. The report has two sections, harness and decoder, and a test asserts the stable section's variance is zero. If you change N, update the expected shaky count in the same commit as the code.

## Components

| Piece | Role |
| --- | --- |
| Repeat runner | N runs, fixed seed, recorded bits. |
| Stable adapter | Deterministic answers. |
| Shaky adapter | Seeded coin flip inside the answer. |
| Budget | Zero range for the stable adapter, a named band for the shaky one. |

## How it works

1. Implement both adapters and the repeat runner.
2. Run N repeats and write `flake.json`.
3. Assert the stable range is zero.
4. Compute the shaky pass count from the seed by hand or with a one-line replica and assert it matches.
5. Document the budget in `budget.md` before quoting the shaky band.

## Tech stack

- Python 3.11 or newer
- Standard library `random`
- JSON report

## Setup

1. Create `flake/` with `adapters.py`, `repeat.py`, and tests.
2. Run both adapters.
3. Run tests.
4. Keep N at 30 in one constant.

## What done looks like

- The stable adapter's pass bits are identical across repeats.
- The shaky adapter's pass count matches the seeded expectation.
- The report separates harness variance from decoder variance.
- The budget file states the allowed shaky band and the value of N.

## Step ahead

Thirty repeats is arbitrary. Add a stopping rule that runs the shaky adapter until the running mean's Chebyshev bound, which you can compute from the observed variance without a statistics library, is inside a width you set, or until a max N of 200. Fixture a coin that is fair and show it stopping later than a coin that always passes. The follow-on is spending repeats where the bit actually moves, and the stable adapter must still stop at the minimum sample size because its variance is zero.
