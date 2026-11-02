# Budgets and Partial Answers

**Day 58** · **Advanced** · Phase 05: Agent Workshop

Stop the loop at a step budget and return a partial answer that lists unfinished checklist items.

## Concept

An agent that runs until it feels done will run until someone kills the process. This project adds a budget: a maximum number of tool calls and a maximum number of transcript lines. When either limit is hit, the runner does not raise a generic timeout and discard the work. It returns a structured partial answer: status `partial`, the observations so far, and the checklist item ids still open. A complete answer is illegal if the budget is already exhausted. You will fixture a planner that emits four items and a budget of two calls, and show the partial result containing the two finished observations and the two open ids. You will also fixture a task that finishes inside the budget and show status `complete` with an empty open list. The budget is part of the task file so a test can tighten it without editing code.

## Approach

Count tool calls, not thoughts. A thought does not spend the tool budget. Transcript-line budget counts every line. Hitting either budget triggers the same partial response shape so callers do not special-case the reason, but the response includes `stop_reason` of `tool-budget` or `line-budget`. A test sets the tool budget to zero and expects a partial answer with every item open and zero observations. The runner must check the budget before the call, not after, so a zero budget does not sneak one execution through. Write `budget_notes.md` with both fixture outputs.

## Components

| Piece | Role |
| --- | --- |
| Tool budget | Checked before a call is dispatched. |
| Line budget | Checked before a line is appended. |
| Partial response | Observations so far and open item ids. |
| Stop reason | Which budget fired, on the response. |

## How it works

1. Add budgets to the checklist runner from Day 52.
2. Run the four-item plan with a tool budget of two.
3. Run a two-item plan inside the budget and expect `complete`.
4. Run a zero tool budget and expect no function executions.
5. Hit the line budget with a talkative scripted policy and expect `line-budget` without a tool call that would exceed the tool budget. Keep the fixture simple: a line budget of one.

## Tech stack

- Python 3.11 or newer
- The checklist runner
- JSON task files that include budgets

## Setup

1. Create `budgets/` with `budget_loop.py` and tests.
2. Run the three fixtures and save their responses.
3. Run tests, including the zero-budget case.
4. Confirm a function-body counter stays at zero when the tool budget is zero.

## What done looks like

- Partial responses list finished observations and open ids.
- A zero tool budget executes nothing.
- `stop_reason` distinguishes the two budgets.
- A task that finishes inside budget has status `complete` and no open ids.

## Step ahead

A partial answer can still be mistaken for a fee quote if a reader looks only at the observations. Add a renderer that refuses to print a currency number unless status is `complete`, and otherwise prints the open item ids first. Fixture a partial run whose observations already contain a fee amount, and assert the rendered text does not contain that amount. The follow-on failure you are preventing is a UI that shows the observation log as if it were the answer.
