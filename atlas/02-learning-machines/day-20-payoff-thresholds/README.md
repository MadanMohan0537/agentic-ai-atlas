# A Threshold from a Payoff Table

**Day 20** · **Intermediate** · Phase 02: Learning Machines

Choose a classification threshold from costs you write down, then show how a different cost flips it.

## Concept

Day 15 fixed a workload budget. Some decisions are better framed as costs. Suppose an overrun that is not staffed costs Harbor Loop a voucher, and a false alert costs a few minutes of crew time. Those are not the same unit until you write them in one currency. This project builds a two-by-two payoff table, sweeps thresholds on the test scores, and picks the threshold that minimizes expected cost on the test set. Then it does the dangerous version: picking the threshold on the test set is itself a use of the test set. You will split the old test riders in half, pick the threshold on the first half, and report cost on the second half. The second number is the one that goes on the card. You will also change one cost, rerun, and show the chosen threshold moving or not moving. A threshold that ignores the payoff is a default you have not earned.

## Approach

Write costs in `payoff.json` as four numbers: true positive, false positive, true negative, false negative. Expected cost is the sum of count times cost, divided by the number of rows, so it stays comparable across folds. Sweep thresholds from the unique predicted scores rather than from a fixed grid, so you do not miss the points where the decision actually changes. Selection fold and report fold are rider-disjoint. Document that both folds were already used to train nothing; they are carved from the original test riders only. If your test set is too small to split, regenerate a larger one with the same rule and say so. Compare the payoff-chosen threshold to 0.5 on the report fold.

## Components

| Piece | Role |
| --- | --- |
| Payoff file | Four costs in one currency, with a sentence defining the currency. |
| Threshold sweep | One row per distinct score, with counts and expected cost. |
| Selection fold | Where the threshold is chosen. |
| Report fold | Where the cost is quoted. |

## How it works

1. Write `payoff.json` and the currency sentence before the sweep.
2. Carve the original test riders into selection and report.
3. Sweep on the selection fold and store the winning threshold.
4. Apply that threshold to the report fold and compute cost. Also compute cost at 0.5.
5. Edit one cost, repeat, and record whether the threshold changed.
6. Test the sweep on a four-row hand example whose best threshold you computed on paper.

## Tech stack

- Python 3.11 or newer
- Standard library `json`
- Scores from the locked model

## Setup

1. Create `payoff/` with `payoff.json`, `sweep.py`, and tests.
2. Run the sweep and write `out/threshold_card.md`.
3. Run the cost-edit as a second config, `payoff_alt.json`, not by overwriting the first result.
4. Run tests.

## What done looks like

- The quoted cost uses the report fold, and the selection fold is a different set of riders.
- Cost at the chosen threshold and cost at 0.5 are both on the card.
- The alternate payoff is a separate file, and the note says whether the threshold moved.
- The hand example in the test matches your paper calculation.
