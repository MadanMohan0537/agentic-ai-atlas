# Where Position Lives

**Day 25** · **Intermediate** · Phase 03: Transformer Workbench

Add sinusoidal positions and a rotary-style pairing, and show a model with neither cannot tell order.

## Concept

A bag of token vectors is invariant to order. "Bike at dock" and "dock at bike" become the same multiset, and attention without positions cannot prefer one reading. This project demonstrates that collapse, then adds two positional mechanisms on a toy sequence. Sinusoidal positions are added to the token vectors. A rotary-style pairing rotates adjacent pairs of dimensions by an angle that depends on the index, which you implement for a single query-key dot product so the relative offset appears in the score. You are not reimplementing a production RoPE kernel. You are showing, on a sequence of length four and dimension four, that a shift in position changes the score in the rotary version and that the no-position version is unchanged by a swap you construct. Write the swap explicitly.

## Approach

Build two token sequences that are permutations of each other. Run attention with no positions and show identical outputs up to the permutation of positions, or identical pooled outputs if you mean-pool. Then add sinusoidal vectors from the original formula, with a base you set to 10000, and show the pooled outputs differ. For the rotary demo, take one query and one key, both in R4, rotate the pairs by index times a frequency, and compute the dot product at offsets 0, 1, and 2. Put the three scores in `positions.md`. A test locks the sinusoidal vector at position 0, which should be a specific pattern of zeros and ones you derive.

## Components

| Piece | Role |
| --- | --- |
| Order-swap fixture | Two sequences with the same tokens in different order. |
| No-position attention | The collapse you are trying to expose. |
| Sinusoidal add | Position vectors added before attention. |
| Rotary dot-product demo | Scores at three relative offsets for one pair. |

## How it works

1. Compute the no-position outputs on the swapped sequences and record the comparison you promised.
2. Add sinusoidal positions and repeat the comparison.
3. Derive the position-0 sinusoid and lock it in a test.
4. Compute the three rotary scores and write them down.
5. State in one sentence which mechanism you would reach for first in a tiny character model and why. Either answer is acceptable if the sentence cites your numbers.

## Tech stack

- Python 3.11 or newer
- Standard library `math`, plus NumPy if you already use it
- No pretrained model

## Setup

1. Create `positions/` with `positions.py` and tests.
2. Run the swap experiment and write `positions.md`.
3. Run tests, including the position-0 sinusoid.
4. Keep the sequence length at 4 so the matrices stay printable.

## What done looks like

- The no-position case shows the order invariance you claimed, on the fixture.
- The sinusoidal case breaks that invariance on the same fixture.
- Position 0 matches the hand derivation.
- Three rotary scores are recorded.
