# Phase 03: Transformer Workbench

Days 21–32. Build the pieces of a transformer until a tiny model overfits a text you wrote, then adapt it with a narrow low-rank update.

| Day | Level | Project | Summary |
| --- | --- | --- | --- |
| 21 | Intermediate | [Byte Pair Literacy](day-21-byte-pair-literacy/README.md) | Train a byte-pair vocabulary on a tiny corpus and show the merges that hide a word boundary. |
| 22 | Intermediate | [Neighborhoods in Embedding Space](day-22-embedding-neighborhoods/README.md) | Train skip-gram embeddings on your notes and inspect neighbors, including a pair that should not be close. |
| 23 | Intermediate | [One Attention Head, On Paper](day-23-one-attention-head/README.md) | Implement scaled dot-product attention for one head and check a hand-computed 2 by 2 case. |
| 24 | Intermediate | [Heads that Disagree](day-24-heads-that-disagree/README.md) | Run two attention heads on one sentence and show that their weight patterns are not copies. |
| 25 | Intermediate | [Where Position Lives](day-25-where-position-lives/README.md) | Add sinusoidal positions and a rotary-style pairing, and show a model with neither cannot tell order. |
| 26 | Intermediate | [A Block, Shape by Shape](day-26-block-shapes/README.md) | Stack attention, residual, layer norm, and a position-wise MLP, and assert every shape. |
| 27 | Intermediate | [Overfit a Short Text on Purpose](day-27-overfit-a-text/README.md) | Train a character-level transformer until it memorizes a short text you wrote, and show the memorized continuation. |
| 28 | Intermediate | [A Loss Curve You Trust](day-28-a-loss-you-trust/README.md) | Instrument learning rate, gradient clipping, and checkpoints until a rerun overlays the same curve. |
| 29 | Intermediate | [Decoding and Its Failure Modes](day-29-decoding-failures/README.md) | Compare greedy, temperature, and top-k decoding, and catch a repetition loop on purpose. |
| 30 | Intermediate | [A Frozen Encoder and a Small Head](day-30-frozen-encoder-head/README.md) | Freeze a tiny encoder and train a linear head to classify your own labeled sentences. |
| 31 | Intermediate | [Chat Templates and Stop Sequences](day-31-chat-templates/README.md) | Render a chat transcript with special tokens and show a wrong stop sequence swallowing the answer. |
| 32 | Advanced | [A Narrow Low-Rank Update](day-32-narrow-lora/README.md) | Adapt a tiny pretrained-by-you model with LoRA on one style task, and show a rank that is too small. |
