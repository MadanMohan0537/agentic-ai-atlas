# Agentic AI Atlas

A build curriculum for people who need to construct agent systems and explain them: measurement, classical learning, transformers, retrieval, tool-using agents, evaluation harnesses, analytics pipelines, and the system patterns that showed up once a chat window was no longer the product.

Madan Mohan maintains this atlas as portfolio work for technical product management. Each folder is a project you can build, run, and talk through. The write-up is the spec: concept, approach, components, flow, stack, setup, and a definition of done. Advanced projects end with **Step ahead**, the next failure the first design will meet.

**Read the full plan:** [PLAN.md](PLAN.md) is the consolidated document. It spells out every phase — goal, day range, and skills — and every project: concept, approach, components, flow, stack, setup, deliverable, and, for advanced projects, the step-ahead extension. The tables on this page are the catalog. The plan is the page you read straight through.

Work in order if the material is new. Drop into a phase if you already know the earlier ground. Every project has an offline path. Hosted models are optional and named where they help.

## Phase map

| Phase | Days | Projects | What you leave able to do |
| --- | --- | --- | --- |
| [01. Field Notes: Data & Measurement](atlas/01-field-notes/README.md) | 01–10 | 10 | Defend a dataset: grain, time, labels, uncertainty, and leakage. |
| [02. Learning Machines](atlas/02-learning-machines/README.md) | 11–20 | 10 | Fit, slice, and threshold a tabular model without fooling yourself. |
| [03. Transformer Workbench](atlas/03-transformer-workbench/README.md) | 21–32 | 12 | Explain tokens, attention, training, decoding, and a small adaptation. |
| [04. Retrieval Studio](atlas/04-retrieval-studio/README.md) | 33–48 | 16 | Build a retrieval stack that cites, filters, and admits when the handbook does not say. |
| [05. Agent Workshop](atlas/05-agent-workshop/README.md) | 49–64 | 16 | Build agents whose tools, memory, and handoffs you can replay without a hosted account. |
| [06. Proof Bench: Evals and Harnesses](atlas/06-proof-bench/README.md) | 65–78 | 14 | Put a number and a failing fixture on an agent behavior you care about. |
| [07. Flowroom: Analytics and Pipelines](atlas/07-flowroom/README.md) | 79–90 | 12 | Build a small warehouse path you can rerun without double-counting or leaking the future. |
| [08. Frontier Lab](atlas/08-frontier-lab/README.md) | 91–100 | 10 | Explain a recent system pattern by building a small, testable version of it. |

## How a project folder works

- Build only what that folder asks for. A finished project is a small program or notebook plus the checks in **What done looks like**.
- Prefer the standard library early. Add a dependency when the folder names it, and pin it in that folder's notes.
- When a model is involved, ship a scripted or fixture response first so the control flow is testable without a key.
- Treat **Step ahead** as the design you would propose in a review, after the core path already works. Do not start there.

## What this collection is for

The atlas covers AI agents, retrieval-augmented generation, evals, eval harnesses, classical machine learning, data analytics, analytics workflows, data pipelines, transformers, and recent system patterns. It is a curriculum, not a framework. Projects stay separate so you can show one of them without dragging the other ninety-nine along.

## Phase 01: Field Notes: Data & Measurement

Days 01–10. Say what a row means, what a metric counts, and which records you refused before any model is worth training.

