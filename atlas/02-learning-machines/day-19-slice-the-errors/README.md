# Slice the Errors

**Day 19** · **Intermediate** · Phase 02: Learning Machines

Break test error down by a feature you did not train on as a target, and write what you would do next.

## Concept

Average log loss can look fine while rainy outdoor docks are where the model is lost. This project slices the test set by a column, reports support and log loss per slice, and requires a minimum support before you are allowed to call a slice worse. You will predeclare the slices from the product, not from fishing: weather code, dock type, and a tenure band. Fishing is allowed only in a separate section labeled exploratory, and those slices cannot be the ones you act on today. The action is a written choice: collect more labeled rows, add a feature, or refuse to deploy the model for a slice below the support floor. You are not running a fairness audit that swaps attributes and estimates causal gaps. You are doing the earlier, plainer thing: looking at the error you already have, by a group you can define from columns.

## Approach

Use the locked run's test predictions so the scores are the ones the card refers to. Join them back to features by row id. For each predeclared slice, compute count, positive count, and mean log loss. A slice with fewer than thirty test rows is marked `thin` and is not ranked. Compare each eligible slice's loss to the overall test loss. Write `slice_report.md` with a table and a decision paragraph. Add one exploratory slice in a second table, and a sentence that says it did not drive the decision. A test builds a toy prediction file where one weather code has obviously worse loss and asserts the report names it, and asserts a tiny slice is marked thin.

## Components

| Piece | Role |
| --- | --- |
| Joined test frame | Predictions plus the slicing columns and the label. |
| Slice table | Support, positives, and mean log loss. |
| Support floor | A constant that marks thin slices. |
| Decision paragraph | One next step tied to an eligible slice, or a refusal to deploy. |

## How it works

1. Load predictions and features. Drop rows that fail the join rather than filling them.
2. Compute overall test log loss as the reference.
3. Compute the predeclared slices and apply the support floor.
4. Write the decision using only eligible slices.
5. Append the exploratory table underneath a heading that keeps it out of the decision.
6. Test the thin-slice rule and the obvious-bad-slice rule on toy data.

## Tech stack

- Python 3.11 or newer
- Standard library `csv` and `math`
- Predictions from the locked run

## Setup

1. Create `slices/` with `slice_report.py` and tests that do not need the full rental file.
2. Run the report on the real predictions.
3. If every eligible slice matches the overall loss, say so. Do not invent a gap.
4. Run tests.

## What done looks like

- Thin slices are visible and are not the subject of the decision sentence.
- The decision names a slice key and a support count, or explicitly says no eligible slice is worse.
- Exploratory slices are in a separate table.
- A failed join drops the row and increments a counter you print.
