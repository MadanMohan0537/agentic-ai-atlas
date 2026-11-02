# Borderline Entity Matches

**Day 89** · **Advanced** · Phase 07: Flowroom: Analytics and Pipelines

Match rider records across two files with a score, and send only the borderline band to a review sheet.

## Concept

Two exports call the same rider different names. A greedy match will either merge strangers or drop true pairs. This project scores candidate pairs from two files using rules you can read: exact email, exact phone, and a normalized name similarity you implement with a simple token Jaccard. High scores auto-link. Low scores are ignored. A middle band is written to `review.csv` with the two ids, the score, and the reason codes that fired. You do not auto-link the middle. You will plant one true pair that differs by a nickname and one false pair that shares a last name only. The true pair should land in review or in auto-link according to thresholds you set before seeing the result, and the false pair must not auto-link. The review file is the product. A silent merge is the failure.

## Approach

Blocking: only compare pairs that share a phone, an email, or a last-name token, so you do not score the full cross product. Say so, because blocking can miss a pair with no shared token. Plant one true pair with no shared block key and show it absent from review. That miss belongs in the notes. Thresholds live in `thresholds.json` with `auto` and `review` cutoffs. Auto requires the score to be greater than or equal to `auto`. Review is the half-open band `[review, auto)`. Below `review` is drop. A test constructs three scores and expects three different destinations.

## Components

| Piece | Role |
| --- | --- |
| Blocker | Candidate pairs that share a strong token. |
| Scorer | Email, phone, and token Jaccard, combined by rules you write down. |
| Thresholds | Auto, review, and drop. |
| Review sheet | Borderline pairs only. |

## How it works

1. Write two small files with the planted pairs, including the unblockable true pair.
2. Generate candidates and scores.
3. Route each candidate to auto, review, or drop.
4. Assert the last-name-only pair is not auto-linked.
5. Assert the unblockable true pair appears in a `missed_blocks` note and not in the review sheet.

## Tech stack

- Python 3.11 or newer
- CSV and JSON
- No external matching library

## Setup

1. Create `entities/` with `left.csv`, `right.csv`, `match.py`, and tests.
2. Set thresholds before the run you will quote.
3. Run the matcher.
4. Run tests.

## What done looks like

- The three destinations are tested with constructed scores.
- The false pair is not auto-linked.
- The review sheet contains only the middle band.
- The unblockable true pair is reported as a block miss, not quietly dropped.

## Step ahead

Review decisions should feed the next run. Add `decisions.csv` with pair id and `link` or `reject`, and make the matcher honor a decision even when the score would have routed the pair differently. A later score change must not auto-link a pair a human rejected. Fixture a rejected pair whose score rises above the auto threshold and assert it stays unlinked, with reason `human-reject`. The follow-on is a decision that outranks the score.
