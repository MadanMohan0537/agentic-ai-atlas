# One Attention Head, On Paper

**Day 23** · **Intermediate** · Phase 03: Transformer Workbench

Implement scaled dot-product attention for one head and check a hand-computed 2 by 2 case.

## Concept

Attention is a weighted average of values, with weights coming from queries and keys. The sentence is short and the bugs are ordinary: forgetting the scale, applying the mask after the softmax, or letting a padded position vote. This project implements single-head scaled dot-product attention in NumPy or in pure Python if you want to avoid the dependency. You will first compute a 2 by 2 example by hand, including the scale by square root of the key dimension, and lock it in a test. Then you will run a short sequence of token vectors you choose and print the weight matrix. A causal mask will zero the future, and a padding mask will zero a pad position in both directions that matter: it should not attend, and others should not attend to it. You will write the mask rule in one sentence above the code.

## Approach

Represent a batch of one so the shapes stay visible: query, key, and value are lists of vectors or a 2-D array of shape (time, dim). Scores are query times key transpose, divided by sqrt(dim). Masked positions are set to a large negative number before softmax, not to zero after. Softmax is numerically stable: subtract the max. The output is the weighted sum of values. The hand example uses dim 2 and two positions so you can show the arithmetic in `hand.md`. Do not import a transformer library for this day. If you use NumPy, pin the version in a requirements file that contains only that dependency.

## Components

| Piece | Role |
| --- | --- |
| Score function | Dot products scaled by sqrt(dim). |
| Mask | Causal and pad positions set to a large negative before softmax. |
| Stable softmax | Subtract the max, then exponentiate. |
| Hand example | A 2 by 2 case with the arithmetic written out. |

## How it works

1. Write the 2 by 2 example on paper and then in `hand.md`.
2. Implement attention and assert it matches the hand example within 1e-5.
3. Build a length-4 sequence and print causal weights. Later positions may attend backward. Earlier positions must put zero mass on the future, within tolerance.
4. Mark the last position as pad and assert its incoming and outgoing attention mass is zero after masking.
5. Assert the rows of a fully valid causal mask still sum to 1.

## Tech stack

- Python 3.11 or newer
- NumPy, pinned, or pure Python lists if you prefer
- No transformer framework

## Setup

1. Create `attention-head/` with a virtual environment and `requirements.txt` if you use NumPy.
2. Implement `attention.py` and `tests/test_hand.py`.
3. Run the tests and print one weight matrix into `weights.md`.
4. If a row does not sum to 1, fix the mask order before you add more features.

## What done looks like

- The hand example matches the code.
- Causal weights put no mass on future positions.
- A pad position does not receive or send mass.
- The mask sentence above the function matches the behavior the tests lock.
