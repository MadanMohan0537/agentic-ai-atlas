# A Summary of What Was Dropped

**Day 53** · **Intermediate** · Phase 05: Agent Workshop

Keep a sliding window of turns and a summary that names which facts were pushed out of the window.

## Concept

Context windows fill up, and the usual fix is to delete old turns. The failure is silent: a fee code mentioned at the start is gone, and the agent asks for it again or invents one. This project keeps two stores. The window holds the last N transcript lines. The summary holds facts that were in lines you dropped, but only facts that match a small extractor: fee codes, dock names, and times. When a line leaves the window, the extractor runs on it and the summary records the fact and the line id it came from. If the extractor finds nothing, the summary records `dropped-without-fact` and the line id. You will replay a transcript long enough to force a drop and show the fee code surviving in the summary. You will also show a line whose only content is small talk, dropped without a fact, so the summary does not pretend to remember chatter.

## Approach

N is a named constant, small enough that your fixture crosses it, such as 4 lines. The extractor is a set of regular expressions, not a model. The summary is a list of records, not a paragraph, so a test can see whether `HL-FEE-14` is present. The prompt or policy input for the next step is the summary plus the window, and a test asserts the dropped line's full text is absent from that input while the extracted code is present. Do not summarize by asking a model to "keep the important parts." That hides the exact loss this day is about.

## Components

| Piece | Role |
| --- | --- |
| Sliding window | The last N transcript lines. |
| Extractor | Patterns for codes, docks, and times. |
| Summary records | Fact plus source line id, or an explicit drop with no fact. |
| Next-step input | Summary plus window, never the raw dropped text. |

## How it works

1. Feed a scripted transcript longer than N that mentions a fee code early and small talk in another early line.
2. Drop lines one at a time and update the summary.
3. Assert the fee code is in the summary with the right line id.
4. Assert the small-talk line produced `dropped-without-fact`.
5. Build the next-step input and assert the raw dropped text is not in it.

## Tech stack

- Python 3.11 or newer
- Standard library `re`
- JSONL transcript fixture

## Setup

1. Create `window-summary/` with `memory.py` and tests.
2. Run the fixture and write `out/summary.json`.
3. Run tests.
4. Set N in one place and refer to it from the test so a change updates both.

## What done looks like

- The fee code survives with a source line id.
- Small talk is recorded as dropped without a fact, not omitted silently.
- The next-step input excludes raw dropped lines.
- A test fails if the extractor misses a code that is still inside the window. Extraction on drop is the path under test, and in-window lines stay verbatim.
