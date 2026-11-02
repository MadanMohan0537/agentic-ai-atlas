# Quote or Abstain

**Day 40** · **Intermediate** · Phase 04: Retrieval Studio

Answer with a quotation from a retrieved chunk, or refuse, when the handbook does not contain the fact.

## Concept

A retrieval stack that always answers will invent a fee when the handbook is silent. This project draws a hard line. The answer is either a quotation copied from a retrieved chunk, plus the chunk id and offsets, or an abstention with a reason. Paraphrase is out of scope for the required path, because paraphrase makes grading mushy and makes fabrication easy. You will implement a local answerer that selects the highest-scoring sentence that covers the query tokens, and abstains when the coverage is below a threshold you set before looking at a new holdout. The holdout includes three questions whose answers are not in the handbook at all. Those must abstain. A question that quotes the wrong edition is also a failure even if the words are confident.

## Approach

Split candidate chunks into sentences. Score a sentence by the fraction of query tokens it contains, excluding a tiny stoplist. The threshold lives in `threshold.txt` with a one-line justification written before you run the holdout. The gold questions from earlier days are the development set. The three unanswerable questions are the holdout, and you do not tune the threshold after seeing them. If you fail them, you report the miss and adjust in a follow-up run that you label as such. Output JSON has `status` of `quote` or `abstain`, and quotes must be exact substrings of the cited chunk. A test tampers with a quote character and expects rejection.

## Components

| Piece | Role |
| --- | --- |
| Sentence splitter | Breaks a chunk without dropping the source offsets. |
| Coverage scorer | Query-token fraction with a stoplist. |
| Threshold file | A number justified before the holdout run. |
| Exact-quote check | The returned string is a substring of the cited chunk. |

## How it works

1. Write the threshold and the justification.
2. Run the ten gold questions and record quotes or abstentions.
3. Freeze the threshold. Run the three unanswerable questions.
4. Reject any quote that is not an exact substring.
5. Write `answers.md` with the unanswerable outcomes called out.

## Tech stack

- Python 3.11 or newer
- Retrieved shortlists from the previous day
- No required generative model

## Setup

1. Create `quote-or-abstain/` with `answer.py`, `threshold.txt`, and the holdout file.
2. Run development questions, then holdout.
3. Add the tamper test.
4. If you optionally attach a generative model, it may only choose among sentences the retriever returned, and the exact-substring check still applies.

## What done looks like

- Every quote passes the substring test against the cited chunk.
- The three unanswerable questions were not used to pick the threshold.
- Abstentions include a reason code, such as `low-coverage`.
- A tampered quote fails the test.
