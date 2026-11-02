# A Persona with a Patience Counter

**Day 75** · **Advanced** · Phase 06: Proof Bench: Evals and Harnesses

Simulate a user who ends the conversation after a fixed number of unhelpful turns, and score task completion.

## Concept

An agent can be polite for twenty turns and never collect the dock id. This project scripts a persona with a goal, a patience counter, and a list of facts it will reveal when asked the right slot. Each agent question that does not name a missing slot decrements patience. At zero, the persona ends the conversation. The score is whether the goal slot values are filled at the end, not whether the agent said thank you. You will run a terse agent that asks the right slots and a rambling agent that asks open-ended questions. Both can be scripted. The rambling agent must hit patience zero with the goal incomplete. Completing the goal on the last remaining patience point still scores as complete. You will not add a sentiment score.

## Approach

The persona is a pure function. Patience starts at three. The goal is a set of slots. The agent's utterances are classified by a rule: if they contain a slot name from the missing set, the persona reveals it and patience stays. Otherwise patience drops. The harness records the turn count, the ending patience, and the unfilled slots. A test uses a persona that reveals nothing unless asked, so an agent cannot score a point from the opening line alone unless the fixture says the opening line included a slot. Put that rule in the fixture file.

## Components

| Piece | Role |
| --- | --- |
| Persona | Goal slots, patience, and a reveal rule. |
| Question classifier | Whether the utterance names a missing slot. |
| Terse agent | Asks only missing slots. |
| Rambling agent | Never names a slot. |

## How it works

1. Implement the persona and the classifier.
2. Run the terse agent and expect completion with patience at or above one.
3. Run the rambling agent and expect an incomplete goal and patience zero.
4. Run a terse agent that finishes on the last patience point and expect complete.
5. Assert the report contains no sentiment or politeness field.

## Tech stack

- Python 3.11 or newer
- Scripted persona and agents
- JSON report

## Setup

1. Create `patience/` with `persona.py`, `harness.py`, and tests.
2. Run both agents.
3. Run the last-point fixture.
4. Run tests.

## What done looks like

- The rambling agent fails by patience, not by a string match on the final answer alone.
- The terse agent completes the goal.
- Finishing on the last patience point counts as complete.
- The report fields are goal completion, unfilled slots, and ending patience.

## Step ahead

Patience is harsher when the user is underspecified and friendlier when they volunteer facts. Add a second persona config, `impatient`, with patience 1, and run the same terse agent. The terse agent should still finish if the opening line volunteers one of two slots. Fixture a terse agent that asks for the volunteered slot again and show it failing under `impatient` while passing under the original patience of three. The follow-on is a grid of persona configs, not a new agent architecture.
