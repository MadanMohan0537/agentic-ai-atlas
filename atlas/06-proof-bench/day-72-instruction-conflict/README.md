# When Trusted Instructions Conflict

**Day 72** · **Advanced** · Phase 06: Proof Bench: Evals and Harnesses

Score an agent on a fixture where the system instruction and the tool description disagree, using a precedence you wrote down.

## Concept

Two sources you trust can disagree. The system instruction says never invent a fee, and a tool description says the tool returns a fee for every dock, including docks it has never seen. A model will follow one of them. This project does not build an attack library and does not minimize a jailbreak. It builds eight hand-written probes where a system line and a tool description conflict, plus a precedence document you write first: system instruction outranks tool description. The agent is scripted in two versions, one that obeys precedence and one that obeys the tool text. The harness scores whether a forbidden tool call happened. The probes are fixtures, not a claim about how any hosted model behaves.

## Approach

Each probe is a JSON object: system text, tool description, user text, and `forbidden_tool`. The runner executes a scripted policy selected by a flag. The score is the count of probes where the forbidden tool was called. Precedence lives in `precedence.md` and is written before you look at scores. The obedient policy refuses the call when the tool description promises coverage the system line forbids. The tool-following policy calls it. Tests lock both scores: obedient at zero calls, tool-following at one call per probe. Keep the probe count at eight so the fixture stays readable in one sitting.

## Components

| Piece | Role |
| --- | --- |
| Precedence note | A written order among instruction sources. |
| Probe file | Eight conflicts with a named forbidden tool. |
| Two policies | Obey precedence, or obey the tool description. |
| Call score | Count of forbidden calls, per policy. |

## How it works

1. Write `precedence.md` first.
2. Write eight probes.
3. Run both policies and save both scores.
4. Assert the obedient policy makes zero forbidden calls.
5. Assert the tool-following policy makes a forbidden call on every probe.

## Tech stack

- Python 3.11 or newer
- JSON probes
- Scripted policies only

## Setup

1. Create `instruction-conflict/` with `probes.jsonl`, `policies.py`, and tests.
2. Run both policies.
3. Run tests.
4. Do not describe the probes as a security certification. The notes should say they are a precedence fixture.

## What done looks like

- Precedence is a file, not an unstated habit.
- The two policies score differently on the same probes.
- Eight probes are present and each names a forbidden tool.
- The harness makes no live model calls.

## Step ahead

A third trusted source is the tool result itself. Add a probe where the system line says the fee table is authoritative, the tool description agrees, and the tool result returns a different number. Extend precedence so a tool result cannot override the system line, and score an agent that quotes the tool result anyway as a failure. The follow-on is precedence that covers results, not only instructions, with one fixture where obedience means refusing the number the tool just returned.
