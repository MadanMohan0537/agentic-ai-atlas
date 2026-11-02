# Overfit a Short Text on Purpose

**Day 27** · **Intermediate** · Phase 03: Transformer Workbench

Train a character-level transformer until it memorizes a short text you wrote, and show the memorized continuation.

## Concept

A model that cannot memorize one page is not ready for a conversation about generalization. This project trains a tiny causal transformer, character level so the tokenizer cannot take the credit, until training loss collapses on a text of a few hundred characters you write. You will sample a continuation from a prefix of that text and show that it reproduces the source. Then you will sample from a prefix that never appeared and show the garbage or the groove the model falls into. Both outputs go in the notes. Memorization is the success criterion today. If you stop early because the samples "look creative," you have skipped the evidence that the training loop, the mask, and the loss are wired together. Creativity is a later conversation, and it requires a model that can also overfit when you ask it to.

## Approach

Use your block, two layers, model dim 32, two heads, context length covering the whole text so the task is not artificially hard. Optimize with a hand-written SGD or Adam update on one sequence, or on chunks if you prefer, but keep the full text in the training set. Teacher forcing: predict the next character at every position. Loss is mean cross-entropy. Train until the loss is near zero or until a step cap you set only after you have seen a curve that flattened. Sample with greedy decoding for the memorization check so randomness does not excuse a miss. The unseen prefix can be a single character that appears in the text but starts a different continuation than the one you request. Record both samples unedited.

## Components

| Piece | Role |
| --- | --- |
| Character vocabulary | Every character in the text, plus a stop symbol if you need one. |
| Tiny causal model | Two blocks, trained with next-character loss. |
| Greedy memorization sample | A prefix from the text and the reproduced continuation. |
| Unseen-prefix sample | The same decoder on a prefix the text does not contain as a start. |

## How it works

1. Write `text.txt`, a few hundred characters of original prose.
2. Train and log loss every few steps to `loss.csv`.
3. Greedy-sample from a 20-character prefix taken from the text and compare to the source continuation.
4. Greedy-sample from a prefix you invent and paste the raw output.
5. Assert the training loss decreased from the first logged step to the last on this run, and store the curve.

## Tech stack

- Python 3.11 or newer
- NumPy, or PyTorch if you want autograd and you pin it
- A text you wrote

## Setup

1. Create `memorize/` with `train.py` and `text.txt`.
2. If you switch to PyTorch, use it for autograd only and keep your block's structure visible in the module code.
3. Run training until memorization or until you hit a cap and the notes explain the miss.
4. Save `samples.md` with both outputs and the final loss.

## What done looks like

- The in-text prefix continuation matches the source for a length you declare, or the notes show the exact mismatch and the loss.
- The unseen-prefix sample is pasted unedited.
- The loss curve file exists and ends lower than it starts, or you explain the failed run.
- The context length and depth are written at the top of the notes.