| Day | Level | Project | Summary |
| --- | --- | --- | --- |
| 01 | Beginner | [Row Contracts for a Messy Extract](atlas/01-field-notes/day-01-row-contracts/README.md) | Accept or reject each rental row with a reason code instead of silently coercing bad fields. |
| 02 | Beginner | [Diff Two Extracts by Distribution](atlas/01-field-notes/day-02-extract-diff/README.md) | Compare two weekly rental files by quantiles and category mix, not by staring at the first rows. |
| 03 | Beginner | [Grain, Joins, and Double-Counted Revenue](atlas/01-field-notes/day-03-grain-and-double-counts/README.md) | Show how a plausible join inflates revenue, then publish a grain checklist that would have stopped it. |
| 04 | Beginner | [Event Time, Time Zones, and Late Arrivals](atlas/01-field-notes/day-04-event-time/README.md) | Bucket rentals by event time in one zone, and show a late event landing in yesterday's bucket. |
| 05 | Beginner | [Text Profiles Before Any Embedding](atlas/01-field-notes/day-05-text-profiles/README.md) | Profile a pile of support notes: length, scripts, boilerplate, and exact-duplicate rate. |
| 06 | Beginner | [One Definition of Active](atlas/01-field-notes/day-06-metric-dictionary/README.md) | Write a metric dictionary entry for an active rider and compute it two ways that must agree. |
| 07 | Beginner | [Bootstrap a Rate by Hand](atlas/01-field-notes/day-07-bootstrap-a-rate/README.md) | Estimate a completion rate and a percentile interval with a seeded resample you can recompute. |
| 08 | Beginner | [Double Annotation and Agreement](atlas/01-field-notes/day-08-double-annotation/README.md) | Label the same support notes twice, measure agreement, and fix the guideline where you disagreed. |
| 09 | Beginner | [Features from Events Without Peeking](atlas/01-field-notes/day-09-features-from-events/README.md) | Build a rider feature table where every aggregate uses only events at or before a cutoff. |
| 10 | Beginner | [Split Leakage Hunt](atlas/01-field-notes/day-10-split-leakage/README.md) | Find riders who landed in both train and test, and rebuild the split so a rider lives in only one side. |

## Phase 02: Learning Machines

Days 11–20. Train classical models on a tabular rental problem you can explain, and refuse any score that does not beat a boring baseline.

| Day | Level | Project | Summary |
| --- | --- | --- | --- |
| 11 | Beginner | [Baselines that Humiliate Models](atlas/02-learning-machines/day-11-humbling-baselines/README.md) | Score a majority-class rule and a mean predictor before any learned model is allowed to look good. |
| 12 | Beginner | [A Linear Model You Can Read](atlas/02-learning-machines/day-12-readable-linear/README.md) | Fit a logistic model with gradient descent, standardize inputs, and plot reliability in five bins. |
| 13 | Beginner | [A Tree You Can Draw](atlas/02-learning-machines/day-13-a-tree-you-can-draw/README.md) | Grow a shallow decision tree, draw it, and show the overfit when you let it memorize leaves. |
| 14 | Beginner | [Boosted Trees and a Local Reason](atlas/02-learning-machines/day-14-boosted-tables/README.md) | Fit a small gradient-boosted stumps model and explain one prediction by occluding a single feature. |
| 15 | Beginner | [Precision Where It Matters](atlas/02-learning-machines/day-15-precision-at-the-point/README.md) | Rank predictions and read precision and recall at the alert rate operations can actually handle. |
| 16 | Intermediate | [Clusters with Names](atlas/02-learning-machines/day-16-clusters-with-names/README.md) | Cluster docks from usage features and name each cluster from examples, or refuse to name it. |
| 17 | Intermediate | [A Ranker from Pairs](atlas/02-learning-machines/day-17-pairs-ranker/README.md) | Learn to order docks for a rider from pairwise preferences, and evaluate with a rank metric. |
| 18 | Intermediate | [Locked Training Runs](atlas/02-learning-machines/day-18-locked-training-runs/README.md) | Make a training run reproducible: seed, data hash, config file, and a model card stub. |
| 19 | Intermediate | [Slice the Errors](atlas/02-learning-machines/day-19-slice-the-errors/README.md) | Break test error down by a feature you did not train on as a target, and write what you would do next. |
| 20 | Intermediate | [A Threshold from a Payoff Table](atlas/02-learning-machines/day-20-payoff-thresholds/README.md) | Choose a classification threshold from costs you write down, then show how a different cost flips it. |

