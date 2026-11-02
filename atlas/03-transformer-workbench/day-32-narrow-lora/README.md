# A Narrow Low-Rank Update

**Day 32** · **Advanced** · Phase 03: Transformer Workbench

Adapt a tiny pretrained-by-you model with LoRA on one style task, and show a rank that is too small.

## Concept

Full fine-tuning copies every weight for a task that may need a nudge. A low-rank update adds a pair of small matrices to a linear map and trains only those. This project takes the tiny model you already trained and adapts it so continuations prefer a house style you define, such as ending every completion with a fixed sign-off you invent. You will implement LoRA on one linear layer: the update is B times A, with A and B much narrower than the layer, scaled by a constant. Base weights stay frozen, and a checksum proves it. You will train at rank 1 and at a higher rank you choose, and you will report how often the sign-off appears in greedy samples from a shared prefix list. The base model without adaptation is the control. The day is successful when you can say what the low-rank update changed and what it did not, including a prefix the adaptation should leave alone.

## Approach

Choose a single projection inside the MLP or the attention output. Initialize A with small random values and B at zero so the update starts at zero and the model behavior matches the base checkpoint at step 0. A test locks that. Train on a handful of style examples you write, in the chat template if you have it. Evaluate on ten prefixes: five that should gain the sign-off and five control prefixes where adding the sign-off would be a failure, such as a prefix that asks for a station code only. Report both rates at both ranks. Do not download a large instruction model. The mechanism is the same on the tiny net, and the failure modes are easier to see. If you later swap in an open model, keep this harness.

## Components

| Piece | Role |
| --- | --- |
| LoRA pair | Low-rank A and B on one frozen linear map, scaled. |
| Zero-at-init test | B starts at zero, so outputs match the base model. |
| Style data | Short examples you wrote that demonstrate the sign-off. |
| Two-rate report | Sign-off rate and control-prefix false rate, at two ranks. |

## How it works

1. Implement the wrapped linear layer and the zero-at-init test.
2. Checksum the base weights, train rank 1, and checksum again.
3. Sample the ten prefixes greedily.
4. Repeat at the higher rank from the same base checkpoint, not from the rank-1 weights.
5. Write `lora_report.md` with both rates and one sample that shows a miss.

## Tech stack

- Python 3.11 or newer
- Your tiny transformer and checkpoint code
- No external LoRA library

## Setup

1. Create `narrow-lora/` with `lora.py`, `style.jsonl`, and the prefix list.
2. Run both ranks.
3. Run the zero-init and freeze tests.
4. Keep the base checkpoint read-only.

## What done looks like

- At step 0, LoRA outputs match the base model on a fixture batch.
- Base weight checksums match before and after training.
- The report includes both ranks and the control prefixes, not only the style successes.
- One miss is pasted unedited.

## Step ahead

The follow-on is forgetting. After the style update, measure greedy continuation quality on the original memorization prefixes from Day 27. A rank that nails the sign-off and wrecks the original text has not adapted the model. It has replaced a behavior. Add a second task, a different sign-off, trained after the first, and report whether the first sign-off survives. If it does not, try a smaller learning rate or a higher rank and record which lever you moved. The design you want is one that names, before training, which old behavior is in scope to keep.
