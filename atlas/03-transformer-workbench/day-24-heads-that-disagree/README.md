# Heads that Disagree

**Day 24** · **Intermediate** · Phase 03: Transformer Workbench

Run two attention heads on one sentence and show that their weight patterns are not copies.

## Concept

Multi-head attention is often described as "looking at different things," and then implemented as a reshape nobody inspects. This project builds two heads with separate projections on a single sentence you embed with a fixed, seeded random projection from token ids. You will print both weight matrices and write what each head concentrates on. If they match, you have not failed the day, but you must change the initialization or the sentence until you can say whether the heads are redundant. You will also implement the output projection that concatenates head outputs and maps them back to the model dimension, and check the shape on a sequence. The lesson is the contrast between heads and the shape contract, not a claim that heads have human-readable jobs in a large model. In a tiny random model they mostly do not. Say that plainly if the patterns are noise.

## Approach

Use model dimension 8 and two heads of dimension 4, so concatenation returns to 8 before a square output projection. Initialize projections with a seeded normal and a scale you write down. Share the same token vectors across heads. After computing both weight matrices, measure their mean absolute difference. A difference near zero means the heads collapsed. You may reseed once and record both seeds. Do not train today. This is a shape and interpretation exercise. The output projection is a matrix multiply you test with a known input so a reshape bug cannot hide behind attention weights that happen to look plausible.

## Components

| Piece | Role |
| --- | --- |
| Token vectors | Seeded random projection from a short sentence. |
| Two heads | Independent Q, K, V projections. |
| Disagreement note | Mean absolute difference of the two weight matrices and a sentence of interpretation. |
| Output projection | Concatenation checked by shape and by a known multiply. |

## How it works

1. Tokenize a sentence of at least six tokens with your Day 21 encoder or with whitespace plus a tiny vocab.
2. Project tokens and run both heads with a causal mask.
3. Write both matrices and the mean absolute difference.
4. Concatenate outputs and apply the output projection. Assert the shape equals (time, model dim).
5. Test the projection math on a 1 by 8 vector you multiply by hand.

## Tech stack

- Python 3.11 or newer
- The attention function from Day 23
- NumPy or pure Python, consistent with Day 23

## Setup

1. Create `multi-head/` and import or copy `attention.py`.
2. Run `python3 heads.py` and fill `heads.md` from the printout.
3. Run tests for shape and for the known multiply.
4. If the heads match to many decimals, record the seed and try one more. Keep both notes.

## What done looks like

- Both weight matrices are in the notes, with the mask visible in the upper triangle.
- The mean absolute difference is a number, not an adjective.
- The output shape test passes.
- The notes say whether you believe the heads specialized, and the evidence is the matrices, not a diagram from a blog.
