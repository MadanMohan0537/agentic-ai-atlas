# Recall at K, Written Down

**Day 46** · **Advanced** · Phase 04: Retrieval Studio

Freeze a retrieval eval file and report recall at five and at twenty, with a denominator you can recount.

## Concept

You have been watching individual questions. A phase needs a number that does not move just because you remember a favorite example. This project freezes an evaluation file: question id, question text, and the set of gold chunk ids. It runs the current retrieval stack and reports recall at 5 and recall at 20. Recall is the fraction of gold ids that appear in the top k, averaged per question and also reported as a micro average over gold ids. Those two averages answer different questions, and you will show a case where they diverge by writing one question with three gold chunks and several with one. You will not tune the stack against this file after the first measurement. If you change the stack, you add a new row to a results table rather than replacing the old number. The history is the point.

## Approach

Copy questions into `eval/retrieval.jsonl` and treat that file as append-only in spirit: a changed gold set is a new file version in the name, `retrieval_v2.jsonl`, not an edit. The runner reads a versioned config naming the retriever. Metrics code is separate from retrieval code so a test can score a fake ranking. Include a question with empty gold and define the metric: it is excluded from recall, and counted in a separate `no-gold` tally, because a silent zero would punish abstentions you wanted. Write `eval_report.md` with both averages, the tally, and the config name.

## Components

| Piece | Role |
| --- | --- |
| Frozen eval file | Question ids and gold chunk id sets. |
| Metric function | Macro and micro recall at k, tested on a fake ranking. |
| No-gold tally | Questions excluded from the denominator, counted aside. |
| Results table | Append-only rows of config name and scores. |

## How it works

1. Assemble the eval file from the questions you trust. Drop any you are unwilling to stand behind.
2. Score a hand-built ranking in a unit test: one hit of two gold ids is recall 0.5 on that question.
3. Run the real stack once and append a results row.
4. Change a single, named setting, run again, and append a second row. Do not delete the first.
5. Note which average you would quote to a teammate and why.

## Tech stack

- Python 3.11 or newer
- The retrieval stack you have been building
- JSONL eval file

## Setup

1. Create `recall-eval/` with `eval/retrieval_v1.jsonl`, `metrics.py`, and `run_eval.py`.
2. Run the unit test for the metric before the real run, so a bug in retrieval does not look like a bug in recall.
3. Run the stack twice with two configs if you have a real knob. If you do not, run the same config twice and show the rows match.
4. Write the report.

## What done looks like

- Macro and micro recall are both present, and the unit test locks a hand-computed value.
- Questions with no gold are excluded and tallied.
- The results table has more than one row or a documented second run that matches the first.
- The eval file's version is in the report.

## Step ahead

Recall does not know whether the chunk that matched is the stale edition. Add an edition-conditioned recall that counts a hit only when the chunk's edition equals the case edition on the eval row. A ranking that surfaces the right words in the wrong edition must not increase the score. Put three rows in a fixture where the text matches and the edition does not, and show the conditioned recall fall while the unconditioned recall stays high. That gap is the number you would add to the results table before calling the stack ready for the casework in Day 42.
