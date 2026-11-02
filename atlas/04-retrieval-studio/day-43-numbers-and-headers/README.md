# Numbers that Stay with Their Headers

**Day 43** · **Intermediate** · Phase 04: Retrieval Studio

Chunk a fee table so a cell is never separated from the column header that gives it a unit.

## Concept

A markdown table of fees becomes dangerous when a chunker cuts between a header and a cell. The retriever returns "14" and the quoter says fourteen dollars, or fourteen minutes, or fourteen days. This project adds a table-aware chunker. Each row chunk includes the header row text, the row label, and the cell, and it records the column name as metadata. You will plant a question — "what is the late fee for a cargo bike" — and show a naive window that can return the cargo-bike row without the header. The table-aware chunk must contain both the column name and the number. Quoting that chunk passes an assertion that the column name is present. This is structure-aware indexing, not a spreadsheet product.

## Approach

Parse a simple GitHub-style markdown table yourself: header, separator, rows. Do not accept merged cells. Each data row produces one chunk per numeric cell, and the chunk text is a rendered sentence you control, such as "Late fee | cargo bike | 14 USD", built from the header and the row label. The original table is also stored so you can show it. The naive window chunker runs on the raw markdown for contrast. A test checks that every numeric chunk contains its column header string. A second test feeds a ragged row and expects a rejected table, not a shifted column.

## Components

| Piece | Role |
| --- | --- |
| Table parser | Header plus rows, rejecting ragged lines. |
| Cell chunks | Header, row label, and value rendered together. |
| Naive contrast | A window chunk that can isolate the bare number. |
| Header assertion | Every numeric chunk contains the column name. |

## How it works

1. Add `fees.md` with a real markdown table, including a cargo-bike late fee.
2. Parse it and emit cell chunks.
3. Run the naive window chunker on the same file.
4. Show one naive chunk that lacks the header, if the window produces one. Adjust the window on a copy of the file only for the demonstration, and label it as a constructed cut if you have to force it.
5. Query the late fee and assert the returned table chunk contains the column name and the row label.

## Tech stack

- Python 3.11 or newer
- A small markdown table parser you write
- The existing quoter's substring check

## Setup

1. Create `tables/` with `fees.md`, `table_chunks.py`, and tests.
2. Run both chunkers.
3. Run the ragged-row test.
4. Write `table_notes.md` with the naive chunk and the cell chunk side by side.

## What done looks like

- A ragged table is rejected.
- Every numeric cell chunk includes its column header, and a test walks all of them.
- The cargo-bike question returns a chunk containing the row label and the column name.
- The notes show the contrast with a headerless fragment.
