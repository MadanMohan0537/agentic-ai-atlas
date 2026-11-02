# Boosted Trees and a Local Reason

**Day 14** · **Beginner** · Phase 02: Learning Machines

Fit a small gradient-boosted stumps model and explain one prediction by occluding a single feature.

## Concept

Boosting is the usual next step on tabular problems, and it is also where explanations go vague. Harbor Loop does not need a leaderboard. It needs a model that beats the Day 11 card and a way to say, for one rental, which feature moved the score. This project fits additive stumps: each new tree is a depth-1 tree fit to the negative gradient of log loss. You will keep the ensemble small, on the order of twenty stumps, and you will stop if validation log loss rises. For a single test rental you will compute a local reason by occlusion: replace one feature with its train median, measure the change in predicted probability, and restore it. The largest change is the reason you write down. This is not a global importance trophy and it is not a production explainer for credit or safety decisions. It is a check you can recompute with a calculator and a median.

## Approach

Implement stumps, not a full boosting library. Use a learning rate of 0.1 and add each stump's contribution scaled by that rate. Hold a validation slice out of the training riders so early stopping does not look at the test riders. Log the validation loss per stump. Occlusion uses the train median for numeric features and the train mode for categories. Apply the same scaler logic you used before if features are not already on comparable scales; for stumps, raw scales are acceptable because thresholds adapt, and you should say that in the notes so you do not pretend the median swap is scale-free in meaning. Compare test log loss to the linear model and to the majority baseline.

## Components

| Piece | Role |
| --- | --- |
| Stump fitter | A depth-1 tree on the current residual. |
| Additive ensemble | Learning rate times stump, with early stopping on validation riders. |
| Occlusion probe | One-feature median swap and the delta in probability. |
| Scoreboard | Baseline, linear, and boosted test log loss in one file. |

## How it works

1. Split riders into train, validation, and test. Write the counts.
2. Fit stumps until the validation loss increases, or until you hit the cap.
3. Score the test set once with the chosen number of stumps.
4. Pick one test row whose predicted probability is between 0.3 and 0.7 if you have one, and occlude each feature.
5. Write `local_reason.md` with the row id and the ordered deltas.
6. Assert that occluding a feature and then restoring it returns the original probability within a tight tolerance.

## Tech stack

- Python 3.11 or newer
- Your own stump code from Day 13, simplified to depth 1
- No XGBoost requirement

## Setup

1. Create `boosted-stumps/` and reuse the CSV.
2. Implement `boost.py` and `occlude.py`.
3. Run the fit. If it never beats the linear model, record that. A loss is an acceptable outcome if the scoreboard is honest.
4. Run tests, including the restore-after-occlusion check.

## What done looks like

- The scoreboard lists three test log losses: majority, linear, boosted.
- Early stopping uses validation riders, never test riders.
- The local reason names a feature, a median, and a probability delta.
- A test shows occlusion is side-effect free on the row.
