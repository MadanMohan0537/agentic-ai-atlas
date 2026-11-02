# Repair After a Correction

**Day 64** · **Advanced** · Phase 05: Agent Workshop

When the user says the other dock was meant, revise the slot you filled and do not defend the first one.

## Concept

A form-filling agent stores a dock id from the first user turn. The user then says "no, the other one, the indoor dock." A brittle agent repeats the first id because it is already in the scratchpad. This project models dialogue state as slots: `dock_id` and `fee_code`, each with a value and a `source_turn`. A correction pattern clears the slot the pattern names and sets it from the next resolvable description. "Indoor dock" resolves through a table of dock attributes, not through the previous slot. If two docks are indoor, the agent must ask which, and it must not keep the previous dock id while it asks. You will script the user with two turns and assert the slot after turn two is the indoor dock, and that the first dock id is recorded only as a superseded value, not as the current one.

## Approach

The resolver maps attributes to dock ids. Corrections match a small set of phrases you list, including "the other one" and "no". A correction without a resolvable replacement clears the slot and sets status `needs-clarification`. It does not leave the old value in place with a note. Superseded values go to a history list the answer renderer ignores. The answer renderer reads current slots only. A test renders the answer after the correction and asserts the first dock id is absent. Another test has two indoor docks and asserts the current slot is empty and the question names the attribute, not the old id.

## Components

| Piece | Role |
| --- | --- |
| Slots | Value, source turn, and status. |
| History | Superseded values that the answer renderer does not read. |
| Attribute resolver | A table from attributes to dock ids. |
| Clarification | Empty slot when the correction is ambiguous. |

## How it works

1. Fill `dock_id` from turn one with an outdoor dock.
2. Apply the correction turn that says indoor.
3. Assert the current value is the indoor dock and history holds the outdoor id.
4. Render the answer and assert the outdoor id is absent.
5. Run the two-indoor-docks fixture and assert clarification with an empty current value.

## Tech stack

- Python 3.11 or newer
- JSON dialogue scripts
- No model required

## Setup

1. Create `repair/` with `slots.py`, `dialogues.jsonl`, and tests.
2. Run both dialogues.
3. Run tests.
4. Write one sentence in the notes: the current slot is the only value the answer may use.

## What done looks like

- After a clear correction, the answer text contains the new dock and not the old one.
- The old value is still in history for audit.
- An ambiguous correction clears the current slot.
- The renderer has no parameter that passes history into the answer, and a signature test can lock that.

## Step ahead

A second correction can refer to history: "go back to the first one." Add an explicit undo command that pops history into the current slot, and reject it when history is empty. Do not make ordinary noun phrases search history. Fixture "go back to the first one" succeeding once and a second undo failing with `empty-history`. The follow-on keeps undo as a named command so a vague sentence cannot resurrect a superseded fee code by accident.
