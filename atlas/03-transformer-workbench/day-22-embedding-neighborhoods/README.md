# Neighborhoods in Embedding Space

**Day 22** · **Intermediate** · Phase 03: Transformer Workbench

Train skip-gram embeddings on your notes and inspect neighbors, including a pair that should not be close.

## Concept

An embedding is a point you learned from co-occurrence, not a definition. Two station names that share a sentence template will sit near each other even when a rider would never confuse the docks. This project trains a small skip-gram model on the tokenized notes from Day 21, or on whitespace tokens if you want a shorter path. You will look up nearest neighbors for a handful of tokens and write down one neighborhood that is useful and one that is a trap. You will also check a crude analogy, of the kind people demo on stage, and record whether the arithmetic returns anything you would show a teammate. The point of the failed analogy is the point of the day. Geometry that only works in a keynote is not a feature you should describe as understanding.

## Approach

Use a tiny vocabulary, under a few hundred tokens, and vectors of size 16 or 32 so training finishes on a laptop in a short run. Negative sampling can be three draws from the unigram distribution raised to the three-quarter power, which you should implement because it changes what "common word" means. Train for a fixed number of steps with a seed. Nearest neighbors use cosine similarity. Exclude the query token itself. Write `neighbors.md` with five queries. For the analogy, implement `king - man + woman` style arithmetic on tokens you actually have, such as a pair of docks and a pair of time words, and state the top three results. If your corpus is too small for any analogy to be meaningful, say that and do not borrow a pretrained vector file to make the demo prettier.

## Components

| Piece | Role |
| --- | --- |
| Skip-gram trainer | Center and context pairs with negative samples. |
| Cosine lookup | Top neighbors for a query token. |
| Neighbor notes | One useful neighborhood and one trap, with the query named. |
| Analogy probe | Vector arithmetic and the top three tokens, or an explicit refusal. |

## How it works

1. Build pairs from a window of size 2 on either side of each center.
2. Train and save vectors as a JSON map of token to list of floats.
3. Query five tokens and write the notes.
4. Run one analogy using tokens that occur at least five times. If you cannot find such a pair, document the frequency table instead of forcing it.
5. Test cosine of a vector with itself is 1 within tolerance, and that a reversed vector is not the nearest neighbor of the original unless the vocabulary is pathological.

## Tech stack

- Python 3.11 or newer
- Standard library `math` and `random`
- Vectors stored as JSON so you can diff them

## Setup

1. Create `embeddings/` with `skipgram.py` and the corpus.
2. Run training. Log the loss every few hundred steps to see that it moves.
3. Write `neighbors.md` from the actual output, not from memory.
4. Run tests.

## What done looks like

- Five queries have neighbors computed from your vectors.
- The trap neighborhood is a real pair from the output, with a sentence on why closeness is misleading.
- The analogy section either shows top three tokens or explains that the corpus cannot support the probe.
- A self-cosine test passes.