## Phase 03: Transformer Workbench

Days 21–32. Build the pieces of a transformer until a tiny model overfits a text you wrote, then adapt it with a narrow low-rank update.

| Day | Level | Project | Summary |
| --- | --- | --- | --- |
| 21 | Intermediate | [Byte Pair Literacy](atlas/03-transformer-workbench/day-21-byte-pair-literacy/README.md) | Train a byte-pair vocabulary on a tiny corpus and show the merges that hide a word boundary. |
| 22 | Intermediate | [Neighborhoods in Embedding Space](atlas/03-transformer-workbench/day-22-embedding-neighborhoods/README.md) | Train skip-gram embeddings on your notes and inspect neighbors, including a pair that should not be close. |
| 23 | Intermediate | [One Attention Head, On Paper](atlas/03-transformer-workbench/day-23-one-attention-head/README.md) | Implement scaled dot-product attention for one head and check a hand-computed 2 by 2 case. |
| 24 | Intermediate | [Heads that Disagree](atlas/03-transformer-workbench/day-24-heads-that-disagree/README.md) | Run two attention heads on one sentence and show that their weight patterns are not copies. |
| 25 | Intermediate | [Where Position Lives](atlas/03-transformer-workbench/day-25-where-position-lives/README.md) | Add sinusoidal positions and a rotary-style pairing, and show a model with neither cannot tell order. |
| 26 | Intermediate | [A Block, Shape by Shape](atlas/03-transformer-workbench/day-26-block-shapes/README.md) | Stack attention, residual, layer norm, and a position-wise MLP, and assert every shape. |
| 27 | Intermediate | [Overfit a Short Text on Purpose](atlas/03-transformer-workbench/day-27-overfit-a-text/README.md) | Train a character-level transformer until it memorizes a short text you wrote, and show the memorized continuation. |
| 28 | Intermediate | [A Loss Curve You Trust](atlas/03-transformer-workbench/day-28-a-loss-you-trust/README.md) | Instrument learning rate, gradient clipping, and checkpoints until a rerun overlays the same curve. |
| 29 | Intermediate | [Decoding and Its Failure Modes](atlas/03-transformer-workbench/day-29-decoding-failures/README.md) | Compare greedy, temperature, and top-k decoding, and catch a repetition loop on purpose. |
| 30 | Intermediate | [A Frozen Encoder and a Small Head](atlas/03-transformer-workbench/day-30-frozen-encoder-head/README.md) | Freeze a tiny encoder and train a linear head to classify your own labeled sentences. |
| 31 | Intermediate | [Chat Templates and Stop Sequences](atlas/03-transformer-workbench/day-31-chat-templates/README.md) | Render a chat transcript with special tokens and show a wrong stop sequence swallowing the answer. |
| 32 | Advanced | [A Narrow Low-Rank Update](atlas/03-transformer-workbench/day-32-narrow-lora/README.md) | Adapt a tiny pretrained-by-you model with LoRA on one style task, and show a rank that is too small. |

## Phase 04: Retrieval Studio

Days 33–48. Index a handbook you write, retrieve with lexical and dense methods, and answer only when a span in the index supports the sentence.

