# A Tree You Can Draw

**Day 13** · **Beginner** · Phase 02: Learning Machines

Grow a shallow decision tree, draw it, and show the overfit when you let it memorize leaves.

## Concept

Trees are easy to praise because a picture of a split looks like a policy. They are also easy to overfit: a deep tree will isolate single rentals and call that structure. This project grows a classification tree for overrun with a depth limit you choose, using Gini impurity computed from counts. You will print the tree as indented text you can redraw on paper, with the train count and the train overrun rate in every node. Then you will grow the same tree with the depth limit removed, or set absurdly high, and compare train accuracy to test accuracy. The gap is the lesson. You will also name one split that matches the labeling rule you wrote on Day 11 and one split that looks like noise. If you cannot tell those apart from the picture, the picture is too deep to trust.

## Approach

Implement a binary tree on numeric features and on already-encoded binary categories. Candidate thresholds are midpoints between sorted unique values, capped at a small number per feature so the day stays short. Stop when depth hits the limit, when a node is pure, or when a node has fewer than a minimum count you set in a constant. Do not prune with a library. The comparison is shallow versus deep on the same split. Write `tree.txt` for the shallow model and a three-line overfit note: train accuracy, test accuracy, and the depth of the deepest leaf in the unconstrained run.

## Components

| Piece | Role |
| --- | --- |
| Impurity function | Gini from class counts, tested on a hand example. |
| Split search | Midpoint thresholds with a cap on candidates. |
| Text tree | Indented nodes with counts and rates. |
| Depth contrast | Shallow versus unconstrained, same data, both scores. |

## How it works

1. Reuse the rider split and the overrun table.
2. Fit a tree with max depth 3 and minimum node size 15.
3. Render it to text and confirm every leaf shows a count.
4. Fit an unconstrained tree and record train versus test accuracy.
5. Write two sentences identifying a meaningful split and a suspicious one.
6. Test Gini on a node with counts (3, 1) against the value you computed by hand.

## Tech stack

- Python 3.11 or newer
- Standard library only
- Plain text rendering, no graphviz requirement

## Setup

1. Create `tree-model/` with `tree.py` and tests.
2. Run the shallow fit and read `tree.txt` top to bottom.
3. Run the deep fit and append the contrast to `notes.md`.
4. If the shallow tree and the deep tree have the same test accuracy, increase the noise in a copy of the generator or lower the minimum node size on the deep run only, and say which lever you moved.

## What done looks like

- The text tree is complete: every internal node names a feature and a threshold.
- Train accuracy of the deep tree is higher than its test accuracy on your run, or you documented a dataset too small to show the gap and enlarged it.
- Gini matches a hand-computed example in a test.
- The notes name one split you would keep and one you do not trust.
