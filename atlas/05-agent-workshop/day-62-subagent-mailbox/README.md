# A Mailbox for Subagents

**Day 62** · **Advanced** · Phase 05: Agent Workshop

Let a parent post a task to a child and accept only a structured reply on a mailbox, not a shared scratchpad.

## Concept

A parent agent that calls a child as a function and reads the child's scratchpad will depend on private details. This project gives the child a mailbox. The parent writes a task message with an id, a question, and the chunk ids the child is allowed to read. The child may use only those ids. It posts a reply message with the same task id, a status, and either a quote or an error code. The parent is not given a function that reads the child's tool log. A test asserts the parent's visible state after the reply does not contain the child's intermediate search strings. You will run one successful delegation and one where the child is asked about a chunk id that was not in the allow-list. That reply is an error, and the parent must surface the error rather than retry the child with a widened list. Widening is a different task with a different id.

## Approach

Messages are JSON records on two lists: inbox and outbox. The child function receives one task and returns one reply. It does not receive a callback into the parent. The allow-list is checked inside the child's search tool, which is a filtered view of the index. A reply that cites a chunk outside the list is rejected by the mailbox validator before the parent sees it, and replaced with an error reply. This keeps a buggy child from laundering a citation. The parent policy is scripted: post, wait, stop. No recursive delegation. A test that tries to post a second child task while the first is open fails, so mailboxes do not become an unbounded tree on this day.

## Components

| Piece | Role |
| --- | --- |
| Task message | Id, question, and allowed chunk ids. |
| Child view | Search restricted to the allow-list. |
| Reply validator | Rejects citations outside the list before the parent reads them. |
| Parent state | Sees the reply and not the child's scratchpad. |

## How it works

1. Implement the mailbox and the allow-list filter.
2. Run a task whose answer is inside the allow-list.
3. Run a task whose only supporting chunk is outside the list and expect an error reply.
4. Assert the parent state lacks the child's query strings.
5. Assert a second open task is rejected.

## Tech stack

- Python 3.11 or newer
- Local notes index
- JSON messages

## Setup

1. Create `mailbox/` with `mail.py`, `child.py`, `parent.py`, and tests.
2. Run both delegations.
3. Run tests.
4. Keep the child's log on disk for you to debug, but do not pass that path into the parent function.

## What done looks like

- A citation outside the allow-list never appears in the parent's reply object.
- The parent function signature does not accept a child log path.
- Two open tasks are rejected.
- The successful reply quotes a chunk that was on the list.

## Step ahead

The parent currently stops on the first error. Add a single, explicit follow-up task id that may cite one extra chunk id, chosen from the error's `blocked_ids` field, and no others. The follow-up must reference the original task id. A parent that opens a follow-up without that reference, or that adds two extra ids, is rejected. The step-ahead is a bounded widening you can see in the mailbox, not a retry with a fresh unrestricted child.
