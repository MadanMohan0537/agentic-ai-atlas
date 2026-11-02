# Baselines that Humiliate Models

**Day 11** · **Beginner** · Phase 02: Learning Machines

Score a majority-class rule and a mean predictor before any learned model is allowed to look good.

## Concept

Harbor Loop wants a first model for a yes-or-no question: did a booked rental overrun its slot? Ninety percent of rentals do not overrun. A classifier that always says "no" is right ninety percent of the time and useless at the dock. This project builds the dataset — a few hundred synthetic rows with a seeded generator — and the two baselines every later model has to beat. For classification, the baseline is the majority class, scored with accuracy and with balanced accuracy so the base rate cannot hide. For a companion regression, predicting overrun minutes, the baseline predicts the training mean. You will write both metrics yourself on the confusion counts. The artifact is a one-page baseline card that later days must paste their scores next to. A model that cannot beat the card does not get a paragraph in your notes.

## Approach

Generate rows with `random.Random(11)`. Columns: booked minutes, start hour, dock type (open or indoor), rider tenure days, weather code (clear, rain), and the label `overrun`. Plant the base rate near 0.1 by sampling the label from a rule you write down, plus noise, so the problem is learnable later and still imbalanced. Split riders, not rows, using the stable hash from the split day, even if you reimplement the ten lines here. Compute the majority baseline only from the training fold. Evaluating the majority class on data you used to pick it is a small leak; picking it on train and scoring on test is the habit. Write `baseline_card.md` with the test accuracy, balanced accuracy, and the regression mean absolute error of the mean predictor.

## Components

| Piece | Role |
| --- | --- |
| Seeded generator | Synthetic rentals with a documented labeling rule. |
| Rider split | Whole riders assigned to train or test. |
| Majority baseline | Train-fold mode, scored on the test fold. |
| Mean predictor | Train-fold mean of overrun minutes, with test MAE. |

## How it works

1. Generate the table and write `data/rentals.csv` plus `data/RULE.txt` describing the labeling rule in words.
2. Split by rider id into train and test.
3. Compute the majority label on train only and score it on test.
4. Compute balanced accuracy from the four confusion counts, not from a library.
5. Fit the mean overrun on train rows that did overrun, and separately on all train rows. Document which one you are using and why.
6. Write the baseline card. A test locks the majority label for this seed so a generator change cannot pass quietly.

## Tech stack

- Python 3.11 or newer
- Standard library `random`, `csv`, `hashlib`
- Metrics implemented from counts

## Setup

1. Create `baselines/` with `generate.py`, `score.py`, and tests.
2. Run `python3 generate.py` then `python3 score.py`.
3. Run `python3 -m unittest discover -s tests -v`.
4. If balanced accuracy and accuracy are almost equal, your base rate is too close to one half. Push the negative rate up and regenerate.

## What done looks like

- The baseline card quotes test numbers and names the seed and the split rule.
- Majority class is chosen on train, and a test would fail if it were chosen on test.
- Balanced accuracy is computed from TP, FP, TN, and FN in your own function.
- The labeling rule is written in `RULE.txt` before any later model day starts.