| Day | Level | Project | Summary |
| --- | --- | --- | --- |
| 33 | Intermediate | [Chunks that Respect Questions](atlas/04-retrieval-studio/day-33-chunks-and-questions/README.md) | Split a staff handbook into chunks and show a question that breaks when the answer straddles a cut. |
| 34 | Intermediate | [Brute-Force Dense Search](atlas/04-retrieval-studio/day-34-brute-force-dense/README.md) | Embed chunks with a local bag-of-hashes or a small model and rank them by cosine, exhaustively. |
| 35 | Intermediate | [An Index with Metadata](atlas/04-retrieval-studio/day-35-index-with-metadata/README.md) | Persist vectors and filter by handbook version and section before similarity is computed. |
| 36 | Intermediate | [BM25 Beside Vectors](atlas/04-retrieval-studio/day-36-bm25-beside-vectors/README.md) | Rank the same chunks with BM25 and show a query the hashing embedder misses and BM25 hits. |
| 37 | Intermediate | [Reciprocal Rank Fusion](atlas/04-retrieval-studio/day-37-reciprocal-rank-fusion/README.md) | Fuse lexical and dense rankings with reciprocal rank fusion you recompute by hand on a toy list. |
| 38 | Intermediate | [Rewrite, Then Keep the Original](atlas/04-retrieval-studio/day-38-rewrite-keep-original/README.md) | Rewrite a vague question into a handbook query and search both, because the rewrite can drop the only specific token. |
| 39 | Intermediate | [Rerank the Shortlist](atlas/04-retrieval-studio/day-39-rerank-the-shortlist/README.md) | Rerank the top twenty fused hits with a lexical overlap feature and show when the new order hurts. |
| 40 | Intermediate | [Quote or Abstain](atlas/04-retrieval-studio/day-40-quote-or-abstain/README.md) | Answer with a quotation from a retrieved chunk, or refuse, when the handbook does not contain the fact. |
| 41 | Intermediate | [Parents and Children](atlas/04-retrieval-studio/day-41-parents-and-children/README.md) | Search small child chunks, then expand to the parent section before you quote. |
| 42 | Intermediate | [The Wrong Manual Version](atlas/04-retrieval-studio/day-42-wrong-manual-version/README.md) | Bind a question to a handbook edition from the conversation, and block a newer chunk the user did not ask for. |
| 43 | Intermediate | [Numbers that Stay with Their Headers](atlas/04-retrieval-studio/day-43-numbers-and-headers/README.md) | Chunk a fee table so a cell is never separated from the column header that gives it a unit. |
| 44 | Intermediate | [Several Queries, One Pool](atlas/04-retrieval-studio/day-44-several-queries-one-pool/README.md) | Fan a question out to several lexical queries, pool the hits, and dedupe by chunk id before fusion. |
| 45 | Advanced | [A Second Search When the First Is Empty](atlas/04-retrieval-studio/day-45-second-search/README.md) | If the first query abstains for low coverage, rewrite once and search again, with a hard stop at two passes. |
| 46 | Advanced | [Recall at K, Written Down](atlas/04-retrieval-studio/day-46-recall-at-k/README.md) | Freeze a retrieval eval file and report recall at five and at twenty, with a denominator you can recount. |
| 47 | Advanced | [Compress Before You Prompt](atlas/04-retrieval-studio/day-47-compress-before-prompt/README.md) | Extract the sentences that overlap the query before anything is shown to a generator, and measure what you dropped. |
| 48 | Advanced | [One Hop on an Entity Graph](atlas/04-retrieval-studio/day-48-one-hop-graph/README.md) | Link handbook chunks to entities and expand one hop to a neighbor chunk before answering. |

## Phase 05: Agent Workshop

Days 49–64. Put a model, or a scripted stand-in, in a loop with tools, memory, and explicit state, and make every side effect visible.

