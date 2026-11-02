# Chunks that Respect Questions

**Day 33** · **Intermediate** · Phase 04: Retrieval Studio

Split a staff handbook into chunks and show a question that breaks when the answer straddles a cut.

## Concept

Retrieval fails before search exists if the chunk boundary cuts the only sentence that answers the question. This project writes a short Harbor Loop staff handbook as eight markdown files: hours, fees, weather closures, lost-bike procedure, and so on. You will split them with a fixed character window and an overlap, then write ten questions by hand whose answers you can point to. At least two questions must require a sentence pair that a naive window separates. You will record, for each question, the chunk ids a human says are necessary. That labeled file is the gold set for the rest of the phase. Do not generate the questions with a model and then grade the model against them. You wrote the handbook, and you should write the questions. The artifact is `chunks.jsonl` plus `questions.jsonl` with the character offsets of the supporting spans.

## Approach

Chunk on character windows first, because the failure is easier to see than with a clever splitter. Record start and end offsets into the source file so a later citation can highlight the original text. Overlap by a fraction you declare, such as one fifth of the window. After you have seen a straddling question fail, add a second splitter that prefers markdown headings and paragraph breaks, and compare the gold chunk ids. Keep both chunk files. The heading splitter is not automatically better: a long section can still bury the answer. The comparison table is the deliverable, not a claim that semantic chunking is solved.

## Components

| Piece | Role |
| --- | --- |
| Handbook | Eight markdown files you wrote. |
| Window chunker | Fixed size, overlap, source offsets. |
| Heading chunker | Splits on headings and paragraphs, with a max size. |
| Gold questions | Ten questions with the supporting offsets marked by you. |

## How it works

1. Write the handbook. Include one answer that is a pair of sentences in different paragraphs.
2. Run both chunkers.
3. Write ten questions and mark supporting offsets against the source, not against a chunk you hope will match.
4. For each question, list the window chunks and the heading chunks that overlap the gold offsets.
5. Note the questions where the window chunker splits the gold span across two chunks and the heading chunker does not, or the reverse.

## Tech stack

- Python 3.11 or newer
- Standard library `pathlib` and `json`
- Markdown handbook you authored

## Setup

1. Create `chunking/` with `handbook/`, `chunk.py`, and `questions.jsonl`.
2. Run both chunkers into `out/window.jsonl` and `out/heading.jsonl`.
3. Add a test that every chunk's text equals the source slice for its offsets.
4. Keep questions free of answers that the handbook does not contain. Those have a later day.

## What done looks like

- Offsets round-trip to the source text in a test.
- Ten questions have gold offsets.
- The comparison note names at least one straddling question.
- Both chunk files are kept, and neither is silently overwritten.
