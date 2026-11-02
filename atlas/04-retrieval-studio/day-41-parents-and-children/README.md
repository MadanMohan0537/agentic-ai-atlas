# Parents and Children

**Day 41** · **Intermediate** · Phase 04: Retrieval Studio

Search small child chunks, then expand to the parent section before you quote.

## Concept

Small chunks retrieve sharply and quote poorly, because the sentence that matched is missing its condition. Large chunks quote with context and retrieve poorly, because the vector or the BM25 score is diluted. This project stores both. Child chunks are the search units. Each child points at a parent, which is the heading section that contained it. Retrieval returns children. The quoter from Day 40 reads the parent text, while the citation still records the child id that won retrieval and the parent id that supplied context. You will construct one question where the child match is a pronoun or a short rule, and the condition lives in the previous paragraph inside the parent. Quoting only the child must be incomplete, and quoting from the parent must include the condition. That pair of quotes is the artifact.

## Approach

Build the parent as the heading chunk from Day 33, and the children as smaller windows inside it, each storing `parent_id`. Search children with BM25. Expansion replaces the text handed to the quoter, not the id used for gold-rank calculations. Gold rank stays on the child, so you do not take credit for retrieving a giant section. Add a test that a child from edition 2024 does not expand to a parent from edition 2026 even if someone wires the ids wrong. Parent and child must share edition. Write `expansion.md` with the child-only quote and the parent quote for the pronoun question.

## Components

| Piece | Role |
| --- | --- |
| Child records | Small searchable slices with a parent id and an edition. |
| Parent records | Heading sections keyed by id and edition. |
| Expansion step | Quoter sees parent text; gold rank stays on the child. |
| Edition guard | Refuses to expand across editions. |

## How it works

1. Generate parents and children from the handbook.
2. Plant the pronoun question and mark the child offsets and the parent offsets separately.
3. Retrieve children and expand.
4. Run the quoter twice: once on child text, once on parent text.
5. Assert the cross-edition expansion is rejected.

## Tech stack

- Python 3.11 or newer
- BM25 search on children
- The quote checker from Day 40

## Setup

1. Create `parent-child/` with `build_hierarchy.py` and tests.
2. Write the pronoun example into the handbook if it is not there.
3. Run both quoters and save `expansion.md`.
4. Run the edition-guard test.

## What done looks like

- The notes show a child quote that misses the condition and a parent quote that includes it.
- Gold rank is computed on child ids.
- Cross-edition expansion fails the test.
- Every child record has a parent that exists in the same edition.
