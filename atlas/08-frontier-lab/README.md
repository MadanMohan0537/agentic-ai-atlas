# Phase 08: Frontier Lab

Days 91–100. Practice the system patterns that showed up after plain chat: verifiers, constrained output, prefix reuse, small models, tool protocols, and a capstone that cites its own evidence.

| Day | Level | Project | Summary |
| --- | --- | --- | --- |
| 91 | Advanced | [Retry Under a Verifier](day-91-retry-under-a-verifier/README.md) | Let a scripted model retry until a verifier accepts the format, and stop when the budget is spent. |
| 92 | Advanced | [Constrained JSON Versus Repair](day-92-constrained-json/README.md) | Emit a tiny JSON object under a schema you enforce during decoding, and compare it to parsing and repairing free text. |
| 93 | Advanced | [Accounting for a Shared Prefix](day-93-prefix-accounting/README.md) | Measure how many prompt tokens a shared system prefix would reuse, and invalidate the reuse when the tool list changes. |
| 94 | Advanced | [A Small Model for a Narrow Label](day-94-narrow-small-model/README.md) | Train a tiny local classifier on labels from a teacher script, and list the cases where the student disagrees. |
| 95 | Advanced | [A Read-Only Field Notebook Protocol](day-95-field-notebook-protocol/README.md) | Expose local markdown notes through two tools, search and get, with a schema and no write path. |
| 96 | Advanced | [Window Versus Index](day-96-window-versus-index/README.md) | Answer the same questions from the full handbook in the prompt and from retrieval, and compare citations and cost. |
| 97 | Advanced | [A Chart with an Expected Peak](day-97-chart-peak/README.md) | Read a chart you render to SVG, answer the peak with a tolerance, and refuse a chart whose axis is cut. |
| 98 | Advanced | [Task Envelopes Between Processes](day-98-task-envelopes/README.md) | Pass a task envelope from a requester to a worker and return a completion receipt a third process can cancel. |
| 99 | Advanced | [A Cheap Proposal and a Strong Confirm](day-99-cheap-confirm/README.md) | Let a cheap policy propose a tool and a strong policy confirm or override it, and log the override rate. |
| 100 | Advanced | [Field Study: A Handbook Agent Under a Harness](day-100-handbook-field-study/README.md) | Answer handbook questions with retrieval, a budget, and a cassette, and attach an evidence note to the run. |
