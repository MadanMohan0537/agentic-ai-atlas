# A Loss Curve You Trust

**Day 28** · **Intermediate** · Phase 03: Transformer Workbench

Instrument learning rate, gradient clipping, and checkpoints until a rerun overlays the same curve.

## Concept

A falling loss is not evidence if you cannot rerun it. This project takes the memorization trainer and adds three pieces of discipline: a logged learning rate, gradient clipping with a threshold you choose, and a checkpoint that stores step, weights, and the RNG state you control. You will run training twice from a checkpoint saved halfway and show the remaining loss values match. You will also run once without clipping on a learning rate high enough to spike, save that curve, and keep it next to the clipped run. Deleting the spike is how people convince themselves training is stable. The spike is the artifact. The trusted curve is the one you can regenerate from the checkpoint and the config, not the one that looks smoothest.

## Approach

Clip global gradient norm: if the norm exceeds the threshold, scale the gradient vector. Log the norm before clipping so you can see how often you hit the cap. Checkpoints are NumPy `.npz` or a JSON of lists if the model is tiny. Tests can use a toy parameter vector to verify clipping math without training a model. The resume test trains for 20 steps, saves, trains 20 more, and compares to a fresh run that loaded the checkpoint and trained 20. Match within a tight tolerance. Record the learning rate schedule even if it is constant. A constant you did not log is indistinguishable from a bug when you return next week.

## Components

| Piece | Role |
| --- | --- |
| Grad-norm log | Norm before clipping, per step. |
| Clipper | Scales the gradient when the norm exceeds a threshold. |
| Checkpoint | Step, parameters, and any RNG state you own. |
| Resume comparison | A continued run versus a resumed run. |

## How it works

1. Implement clipping and test it on a vector of known norm.
2. Train a short run that spikes without clipping. Save `curve_unclipped.csv`.
3. Train with clipping and checkpoint at the midpoint.
4. Resume and compare to an uninterrupted logged run, or to a second resume.
5. Write `trust.md` with the clip threshold, the spike step if any, and whether resume matched.

## Tech stack

- Python 3.11 or newer
- The memorization trainer
- Standard library plus your numeric library

## Setup

1. Create `trust-the-loss/` and copy the trainer forward.
2. Run the unclipped spike on a tiny config so it finishes quickly. A spike from a huge learning rate counts.
3. Run the clipped resume experiment.
4. Run the clip unit test.

## What done looks like

- The clip unit test matches a hand-computed scaled vector.
- The unclipped curve is saved, spikes included.
- Resume matches the continued curve within the tolerance you set.
- `trust.md` names the threshold and the checkpoint step.
