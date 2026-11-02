# Double Annotation and Agreement

**Day 08** · **Beginner** · Phase 01: Field Notes: Data & Measurement

Label the same support notes twice, measure agreement, and fix the guideline where you disagreed.

## Concept

You want a later classifier to separate `bike_issue`, `billing`, and `other` in Harbor Loop support notes. The labels are the product. If two careful readers cannot apply the guideline the same way, a model will only freeze the confusion. This project writes a one-page guideline, labels the same twenty notes twice (you can play both annotators if you wait a few minutes and hide the first pass), and computes raw agreement and Cohen's kappa by hand. Wherever you disagreed, you rewrite the guideline with an example. You do not train a model. The artifact is a guideline that got stricter because of a disagreement, plus a second labeling pass whose agreement you also report. That second number is allowed to be imperfect. Hiding a disagreement is the failure.

## Approach

Put notes in `notes.jsonl` with ids. Store labels in `pass1.json` and `pass2.json` mapping id to label, so you cannot silently edit pass 1 after seeing pass 2. Implement a confusion matrix among the three labels and kappa from the formula: agreement relative to chance, using the observed label margins. Where the two passes differ, append a row to `disagreements.md` with the note id, both labels, and the sentence you added to the guideline. Then label a fresh ten notes twice under the revised guideline and report that agreement separately. Do not average it into the first number.

## Components

| Piece | Role |
| --- | --- |
| Guideline | Definitions, two positive examples per class, and one near-miss. |
| Blind passes | Two JSON maps that you do not edit in place. |
| Agreement math | Confusion counts, raw agreement, and kappa. |
| Guideline patch | A new example born from a specific disagreement. |

## How it works

1. Write the guideline before labeling. Keep it under a page.
2. Label twenty notes into `pass1.json`. Start `pass2.json` only after pass 1 is written.
3. Compute the matrix and kappa. A test can lock kappa for a fixture pair you construct, separate from your real notes.
4. Record each disagreement and amend the guideline.
5. Label ten new notes twice and write both agreement numbers in `report.md`.

## Tech stack

- Python 3.11 or newer
- Standard library `json`
- Markdown guideline

## Setup

1. Create `double-annotation/` with the notes, the guideline, and `agree.py`.
2. Add a unit test with a hand-computed kappa on a 6-item fixture so the formula is checked without your real labels.
3. Run `python3 agree.py --a pass1.json --b pass2.json`.
4. If your two passes agree perfectly, you picked notes that are too easy. Add three borderline notes and label again. Perfect agreement on toys teaches nothing.

## What done looks like

- Kappa on the hand-computed fixture matches the value you calculated on paper.
- At least one guideline change cites a note id and the two labels.
- The first-pass agreement and the revised-guideline agreement are reported separately.
- Label files are maps from id to label, and a test rejects a label outside the three classes.
