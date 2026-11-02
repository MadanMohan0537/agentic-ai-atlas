# Bootstrap a Rate by Hand

**Day 07** · **Beginner** · Phase 01: Field Notes: Data & Measurement

Estimate a completion rate and a percentile interval with a seeded resample you can recompute.

## Concept

Harbor Loop completed 18 rides out of 40 attempts on a rainy pilot dock. Reporting "45 percent" as if it were exact will over-commit the next staffing decision. This project estimates a completion rate and a simple uncertainty interval by resampling the 40 attempts with a fixed seed. You will implement the bootstrap yourself: draw with replacement, compute the mean, repeat, and read off percentiles. The goal is not a statistics library demo. The goal is to see that a different seed moves the interval slightly and a larger sample shrinks it. You will also write the sentence you are willing to say out loud, including what the interval is not: it does not fix a biased sample, and it does not know about next week's weather.

## Approach

Represent each attempt as 1 or 0. Use `random.Random(seed)` so the resample is reproducible. Implement `bootstrap_mean(xs, rounds, seed) -> list[float]` and `percentile(sorted_stats, p)`. Use 2000 rounds. Report the 2.5th and 97.5th percentiles as the interval. Add a second fixture with 400 attempts at the same underlying rate, generated from a seeded Bernoulli, and show the interval is narrower. Do not import scipy. Document the sentence in `finding.md` next to the numbers your program printed.

## Components

| Piece | Role |
| --- | --- |
| Attempt vector | Forty binary outcomes you can inspect. |
| Seeded resampler | Draws with replacement from a private `random.Random`. |
| Percentile reader | Reads the interval off the sorted bootstrap means. |
| Finding note | One sentence a stakeholder could hear, plus one limitation. |

## How it works

1. Hard-code or generate the 40 outcomes and compute the point estimate.
2. Resample 2000 times with seed 7 and store the means.
3. Sort and read the 2.5 and 97.5 percentiles.
4. Repeat with seed 8 and assert the point estimate is unchanged while the interval endpoints may move.
5. Build a larger seeded sample and assert its interval width is smaller than the n=40 width.
6. Write `finding.md` using the printed numbers.

## Tech stack

- Python 3.11 or newer
- Standard library `random` and `statistics`
- No scipy and no statsmodels

## Setup

1. Create `bootstrap-rate/` with `bootstrap.py` and `tests/test_bootstrap.py`.
2. Run the script and paste the interval into `finding.md`.
3. Run the tests. Include a test that a constant vector of ones yields an interval of exactly 1.
4. Keep the round count at 2000 so the test runtime stays trivial.

## What done looks like

- The same seed reproduces the same interval endpoints bit for bit on this machine.
- A constant vector produces a zero-width interval at that constant.
- The n=400 interval is narrower than the n=40 interval in the test.
- `finding.md` states a limitation that resampling does not cure.
