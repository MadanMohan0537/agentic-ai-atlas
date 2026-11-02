# Where Three Models Disagree

**Day 69** · **Advanced** · Phase 06: Proof Bench: Evals and Harnesses

Run one prompt through three scripted models and list the cases where their structured answers differ.

## Concept

A single model output has no internal argument. Three different outputs on the same prompt show you where a human should look. This project runs a frozen prompt set through three scripted model adapters that return JSON docks and fees. The adapters are deterministic functions, so the harness is testable without keys. One adapter is correct. One swaps two docks. One abstains on rare codes. The harness groups cases by the set of distinct normalized answers and writes a disagreement file: cases where the set has more than one answer. It does not vote and it does not declare a winner. Voting would hide the abstention. You are building a queue of cases to read, not a judge of judges and not a calibration study of pairwise preferences.

## Approach

Each case result stores the three raw outputs and the normalized forms. Agreement means normalized equality under the Day 68 rules. The report lists disagreeing case ids and the answer set. A case where all three agree is counted and not listed in full. Include one case where two agree and one abstains, and keep it in the disagreement list. Dropping abstentions is a bug the test is named for. The adapters implement one function `complete(case) -> dict` and live in a file you can replace later with HTTP. Tests never do that replacement.

## Components

| Piece | Role |
| --- | --- |
| Frozen prompts | A handful of cases with gold, used only as a label in the report, not as a voter. |
| Three adapters | Deterministic scripted models. |
| Disagreement list | Cases whose normalized answer set has size greater than one. |
| Abstention marker | A distinct answer value that must not be dropped. |

## How it works

1. Write the three adapters and five cases.
2. Run the harness and write `disagreements.json`.
3. Assert the all-agree case is absent from the list and present in the agree count.
4. Assert the abstention case is present.
5. Assert the harness does not import a voting function. If you are tempted to add one, put it in a file the default command does not call, and test that the default output has no `winner` field.

## Tech stack

- Python 3.11 or newer
- Scripted adapters
- The set normalizer

## Setup

1. Create `disagreement/` with `adapters.py`, `harness.py`, and tests.
2. Run the harness.
3. Run tests.
4. Write one sentence: this list is a reading queue, not a score.

## What done looks like

- Agreeing cases are counted and not expanded in the disagreement list.
- Abstentions count as disagreements against a concrete answer.
- The default report has no winner field.
- Adapters are replaceable functions, and tests use the scripted ones.

## Step ahead

A long queue is not yet a way to choose the next case to read. Add a priority: cases where all three answers differ outrank cases where two agree. Sort the file that way and fixture six cases that force the order. Do not drop the lower group. The follow-on is a reading order you can explain, still without declaring which model was right.
