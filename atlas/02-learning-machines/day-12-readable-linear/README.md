# A Linear Model You Can Read

**Day 12** · **Beginner** · Phase 02: Learning Machines

Fit a logistic model with gradient descent, standardize inputs, and plot reliability in five bins.

## Concept

A linear model earns its place when you can read a coefficient and say what would happen if that input moved. On the overrun table, tenure and rain should not share a scale: tenure is in days, weather is a code. Fit without standardizing and the steps fight each other. This project implements binary logistic regression with batch gradient descent, no scikit-learn. You will one-hot the small categories yourself, standardize numeric columns using train-fold mean and variance, and apply those same numbers to test. Then you will bin the test set by predicted probability and compare the average prediction in each bin to the observed overrun rate. That reliability table is the model's honesty check. Coefficients come after, as a sentence each: direction, rough size, and whether the feature's scale makes the size comparable.

## Approach

Use a learning rate you log, a fixed iteration count, and a seed only if you shuffle rows. Initialize weights at zero so the run is determined by the data. Clip the linear score before the exp in the sigmoid so a wild step cannot overflow. Hold out the test fold from standardization statistics. Reliability uses five bins of equal width on [0, 1], and bins with fewer than five test rows are reported but not trusted. Compare test log loss to the majority baseline's log loss. Accuracy alone is not the headline. If the linear model cannot beat the baseline card on log loss, say so in the notes and keep the baseline.

## Components

| Piece | Role |
| --- | --- |
| Design matrix | Numeric columns standardized, categories one-hot encoded. |
| Gradient step | Batch logistic gradient with a clipped score. |
| Reliability table | Five bins comparing mean prediction to observed rate. |
| Coefficient notes | One sentence per weight, after scaling is explained. |

## How it works

1. Load the Day 11 table or regenerate it with the same seed and rule.
2. Build the train-only scaler and apply it to train and test.
3. Fit for a logged number of steps. Save the loss every ten steps to `loss.csv`.
4. Predict on test and write the reliability table.
5. Write coefficient sentences into `coefficients.md`, noting which columns were standardized.
6. Assert test log loss is finite and that a column excluded from the scaler does not change the scaler's stored mean.

## Tech stack

- Python 3.11 or newer
- Standard library only, including `math`
- CSV loss curve you can open in any spreadsheet

## Setup

1. Create `linear-model/` and copy the generator or read the CSV from a relative path you document.
2. Implement `logit.py` with `fit` and `predict_proba` separated.
3. Run the fit and the tests.
4. If the loss curve increases, divide the learning rate by ten and record both attempts in the notes. Do not hide the failed rate.

## What done looks like

- Train mean and variance are not computed from test rows, and a test locks that.
- The reliability table has a row per non-empty bin.
- Test log loss is compared to the majority baseline in the written notes.
- You can point to one coefficient and say what scaling was applied before it was fit.
