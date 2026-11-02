# Compress Before You Prompt

**Day 47** · **Advanced** · Phase 04: Retrieval Studio

Extract the sentences that overlap the query before anything is shown to a generator, and measure what you dropped.

## Concept

Stuffing five parent sections into a prompt spends the context window on instructions for docks the user did not ask about, and it gives a generator more room to stitch unrelated numbers. This project compresses each retrieved parent to the sentences that pass the Day 40 coverage score, in their original order, with offsets preserved. If no sentence passes, the parent is dropped, not replaced with a summary you invent. You will measure, on the gold questions, how many characters you removed and whether every gold offset still intersects the compressed text. A compression that deletes the gold span is a failed compression even if the remaining text looks focused. You will also run one question where the answer is the absence of a sentence — a rule that only appears as a header plus a table — and show that sentence-level compression can delete the header. That case sets up the fix.

## Approach

Compression is a pure function of the parent text, the query, and the threshold. It does not call a generative model. Output is a list of kept spans with offsets. The coverage metric against gold is: a gold offset range is preserved if any kept span overlaps it. Report per-question preservation and the character reduction ratio. The header-loss fixture is a table chunk from Day 43 passed through a sentence splitter that does not understand tables. You will see it fail, write the failure down, and only then special-case chunks whose metadata says `table` so they bypass sentence compression and pass through whole. The bypass is the patch. The failed run stays in the notes.

## Components

| Piece | Role |
| --- | --- |
| Sentence compressor | Keeps sentences above the coverage threshold, in order. |
| Preservation check | Gold offsets still overlap a kept span. |
| Reduction ratio | Characters kept divided by characters retrieved. |
| Table bypass | Chunks tagged as tables skip sentence dropping, added after the fixture fails. |

## How it works

1. Implement compression without the table bypass.
2. Run the gold questions and the table fixture. Record preservation.
3. Write the table failure into `compression.md`.
4. Add the bypass for `kind=table` and rerun. Append a second results row.
5. Test that a non-table parent still drops a sentence below threshold.

## Tech stack

- Python 3.11 or newer
- Coverage scorer from the quoter
- Parent texts and gold offsets

## Setup

1. Create `compress/` with `compress.py` and tests.
2. Run the before-bypass measurement and save it.
3. Add the bypass and run again.
4. Do not delete the before numbers.

## What done looks like

- Preservation and reduction are reported per question.
- The table-loss failure is documented before the bypass exists in the results history.
- A non-table low-coverage sentence is still dropped, and a test proves it.
- Kept spans carry source offsets.

## Step ahead

Sentence coverage keeps boilerplate that shares many words with the query and drops a short sentence that actually states the exception. Add a second keep rule for sentences that contain a negation cue you list, such as "unless" or "not", when they sit in a parent that already has a kept sentence. Measure how many extra characters that rule admits on the gold set and whether any gold span is saved that coverage alone dropped. If the cue list fires on every parent, the list is too broad and the step-ahead result is a narrower list, not a larger prompt.
