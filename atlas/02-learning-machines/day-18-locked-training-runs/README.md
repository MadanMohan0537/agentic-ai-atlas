# Locked Training Runs

**Day 18** · **Intermediate** · Phase 02: Learning Machines

Make a training run reproducible: seed, data hash, config file, and a model card stub.

## Concept

A score you cannot rerun is a rumor. This project wraps the linear model or the stumps in a single command that reads a config file, hashes the training CSV, records the seed, writes predictions, and writes a model card stub. The card is short on purpose: data hash, row counts, split rule, metric name, test number, and a list of things the model must not be used for. You will run the command twice and show that predictions match. Then you will change one config field, the learning rate or the stump cap, and show that the card's config section changed while the data hash did not. The failure you are catching is a notebook that was edited after the number was copied into a slide. The card lives next to the predictions, not in a wiki page you update later.

## Approach

Put hyperparameters only in `config.json`. The training script refuses to run if required keys are missing. Hash the training file bytes with SHA-256. Write `artifacts/<utc-stamp>/` containing `config.json`, `card.md`, `predictions.csv`, and `metrics.json`. Use a stamp you pass in, or a frozen stamp in tests, so tests do not depend on the clock. The reproduce check diffs predictions from two runs with the same config and stamp. Do not pickle a model unless you also store enough to recompute predictions from source. Source plus config plus data hash is the real artifact. A pickle without those is how runs go missing.

## Components

| Piece | Role |
| --- | --- |
| Config file | The only place hyperparameters are set. |
| Data hash | SHA-256 of the training file bytes. |
| Artifact directory | Config, card, predictions, and metrics written together. |
| Reproduce check | Byte-level or value-level match of two runs. |

## How it works

1. Copy the chosen model into a function `train(config, csv_path, out_dir)`.
2. Hash the CSV and store the hash in `metrics.json` and in the card.
3. Run twice into two directories with the same stamp argument if needed, or overwrite a fixed out dir sequentially and copy outputs.
4. Diff predictions.
5. Change one hyperparameter, rerun, and show the hash stayed put and the metric changed or the notes say it did not.
6. Fill the must-not-use list with two concrete prohibitions, such as pricing or disciplinary decisions.

## Tech stack

- Python 3.11 or newer
- Standard library `hashlib`, `json`, `pathlib`
- Your earlier model code, imported or copied with attribution in a comment

## Setup

1. Create `locked-runs/` with `config.json`, `train.py`, and `tests/test_repro.py`.
2. Run the script twice.
3. Run the tests, which should call `train` in a temporary directory.
4. Read the card and delete any sentence you could not defend from `metrics.json`.

## What done looks like

- Two runs with the same inputs write the same predictions.
- The card's data hash matches `hashlib` of the file on disk.
- A missing config key fails the run before training starts.
- The must-not-use list has two specific items, not a generic disclaimer.
