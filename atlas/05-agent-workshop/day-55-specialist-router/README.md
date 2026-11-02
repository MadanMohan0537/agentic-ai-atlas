# A Specialist Router

**Day 55** · **Intermediate** · Phase 05: Agent Workshop

Route a user turn to a specialist prompt by rules, and log the route even when you override it.

## Concept

One prompt that tries to be a fee clerk, a weather clerk, and a small-talk partner will follow the loudest instruction in the turn. This project routes each turn to one specialist: `fees`, `weather`, or `fallback`. Routing is a deterministic rule list you can read, plus an optional model router behind the same interface that tests do not use. The rule list looks for fee codes, weather words, and otherwise falls back. The specialist receives only its own instruction block and the turn, not the other specialists' instructions. You will include a turn that matches two rules and show that the first matching rule wins, and that the log records both the winner and the rules that also matched. An override argument exists for tests and must be logged as `override`, not as if the rules had chosen it.

## Approach

Rules are an ordered list of objects with a name, a pattern, and a specialist id. First match wins. The log line contains the turn id, the specialist, the winning rule name, the other matching rule names, and whether an override was used. A test sends "late fee in the rain" and expects `fees` if that rule is first, with `weather` listed as also matched. Swapping rule order changes the winner, and a second test locks the swapped order so the priority is data, not an accident of if-statements scattered in code. The fallback specialist has a short instruction that says it cannot look up fees. Assert that the fee instruction text is absent from the fallback prompt.

## Components

| Piece | Role |
| --- | --- |
| Ordered rules | Patterns and specialist ids, first match wins. |
| Specialist prompts | Separate instruction blocks. |
| Route log | Winner, also-matched rules, and override flag. |
| Prompt assembly | Only the chosen specialist's instructions are included. |

## How it works

1. Write three specialist instruction files.
2. Route a fee turn, a weather turn, an ambiguous turn, and a turn that matches nothing.
3. Assert the ambiguous turn logs the runner-up rule.
4. Override the fallback turn to `fees` and assert the log says override.
5. Assert the assembled prompt for fallback does not contain the fee instruction.

## Tech stack

- Python 3.11 or newer
- JSON rules and plain text instruction files
- Model router off unless a flag is set

## Setup

1. Create `router/` with `rules.json`, `specialists/`, `route.py`, and tests.
2. Run the four turns and write `out/routes.jsonl`.
3. Run tests, including the swapped-order test.
4. Read the assembled fallback prompt and confirm it is short.

## What done looks like

- Ambiguous turns log the winner and the also-matched rules.
- Rule order is data, and a test proves a swap changes the winner.
- Overrides are labeled as overrides in the log.
- Unchosen specialist instructions are not in the assembled prompt.
