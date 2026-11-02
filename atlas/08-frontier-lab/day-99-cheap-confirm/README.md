# A Cheap Proposal and a Strong Confirm

**Day 99** · **Advanced** · Phase 08: Frontier Lab

Let a cheap policy propose a tool and a strong policy confirm or override it, and log the override rate.

## Concept

Running the expensive path on every turn is a choice, not a law. This project splits a decision. The cheap policy proposes a tool name from a small rule list. The strong policy, also scripted but allowed to see the gold tool for the fixture, confirms or overrides. In the real pattern the strong policy would be a larger model. Here it is a function you can score. The harness logs proposals, confirmations, and overrides. The override rate is overrides divided by proposals. You will fixture a set where the cheap policy is usually right and one where it proposes `quote` before any search. The strong policy must override that case. The cheap policy does not get to call the tool. Only a confirmed name is executed. This is not a human review queue and not a confidence score routed to an analyst. It is a two-policy gate in front of a tool call.

## Approach

Execution uses the confirmed name only. A test stubs the tools and counts calls. An overridden proposal produces zero calls under the cheap name and one call under the strong name. If the strong policy rejects both, nothing is called and the status is `no-tool`. Include that third outcome so confirmation is not forced to pick something. The report lists the override rate and the no-tool count. Do not hide overrides. They are the price of letting the cheap policy speak first.

## Components

| Piece | Role |
| --- | --- |
| Cheap proposer | A rule list that emits a tool name. |
| Strong confirmer | Confirm, override, or reject. |
| Execution gate | Calls only the confirmed name. |
| Override log | Proposal, decision, and whether a call happened. |

## How it works

1. Run a batch where the cheap policy matches the fixture's expected tool.
2. Run the premature-quote case and assert an override and a search call.
3. Run a case the strong policy rejects and assert zero calls.
4. Compute the override rate from the log in a test, not by hand only.
5. Assert the cheap name was not called on the override fixture.

## Tech stack

- Python 3.11 or newer
- Scripted policies
- Stub tools that count calls

## Setup

1. Create `cheap-confirm/` with `policies.py`, `gate.py`, and tests.
2. Run the batch and write `out/overrides.jsonl`.
3. Run tests.
4. State that both policies are scripted stand-ins.

## What done looks like

- Confirmed tools run and proposed-but-overridden tools do not.
- A reject runs nothing.
- The override rate is computed from the log.
- The premature quote is overridden to a search in the fixture.

## Step ahead

A cheap policy that is almost never overridden is paying for a confirmer it may not need on that tool. Add a per-tool tally. If `search` was confirmed ten times with zero overrides, mark it `eligible-for-autonomy` in a recommendation file that does not itself disable the confirmer. Fixture the tally and assert the file is a recommendation, by checking that the gate still confirms `search` until a separate config flag is flipped. The follow-on separates the measurement from the permission change.
