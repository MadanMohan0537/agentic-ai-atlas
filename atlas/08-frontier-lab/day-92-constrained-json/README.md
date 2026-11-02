# Constrained JSON Versus Repair

**Day 92** · **Advanced** · Phase 08: Frontier Lab

Emit a tiny JSON object under a schema you enforce during decoding, and compare it to parsing and repairing free text.

## Concept

Models that are asked for JSON often add a preamble or a trailing comma. Repair functions hide that by being clever, and they also hide when the model never produced the field you needed. This project implements a tiny constrained decoder over a vocabulary of tokens you define, including braces, keys, and a closed set of values. The decoder may only emit a token the schema allows in the current state. You will also implement a repair function that strips a preamble and trailing commas. On a scripted unconstrained token stream that is almost JSON, repair succeeds. On a stream that omits the required fee key, repair must fail rather than insert a default. The constrained decoder must be unable to omit the key because the state machine never reaches done without it. The comparison is the artifact.

## Approach

The schema is one object with a required `code` from a fixed set and a required `amount` integer. The constrained decoder is a state machine, not a general JSON Schema validator bolted on after the fact. It chooses the only legal next token when the scripted model proposes an illegal one, and it logs the override. If you would rather have it stop on an illegal token, pick that behavior and test it, but do not silently skip a required key. The repair path is separate and is not called by the constrained path. A test feeds the repair path a missing-key string and expects an error. A test feeds the constrained decoder a proposal to emit `done` too early and expects a refusal or an inserted required key that is logged as an override. Prefer refusal if insertion feels like inventing a value. Refusal is the better default.

## Components

| Piece | Role |
| --- | --- |
| Schema state machine | Legal tokens from the current state. |
| Constrained decoder | Refuses illegal tokens and logs them. |
| Repair function | Strips preamble and trailing commas, and does not invent keys. |
| Missing-key fixture | Repair fails, constrained decoding cannot finish early. |

## How it works

1. Write the state machine and a diagram of states in the notes.
2. Decode a fully legal proposal and expect no overrides.
3. Propose an early finish and expect refusal.
4. Repair a trailing-comma string and expect success.
5. Repair a missing-key string and expect failure.

## Tech stack

- Python 3.11 or newer
- A token vocabulary you define
- No grammar library required

## Setup

1. Create `constrained/` with `decode.py`, `repair.py`, and tests.
2. Run both paths on the shared fixtures where both apply.
3. Run tests.
4. State in the notes that repair and constrained decoding are different policies.

## What done looks like

- The constrained decoder never emits an object missing `code` or `amount`.
- Repair does not invent a missing key.
- A trailing comma is repairable and is unnecessary on the constrained path.
- Overrides or refusals are logged rather than dropped.

## Step ahead

Schemas change. Add a version field and a decoder that refuses a v1 stream when asked for v2, where v2 requires `currency`. Show a repaired v1 object, which is valid JSON, failing a v2 check. The follow-on is that valid JSON is not the same as the object your caller required, and the version is part of the contract rather than a comment in the prompt.
