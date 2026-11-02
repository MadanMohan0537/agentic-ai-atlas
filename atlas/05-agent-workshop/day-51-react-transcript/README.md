# A Transcript You Can Grade

**Day 51** · **Intermediate** · Phase 05: Agent Workshop

Record thought, action, and observation lines, and grade the transcript against a scripted trace.

## Concept

A loop that only stores tool calls hides why the next call was chosen. The ReAct pattern writes a thought, then an action, then an observation, and repeats. This project implements that transcript with a scripted reasoner so you can grade the text without a model. The reasoner emits a thought that names the missing field, then an action. You will compare a run to a golden transcript: same actions in the same order, observations equal to the tool results. Thoughts may differ in wording only if you are using a model. Under the scripted reasoner they must match too, because they are part of the contract of the fixture. Grading is exact on actions and observations. A mismatched thought under the script fails the run. That strictness is what makes the later model swap measurable.

## Approach

Each transcript line has a kind: `thought`, `action`, `observation`, or `answer`. The runner rejects two actions in a row without an observation, and rejects an observation that did not come from the tool. The golden file is a transcript you write by hand for one task. The grader reports the first diverging line index. Include a second golden file for the missing-input task that contains a thought and an answer and no action. A model backend, if you add one, is behind a flag and is not used by tests. Tests use the scripted reasoner only.

## Components

| Piece | Role |
| --- | --- |
| Line types | Thought, action, observation, and answer, in a fixed order. |
| Scripted reasoner | Emits the next thought and action from the task state. |
| Golden transcript | A hand-written trace for one successful task. |
| Grader | Reports the first line where the run diverges. |

## How it works

1. Define the line schema and the runner rules that forbid doubled actions.
2. Write the golden transcript for the fee-and-time task.
3. Run the scripted reasoner and grade it. It should match.
4. Mutate one action in a copy of the run and assert the grader names that line.
5. Grade the missing-input transcript and assert it contains no action lines.

## Tech stack

- Python 3.11 or newer
- JSONL transcripts
- Scripted reasoner required, model optional and off by default

## Setup

1. Create `react-transcript/` with `transcript.py`, `gold/`, and tests.
2. Run the match and the deliberate mismatch.
3. Run tests.
4. If you try a model, save that transcript as `out/model.jsonl` and do not overwrite the golden file when it differs.

## What done looks like

- The scripted run matches the golden transcript exactly.
- A mutated action fails the grader at the right line index.
- The runner rejects an action that is not followed by a tool observation when another action arrives.
- Tests pass with no model key present in the environment.