| Day | Level | Project | Summary |
| --- | --- | --- | --- |
| 49 | Intermediate | [Two Pure Tools and a Scratchpad](atlas/05-agent-workshop/day-49-two-pure-tools/README.md) | Run a loop that may only call two pure functions, and record every call on a scratchpad. |
| 50 | Intermediate | [Schemas that Reject Arguments](atlas/05-agent-workshop/day-50-schemas-that-reject/README.md) | Validate tool arguments against a JSON schema before the function runs, and return the error as an observation. |
| 51 | Intermediate | [A Transcript You Can Grade](atlas/05-agent-workshop/day-51-react-transcript/README.md) | Record thought, action, and observation lines, and grade the transcript against a scripted trace. |
| 52 | Intermediate | [A Checklist the Executor Cannot Skip](atlas/05-agent-workshop/day-52-checklist-executor/README.md) | Separate a planner that writes a checklist from an executor that may only mark listed items done. |
| 53 | Intermediate | [A Summary of What Was Dropped](atlas/05-agent-workshop/day-53-summary-of-dropped-turns/README.md) | Keep a sliding window of turns and a summary that names which facts were pushed out of the window. |
| 54 | Intermediate | [Facts with Provenance](atlas/05-agent-workshop/day-54-facts-with-provenance/README.md) | Store long-term facts only with a source id, and refuse a fact the agent tries to save without one. |
| 55 | Intermediate | [A Specialist Router](atlas/05-agent-workshop/day-55-specialist-router/README.md) | Route a user turn to a specialist prompt by rules, and log the route even when you override it. |
| 56 | Intermediate | [Handoff by Artifact](atlas/05-agent-workshop/day-56-handoff-by-artifact/README.md) | Pass work from a researcher role to a writer role only as a file with required fields, never as a shared transcript. |
| 57 | Intermediate | [Illegal Transitions](atlas/05-agent-workshop/day-57-illegal-transitions/README.md) | Model the agent as a state machine and reject any event that the current state does not allow. |
| 58 | Advanced | [Budgets and Partial Answers](atlas/05-agent-workshop/day-58-budgets-and-partial-answers/README.md) | Stop the loop at a step budget and return a partial answer that lists unfinished checklist items. |
| 59 | Advanced | [Idempotency Keys on Retried Tools](atlas/05-agent-workshop/day-59-idempotency-keys/README.md) | Retry a tool that appends a ledger row without appending it twice, using a key the caller supplies. |
| 60 | Advanced | [A Fixed Action Space on a Local Form](atlas/05-agent-workshop/day-60-fixed-action-form/README.md) | Drive a local HTML form with click, type, and read actions, and reject any action outside that set. |
| 61 | Advanced | [A Notes Researcher that Cites](atlas/05-agent-workshop/day-61-notes-researcher/README.md) | Answer a question from local markdown notes with the quote-or-abstain rule wired into the tool loop. |
| 62 | Advanced | [A Mailbox for Subagents](atlas/05-agent-workshop/day-62-subagent-mailbox/README.md) | Let a parent post a task to a child and accept only a structured reply on a mailbox, not a shared scratchpad. |
| 63 | Advanced | [A Scored Gridworld](atlas/05-agent-workshop/day-63-scored-gridworld/README.md) | Put an agent in a tiny grid, score a task, and show a script that loops without progress. |
| 64 | Advanced | [Repair After a Correction](atlas/05-agent-workshop/day-64-repair-after-correction/README.md) | When the user says the other dock was meant, revise the slot you filled and do not defend the first one. |

## Phase 06: Proof Bench: Evals and Harnesses

Days 65–78. Score agent behavior with harnesses you can rerun offline: plan fidelity, cassettes, properties, and checks that do not depend on a single judge model.

