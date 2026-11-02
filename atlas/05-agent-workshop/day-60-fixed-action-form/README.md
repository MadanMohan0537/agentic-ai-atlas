# A Fixed Action Space on a Local Form

**Day 60** · **Advanced** · Phase 05: Agent Workshop

Drive a local HTML form with click, type, and read actions, and reject any action outside that set.

## Concept

A browser agent that can run arbitrary scripts is a shell with extra steps. This project hosts a single HTML form on localhost — a lost-bike report with fields for dock id, fee code, and a submit button — and allows exactly three actions: `click(id)`, `type(id, text)`, and `read(id)`. The fixture page uses stable element ids. The agent is scripted. It reads the dock label, types a dock id and a fee code, clicks submit, and reads a confirmation element. There is no action for evaluating a string as code, and a test rejects `eval` and `navigate` if someone adds them to the action enum. The page is a file you wrote. You are practicing a bounded action space, not building a general computer-use product.

## Approach

Serve the file with `http.server` or parse it with `html.parser` and apply actions to a small DOM you implement for the three element types you need: input, button, and output. A full browser is optional. The required path is a tiny DOM so tests do not need a browser binary. Submit copies the input values into the confirmation text only if both fields match patterns you set on the form. The scripted agent reads the confirmation and stops. An agent that types into an unknown id gets an observation `unknown-target` and does not change state. Log every action. Assert the log contains no action names outside the three.

## Components

| Piece | Role |
| --- | --- |
| Fixture form | Local HTML with stable ids and a confirmation element. |
| Tiny DOM | Inputs, a button, and text output. |
| Action enum | Click, type, and read only. |
| Scripted agent | A fixed sequence that fills and submits the form. |

## How it works

1. Write `form.html` and the tiny DOM that loads it.
2. Implement the three actions and the unknown-target observation.
3. Run the scripted agent and assert the confirmation text contains the dock id.
4. Attempt a disallowed action name and assert rejection.
5. Attempt a type into an unknown id and assert the inputs are unchanged.

## Tech stack

- Python 3.11 or newer
- Standard library `html.parser`
- A local HTML fixture you wrote

## Setup

1. Create `form-agent/` with `form.html`, `dom.py`, `agent.py`, and tests.
2. Run the scripted agent.
3. Run tests.
4. Do not add Selenium or a browser dependency on the required path.

## What done looks like

- The confirmation text contains the values the agent typed.
- Action names outside the three are rejected, and a test lists the rejected names it tried.
- Unknown targets do not mutate inputs.
- The action log is complete for the successful run.

## Step ahead

The form gains a second page after submit, with a new confirmation id and a hidden field the agent did not type. Extend the tiny DOM with one page transition triggered by submit, and require the agent to `read` the new page's id before it is allowed to answer. A script that answers from the first page's confirmation alone must fail. The follow-on is carrying state across a transition without adding a new action type.
