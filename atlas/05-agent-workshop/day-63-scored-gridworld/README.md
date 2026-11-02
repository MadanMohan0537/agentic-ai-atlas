# A Scored Gridworld

**Day 63** · **Advanced** · Phase 05: Agent Workshop

Put an agent in a tiny grid, score a task, and show a script that loops without progress.

## Concept

Tool-using transcripts are hard to score because the world is implicit. A grid is a world you can score. This project builds a 5 by 5 grid with a dock, a bike, and a goal cell. The agent may `move` in four directions and `pickup`. Walls and the edge reject the move with an observation and do not change position. The score is 1 when the bike reaches the goal in at most 12 actions, otherwise 0. A scripted policy solves it. A second policy chases a loop: move left, move right, forever. The runner's budget stops it, and the score is 0. You will log positions after every action. This is an environment and a score, not a trace debugger and not a failure-taxonomy product. You do not need to classify why the loop happened beyond showing that position did not change across a full cycle.

## Approach

The environment is a pure function from state and action to state and observation, plus a reward of 0 until the goal condition, then 1, and the episode ends. Illegal moves return the same state. The loop policy is deterministic. The progress check in the required path is simple: if the position set of the last four actions has size 1, stop early with score 0 and reason `no-progress`. That check is local to this environment. Do not generalize it into a library of agent failure types. Seed nothing unless you add an obstacle that is random. The grid is fixed so the successful action list is a test fixture.

## Components

| Piece | Role |
| --- | --- |
| Grid state | Agent position, bike position, goal, and whether the bike is held. |
| Action set | Four moves and pickup, with rejected moves leaving state unchanged. |
| Score | 1 only if the bike is on the goal within the action cap. |
| Loop policy | A policy the no-progress rule stops. |

## How it works

1. Implement the transition function and a test that an illegal move does not change state.
2. Run the solving script and assert score 1 and a known action count.
3. Run the loop policy and assert score 0 and reason `no-progress`.
4. Assert the position log length matches the action count for the solver.
5. Assert pickup off the bike cell is a no-op observation and does not set the held flag.

## Tech stack

- Python 3.11 or newer
- Standard library only
- No game engine

## Setup

1. Create `gridworld/` with `env.py`, `policies.py`, and tests.
2. Run both policies and write `out/trace.json` for each.
3. Run tests.
4. Draw the grid in the notes with the goal marked, so a reader can replay the solver by hand.

## What done looks like

- The solver scores 1 on the fixed grid.
- The loop policy scores 0 with `no-progress`.
- Illegal moves do not change state.
- The notes include the grid and the solver's action list.

## Step ahead

The no-progress rule misses a policy that walks in a large square and never picks up the bike. Add a second stagnation rule: if `pickup` has not succeeded and the Manhattan distance to the bike has not decreased for six moves, stop with reason `no-approach`. Fixture a square-walk policy that stays far from the bike and assert that reason. Keep the original no-progress rule for the left-right loop. The follow-on is two stopping rules with different fixtures, not one vague notion of being stuck.
