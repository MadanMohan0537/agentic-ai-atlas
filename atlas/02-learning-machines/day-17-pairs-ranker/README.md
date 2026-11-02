# A Ranker from Pairs

**Day 17** · **Intermediate** · Phase 02: Learning Machines

Learn to order docks for a rider from pairwise preferences, and evaluate with a rank metric.

## Concept

Classification says whether a rental overran. Ranking says which dock a rider should be offered first. Harbor Loop can log a weak preference: when a rider is shown two docks and completes a rental at one of them, that dock won the pair. This project builds pairs from synthetic choice logs, fits a linear scoring function so that the winner's score exceeds the loser's, and evaluates with top-1 accuracy on held-out riders. You will use a pairwise hinge: the loss is zero when the score gap clears a margin, and linear otherwise. A constant model that always prefers the globally popular dock is the baseline. If your ranker cannot beat popularity on riders it has not seen, the features are not doing work. Do not report a classification accuracy on pairs as if it were the product metric. The product shows a list.

## Approach

Each candidate dock has features you already understand: distance bucket, indoor flag, historical overrun rate computed with a cutoff so the pair's own outcome is not inside the feature. That cutoff matters. Compute dock history from events before the choice time. Train with stochastic updates over pairs, seeded shuffle, fixed step size. Evaluate on riders held out entirely. Top-1 means the dock with the highest score is the one the rider completed, among the docks that were actually shown. Include a popularity baseline that ranks by prior completion count, also cutoff-safe. Write both numbers.

## Components

| Piece | Role |
| --- | --- |
| Choice log | Shown docks, chosen dock, timestamp, rider id. |
| Cutoff features | Dock history strictly before the choice. |
| Pairwise hinge | A linear score with a margin. |
| Top-1 versus popularity | Held-out riders, both methods. |

## How it works

1. Generate choices with a seeded rule and a little noise.
2. Build features with a strict time cutoff and test that the choice itself is absent from the history count.
3. Fit the linear ranker on training riders' pairs.
4. Score held-out riders' lists and compute top-1.
5. Score the popularity baseline the same way.
6. Write `rank_card.md`. If the ranker loses, keep the card anyway.

## Tech stack

- Python 3.11 or newer
- Standard library only
- Held-out riders as the evaluation unit

## Setup

1. Create `ranker/` with `choices.py`, `train_rank.py`, and tests.
2. Run generation and training.
3. Add a test that a feature builder raises or drops the current choice if someone includes it.
4. Run the tests.

## What done looks like

- Top-1 for the ranker and for popularity are both on the card, on held-out riders.
- A test rejects features that include the choice being scored.
- The hinge margin is a named constant.
- You can explain why pair accuracy would have flattered a model that only learns to pick the popular dock inside a pair of unequals.
