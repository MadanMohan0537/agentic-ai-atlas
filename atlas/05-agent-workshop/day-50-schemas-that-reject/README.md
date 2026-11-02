# Schemas that Reject Arguments

**Day 50** · **Intermediate** · Phase 05: Agent Workshop

Validate tool arguments against a JSON schema before the function runs, and return the error as an observation.

## Concept

A tool that accepts a string where it expected a code will either crash the loop or, worse, quietly search for nothing. This project puts a schema in front of each pure function. The schema names required fields, types, and simple bounds: a fee code matches a pattern, minutes are an integer from 1 to 240. Validation runs before the function. A failure becomes an observation the policy can see, with the schema path of the error, and the function is not called. This is argument shape checking for a local tool. It is not an authorization gateway, not an approval workflow, and not a place to encode who is allowed to move money. The question today is only: did this call match the shape the function was written for?

## Approach

Write schemas as JSON objects you interpret yourself for a subset: object types, required keys, string patterns, integer minimum and maximum. Do not import a full JSON Schema library unless you also keep a test that shows your subset rejecting the cases you care about. The runner's order is fixed: known tool, then schema, then function. A schema error appends an observation of type `invalid-arguments` and does not increment a success counter. Add a policy that repairs one bad call: it sends minutes as a string, reads the observation, and sends an integer. Add another task that sends a fee code with a space and does not repair, so the loop stops on the observation after one attempt. Log both.

## Components

| Piece | Role |
| --- | --- |
| Schema subset | Required keys, types, patterns, and integer bounds. |
| Validator | Returns a path and a message, or accepts. |
| Observation | Invalid arguments are data the policy can read. |
| Repair transcript | One bad call followed by a corrected call. |

## How it works

1. Attach a schema to each tool from Day 49.
2. Reject a call before the function and record that the function body did not run. A counter inside the function makes this obvious.
3. Run the repair task and save the scratchpad.
4. Run the unrepaired bad code and assert the function call count stays zero.
5. Test a missing required field, a pattern miss, and an integer above the maximum.

## Tech stack

- Python 3.11 or newer
- Standard library `re` and `json`
- The tool loop from Day 49

## Setup

1. Create `schemas/` with `schema.py`, `loop.py`, and tests.
2. Run both tasks.
3. Run the unit tests for the three rejection cases.
4. Confirm in the scratchpad that the function-call counter did not move on the rejected attempt.

## What done looks like

- Rejected calls do not execute the function, and a test locks that.
- The repair transcript shows the invalid observation and then a valid call.
- Error observations include the field path.
- The notes state that this layer checks shape, not permission to perform a side effect.
