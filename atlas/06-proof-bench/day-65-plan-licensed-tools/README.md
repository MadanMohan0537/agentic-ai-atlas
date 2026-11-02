# Was that Tool Licensed by the Plan?

**Day 65** · **Advanced** · Phase 06: Proof Bench: Evals and Harnesses

Score each tool call on whether the checklist named it, separate from whether the final answer was right.

## Concept

An agent can reach the right fee with a tool the plan never mentioned, which means the next run can wander. This project scores a finished transcript against the checklist that was approved before any call. Each action is `licensed` if its tool name appears on the current open item, and `unlicensed` otherwise. The final-answer check is a separate boolean: did `quote` match the gold substring. You will report both numbers. A fixture with the right answer and one unlicensed lookup must fail the license score and pass the answer score. A fixture with only licensed calls and a wrong quote must do the opposite. Collapsing these into one pass mark hides which part broke. The harness reads files. It does not run the agent.

## Approach

Inputs are `plan.json` and `transcript.jsonl`. The scorer walks actions in order, matching them to open items as the executor would, and emits a row per action. Summary metrics are license rate and answer correctness. A missing plan file is an error, not a vacuously licensed run. Write three fixtures: clean pass, unlicensed success, licensed wrong answer. The harness prints a table and exits non-zero if license rate is below 1 or the answer is wrong, and the exit code distinguishes the two failures so a script can tell them apart.

## Components

| Piece | Role |
| --- | --- |
| Plan file | Checklist items with tool names. |
| Transcript file | Actions and a final answer. |
| License rows | One verdict per action. |
| Separate exit codes | License failure and answer failure are different statuses. |

## How it works

1. Implement the scorer as a pure function of the two files.
2. Score the three fixtures and save the tables.
3. Assert the unlicensed-success fixture fails only the license status.
4. Assert a missing plan raises rather than returning a perfect license rate.
5. Document the two metrics in `score_notes.md`.

## Tech stack

- Python 3.11 or newer
- JSON fixtures
- No model calls inside the harness

## Setup

1. Create `plan-license/` with `score.py`, `fixtures/`, and tests.
2. Run the three fixtures.
3. Run tests.
4. Confirm the harness does not import the agent loop. It only reads files the loop already wrote.

## What done looks like

- License rate and answer correctness are both reported.
- The unlicensed success and the licensed failure produce different statuses.
- A missing plan is an error.
- The scorer has no network access and no model import.

## Step ahead

A later call can repair an earlier unlicensed lookup, and a single license rate hides the recovery. Extend the row with `repaired_by`, the later action id that produced the gold answer, and report two rates: licensed actions, and unlicensed actions that were never needed for the gold quote. Fixture a transcript where an unlicensed call's result is unused because a later licensed call quotes the gold span. The follow-on question is whether the stray call was load-bearing. If you cannot tell from the transcript, the transcript is missing the field that would say so, and that gap belongs in the notes.
