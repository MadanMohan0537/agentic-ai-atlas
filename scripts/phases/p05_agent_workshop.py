"""Phase 5 — Agent Workshop. Days 49–64."""

PHASE = {
    "id": "05",
    "dir": "05-agent-workshop",
    "name": "Agent Workshop",
    "blurb": "Put a model, or a scripted stand-in, in a loop with tools, memory, and explicit state, and make every side effect visible.",
    "outcome": "Build agents whose tools, memory, and handoffs you can replay without a hosted account.",
    "goal": "Finish this phase with a small agent loop you can read end to end: tools with schemas, a transcript, a plan that the executor is not allowed to ignore, memory that names its sources, a budget that stops the loop, and a handoff that is a file rather than a shared chat.",
    "skills": [
        "Tool loops with pure functions and a scratchpad",
        "JSON schemas that reject bad arguments before the function runs",
        "ReAct-style transcripts",
        "Checklist plans and strict executors",
        "Sliding windows and summaries of dropped turns",
        "Long-term facts stored with provenance",
        "Routing a turn to a specialist prompt",
        "Handoffs by artifact",
        "State machines that reject illegal transitions",
        "Step and token budgets with partial answers",
        "Idempotency keys on retried tools",
        "A fixed action space against a local HTML fixture",
        "Citation-bound research over local notes",
        "Subagents that return structured mail",
        "A scored gridworld environment",
        "Dialogue repair after a user correction",
    ],
    "projects": [
        {
            "day": 49,
            "slug": "two-pure-tools",
            "title": "Two Pure Tools and a Scratchpad",
            "level": "Intermediate",
            "summary": "Run a loop that may only call two pure functions, and record every call on a scratchpad.",
            "concept": """
An agent that can call the network on day one teaches you nothing about the loop, because the interesting behavior is hidden in the response. This project builds the smallest loop that still deserves the name. The agent may call two pure functions: `lookup_fee(code)` reads a dictionary you wrote, and `add_minutes(start, minutes)` does arithmetic. A scripted policy, not a model, chooses the next call from the scratchpad. The scratchpad is an append-only list of calls and results. The final answer is a string that must be computable from the scratchpad alone. If you deleted the functions and kept the scratchpad, a reader could still check the answer. That is the bar. A model can replace the scripted policy later. It does not get to replace the log.
            """.strip(),
            "approach": """
Represent a step as a JSON object with `tool` and `arguments`, or a final object with `answer`. The runner refuses unknown tool names and refuses a second call with the same arguments if you set a flag that the fixture uses to catch loops. The scripted policy solves one task: given a fee code and a start time, return the end time of a rental that lasts the fee's included minutes. Write three tasks in `tasks.jsonl`. One of them should omit the fee code so the policy must stop with `missing-input` rather than invent a code. Pure functions means no clock and no file writes inside the tool. The scratchpad writer is the only thing that touches disk.
            """.strip(),
            "components": [
                ("Tool registry", "Two pure functions and a map from name to function."),
                ("Scratchpad", "Append-only call and result records."),
                ("Scripted policy", "Chooses the next call from the scratchpad and the task."),
                ("Task file", "Three tasks, including one that must not invent a fee code."),
            ],
            "flow": [
                "Implement the two functions and a registry that rejects unknown names.",
                "Implement the runner: policy, call, append, repeat, until a final answer or a step cap of six.",
                "Run the three tasks and write one scratchpad file each.",
                "Assert the successful answers match a hand computation.",
                "Assert the missing-code task ends with `missing-input` and an empty call list.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library `json`",
                "No model and no network",
            ],
            "setup": [
                "Create `two-tools/` with `tools.py`, `loop.py`, `tasks.jsonl`, and tests.",
                "Run `python3 loop.py` and inspect `out/`.",
                "Run `python3 -m unittest discover -s tests -v`.",
                "Read one scratchpad aloud and confirm the answer uses only values that appear in it.",
            ],
            "done": [
                "Unknown tool names fail before any function body runs.",
                "The missing-input task makes zero tool calls.",
                "A successful answer can be recomputed from its scratchpad by a test that ignores the policy.",
                "The step cap is a named constant and a test exceeds it with a policy that never finishes.",
            ],
        },
        {
            "day": 50,
            "slug": "schemas-that-reject",
            "title": "Schemas that Reject Arguments",
            "level": "Intermediate",
            "summary": "Validate tool arguments against a JSON schema before the function runs, and return the error as an observation.",
            "concept": """
A tool that accepts a string where it expected a code will either crash the loop or, worse, quietly search for nothing. This project puts a schema in front of each pure function. The schema names required fields, types, and simple bounds: a fee code matches a pattern, minutes are an integer from 1 to 240. Validation runs before the function. A failure becomes an observation the policy can see, with the schema path of the error, and the function is not called. This is argument shape checking for a local tool. It is not an authorization gateway, not an approval workflow, and not a place to encode who is allowed to move money. The question today is only: did this call match the shape the function was written for?
            """.strip(),
            "approach": """
Write schemas as JSON objects you interpret yourself for a subset: object types, required keys, string patterns, integer minimum and maximum. Do not import a full JSON Schema library unless you also keep a test that shows your subset rejecting the cases you care about. The runner's order is fixed: known tool, then schema, then function. A schema error appends an observation of type `invalid-arguments` and does not increment a success counter. Add a policy that repairs one bad call: it sends minutes as a string, reads the observation, and sends an integer. Add another task that sends a fee code with a space and does not repair, so the loop stops on the observation after one attempt. Log both.
            """.strip(),
            "components": [
                ("Schema subset", "Required keys, types, patterns, and integer bounds."),
                ("Validator", "Returns a path and a message, or accepts."),
                ("Observation", "Invalid arguments are data the policy can read."),
                ("Repair transcript", "One bad call followed by a corrected call."),
            ],
            "flow": [
                "Attach a schema to each tool from Day 49.",
                "Reject a call before the function and record that the function body did not run. A counter inside the function makes this obvious.",
                "Run the repair task and save the scratchpad.",
                "Run the unrepaired bad code and assert the function call count stays zero.",
                "Test a missing required field, a pattern miss, and an integer above the maximum.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library `re` and `json`",
                "The tool loop from Day 49",
            ],
            "setup": [
                "Create `schemas/` with `schema.py`, `loop.py`, and tests.",
                "Run both tasks.",
                "Run the unit tests for the three rejection cases.",
                "Confirm in the scratchpad that the function-call counter did not move on the rejected attempt.",
            ],
            "done": [
                "Rejected calls do not execute the function, and a test locks that.",
                "The repair transcript shows the invalid observation and then a valid call.",
                "Error observations include the field path.",
                "The notes state that this layer checks shape, not permission to perform a side effect.",
            ],
        },
        {
            "day": 51,
            "slug": "react-transcript",
            "title": "A Transcript You Can Grade",
            "level": "Intermediate",
            "summary": "Record thought, action, and observation lines, and grade the transcript against a scripted trace.",
            "concept": """
A loop that only stores tool calls hides why the next call was chosen. The ReAct pattern writes a thought, then an action, then an observation, and repeats. This project implements that transcript with a scripted reasoner so you can grade the text without a model. The reasoner emits a thought that names the missing field, then an action. You will compare a run to a golden transcript: same actions in the same order, observations equal to the tool results. Thoughts may differ in wording only if you are using a model. Under the scripted reasoner they must match too, because they are part of the contract of the fixture. Grading is exact on actions and observations. A mismatched thought under the script fails the run. That strictness is what makes the later model swap measurable.
            """.strip(),
            "approach": """
Each transcript line has a kind: `thought`, `action`, `observation`, or `answer`. The runner rejects two actions in a row without an observation, and rejects an observation that did not come from the tool. The golden file is a transcript you write by hand for one task. The grader reports the first diverging line index. Include a second golden file for the missing-input task that contains a thought and an answer and no action. A model backend, if you add one, is behind a flag and is not used by tests. Tests use the scripted reasoner only.
            """.strip(),
            "components": [
                ("Line types", "Thought, action, observation, and answer, in a fixed order."),
                ("Scripted reasoner", "Emits the next thought and action from the task state."),
                ("Golden transcript", "A hand-written trace for one successful task."),
                ("Grader", "Reports the first line where the run diverges."),
            ],
            "flow": [
                "Define the line schema and the runner rules that forbid doubled actions.",
                "Write the golden transcript for the fee-and-time task.",
                "Run the scripted reasoner and grade it. It should match.",
                "Mutate one action in a copy of the run and assert the grader names that line.",
                "Grade the missing-input transcript and assert it contains no action lines.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "JSONL transcripts",
                "Scripted reasoner required, model optional and off by default",
            ],
            "setup": [
                "Create `react-transcript/` with `transcript.py`, `gold/`, and tests.",
                "Run the match and the deliberate mismatch.",
                "Run tests.",
                "If you try a model, save that transcript as `out/model.jsonl` and do not overwrite the golden file when it differs.",
            ],
            "done": [
                "The scripted run matches the golden transcript exactly.",
                "A mutated action fails the grader at the right line index.",
                "The runner rejects an action that is not followed by a tool observation when another action arrives.",
                "Tests pass with no model key present in the environment.",
            ],
        },
        {
            "day": 52,
            "slug": "checklist-executor",
            "title": "A Checklist the Executor Cannot Skip",
            "level": "Intermediate",
            "summary": "Separate a planner that writes a checklist from an executor that may only mark listed items done.",
            "concept": """
A single loop that plans and acts in the same breath will skip a step and still sound finished. This project splits the roles. The planner writes a checklist of items, each with an id and a tool call, and then it is done. The executor may run only those calls, in order, and may mark an item done only after an observation is stored. It may not add a checklist item. A final answer that arrives with an open item is rejected. You will build one hostile executor, used only in a test, that tries to mark an item done without a call, and you will show the runner refusing. The planner in the required path is scripted from the task. The lesson is the boundary, not a clever plan.
            """.strip(),
            "approach": """
The checklist is JSON. Item states are `open` or `done`. The executor function takes the checklist and the scratchpad and returns the next call or a final answer. The runner checks that the call's item id exists, is open, and matches the tool the planner named. Arguments may be filled from earlier observations if the plan used placeholders such as `$item1.minutes`. Placeholders are the only flexibility. Free-form extra calls are rejected. Write a task whose plan has two items and a third tempting call that is not on the list. Assert the tempting call never runs.
            """.strip(),
            "components": [
                ("Planner output", "A checklist of item ids and tool names."),
                ("Executor", "Runs listed calls in order and resolves placeholders."),
                ("State gate", "An item becomes done only after an observation."),
                ("Hostile executor", "A test double that tries to skip the call."),
            ],
            "flow": [
                "Script a planner for the fee-and-time task with two items.",
                "Run the executor through the runner and save the checklist with states.",
                "Assert the final answer is rejected if you force an item to stay open.",
                "Assert the hostile executor's premature done mark raises.",
                "Assert a call whose tool name is not on the current item is rejected.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "JSON checklist and scratchpad",
                "No model required",
            ],
            "setup": [
                "Create `checklist/` with `plan.py`, `execute.py`, and tests.",
                "Run the happy path and write `out/checklist.json`.",
                "Run the hostile tests.",
                "Document the placeholder syntax in a short comment at the top of `execute.py`.",
            ],
            "done": [
                "The happy-path checklist ends with every item done and observations attached.",
                "A premature done mark fails a test.",
                "A tool that was not on the list does not run.",
                "Placeholders resolve from earlier observations, and a missing placeholder fails the item rather than calling the tool with a literal dollar string.",
            ],
        },
        {
            "day": 53,
            "slug": "summary-of-dropped-turns",
            "title": "A Summary of What Was Dropped",
            "level": "Intermediate",
            "summary": "Keep a sliding window of turns and a summary that names which facts were pushed out of the window.",
            "concept": """
Context windows fill up, and the usual fix is to delete old turns. The failure is silent: a fee code mentioned at the start is gone, and the agent asks for it again or invents one. This project keeps two stores. The window holds the last N transcript lines. The summary holds facts that were in lines you dropped, but only facts that match a small extractor: fee codes, dock names, and times. When a line leaves the window, the extractor runs on it and the summary records the fact and the line id it came from. If the extractor finds nothing, the summary records `dropped-without-fact` and the line id. You will replay a transcript long enough to force a drop and show the fee code surviving in the summary. You will also show a line whose only content is small talk, dropped without a fact, so the summary does not pretend to remember chatter.
            """.strip(),
            "approach": """
N is a named constant, small enough that your fixture crosses it, such as 4 lines. The extractor is a set of regular expressions, not a model. The summary is a list of records, not a paragraph, so a test can see whether `HL-FEE-14` is present. The prompt or policy input for the next step is the summary plus the window, and a test asserts the dropped line's full text is absent from that input while the extracted code is present. Do not summarize by asking a model to "keep the important parts." That hides the exact loss this day is about.
            """.strip(),
            "components": [
                ("Sliding window", "The last N transcript lines."),
                ("Extractor", "Patterns for codes, docks, and times."),
                ("Summary records", "Fact plus source line id, or an explicit drop with no fact."),
                ("Next-step input", "Summary plus window, never the raw dropped text."),
            ],
            "flow": [
                "Feed a scripted transcript longer than N that mentions a fee code early and small talk in another early line.",
                "Drop lines one at a time and update the summary.",
                "Assert the fee code is in the summary with the right line id.",
                "Assert the small-talk line produced `dropped-without-fact`.",
                "Build the next-step input and assert the raw dropped text is not in it.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library `re`",
                "JSONL transcript fixture",
            ],
            "setup": [
                "Create `window-summary/` with `memory.py` and tests.",
                "Run the fixture and write `out/summary.json`.",
                "Run tests.",
                "Set N in one place and refer to it from the test so a change updates both.",
            ],
            "done": [
                "The fee code survives with a source line id.",
                "Small talk is recorded as dropped without a fact, not omitted silently.",
                "The next-step input excludes raw dropped lines.",
                "A test fails if the extractor misses a code that is still inside the window. Extraction on drop is the path under test, and in-window lines stay verbatim.",
            ],
        },
        {
            "day": 54,
            "slug": "facts-with-provenance",
            "title": "Facts with Provenance",
            "level": "Intermediate",
            "summary": "Store long-term facts only with a source id, and refuse a fact the agent tries to save without one.",
            "concept": """
A memory note that says "the late fee is 14" is a liability if nobody can find the sentence it came from. This project is a long-term store, separate from the sliding window. A fact is admitted only with a `source_id` that exists in a catalog of handbook chunks or tool observations. The store records the fact text, the source id, and a hash of the source text at save time. On read, if the source text has changed, the fact is returned with `stale: true` and is not silently refreshed. An agent tool `remember(text, source_id)` calls this store. A call with an unknown source id is an observation of type `rejected-memory`, and nothing is written. You will try to remember a fee that does not appear in the cited chunk and, in the required design, still accept it only if the source id exists — then add a second check that the fact's numbers appear in the source text. The second check is in scope today. A memory that can attach any sentence to any id is not provenance.
            """.strip(),
            "approach": """
The catalog is a JSON file of id to text, built from a few handbook chunks. `remember` verifies the id, verifies that every integer in the fact text occurs in the source text, and only then appends. This will reject some true paraphrases. That is acceptable for this day. Write the limitation down: paraphrases need a later design, and the current rule prefers false rejects over free invention. The stale flag flips when you edit the catalog text without updating the hash. A test edits the catalog and expects `stale: true` on the next read.
            """.strip(),
            "components": [
                ("Source catalog", "Ids and texts the memory is allowed to cite."),
                ("Remember tool", "Rejects unknown ids and facts whose numbers are not in the source."),
                ("Hash", "SHA-256 of the source text at save time."),
                ("Stale read", "A changed source marks the fact stale instead of rewriting it."),
            ],
            "flow": [
                "Load a tiny catalog with one fee chunk and one unrelated chunk.",
                "Remember a fact whose number appears in the fee chunk. Assert it is stored.",
                "Attempt a fact with a number that does not appear. Assert rejection and an unchanged store.",
                "Edit the catalog, reread, and assert the stale flag.",
                "Attempt an unknown source id and assert rejection.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library `hashlib` and `json`",
                "No vector database",
            ],
            "setup": [
                "Create `provenance-memory/` with `store.py`, `catalog.json`, and tests.",
                "Run the four cases and write `out/memory.json`.",
                "Run tests.",
                "Write the paraphrase limitation in `notes.md` in two sentences.",
            ],
            "done": [
                "Unknown source ids write nothing.",
                "A number that is not in the source blocks the write.",
                "A changed source marks the fact stale and does not auto-edit the fact text.",
                "The notes name the paraphrase limitation.",
            ],
        },
        {
            "day": 55,
            "slug": "specialist-router",
            "title": "A Specialist Router",
            "level": "Intermediate",
            "summary": "Route a user turn to a specialist prompt by rules, and log the route even when you override it.",
            "concept": """
One prompt that tries to be a fee clerk, a weather clerk, and a small-talk partner will follow the loudest instruction in the turn. This project routes each turn to one specialist: `fees`, `weather`, or `fallback`. Routing is a deterministic rule list you can read, plus an optional model router behind the same interface that tests do not use. The rule list looks for fee codes, weather words, and otherwise falls back. The specialist receives only its own instruction block and the turn, not the other specialists' instructions. You will include a turn that matches two rules and show that the first matching rule wins, and that the log records both the winner and the rules that also matched. An override argument exists for tests and must be logged as `override`, not as if the rules had chosen it.
            """.strip(),
            "approach": """
Rules are an ordered list of objects with a name, a pattern, and a specialist id. First match wins. The log line contains the turn id, the specialist, the winning rule name, the other matching rule names, and whether an override was used. A test sends "late fee in the rain" and expects `fees` if that rule is first, with `weather` listed as also matched. Swapping rule order changes the winner, and a second test locks the swapped order so the priority is data, not an accident of if-statements scattered in code. The fallback specialist has a short instruction that says it cannot look up fees. Assert that the fee instruction text is absent from the fallback prompt.
            """.strip(),
            "components": [
                ("Ordered rules", "Patterns and specialist ids, first match wins."),
                ("Specialist prompts", "Separate instruction blocks."),
                ("Route log", "Winner, also-matched rules, and override flag."),
                ("Prompt assembly", "Only the chosen specialist's instructions are included."),
            ],
            "flow": [
                "Write three specialist instruction files.",
                "Route a fee turn, a weather turn, an ambiguous turn, and a turn that matches nothing.",
                "Assert the ambiguous turn logs the runner-up rule.",
                "Override the fallback turn to `fees` and assert the log says override.",
                "Assert the assembled prompt for fallback does not contain the fee instruction.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "JSON rules and plain text instruction files",
                "Model router off unless a flag is set",
            ],
            "setup": [
                "Create `router/` with `rules.json`, `specialists/`, `route.py`, and tests.",
                "Run the four turns and write `out/routes.jsonl`.",
                "Run tests, including the swapped-order test.",
                "Read the assembled fallback prompt and confirm it is short.",
            ],
            "done": [
                "Ambiguous turns log the winner and the also-matched rules.",
                "Rule order is data, and a test proves a swap changes the winner.",
                "Overrides are labeled as overrides in the log.",
                "Unchosen specialist instructions are not in the assembled prompt.",
            ],
        },
        {
            "day": 56,
            "slug": "handoff-by-artifact",
            "title": "Handoff by Artifact",
            "level": "Intermediate",
            "summary": "Pass work from a researcher role to a writer role only as a file with required fields, never as a shared transcript.",
            "concept": """
Two roles that share a chat will each assume the other noticed the fee code. This project forbids the shared transcript. The researcher reads the handbook chunks and writes `handoff.json` with required fields: `question`, `quotes` (each an exact substring plus chunk id), and `open_questions`. The writer may read only that file. It produces an answer that quotes only from `quotes`, or it returns `incomplete` if `open_questions` is non-empty. You will run one task where the researcher fills a real quote and an empty open-question list, and one where it sets an open question and leaves quotes empty. The writer must not "helpfully" answer the second task from the handbook, because the writer is not given the handbook path. A test that points the writer at the handbook folder should fail code review in the sense that your writer function's signature does not accept a handbook path.
            """.strip(),
            "approach": """
Define the handoff schema and validate it before the writer runs. Extra fields are rejected so the researcher cannot smuggle a draft answer the writer will paste. The writer function signature is `write_answer(handoff: dict) -> dict`. Tests pass a handoff whose quote does not contain a number the researcher hoped to sneak into an extra field. Assert the extra field is rejected at validation, before the writer. For the successful task, assert the answer text contains the quote and the chunk id. For the incomplete task, assert the status is `incomplete` and the answer text is empty.
            """.strip(),
            "components": [
                ("Handoff schema", "Question, quotes, and open questions. Extra fields rejected."),
                ("Researcher", "A scripted function that fills the handoff from fixture chunks."),
                ("Writer", "Reads only the handoff object."),
                ("Incomplete path", "Non-empty open questions block the answer."),
            ],
            "flow": [
                "Implement validation, including rejection of unknown fields.",
                "Run the researcher on a fixture question and write `handoff.json`.",
                "Run the writer on that file.",
                "Run the open-question fixture and assert `incomplete`.",
                "Assert the writer source does not take a handbook directory argument. A small test can inspect the signature with `inspect`.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "JSON handoff file",
                "Standard library `inspect` for the signature test",
            ],
            "setup": [
                "Create `handoff/` with `schema.py`, `roles.py`, and tests.",
                "Run both fixtures.",
                "Run tests.",
                "Open `handoff.json` and confirm every quote is a substring of the fixture chunk you point at in the test.",
            ],
            "done": [
                "Unknown handoff fields fail validation.",
                "The writer signature accepts the handoff and nothing else.",
                "A non-empty open-question list yields an empty answer and status `incomplete`.",
                "The successful answer cites a chunk id that is inside the handoff.",
            ],
        },
        {
            "day": 57,
            "slug": "illegal-transitions",
            "title": "Illegal Transitions",
            "level": "Intermediate",
            "summary": "Model the agent as a state machine and reject any event that the current state does not allow.",
            "concept": """
Loops get into impossible states: an answer before any retrieval, a second handoff, a tool call after the answer. This project names the states and the events. States are `idle`, `planned`, `acting`, `handoff`, and `answered`. Events are `plan`, `act`, `observe`, `submit_handoff`, and `answer`. A table maps state and event to the next state or to `illegal`. The runner consults the table and refuses illegal events with the state name and the event name in the error. It does not catch the error and continue. You will drive a happy path and three illegal paths: answering from idle, acting after answered, and submitting two handoffs. The table is data, so a test can add a temporary transition without editing the runner.
            """.strip(),
            "approach": """
Store the table as a dictionary of pairs. The runner holds one current state and appends every accepted event to a log. Illegal events raise `IllegalTransition` and leave the state unchanged. A test attempts the illegal event and then a legal one and asserts the legal one still sees the pre-illegal state. Do not encode the table as a chain of if statements inside the runner. The runner should look up the pair and follow it. Print the reachable states from `idle` by a small walk so you notice a state you cannot enter.
            """.strip(),
            "components": [
                ("Transition table", "Pairs of state and event, stored as data."),
                ("Runner", "Looks up the table and refuses misses."),
                ("Event log", "Accepted events only."),
                ("Illegal paths", "Three fixture sequences that must raise."),
            ],
            "flow": [
                "Write the table and a function that lists states unreachable from idle.",
                "Drive the happy path through answer and save the log.",
                "Attempt each illegal path and record the exception message.",
                "Assert state is unchanged after a rejected event.",
                "Assert every named state is reachable, or remove the state from the machine.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library only",
                "No model",
            ],
            "setup": [
                "Create `state-machine/` with `machine.py` and tests.",
                "Run the happy path and the three failures.",
                "Run tests.",
                "If a state is unreachable, fix the table before you call the day done.",
            ],
            "done": [
                "Three illegal sequences raise and name both the state and the event.",
                "State does not change on a rejected event.",
                "The transition table is data the runner looks up.",
                "Every state is reachable from idle, and a test walks the table to prove it.",
            ],
        },
        {
            "day": 58,
            "slug": "budgets-and-partial-answers",
            "title": "Budgets and Partial Answers",
            "level": "Advanced",
            "summary": "Stop the loop at a step budget and return a partial answer that lists unfinished checklist items.",
            "concept": """
An agent that runs until it feels done will run until someone kills the process. This project adds a budget: a maximum number of tool calls and a maximum number of transcript lines. When either limit is hit, the runner does not raise a generic timeout and discard the work. It returns a structured partial answer: status `partial`, the observations so far, and the checklist item ids still open. A complete answer is illegal if the budget is already exhausted. You will fixture a planner that emits four items and a budget of two calls, and show the partial result containing the two finished observations and the two open ids. You will also fixture a task that finishes inside the budget and show status `complete` with an empty open list. The budget is part of the task file so a test can tighten it without editing code.
            """.strip(),
            "approach": """
Count tool calls, not thoughts. A thought does not spend the tool budget. Transcript-line budget counts every line. Hitting either budget triggers the same partial response shape so callers do not special-case the reason, but the response includes `stop_reason` of `tool-budget` or `line-budget`. A test sets the tool budget to zero and expects a partial answer with every item open and zero observations. The runner must check the budget before the call, not after, so a zero budget does not sneak one execution through. Write `budget_notes.md` with both fixture outputs.
            """.strip(),
            "components": [
                ("Tool budget", "Checked before a call is dispatched."),
                ("Line budget", "Checked before a line is appended."),
                ("Partial response", "Observations so far and open item ids."),
                ("Stop reason", "Which budget fired, on the response."),
            ],
            "flow": [
                "Add budgets to the checklist runner from Day 52.",
                "Run the four-item plan with a tool budget of two.",
                "Run a two-item plan inside the budget and expect `complete`.",
                "Run a zero tool budget and expect no function executions.",
                "Hit the line budget with a talkative scripted policy and expect `line-budget` without a tool call that would exceed the tool budget. Keep the fixture simple: a line budget of one.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "The checklist runner",
                "JSON task files that include budgets",
            ],
            "setup": [
                "Create `budgets/` with `budget_loop.py` and tests.",
                "Run the three fixtures and save their responses.",
                "Run tests, including the zero-budget case.",
                "Confirm a function-body counter stays at zero when the tool budget is zero.",
            ],
            "done": [
                "Partial responses list finished observations and open ids.",
                "A zero tool budget executes nothing.",
                "`stop_reason` distinguishes the two budgets.",
                "A task that finishes inside budget has status `complete` and no open ids.",
            ],
            "ahead": """
A partial answer can still be mistaken for a fee quote if a reader looks only at the observations. Add a renderer that refuses to print a currency number unless status is `complete`, and otherwise prints the open item ids first. Fixture a partial run whose observations already contain a fee amount, and assert the rendered text does not contain that amount. The follow-on failure you are preventing is a UI that shows the observation log as if it were the answer.
            """.strip(),
        },
        {
            "day": 59,
            "slug": "idempotency-keys",
            "title": "Idempotency Keys on Retried Tools",
            "level": "Advanced",
            "summary": "Retry a tool that appends a ledger row without appending it twice, using a key the caller supplies.",
            "concept": """
The pure tools from earlier days can be repeated safely. A tool that appends a maintenance ticket cannot. This project adds one effectful tool, `create_ticket`, backed by an in-memory ledger. Each call carries an idempotency key chosen by the agent, not by the tool. The first call with a key appends a row and stores the result. A second call with the same key and the same body returns the stored result and does not append. A second call with the same key and a different body is an error `key-reused-with-different-body`, and the ledger stays as it was. Retries are how you survive a crash after the tool succeeded but before the observation was written. You will simulate that crash by invoking the tool, discarding the observation, and invoking it again. The ledger length must stay one.
            """.strip(),
            "approach": """
The ledger is a list and a dict from key to stored result. Body equality is JSON canonical form: sorted keys, no whitespace surprises. Do not use the key as a substitute for identity of the ticket only; store the body hash next to the key. A missing key is a schema error from Day 50's rules, and the tool does not run. This is not a permission system and not an approval chain. The only question is whether a retry duplicates a row. Include a test where two different keys with the same body create two tickets, because idempotency is not deduplication of intent. Write that distinction in `notes.md` so you do not collapse the two ideas later.
            """.strip(),
            "components": [
                ("Ledger", "Append-only ticket rows in memory."),
                ("Key store", "Maps a key to a body hash and a result."),
                ("Retry simulation", "Two calls, one discarded observation, one row."),
                ("Conflict error", "Same key, different body, no new row."),
            ],
            "flow": [
                "Implement `create_ticket` with required `idempotency_key` and a body.",
                "Call it twice with the same key and body. Assert one row.",
                "Call it with the same key and a changed summary. Assert the error and an unchanged ledger.",
                "Call it with two keys and the same body. Assert two rows.",
                "Omit the key and assert the function body does not run.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library `json`",
                "In-memory ledger, no database server",
            ],
            "setup": [
                "Create `idempotency/` with `ledger.py` and tests.",
                "Run the four cases as a script that prints ledger lengths.",
                "Run tests.",
                "Write the distinction between retry identity and content dedupe in `notes.md`.",
            ],
            "done": [
                "A retry with the same key and body does not append a second row.",
                "The same key with a different body errors and does not append.",
                "Two keys create two rows even if the bodies match.",
                "A missing key never reaches the ledger code, and a test covers it.",
            ],
            "ahead": """
The key store lives in the same process as the crash you simulated, so a real crash would forget the key and the retry would duplicate the ticket. Persist the key store to a file before you append the ledger row, and persist the row after. Fixture a crash between the two writes by stopping after the key file is written and before the ledger append, then resume. The follow-on behavior is: resume sees the key with status `pending`, completes the single append, and a later retry returns that row. If resume appends twice, the order of the two writes is wrong.
            """.strip(),
        },
        {
            "day": 60,
            "slug": "fixed-action-form",
            "title": "A Fixed Action Space on a Local Form",
            "level": "Advanced",
            "summary": "Drive a local HTML form with click, type, and read actions, and reject any action outside that set.",
            "concept": """
A browser agent that can run arbitrary scripts is a shell with extra steps. This project hosts a single HTML form on localhost — a lost-bike report with fields for dock id, fee code, and a submit button — and allows exactly three actions: `click(id)`, `type(id, text)`, and `read(id)`. The fixture page uses stable element ids. The agent is scripted. It reads the dock label, types a dock id and a fee code, clicks submit, and reads a confirmation element. There is no action for evaluating a string as code, and a test rejects `eval` and `navigate` if someone adds them to the action enum. The page is a file you wrote. You are practicing a bounded action space, not building a general computer-use product.
            """.strip(),
            "approach": """
Serve the file with `http.server` or parse it with `html.parser` and apply actions to a small DOM you implement for the three element types you need: input, button, and output. A full browser is optional. The required path is a tiny DOM so tests do not need a browser binary. Submit copies the input values into the confirmation text only if both fields match patterns you set on the form. The scripted agent reads the confirmation and stops. An agent that types into an unknown id gets an observation `unknown-target` and does not change state. Log every action. Assert the log contains no action names outside the three.
            """.strip(),
            "components": [
                ("Fixture form", "Local HTML with stable ids and a confirmation element."),
                ("Tiny DOM", "Inputs, a button, and text output."),
                ("Action enum", "Click, type, and read only."),
                ("Scripted agent", "A fixed sequence that fills and submits the form."),
            ],
            "flow": [
                "Write `form.html` and the tiny DOM that loads it.",
                "Implement the three actions and the unknown-target observation.",
                "Run the scripted agent and assert the confirmation text contains the dock id.",
                "Attempt a disallowed action name and assert rejection.",
                "Attempt a type into an unknown id and assert the inputs are unchanged.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library `html.parser`",
                "A local HTML fixture you wrote",
            ],
            "setup": [
                "Create `form-agent/` with `form.html`, `dom.py`, `agent.py`, and tests.",
                "Run the scripted agent.",
                "Run tests.",
                "Do not add Selenium or a browser dependency on the required path.",
            ],
            "done": [
                "The confirmation text contains the values the agent typed.",
                "Action names outside the three are rejected, and a test lists the rejected names it tried.",
                "Unknown targets do not mutate inputs.",
                "The action log is complete for the successful run.",
            ],
            "ahead": """
The form gains a second page after submit, with a new confirmation id and a hidden field the agent did not type. Extend the tiny DOM with one page transition triggered by submit, and require the agent to `read` the new page's id before it is allowed to answer. A script that answers from the first page's confirmation alone must fail. The follow-on is carrying state across a transition without adding a new action type.
            """.strip(),
        },
        {
            "day": 61,
            "slug": "notes-researcher",
            "title": "A Notes Researcher that Cites",
            "level": "Advanced",
            "summary": "Answer a question from local markdown notes with the quote-or-abstain rule wired into the tool loop.",
            "concept": """
The retrieval stack can quote, and the agent loop can call tools. This project connects them without loosening either rule. The only retrieval tool is `search_notes(query)`, which returns chunk ids and texts from a notes folder using BM25. The only answer tool is `quote(chunk_id, text)` which succeeds only if text is an exact substring of that chunk. A final answer must be one of those successful quotes or an abstention. A scripted policy handles two questions: one answerable from the notes, one not. The unanswerable question must end in abstain even if a chunk shares several words. You will not add a free-text `finish` tool that bypasses `quote`. If the policy tries, the runner rejects it. The point is to make the citation check a tool result, not a convention the model is asked to respect.
            """.strip(),
            "approach": """
Reuse a small BM25 implementation and a handful of notes you write. `quote` looks up the chunk by id from the same index `search_notes` uses, so the policy cannot quote a chunk it invented an id for unless that id exists, and cannot quote text that is not there. The runner's terminal states are `quoted` and `abstained`. Anything else is an error. Log the search results and the quote attempts. A test calls `quote` with a near-miss string that differs by one word and expects failure. Another test omits search and calls `quote` with a real pair, which is allowed if the id exists: search is how the agent discovers ids, not a permission check. Do not confuse the two. Write that down so the citation rule stays about text, not about a ritual of having searched first.
            """.strip(),
            "components": [
                ("Notes index", "Local markdown chunked and scored with BM25."),
                ("Search tool", "Returns ids and texts."),
                ("Quote tool", "Exact substring check against the indexed chunk."),
                ("Terminal states", "Quoted or abstained, with no free-text finish path."),
            ],
            "flow": [
                "Index four short notes, one of which contains a fee sentence.",
                "Run the answerable question and assert the quote tool succeeded.",
                "Run the unanswerable question and assert abstention and zero successful quotes.",
                "Reject a `finish` tool name.",
                "Fail a one-word-off quote in a unit test.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "BM25 over local markdown",
                "Scripted policy, model optional and off in tests",
            ],
            "setup": [
                "Create `notes-researcher/` with `notes/`, `index.py`, `loop.py`, and tests.",
                "Run both questions.",
                "Run tests.",
                "Write `notes.md` explaining that search is discovery and quote is the check.",
            ],
            "done": [
                "The answerable run ends `quoted` with a substring of a real chunk.",
                "The unanswerable run ends `abstained` with no successful quote.",
                "A free-text finish tool is rejected.",
                "A one-word-off quote fails.",
            ],
            "ahead": """
A quote can be exact and still be the wrong edition if notes from two years share a sentence frame. Add an `edition` field on each note and a required `edition` argument on `quote` that must match the chunk. Fixture two notes with the same sentence and different editions, and show that quoting the 2024 sentence while asking for 2026 fails. The follow-on keeps the substring check and adds a second predicate the tool enforces, rather than hoping the policy prefers the right file.
            """.strip(),
        },
        {
            "day": 62,
            "slug": "subagent-mailbox",
            "title": "A Mailbox for Subagents",
            "level": "Advanced",
            "summary": "Let a parent post a task to a child and accept only a structured reply on a mailbox, not a shared scratchpad.",
            "concept": """
A parent agent that calls a child as a function and reads the child's scratchpad will depend on private details. This project gives the child a mailbox. The parent writes a task message with an id, a question, and the chunk ids the child is allowed to read. The child may use only those ids. It posts a reply message with the same task id, a status, and either a quote or an error code. The parent is not given a function that reads the child's tool log. A test asserts the parent's visible state after the reply does not contain the child's intermediate search strings. You will run one successful delegation and one where the child is asked about a chunk id that was not in the allow-list. That reply is an error, and the parent must surface the error rather than retry the child with a widened list. Widening is a different task with a different id.
            """.strip(),
            "approach": """
Messages are JSON records on two lists: inbox and outbox. The child function receives one task and returns one reply. It does not receive a callback into the parent. The allow-list is checked inside the child's search tool, which is a filtered view of the index. A reply that cites a chunk outside the list is rejected by the mailbox validator before the parent sees it, and replaced with an error reply. This keeps a buggy child from laundering a citation. The parent policy is scripted: post, wait, stop. No recursive delegation. A test that tries to post a second child task while the first is open fails, so mailboxes do not become an unbounded tree on this day.
            """.strip(),
            "components": [
                ("Task message", "Id, question, and allowed chunk ids."),
                ("Child view", "Search restricted to the allow-list."),
                ("Reply validator", "Rejects citations outside the list before the parent reads them."),
                ("Parent state", "Sees the reply and not the child's scratchpad."),
            ],
            "flow": [
                "Implement the mailbox and the allow-list filter.",
                "Run a task whose answer is inside the allow-list.",
                "Run a task whose only supporting chunk is outside the list and expect an error reply.",
                "Assert the parent state lacks the child's query strings.",
                "Assert a second open task is rejected.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Local notes index",
                "JSON messages",
            ],
            "setup": [
                "Create `mailbox/` with `mail.py`, `child.py`, `parent.py`, and tests.",
                "Run both delegations.",
                "Run tests.",
                "Keep the child's log on disk for you to debug, but do not pass that path into the parent function.",
            ],
            "done": [
                "A citation outside the allow-list never appears in the parent's reply object.",
                "The parent function signature does not accept a child log path.",
                "Two open tasks are rejected.",
                "The successful reply quotes a chunk that was on the list.",
            ],
            "ahead": """
The parent currently stops on the first error. Add a single, explicit follow-up task id that may cite one extra chunk id, chosen from the error's `blocked_ids` field, and no others. The follow-up must reference the original task id. A parent that opens a follow-up without that reference, or that adds two extra ids, is rejected. The step-ahead is a bounded widening you can see in the mailbox, not a retry with a fresh unrestricted child.
            """.strip(),
        },
        {
            "day": 63,
            "slug": "scored-gridworld",
            "title": "A Scored Gridworld",
            "level": "Advanced",
            "summary": "Put an agent in a tiny grid, score a task, and show a script that loops without progress.",
            "concept": """
Tool-using transcripts are hard to score because the world is implicit. A grid is a world you can score. This project builds a 5 by 5 grid with a dock, a bike, and a goal cell. The agent may `move` in four directions and `pickup`. Walls and the edge reject the move with an observation and do not change position. The score is 1 when the bike reaches the goal in at most 12 actions, otherwise 0. A scripted policy solves it. A second policy chases a loop: move left, move right, forever. The runner's budget stops it, and the score is 0. You will log positions after every action. This is an environment and a score, not a trace debugger and not a failure-taxonomy product. You do not need to classify why the loop happened beyond showing that position did not change across a full cycle.
            """.strip(),
            "approach": """
The environment is a pure function from state and action to state and observation, plus a reward of 0 until the goal condition, then 1, and the episode ends. Illegal moves return the same state. The loop policy is deterministic. The progress check in the required path is simple: if the position set of the last four actions has size 1, stop early with score 0 and reason `no-progress`. That check is local to this environment. Do not generalize it into a library of agent failure types. Seed nothing unless you add an obstacle that is random. The grid is fixed so the successful action list is a test fixture.
            """.strip(),
            "components": [
                ("Grid state", "Agent position, bike position, goal, and whether the bike is held."),
                ("Action set", "Four moves and pickup, with rejected moves leaving state unchanged."),
                ("Score", "1 only if the bike is on the goal within the action cap."),
                ("Loop policy", "A policy the no-progress rule stops."),
            ],
            "flow": [
                "Implement the transition function and a test that an illegal move does not change state.",
                "Run the solving script and assert score 1 and a known action count.",
                "Run the loop policy and assert score 0 and reason `no-progress`.",
                "Assert the position log length matches the action count for the solver.",
                "Assert pickup off the bike cell is a no-op observation and does not set the held flag.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library only",
                "No game engine",
            ],
            "setup": [
                "Create `gridworld/` with `env.py`, `policies.py`, and tests.",
                "Run both policies and write `out/trace.json` for each.",
                "Run tests.",
                "Draw the grid in the notes with the goal marked, so a reader can replay the solver by hand.",
            ],
            "done": [
                "The solver scores 1 on the fixed grid.",
                "The loop policy scores 0 with `no-progress`.",
                "Illegal moves do not change state.",
                "The notes include the grid and the solver's action list.",
            ],
            "ahead": """
The no-progress rule misses a policy that walks in a large square and never picks up the bike. Add a second stagnation rule: if `pickup` has not succeeded and the Manhattan distance to the bike has not decreased for six moves, stop with reason `no-approach`. Fixture a square-walk policy that stays far from the bike and assert that reason. Keep the original no-progress rule for the left-right loop. The follow-on is two stopping rules with different fixtures, not one vague notion of being stuck.
            """.strip(),
        },
        {
            "day": 64,
            "slug": "repair-after-correction",
            "title": "Repair After a Correction",
            "level": "Advanced",
            "summary": "When the user says the other dock was meant, revise the slot you filled and do not defend the first one.",
            "concept": """
A form-filling agent stores a dock id from the first user turn. The user then says "no, the other one, the indoor dock." A brittle agent repeats the first id because it is already in the scratchpad. This project models dialogue state as slots: `dock_id` and `fee_code`, each with a value and a `source_turn`. A correction pattern clears the slot the pattern names and sets it from the next resolvable description. "Indoor dock" resolves through a table of dock attributes, not through the previous slot. If two docks are indoor, the agent must ask which, and it must not keep the previous dock id while it asks. You will script the user with two turns and assert the slot after turn two is the indoor dock, and that the first dock id is recorded only as a superseded value, not as the current one.
            """.strip(),
            "approach": """
The resolver maps attributes to dock ids. Corrections match a small set of phrases you list, including "the other one" and "no". A correction without a resolvable replacement clears the slot and sets status `needs-clarification`. It does not leave the old value in place with a note. Superseded values go to a history list the answer renderer ignores. The answer renderer reads current slots only. A test renders the answer after the correction and asserts the first dock id is absent. Another test has two indoor docks and asserts the current slot is empty and the question names the attribute, not the old id.
            """.strip(),
            "components": [
                ("Slots", "Value, source turn, and status."),
                ("History", "Superseded values that the answer renderer does not read."),
                ("Attribute resolver", "A table from attributes to dock ids."),
                ("Clarification", "Empty slot when the correction is ambiguous."),
            ],
            "flow": [
                "Fill `dock_id` from turn one with an outdoor dock.",
                "Apply the correction turn that says indoor.",
                "Assert the current value is the indoor dock and history holds the outdoor id.",
                "Render the answer and assert the outdoor id is absent.",
                "Run the two-indoor-docks fixture and assert clarification with an empty current value.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "JSON dialogue scripts",
                "No model required",
            ],
            "setup": [
                "Create `repair/` with `slots.py`, `dialogues.jsonl`, and tests.",
                "Run both dialogues.",
                "Run tests.",
                "Write one sentence in the notes: the current slot is the only value the answer may use.",
            ],
            "done": [
                "After a clear correction, the answer text contains the new dock and not the old one.",
                "The old value is still in history for audit.",
                "An ambiguous correction clears the current slot.",
                "The renderer has no parameter that passes history into the answer, and a signature test can lock that.",
            ],
            "ahead": """
A second correction can refer to history: "go back to the first one." Add an explicit undo command that pops history into the current slot, and reject it when history is empty. Do not make ordinary noun phrases search history. Fixture "go back to the first one" succeeding once and a second undo failing with `empty-history`. The follow-on keeps undo as a named command so a vague sentence cannot resurrect a superseded fee code by accident.
            """.strip(),
        },
    ],
}
