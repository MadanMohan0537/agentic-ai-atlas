# Decoding and Its Failure Modes

**Day 29** · **Intermediate** · Phase 03: Transformer Workbench

Compare greedy, temperature, and top-k decoding, and catch a repetition loop on purpose.

## Concept

Decoding is part of the model a user experiences, and it is not the training loss. A memorized transformer will look fluent under greedy decoding on a known prefix and strange under a high temperature. This project adds three decoders to the tiny model: greedy, temperature-scaled softmax sampling, and top-k sampling. You will run each from the same prefix and the same seed where sampling applies. Then you will provoke a repetition loop, either by sampling from a half-trained checkpoint or by constructing a tiny distribution that puts mass on a cycle, and you will implement a repetition breaker you can explain: a ban on repeating the same token more than N times in a row, or a simple frequency penalty. The breaker is not a research claim. It is a switch you can turn off, with a sample on both sides.

## Approach

Temperature divides the logits before softmax. Temperature 0 is not a limit you need to take; call the greedy function instead of pretending zero is a temperature. Top-k sets all but the k largest logits to a large negative number before softmax, and k is at least 1. Seeds apply to the sampler's RNG only. Save three samples from one prefix. For the loop, if your memorized model refuses to loop, use a hand-built logit sequence or a deliberately undertrained checkpoint and say which you used. The breaker must be a flag defaulting to off so the failure remains reproducible.

## Components

| Piece | Role |
| --- | --- |
| Greedy decoder | Argmax at each step. |
| Temperature sampler | Logits divided by a temperature above zero. |
| Top-k sampler | Distribution truncated to k tokens. |
| Repetition breaker | A switch with samples before and after. |

## How it works

1. Load the memorized checkpoint or train a small stand-in.
2. Decode the same prefix three ways and write `samples.md`.
3. Show a repetition failure with the breaker off.
4. Turn the breaker on and decode again from the same seed.
5. Test top-k on a known logit vector: tokens outside the top k receive probability zero.

## Tech stack

- Python 3.11 or newer
- Your tiny transformer
- A seeded RNG for sampling

## Setup

1. Create `decoding/` with `decode.py` and tests for top-k and for temperature-equals-greedy being a separate function.
2. Generate the three samples.
3. Generate the loop pair.
4. Run tests.

## What done looks like

- Three decoders produce written samples from one prefix.
- Top-k assigns zero probability outside the selected set in the unit test.
- The repetition failure and the broken-loop sample are both present, with the flag value named.
- Temperature is never passed as zero.
