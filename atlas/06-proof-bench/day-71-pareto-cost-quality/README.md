# The Pareto Surface of Cost and Quality

**Day 71** · **Advanced** · Phase 06: Proof Bench: Evals and Harnesses

Sweep a grid of retriever depth and scripted model cost and drop the configs that are worse on both axes.

## Concept

A better score that costs ten times as much is not automatically the config you ship, and a cheaper config that loses one gold id may be. This project freezes a tiny retrieval eval and a scripted generator that can see only the chunks you pass it. You sweep `k` in {1, 3, 5} and a `model` label in {cheap, strong} where strong costs more per call in a price table you write. Quality is recall at k from the frozen file, or quote exact-match if you wire the quoter. Cost is the sum of a retrieval cost and a model cost you invented and documented as fictional. You plot nothing fancy: a CSV of config, quality, cost, and a flag `dominated` when another config is at least as good on quality and strictly cheaper, or strictly better and no more expensive. Dominated configs are not candidates. You do not hide them.

## Approach

The price table is `prices.json` with fictional units, and the report says the units are fictional in the first line. The sweep is exhaustive on the small grid. Domination is computed by a function a test can run on a hand-built three-row table, one of which is dominated. The harness does not call a hosted model. The strong scripted model returns the gold quote only if the gold chunk is in the retrieved set. The cheap one returns it only if the gold chunk is rank 1. That difference is enough to make the surface interesting. Write `frontier.csv` and a sentence naming the undominated configs.

## Components

| Piece | Role |
| --- | --- |
| Price table | Fictional costs for retrieval and for each model label. |
| Sweep grid | k and model label. |
| Domination flag | A config that is weakly worse on both axes. |
| Frontier list | The undominated configs, named in a sentence. |

## How it works

1. Write prices and the two scripted models.
2. Run the sweep on a frozen question file with known gold chunks.
3. Compute domination.
4. Test domination logic on a hand-built table.
5. Write the frontier sentence from the actual CSV.

## Tech stack

- Python 3.11 or newer
- CSV and JSON
- Scripted models with a price table

## Setup

1. Create `pareto/` with `sweep.py`, `prices.json`, and tests.
2. Run the sweep.
3. Run the domination unit test.
4. Label the units as fictional in the report's first line.

## What done looks like

- Every grid point is a row, including dominated ones.
- The hand-built domination test passes.
- The frontier sentence names configs that exist in the CSV.
- No hosted model is required to reproduce the file.

## Step ahead

Cost is not the only second axis. Add a latency budget, also fictional, and drop any config whose scripted latency exceeds it before domination runs. Fixture a strong model that is best and over budget so it disappears from the frontier, and show the row still present with `over_budget` set. The follow-on is a constraint applied before you brag about the frontier, not a third score averaged in.
