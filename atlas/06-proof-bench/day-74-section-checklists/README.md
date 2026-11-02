# Section Checklists for Long Answers

**Day 74** · **Advanced** · Phase 06: Proof Bench: Evals and Harnesses

Score a long answer by required sections, forbidden claims, and numbers that must trace to a table.

## Concept

Some answers are not a single span. A lost-bike reply should contain a section for what happened, a section for the fee, and no promise of a replacement bike the handbook does not make. This project scores long answers with a checklist file: required headings, forbidden phrases, and a table of numbers that must appear in both the answer and a cited table chunk. The scorer is deterministic. It does not ask a model whether the answer "covered the spirit" of a section. A missing heading is a miss. A forbidden phrase is a miss even if every heading is present. A number in the answer that is not in the cited table is a miss. You will write one gold answer that passes and two that fail for different reasons.

## Approach

Headings are markdown `##` lines matched to a required list. Order is required unless the checklist says `order: free`. Forbidden phrases are case-sensitive literals so you do not accidentally ban a substring of a legitimate word. Choose phrases long enough to be specific. Numbers are extracted with a regex and compared to the table chunk's numbers as a set. The report lists missing headings, forbidden hits, and unknown numbers separately. A single boolean pass is the conjunction, and the report must still show the parts when it fails.

## Components

| Piece | Role |
| --- | --- |
| Checklist file | Headings, forbidden phrases, and a cited table id. |
| Heading matcher | Exact heading strings, with optional order. |
| Forbidden list | Literal phrases. |
| Number trace | Every number in the answer appears in the cited table. |

## How it works

1. Write the checklist and the table chunk.
2. Score the passing answer.
3. Score an answer missing a heading and one containing a forbidden promise.
4. Score an answer whose fee number is not in the table.
5. Assert the three failure reports name different reason groups.

## Tech stack

- Python 3.11 or newer
- Markdown answers and a JSON checklist
- No model judge

## Setup

1. Create `checklists/` with `checklist.json`, `answers/`, and `score.py`.
2. Run all four answers.
3. Run tests.
4. Keep the passing answer free of extra numbers you did not intend.

## What done looks like

- The passing answer passes all three groups.
- Each planted failure trips a different group, and the report shows which.
- Forbidden matching is literal and covered by a test that a short token does not ban a longer innocent word.
- The conjunction pass is not the only field in the report.

## Step ahead

A missing section and a weak section are different. Add partial credit per heading: full credit when the section contains at least one number traced to the table or an explicit `not-in-handbook` token, and zero when the heading is present but the body is empty. Fixture an empty section. The follow-on score distinguishes absence from a heading with nothing under it, and the notes say you still do not grade prose quality.
