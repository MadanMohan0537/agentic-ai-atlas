# Phase 05: Agent Workshop

Days 49–64. Put a model, or a scripted stand-in, in a loop with tools, memory, and explicit state, and make every side effect visible.

| Day | Level | Project | Summary |
| --- | --- | --- | --- |
| 49 | Intermediate | [Two Pure Tools and a Scratchpad](day-49-two-pure-tools/README.md) | Run a loop that may only call two pure functions, and record every call on a scratchpad. |
| 50 | Intermediate | [Schemas that Reject Arguments](day-50-schemas-that-reject/README.md) | Validate tool arguments against a JSON schema before the function runs, and return the error as an observation. |
| 51 | Intermediate | [A Transcript You Can Grade](day-51-react-transcript/README.md) | Record thought, action, and observation lines, and grade the transcript against a scripted trace. |
| 52 | Intermediate | [A Checklist the Executor Cannot Skip](day-52-checklist-executor/README.md) | Separate a planner that writes a checklist from an executor that may only mark listed items done. |
| 53 | Intermediate | [A Summary of What Was Dropped](day-53-summary-of-dropped-turns/README.md) | Keep a sliding window of turns and a summary that names which facts were pushed out of the window. |
| 54 | Intermediate | [Facts with Provenance](day-54-facts-with-provenance/README.md) | Store long-term facts only with a source id, and refuse a fact the agent tries to save without one. |
| 55 | Intermediate | [A Specialist Router](day-55-specialist-router/README.md) | Route a user turn to a specialist prompt by rules, and log the route even when you override it. |
| 56 | Intermediate | [Handoff by Artifact](day-56-handoff-by-artifact/README.md) | Pass work from a researcher role to a writer role only as a file with required fields, never as a shared transcript. |
| 57 | Intermediate | [Illegal Transitions](day-57-illegal-transitions/README.md) | Model the agent as a state machine and reject any event that the current state does not allow. |
| 58 | Advanced | [Budgets and Partial Answers](day-58-budgets-and-partial-answers/README.md) | Stop the loop at a step budget and return a partial answer that lists unfinished checklist items. |
| 59 | Advanced | [Idempotency Keys on Retried Tools](day-59-idempotency-keys/README.md) | Retry a tool that appends a ledger row without appending it twice, using a key the caller supplies. |
| 60 | Advanced | [A Fixed Action Space on a Local Form](day-60-fixed-action-form/README.md) | Drive a local HTML form with click, type, and read actions, and reject any action outside that set. |
| 61 | Advanced | [A Notes Researcher that Cites](day-61-notes-researcher/README.md) | Answer a question from local markdown notes with the quote-or-abstain rule wired into the tool loop. |
| 62 | Advanced | [A Mailbox for Subagents](day-62-subagent-mailbox/README.md) | Let a parent post a task to a child and accept only a structured reply on a mailbox, not a shared scratchpad. |
| 63 | Advanced | [A Scored Gridworld](day-63-scored-gridworld/README.md) | Put an agent in a tiny grid, score a task, and show a script that loops without progress. |
| 64 | Advanced | [Repair After a Correction](day-64-repair-after-correction/README.md) | When the user says the other dock was meant, revise the slot you filled and do not defend the first one. |