| Day | Level | Project | Summary |
| --- | --- | --- | --- |
| 65 | Advanced | [Was that Tool Licensed by the Plan?](atlas/06-proof-bench/day-65-plan-licensed-tools/README.md) | Score each tool call on whether the checklist named it, separate from whether the final answer was right. |
| 66 | Advanced | [Cassettes for Tool HTTP](atlas/06-proof-bench/day-66-http-cassettes/README.md) | Record an HTTP tool once and replay the bytes so a later run does not touch the network. |
| 67 | Advanced | [Properties of a Tool](atlas/06-proof-bench/day-67-tool-properties/README.md) | Generate random valid and invalid arguments for a tool and shrink the smallest failing case. |
| 68 | Advanced | [Set Equality for Extractions](atlas/06-proof-bench/day-68-set-equality/README.md) | Score extracted dock lists as sets with numeric tolerance, not as strings. |
| 69 | Advanced | [Where Three Models Disagree](atlas/06-proof-bench/day-69-where-models-disagree/README.md) | Run one prompt through three scripted models and list the cases where their structured answers differ. |
| 70 | Advanced | [Hidden Slots Across Turns](atlas/06-proof-bench/day-70-hidden-slots/README.md) | Script a user with hidden slot values and score whether the agent fills them without re-asking a locked slot. |
| 71 | Advanced | [The Pareto Surface of Cost and Quality](atlas/06-proof-bench/day-71-pareto-cost-quality/README.md) | Sweep a grid of retriever depth and scripted model cost and drop the configs that are worse on both axes. |
| 72 | Advanced | [When Trusted Instructions Conflict](atlas/06-proof-bench/day-72-instruction-conflict/README.md) | Score an agent on a fixture where the system instruction and the tool description disagree, using a precedence you wrote down. |
| 73 | Advanced | [Pins for a Retrieval Set](atlas/06-proof-bench/day-73-retrieval-pins/README.md) | Hash the embedder id and the top-k chunk ids for a frozen query set, and fail when a rebuild drifts. |
| 74 | Advanced | [Section Checklists for Long Answers](atlas/06-proof-bench/day-74-section-checklists/README.md) | Score a long answer by required sections, forbidden claims, and numbers that must trace to a table. |
| 75 | Advanced | [A Persona with a Patience Counter](atlas/06-proof-bench/day-75-patience-persona/README.md) | Simulate a user who ends the conversation after a fixed number of unhelpful turns, and score task completion. |
| 76 | Advanced | [Case IDs that Never Change in Place](atlas/06-proof-bench/day-76-immutable-case-ids/README.md) | Store eval cases as immutable ids, and force an edit to mint a new id instead of rewriting history. |
| 77 | Advanced | [A Flake Budget](atlas/06-proof-bench/day-77-flake-budget/README.md) | Repeat a scripted eval many times, separate harness flake from decoder flake, and fail when the pass rate wanders too far. |
| 78 | Advanced | [Accepted Tool Sequences](atlas/06-proof-bench/day-78-accepted-sequences/README.md) | Score a transcript's tool names against a set of accepted sequences, ignoring argument values. |

## Phase 07: Flowroom: Analytics and Pipelines

Days 79–90. Turn raw events into sessions, marts, and features that can be rebuilt, with late data and stale rows called out instead of smoothed over.

| Day | Level | Project | Summary |
| --- | --- | --- | --- |
| 79 | Intermediate | [Sessions and Late Events](atlas/07-flowroom/day-79-sessions-and-late-events/README.md) | Build rider sessions from an inactivity gap and show a late event that should extend a closed session. |
| 80 | Intermediate | [Paths Through the Help Docs](atlas/07-flowroom/day-80-help-doc-paths/README.md) | Count which help-doc sequences precede a resolved event, and ignore paths that never resolve. |
| 81 | Intermediate | [Retention Triangles](atlas/07-flowroom/day-81-retention-triangles/README.md) | Build a cohort retention triangle from signup week and activity week, and do not fill future weeks. |
| 82 | Intermediate | [Rerun-Safe Marts](atlas/07-flowroom/day-82-rerun-safe-marts/README.md) | Load raw events into staging and a mart in SQLite so running the job twice does not double the totals. |
| 83 | Intermediate | [Catalog History](atlas/07-flowroom/day-83-catalog-history/README.md) | Store fee-code changes as dated rows so a question about last March does not see today's price. |
| 84 | Intermediate | [Tumbling Windows on a File](atlas/07-flowroom/day-84-tumbling-windows/README.md) | Aggregate an event file into fixed five-minute windows and put late events in a side bucket. |
| 85 | Intermediate | [Freshness and a Backfill](atlas/07-flowroom/day-85-freshness-backfill/README.md) | Mark a mart table stale when its newest event is too old, then backfill a date without touching the others. |
| 86 | Intermediate | [Labels Joined as Of](atlas/07-flowroom/day-86-labels-as-of/README.md) | Attach a training label to a feature row using only events inside a window that starts after the cutoff. |
| 87 | Advanced | [An Embedding Job that Skips Unchanged Text](atlas/07-flowroom/day-87-embedding-backfill/README.md) | Backfill chunk embeddings keyed by content hash and model id, and skip rows whose hash is already stored. |
| 88 | Advanced | [Seasonal Residuals](atlas/07-flowroom/day-88-seasonal-residuals/README.md) | Alert when a daily rental count departs from a weekday baseline, and suppress dates you listed in advance. |
| 89 | Advanced | [Borderline Entity Matches](atlas/07-flowroom/day-89-borderline-matches/README.md) | Match rider records across two files with a score, and send only the borderline band to a review sheet. |
| 90 | Advanced | [Logs and an Error Budget](atlas/07-flowroom/day-90-error-budget-logs/README.md) | Parse structured logs into typed events and compute an error budget for a single route. |

