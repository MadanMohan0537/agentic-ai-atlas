# Illegal Transitions

**Day 57** · **Intermediate** · Phase 05: Agent Workshop

Model the agent as a state machine and reject any event that the current state does not allow.

## Concept

Loops get into impossible states: an answer before any retrieval, a second handoff, a tool call after the answer. This project names the states and the events. States are `idle`, `planned`, `acting`, `handoff`, and `answered`. Events are `plan`, `act`, `observe`, `submit_handoff`, and `answer`. A table maps state and event to the next state or to `illegal`. The runner consults the table and refuses illegal events with the state name and the event name in the error. It does not catch the error and continue. You will drive a happy path and three illegal paths: answering from idle, acting after answered, and submitting two handoffs. The table is data, so a test can add a temporary transition without editing the runner.

## Approach

Store the table as a dictionary of pairs. The runner holds one current state and appends every accepted event to a log. Illegal events raise `IllegalTransition` and leave the state unchanged. A test attempts the illegal event and then a legal one and asserts the legal one still sees the pre-illegal state. Do not encode the table as a chain of if statements inside the runner. The runner should look up the pair and follow it. Print the reachable states from `idle` by a small walk so you notice a state you cannot enter.

## Components

| Piece | Role |
| --- | --- |
| Transition table | Pairs of state and event, stored as data. |
| Runner | Looks up the table and refuses misses. |
| Event log | Accepted events only. |
| Illegal paths | Three fixture sequences that must raise. |

## How it works

1. Write the table and a function that lists states unreachable from idle.
2. Drive the happy path through answer and save the log.
3. Attempt each illegal path and record the exception message.
4. Assert state is unchanged after a rejected event.
5. Assert every named state is reachable, or remove the state from the machine.

## Tech stack

- Python 3.11 or newer
- Standard library only
- No model

## Setup

1. Create `state-machine/` with `machine.py` and tests.
2. Run the happy path and the three failures.
3. Run tests.
4. If a state is unreachable, fix the table before you call the day done.

## What done looks like

- Three illegal sequences raise and name both the state and the event.
- State does not change on a rejected event.
- The transition table is data the runner looks up.
- Every state is reachable from idle, and a test walks the table to prove it.
