# A Frozen Encoder and a Small Head

**Day 30** · **Intermediate** · Phase 03: Transformer Workbench

Freeze a tiny encoder and train a linear head to classify your own labeled sentences.

## Concept

Not every use of a transformer is next-token training. A common pattern freezes a representation and trains a small classifier, which is cheaper and easier to explain. This project builds a tiny bidirectional encoder — the same block with the causal mask removed — or reuses your causal model by taking the final hidden state. You will freeze those parameters. On top you will train a linear head to classify sentences you label into two classes you define, such as `maintenance` versus `billing`, twenty examples each, written by you. The baseline is a bag of character frequencies with its own linear head. If the transformer does not beat the bag on a held-out set of your sentences, the card says so. With this little data, the bag will often win. That result is welcome. It keeps the phase honest before you touch a pretrained model.

## Approach

Split by sentence id, not by token. Train only the head: a check of parameter ids, or a numerical check that encoder weights are identical before and after, must pass. Use the same log-loss training loop you trust. Evaluate accuracy and, because the set is small, list every held-out sentence with its prediction and label in `errors.md`. Do not claim a general encoder. The write-up's last sentence should state how many held-out sentences you have, because a perfect score on four sentences is a conversation, not a result.

## Components

| Piece | Role |
| --- | --- |
| Frozen encoder | Parameters unchanged by head training. |
| Linear head | A map from one vector to two logits. |
| Bag baseline | Character frequencies and its own linear head. |
| Held-out listing | Every test sentence, prediction, and label. |

## How it works

1. Write forty labeled sentences and a split file.
2. Train the bag baseline and record held-out accuracy.
3. Train the head on frozen representations.
4. Assert encoder parameters did not change.
5. Write the held-out listing and a three-line comparison.

## Tech stack

- Python 3.11 or newer
- Your block, with the mask configurable
- A labeled file you wrote

## Setup

1. Create `frozen-head/` with `data.jsonl`, `train_head.py`, and tests.
2. Run both models.
3. Run the freeze test, which should fail if you forget to stop gradients or if you copy weights back incorrectly.
4. Keep the sentence count in the notes.

## What done looks like

- Encoder weights match a checksum taken before training.
- The bag baseline number is next to the transformer number.
- Every held-out sentence is listed with prediction and label.
- The notes state the held-out count in the first paragraph.