## Phase 08: Frontier Lab

Days 91–100. Practice the system patterns that showed up after plain chat: verifiers, constrained output, prefix reuse, small models, tool protocols, and a capstone that cites its own evidence.

| Day | Level | Project | Summary |
| --- | --- | --- | --- |
| 91 | Advanced | [Retry Under a Verifier](atlas/08-frontier-lab/day-91-retry-under-a-verifier/README.md) | Let a scripted model retry until a verifier accepts the format, and stop when the budget is spent. |
| 92 | Advanced | [Constrained JSON Versus Repair](atlas/08-frontier-lab/day-92-constrained-json/README.md) | Emit a tiny JSON object under a schema you enforce during decoding, and compare it to parsing and repairing free text. |
| 93 | Advanced | [Accounting for a Shared Prefix](atlas/08-frontier-lab/day-93-prefix-accounting/README.md) | Measure how many prompt tokens a shared system prefix would reuse, and invalidate the reuse when the tool list changes. |
| 94 | Advanced | [A Small Model for a Narrow Label](atlas/08-frontier-lab/day-94-narrow-small-model/README.md) | Train a tiny local classifier on labels from a teacher script, and list the cases where the student disagrees. |
| 95 | Advanced | [A Read-Only Field Notebook Protocol](atlas/08-frontier-lab/day-95-field-notebook-protocol/README.md) | Expose local markdown notes through two tools, search and get, with a schema and no write path. |
| 96 | Advanced | [Window Versus Index](atlas/08-frontier-lab/day-96-window-versus-index/README.md) | Answer the same questions from the full handbook in the prompt and from retrieval, and compare citations and cost. |
| 97 | Advanced | [A Chart with an Expected Peak](atlas/08-frontier-lab/day-97-chart-peak/README.md) | Read a chart you render to SVG, answer the peak with a tolerance, and refuse a chart whose axis is cut. |
| 98 | Advanced | [Task Envelopes Between Processes](atlas/08-frontier-lab/day-98-task-envelopes/README.md) | Pass a task envelope from a requester to a worker and return a completion receipt a third process can cancel. |
| 99 | Advanced | [A Cheap Proposal and a Strong Confirm](atlas/08-frontier-lab/day-99-cheap-confirm/README.md) | Let a cheap policy propose a tool and a strong policy confirm or override it, and log the override rate. |
| 100 | Advanced | [Field Study: A Handbook Agent Under a Harness](atlas/08-frontier-lab/day-100-handbook-field-study/README.md) | Answer handbook questions with retrieval, a budget, and a cassette, and attach an evidence note to the run. |

## A note on scope

These projects are original build briefs. They are not wrappers around a single vendor SDK, and they are not renames of other repositories. If a later day needs a score, a policy, or a trace, it specifies the narrow check for that day rather than a general platform.
