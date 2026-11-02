# Precision Where It Matters

**Day 15** · **Beginner** · Phase 02: Learning Machines

Rank predictions and read precision and recall at the alert rate operations can actually handle.

## Concept

An overrun model that flags every other rental will be switched off by the dock crew in a week. The operating point is a workload decision: how many alerts can a shift review? Accuracy at 0.5 is unrelated to that question, especially at a 10 percent base rate. This project sorts the test set by predicted probability and walks down the list, computing precision and recall after each alert. You will mark the point where the alert count matches a budget you set, such as twenty alerts per hundred rentals, and you will report precision there. You will also draw the curve as a CSV of (recall, precision) so you can plot it anywhere. A second curve on the training set will look better. You will put them side by side and refuse to quote the training curve in the baseline card.

## Approach

Use the boosted model's probabilities if you have them, or the linear model's if you do not. The day is about the curve, not about refitting. Implement `precision_recall_curve(labels, scores)` by sorting scores descending and accumulating true positives. Add a synthetic tie: two rows with the same score must not change the curve depending on input order. Break ties by row id so the walk is deterministic. Choose the budget in `budget.txt` before you look at the test curve. If you choose it after, you are fitting the operating point to the test set. Write both the predeclared budget precision and, separately, the best precision anywhere on the curve, labeled as exploratory.

## Components

| Piece | Role |
| --- | --- |
| Ranked list | Test rows sorted by score with a deterministic tie break. |
| Curve table | Precision and recall after each additional alert. |
| Budget marker | A predeclared alert rate and the precision at that rate. |
| Train contrast | The same curve on train, stored so you do not quote it by mistake. |

## How it works

1. Write `budget.txt` with the alert rate and one sentence of operational reason.
2. Load labels and scores for test and for train.
3. Build both curves.
4. Read precision at the budget on the test curve.
5. Confirm a tie fixture produces the same curve under reversed input order.
6. Update the baseline card with the budgeted precision, not with accuracy.

## Tech stack

- Python 3.11 or newer
- Standard library `csv`
- Scores from your Day 12 or Day 14 model

## Setup

1. Create `pr-curve/` with `curve.py` and a small tied fixture in tests.
2. Run it on the real scores and write `out/test_curve.csv` and `out/train_curve.csv`.
3. Add the budgeted number to `baseline_card.md` or a local copy of it.
4. Run tests.

## What done looks like

- The budget was written down before the test precision was computed, and the file's timestamp or your notes say so. If you slipped, change the budget file's reason, not the number, and recompute honestly.
- Ties do not depend on input order in the test.
- Train and test curves are separate files.
- The number you would tell operations is precision at the budget, and the notes say the denominator.
