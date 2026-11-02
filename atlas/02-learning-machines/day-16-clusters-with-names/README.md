# Clusters with Names

**Day 16** · **Intermediate** · Phase 02: Learning Machines

Cluster docks from usage features and name each cluster from examples, or refuse to name it.

## Concept

Someone will ask what kinds of docks Harbor Loop operates. A clustering algorithm will always return groups. Names are the part you are responsible for. This project builds a dock-level table: median start hour, share of rainy rentals, median duration, and overrun rate. It runs k-means with k chosen from a small range using inertia, then tries to name each cluster from the five member docks closest to the center. A name is allowed only if you can write a sentence a teammate could falsify, such as "evening commute, indoor, short bookings." If the members do not support a sentence, the cluster is called `unlabeled-3` and the notes say what you would need to see. You will also refit with a different seed and report which docks changed cluster. Stability is part of the name. An unstable group does not deserve a product label.

## Approach

Standardize dock features with the mean and variance of the dock table you are clustering. That is descriptive, not a train-test model, and you should say so. Implement k-means with a fixed number of iterations and two seeds. Pick k by plotting inertia for k from 2 to 6 and choosing the smallest k after which the drop flattens; write the rule you used in a sentence so "elbow" is not a vibe. For each cluster, list the five nearest docks and their raw feature values, not just the standardized ones, because names should be in real units. The seed comparison reports the fraction of docks whose cluster assignment changed, after matching clusters by center proximity so label switching is not counted as change.

## Components

| Piece | Role |
| --- | --- |
| Dock table | One row per dock, aggregated from rentals. |
| k-means | Your implementation, two seeds, inertia for several k. |
| Naming sheet | Nearest members in raw units and a falsifiable sentence or an explicit refusal. |
| Stability note | Share of docks that move after a seed change, with centers matched. |

## How it works

1. Aggregate rentals to docks. Docks with very few rentals go to an exclusion list, not into a cluster you then name.
2. Standardize and run k-means for k from 2 to 6.
3. Choose k and write the rule.
4. Name or refuse each cluster using nearest members.
5. Refit with a second seed, match centers, and compute the move rate.
6. Test one iteration of k-means on a toy set of points you can solve by eye.

## Tech stack

- Python 3.11 or newer
- Standard library only
- A naming sheet in markdown

## Setup

1. Create `clusters/` with `aggregate.py`, `kmeans.py`, and `name.md`.
2. If you are still on the synthetic generator, give docks three distinct usage patterns so a failure to separate them is informative.
3. Run both seeds and fill in `name.md`.
4. Run the toy-set test.

## What done looks like

- Every cluster is either named with a falsifiable sentence or explicitly unlabeled.
- Excluded low-count docks are listed and are not given a name.
- The move rate between seeds is a number in the notes.
- The toy test fails if assignments on the obvious two-blob set are wrong.
