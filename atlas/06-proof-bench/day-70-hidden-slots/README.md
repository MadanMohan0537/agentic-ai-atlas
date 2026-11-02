# Hidden Slots Across Turns

**Day 70** · **Advanced** · Phase 06: Proof Bench: Evals and Harnesses

Script a user with hidden slot values and score whether the agent fills them without re-asking a locked slot.

## Concept

Multi-turn agents look fine if you read only the last turn. The failure is in the middle: the user already gave the dock, and the agent asks again, or it overwrites a locked fee code. This project is a harness around a scripted user and a scripted agent. The user has hidden slots. It reveals a slot only when asked, or when its opening line includes it. Once a slot is filled and the user has not corrected it, the slot is locked. The score penalizes a question about a locked slot and penalizes an answer that does not match the hidden value. You will run a three-turn script where the dock is given up front and the fee is asked once. A bad agent that re-asks the dock fails even if the final answer is right.

## Approach

The user is a function of the hidden slots and the agent question. It is not a model. The harness logs each turn's asked slot names. Locked slots are those filled and not corrected. The agent under test is also scripted so you can swap in a bad one. Metrics are: final value match, count of questions about locked slots, and turns used. Do not average these into one grade. The report lists them. A correction turn unlocks a slot on purpose, using the Day 64 rule, and a question after the correction is allowed. A fixture covers that so the harness does not punish repair.

## Components

| Piece | Role |
| --- | --- |
| Hidden slot user | Reveals values only under the script rules. |
| Lock set | Filled slots that have not been corrected. |
| Bad agent fixture | Re-asks the dock and still answers correctly at the end. |
| Separate metrics | Match, locked-question count, and turns. |

## How it works

1. Implement the user and the lock rules.
2. Run the good agent and expect zero locked questions and a value match.
3. Run the bad agent and expect a locked question count of at least one, with the match still true.
4. Run a correction fixture and expect the post-correction question not to count as locked.
5. Write the three reports.

## Tech stack

- Python 3.11 or newer
- Scripted user and agents
- JSON reports

## Setup

1. Create `hidden-slots/` with `user.py`, `harness.py`, and tests.
2. Run the three scripts.
3. Run tests.
4. Keep the hidden values out of the agent's initial prompt in the good-agent fixture. The opening line may include only the values the script says were volunteered.

## What done looks like

- The bad agent fails the locked-question metric while passing the final match.
- The good agent passes both.
- A post-correction question is not counted as a locked question.
- Metrics are reported separately.

## Step ahead

Users contradict themselves without using the correction phrases you listed. Add a fixture where turn three states a new dock id as a bare fact, not as "no, the other one." Define the harness rule you will actually enforce: either bare restatements update the slot, or they count as contradictions the agent must ask about. Pick one, fixture both an agent that follows the rule and one that does not, and write the rule in the report header. The follow-on is a contradiction policy you chose on purpose, not an accidental overwrite.
