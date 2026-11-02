# Two Pure Tools and a Scratchpad

**Day 49** · **Intermediate** · Phase 05: Agent Workshop

Run a loop that may only call two pure functions, and record every call on a scratchpad.

## Concept

An agent that can call the network on day one teaches you nothing about the loop, because the interesting behavior is hidden in the response. This project builds the smallest loop that still deserves the name. The agent may call two pure functions: `lookup_fee(code)` reads a dictionary you wrote, and `add_minutes(start, minutes)` does arithmetic. A scripted policy, not a model, chooses the next call from the scratchpad. The scratchpad is an append-only list of calls and results. The final answer is a string that must be computable from the scratchpad alone. If you deleted the functions and kept the scratchpad, a reader could still check the answer. That is the bar. A model can replace the scripted policy later. It does not get to replace the log.

## Approach

Represent a step as a JSON object with `tool` and `arguments`, or a final object with `answer`. The runner refuses unknown tool names and refuses a second call with the same arguments if you set a flag that the fixture uses to catch loops. The scripted policy solves one task: given a fee code and a start time, return the end time of a rental that lasts the fee's included minutes. Write three tasks in `tasks.jsonl`. One of them should omit the fee code so the policy must stop with `missing-input` rather than invent a code. Pure functions means no clock and no file writes inside the tool. The scratchpad writer is the only thing that touches disk.

## Components

| Piece | Role |
| --- | --- |
| Tool registry | Two pure functions and a map from name to function. |
| Scratchpad | Append-only call and result records. |
| Scripted policy | Chooses the next call from the scratchpad and the task. |
| Task file | Three tasks, including one that must not invent a fee code. |

## How it works

1. Implement the two functions and a registry that rejects unknown names.
2. Implement the runner: policy, call, append, repeat, until a final answer or a step cap of six.
3. Run the three tasks and write one scratchpad file each.
4. Assert the successful answers match a hand computation.
5. Assert the missing-code task ends with `missing-input` and an empty call list.

## Tech stack

- Python 3.11 or newer
- Standard library `json`
- No model and no network

## Setup

1. Create `two-tools/` with `tools.py`, `loop.py`, `tasks.jsonl`, and tests.
2. Run `python3 loop.py` and inspect `out/`.
3. Run `python3 -m unittest discover -s tests -v`.
4. Read one scratchpad aloud and confirm the answer uses only values that appear in it.

## What done looks like

- Unknown tool names fail before any function body runs.
- The missing-input task makes zero tool calls.
- A successful answer can be recomputed from its scratchpad by a test that ignores the policy.
- The step cap is a named constant and a test exceeds it with a policy that never finishes.
