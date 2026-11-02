# A Small Model for a Narrow Label

**Day 94** · **Advanced** · Phase 08: Frontier Lab

Train a tiny local classifier on labels from a teacher script, and list the cases where the student disagrees.

## Concept

A large model is an expensive way to map a dock note to `maintenance` or `billing` if a small classifier can do it. This project writes a teacher as a rule list that labels notes, trains a bag-of-words logistic model or a linear model you already built, and compares the student to the teacher on a held-out set of notes you wrote. The teacher is not a hosted model and not a synthetic-data release. It is a stand-in with known rules, so you can see the student's errors. You will report agreement, and you will list every disagreement with the note text. You will not claim the student is safe to deploy. You will say what the student is allowed to do: suggest a label next to the note, with the disagreement list as the review queue.

## Approach

The teacher rules are ordered and readable. The student trains only on the train split. The test split is notes the training loop never sees. Use the rider-level or note-level split you already understand, and do not let a near-duplicate sit in both splits. A test plants a duplicate and expects the splitter to keep both copies on one side. Agreement is exact label match. The disagreement file is the deliverable a person would read. If agreement is perfect, add notes the rules label for a subtle reason and the bag of words is likely to miss, such as a short negation. Do not stop at a perfect score on easy notes.

## Components

| Piece | Role |
| --- | --- |
| Teacher rules | An ordered, readable labeling function. |
| Student model | A small local classifier trained on the teacher's train labels. |
| Held-out notes | Written by you, disjoint from training. |
| Disagreement list | Every note where student and teacher differ. |

## How it works

1. Write the rules and thirty notes. Split them.
2. Label the train notes with the teacher and fit the student.
3. Score the test notes.
4. Write every disagreement.
5. Assert a planted duplicate cannot land in both splits.

## Tech stack

- Python 3.11 or newer
- Your linear classifier or a few dozen lines of new code
- Local text only

## Setup

1. Create `small-label/` with `teacher.py`, `train.py`, and tests.
2. Run training and the report.
3. Run the duplicate-split test.
4. State the allowed use of the student in the first line of the notes.

## What done looks like

- Train notes and test notes are disjoint, including near-duplicates you planted.
- The disagreement list is complete relative to the test set.
- The teacher rules are readable without running the model.
- The notes name what the student is not allowed to do.

## Step ahead

The student can be confidently wrong. Add a score, the predicted probability, and send only disagreements above a probability you choose to a `priority_review` list. Low-probability disagreements stay in the full list and out of the priority list. Fixture one high-probability miss and one low-probability miss. The follow-on is a review queue ordered by how sure the student was, not a claim that the probability is calibrated.
