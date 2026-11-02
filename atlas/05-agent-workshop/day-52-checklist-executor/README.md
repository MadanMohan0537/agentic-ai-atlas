# A Checklist the Executor Cannot Skip

**Day 52** · **Intermediate** · Phase 05: Agent Workshop

Separate a planner that writes a checklist from an executor that may only mark listed items done.

## Concept

A single loop that plans and acts in the same breath will skip a step and still sound finished. This project splits the roles. The planner writes a checklist of items, each with an id and a tool call, and then it is done. The executor may run only those calls, in order, and may mark an item done only after an observation is stored. It may not add a checklist item. A final answer that arrives with an open item is rejected. You will build one hostile executor, used only in a test, that tries to mark an item done without a call, and you will show the runner refusing. The planner in the required path is scripted from the task. The lesson is the boundary, not a clever plan.

## Approach

The checklist is JSON. Item states are `open` or `done`. The executor function takes the checklist and the scratchpad and returns the next call or a final answer. The runner checks that the call's item id exists, is open, and matches the tool the planner named. Arguments may be filled from earlier observations if the plan used placeholders such as `$item1.minutes`. Placeholders are the only flexibility. Free-form extra calls are rejected. Write a task whose plan has two items and a third tempting call that is not on the list. Assert the tempting call never runs.

## Components

| Piece | Role |
| --- | --- |
| Planner output | A checklist of item ids and tool names. |
| Executor | Runs listed calls in order and resolves placeholders. |
| State gate | An item becomes done only after an observation. |
| Hostile executor | A test double that tries to skip the call. |

## How it works

1. Script a planner for the fee-and-time task with two items.
2. Run the executor through the runner and save the checklist with states.
3. Assert the final answer is rejected if you force an item to stay open.
4. Assert the hostile executor's premature done mark raises.
5. Assert a call whose tool name is not on the current item is rejected.

## Tech stack

- Python 3.11 or newer
- JSON checklist and scratchpad
- No model required

## Setup

1. Create `checklist/` with `plan.py`, `execute.py`, and tests.
2. Run the happy path and write `out/checklist.json`.
3. Run the hostile tests.
4. Document the placeholder syntax in a short comment at the top of `execute.py`.

## What done looks like

- The happy-path checklist ends with every item done and observations attached.
- A premature done mark fails a test.
- A tool that was not on the list does not run.
- Placeholders resolve from earlier observations, and a missing placeholder fails the item rather than calling the tool with a literal dollar string.
