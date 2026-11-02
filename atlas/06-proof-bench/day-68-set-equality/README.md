# Set Equality for Extractions

**Day 68** · **Advanced** · Phase 06: Proof Bench: Evals and Harnesses

Score extracted dock lists as sets with numeric tolerance, not as strings.

## Concept

An extractor that returns docks `["B", "A"]` and a gold list `["A", "B"]` is correct, and a string equality check will say it is not. A fee of 14.0 against a gold of 14 is the same story. This project scores extraction outputs as structured values. A list field is compared as a set. A number field allows a tolerance you declare per field, defaulting to zero. Extra ids are false positives. Missing ids are false negatives. You will report precision and recall over the items, plus an exact-match rate after normalization. The harness reads JSONL of predictions and gold. It does not call a model. You will include a fixture that string-matches poorly and set-matches perfectly, and one that set-matches poorly because of a single extra dock the string check might have partially credited.

## Approach

Define a small target schema: `docks` as a list of strings and `fee` as a number or null. Normalization trims strings and sorts nothing in the output you store; sorting is only inside the comparison, so you do not destroy the model's order before you have scored it. Tolerance lives in `tolerances.json`. A missing field is a false negative for that field, not a crash, and it is counted. Write `score.json` with per-case notes and a micro precision and recall across dock items. Exact string match can be reported as a diagnostic and must not be the headline number.

## Components

| Piece | Role |
| --- | --- |
| Normalizer | Trim and type-check without discarding order in the stored prediction. |
| Set comparator | Item precision and recall for list fields. |
| Numeric tolerance | Per-field absolute tolerance. |
| Diagnostic string match | Present, and not the headline. |

## How it works

1. Write five gold and prediction pairs, including the order swap and the extra dock.
2. Score them and write `score.json`.
3. Assert the order swap has item recall 1 and string match 0.
4. Assert the extra dock reduces precision and not recall.
5. Assert a fee of 14.0 matches gold 14 when tolerance is 0, because you normalize ints and floats that are equal.

## Tech stack

- Python 3.11 or newer
- JSONL cases
- No model

## Setup

1. Create `set-score/` with `score.py`, `cases.jsonl`, and tests.
2. Run the scorer.
3. Run tests.
4. State in the notes which number you would quote and why the string diagnostic is not it.

## What done looks like

- Order differences do not reduce set recall.
- Extra items reduce precision.
- Tolerances are configured per field, not hard-coded in the comparison loop.
- The headline metrics are item precision and recall.

## Step ahead

Flat sets miss nested structure. Add a path-level score for one nested field, `fees_by_dock`, a map from dock id to amount. A mismatch should name the path, such as `fees_by_dock.A`, rather than failing the whole object as one bit. Fixture a map that is right on dock A and wrong on dock B and show a score that is not zero and not one. The follow-on is a diff a person can fix from, not a single similarity float.
