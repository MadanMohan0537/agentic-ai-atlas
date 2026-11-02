# Retry Under a Verifier

**Day 91** · **Advanced** · Phase 08: Frontier Lab

Let a scripted model retry until a verifier accepts the format, and stop when the budget is spent.

## Concept

Spending more inference on a hard question only helps if you can reject a bad attempt. This project defines a verifier that accepts a string only when it is a single fee line matching a pattern: a code, an amount, and a unit. A scripted generator produces a sequence of attempts, some malformed. The loop keeps the first accepted attempt and records how many tries it used. If the budget runs out, it returns `unverified` and does not return the last bad string as if it were an answer. You will compare that policy to a one-shot policy that returns the first attempt even when the verifier would fail it. On a fixture where the first attempt is malformed and the second is valid, the retry policy must be the only one that answers. This is test-time compute with an explicit budget, not a claim that a larger model would have gotten the fee right.

## Approach

The generator is a list of strings per question, which stands in for successive samples. The verifier is a pure function. The budget is an integer on the case. The loop never calls the verifier more times than the budget, and a test uses a generator longer than the budget whose only valid line sits past the budget. That case must end `unverified`. Log every attempt and the verifier's reason. Do not add a model. The lesson is the control flow: generate, check, stop.

## Components

| Piece | Role |
| --- | --- |
| Verifier | A pure accept or reject with a reason. |
| Attempt list | Scripted stand-in for successive samples. |
| Budget | Maximum verifier calls. |
| One-shot contrast | Returns the first attempt without verification. |

## How it works

1. Implement the verifier and test it on a valid and an invalid line.
2. Run the retry loop on a case that succeeds on attempt two.
3. Run a case whose only valid attempt is past the budget.
4. Compare to one-shot on the first case and assert the outputs differ.
5. Assert the unverified case does not include the rejected strings in the answer field.

## Tech stack

- Python 3.11 or newer
- Scripted attempt lists
- No hosted model

## Setup

1. Create `verifier-retry/` with `verify.py`, `loop.py`, and tests.
2. Run the three cases.
3. Run tests.
4. Write the budget next to the case id in the output.

## What done looks like

- A later valid attempt is returned and earlier rejects are only in the log.
- A valid attempt past the budget yields `unverified` and an empty answer.
- One-shot and retry disagree on the planted malformed-first case.
- Verifier call count never exceeds the budget.

## Step ahead

Majority vote across attempts can accept a wrong fee that is well formatted. Add a second verifier that checks the amount against a table, and compare vote-of-three to verifier-accept on a fixture where two attempts agree on a wrong amount and one attempt is right and formatted. Voting picks the wrong amount. The table verifier picks the right one or abstains. The follow-on shows a case where agreement is not evidence, and records both decisions without averaging them.
