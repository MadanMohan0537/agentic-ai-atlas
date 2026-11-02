# Phase 06: Proof Bench: Evals and Harnesses

Days 65–78. Score agent behavior with harnesses you can rerun offline: plan fidelity, cassettes, properties, and checks that do not depend on a single judge model.

| Day | Level | Project | Summary |
| --- | --- | --- | --- |
| 65 | Advanced | [Was that Tool Licensed by the Plan?](day-65-plan-licensed-tools/README.md) | Score each tool call on whether the checklist named it, separate from whether the final answer was right. |
| 66 | Advanced | [Cassettes for Tool HTTP](day-66-http-cassettes/README.md) | Record an HTTP tool once and replay the bytes so a later run does not touch the network. |
| 67 | Advanced | [Properties of a Tool](day-67-tool-properties/README.md) | Generate random valid and invalid arguments for a tool and shrink the smallest failing case. |
| 68 | Advanced | [Set Equality for Extractions](day-68-set-equality/README.md) | Score extracted dock lists as sets with numeric tolerance, not as strings. |
| 69 | Advanced | [Where Three Models Disagree](day-69-where-models-disagree/README.md) | Run one prompt through three scripted models and list the cases where their structured answers differ. |
| 70 | Advanced | [Hidden Slots Across Turns](day-70-hidden-slots/README.md) | Script a user with hidden slot values and score whether the agent fills them without re-asking a locked slot. |
| 71 | Advanced | [The Pareto Surface of Cost and Quality](day-71-pareto-cost-quality/README.md) | Sweep a grid of retriever depth and scripted model cost and drop the configs that are worse on both axes. |
| 72 | Advanced | [When Trusted Instructions Conflict](day-72-instruction-conflict/README.md) | Score an agent on a fixture where the system instruction and the tool description disagree, using a precedence you wrote down. |
| 73 | Advanced | [Pins for a Retrieval Set](day-73-retrieval-pins/README.md) | Hash the embedder id and the top-k chunk ids for a frozen query set, and fail when a rebuild drifts. |
| 74 | Advanced | [Section Checklists for Long Answers](day-74-section-checklists/README.md) | Score a long answer by required sections, forbidden claims, and numbers that must trace to a table. |
| 75 | Advanced | [A Persona with a Patience Counter](day-75-patience-persona/README.md) | Simulate a user who ends the conversation after a fixed number of unhelpful turns, and score task completion. |
| 76 | Advanced | [Case IDs that Never Change in Place](day-76-immutable-case-ids/README.md) | Store eval cases as immutable ids, and force an edit to mint a new id instead of rewriting history. |
| 77 | Advanced | [A Flake Budget](day-77-flake-budget/README.md) | Repeat a scripted eval many times, separate harness flake from decoder flake, and fail when the pass rate wanders too far. |
| 78 | Advanced | [Accepted Tool Sequences](day-78-accepted-sequences/README.md) | Score a transcript's tool names against a set of accepted sequences, ignoring argument values. |
