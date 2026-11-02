# A Block, Shape by Shape

**Day 26** · **Intermediate** · Phase 03: Transformer Workbench

Stack attention, residual, layer norm, and a position-wise MLP, and assert every shape.

## Concept

A transformer block is a shape contract with a few nonlinearities. Most implementation bugs are dimension mistakes that still run because a multiply happened to align. This project builds one pre-norm block: layer norm, attention, residual add, layer norm, MLP, residual add. You will assert shapes after every step on a tensor of (batch, time, dim). You will also check a residual property: if the attention and MLP outputs are zero, the block output equals the input, within tolerance. That property catches a residual that was replaced instead of added. Use two layers only if the single block already passes. Depth is not the lesson. The lesson is being able to point at each arrow in the block and name the tensor shape.

## Approach

Layer norm is over the last dimension, with epsilon you set, and with learnable scale and shift initialized to one and zero. The MLP is two linear maps with a GELU or ReLU between them and a hidden size of 4 times dim. Initialize the last linear maps of attention and MLP to zero for the residual test, or pass a debug flag that zeroes those outputs. Do not train. A forward pass on random input with a seed should be deterministic. Write `shapes.md` as a list from input to output. Include the causal mask as an input to the block so a later day does not bolt it on from outside in a contradictory way.

## Components

| Piece | Role |
| --- | --- |
| Layer norm | Last-dimension normalization with scale and shift. |
| Attention sublayer | Your multi-head function plus a residual. |
| MLP sublayer | Expand, nonlinearity, project, residual. |
| Shape log | A written list of shapes after each operation. |

## How it works

1. Implement layer norm and test it on a vector whose mean becomes zero and variance becomes one when scale is one and shift is zero.
2. Wire the block and run a forward pass with batch 2, time 5, dim 8.
3. Record shapes.
4. Zero the sublayer outputs and assert the block returns the input.
5. Change dim to 7, an awkward number, and assert you either handle it or reject it with a clear error if heads do not divide the dimension.

## Tech stack

- Python 3.11 or newer
- NumPy or pure Python
- Your attention and position code

## Setup

1. Create `block/` with `block.py` and tests.
2. Run the forward pass and write `shapes.md` from the asserts you printed, not from a diagram you remember.
3. Run tests.
4. If you reject non-divisible head sizes, the error message must name the dimension and the head count.

## What done looks like

- Every step in `shapes.md` matches an assert in the test.
- Zeroed sublayers reproduce the input.
- Layer norm matches the hand mean and variance check.
- Head-dimension mismatch is either supported or rejected with an explicit error.
