# Accepted Tool Sequences

**Day 78** · **Advanced** · Phase 06: Proof Bench: Evals and Harnesses

Score a transcript's tool names against a set of accepted sequences, ignoring argument values.

## Concept

Some tasks have more than one legal procedure and many illegal ones. Looking up a fee and then quoting is fine. Quoting and then looking up is not, if the rule is that quotes must follow a lookup. This project lists accepted tool-name sequences for a task. Argument values are ignored in the required score, because a separate harness already checks values. A transcript passes if its tool-name list matches one accepted sequence exactly. A prefix of an accepted sequence is a failure labeled `incomplete`, not a pass. An extra tool in the middle is `not-accepted`. You will write three transcripts covering pass, incomplete, and an inserted tool. The harness does not run tools. It reads names in order.

## Approach

Accepted sequences live in `accepted.json` as a list of lists of strings. Matching is equality of the full list. You also compute the longest accepted sequence that is a prefix of the observed names, and report it, so an incomplete run is visible as "matched 2 of 3 of sequence 0" rather than as a mysterious fail. Inserted tools break every prefix at that index. Tests cover a second accepted sequence that is a different legal order, so the harness is not secretly requiring one path. Argument objects may be present in the transcript and must be ignored by the comparator. A test puts different arguments on a passing name sequence and expects a pass.

## Components

| Piece | Role |
| --- | --- |
| Accepted file | A set of tool-name sequences. |
| Exact matcher | Full-list equality against any accepted sequence. |
| Prefix diagnostic | How far the observed list followed some accepted sequence. |
| Argument blindness | Values are not part of this score. |

## How it works

1. Write two accepted sequences for one task.
2. Score a transcript for each sequence as a pass.
3. Score a prefix and expect `incomplete` plus the prefix diagnostic.
4. Score an inserted tool and expect `not-accepted`.
5. Change only arguments on a passing transcript and expect the verdict to stay a pass.

## Tech stack

- Python 3.11 or newer
- JSON transcripts
- No tool execution

## Setup

1. Create `sequences/` with `score.py`, `accepted.json`, and tests.
2. Run the four transcripts.
3. Run tests.
4. Note in the folder README that argument correctness is out of scope for this scorer.

## What done looks like

- Both legal orders pass.
- A prefix is `incomplete` and not a pass.
- An inserted tool is `not-accepted` and the diagnostic names the index.
- Argument changes do not flip a pass to a fail.

## Step ahead

Names-only scoring still passes a lookup with an empty query. Add an argument sketch: for each step, a set of required keys that must be present and non-empty, without specifying the values. Fixture a passing order whose lookup query is an empty string and expect a new status `missing-key` that does not replace `not-accepted`. A wrong order with all keys present should still be `not-accepted`. The follow-on is a sketch of arguments, not a return to exact string match on the fee code.
