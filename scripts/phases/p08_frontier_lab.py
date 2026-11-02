"""Phase 8 — Frontier Lab. Days 91–100. All advanced."""

PHASE = {
    "id": "08",
    "dir": "08-frontier-lab",
    "name": "Frontier Lab",
    "blurb": "Practice the system patterns that showed up after plain chat: verifiers, constrained output, prefix reuse, small models, tool protocols, and a capstone that cites its own evidence.",
    "outcome": "Explain a recent system pattern by building a small, testable version of it.",
    "goal": "Finish this phase with a capstone handbook agent that retrieves, spends a budget, and replays from a cassette, plus a set of small studies: verifiers, schemas, prefix cost, a narrow small model, a read-only tool protocol, and a comparison of full context against retrieval.",
    "skills": [
        "Test-time retries gated by a verifier",
        "Schema-constrained output versus parse-and-repair",
        "Prefix-reuse accounting",
        "A small local classifier compared with a teacher",
        "A read-only tool protocol over local notes",
        "Long-context prompts versus retrieval on one corpus",
        "Reading a chart fixture against an expected number",
        "Task envelopes between processes",
        "A cheap proposer and a strong confirmer",
        "A capstone run with evidence attached",
    ],
    "projects": [
        {
            "day": 91,
            "slug": "retry-under-a-verifier",
            "title": "Retry Under a Verifier",
            "level": "Advanced",
            "summary": "Let a scripted model retry until a verifier accepts the format, and stop when the budget is spent.",
            "concept": """
Spending more inference on a hard question only helps if you can reject a bad attempt. This project defines a verifier that accepts a string only when it is a single fee line matching a pattern: a code, an amount, and a unit. A scripted generator produces a sequence of attempts, some malformed. The loop keeps the first accepted attempt and records how many tries it used. If the budget runs out, it returns `unverified` and does not return the last bad string as if it were an answer. You will compare that policy to a one-shot policy that returns the first attempt even when the verifier would fail it. On a fixture where the first attempt is malformed and the second is valid, the retry policy must be the only one that answers. This is test-time compute with an explicit budget, not a claim that a larger model would have gotten the fee right.
            """.strip(),
            "approach": """
The generator is a list of strings per question, which stands in for successive samples. The verifier is a pure function. The budget is an integer on the case. The loop never calls the verifier more times than the budget, and a test uses a generator longer than the budget whose only valid line sits past the budget. That case must end `unverified`. Log every attempt and the verifier's reason. Do not add a model. The lesson is the control flow: generate, check, stop.
            """.strip(),
            "components": [
                ("Verifier", "A pure accept or reject with a reason."),
                ("Attempt list", "Scripted stand-in for successive samples."),
                ("Budget", "Maximum verifier calls."),
                ("One-shot contrast", "Returns the first attempt without verification."),
            ],
            "flow": [
                "Implement the verifier and test it on a valid and an invalid line.",
                "Run the retry loop on a case that succeeds on attempt two.",
                "Run a case whose only valid attempt is past the budget.",
                "Compare to one-shot on the first case and assert the outputs differ.",
                "Assert the unverified case does not include the rejected strings in the answer field.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Scripted attempt lists",
                "No hosted model",
            ],
            "setup": [
                "Create `verifier-retry/` with `verify.py`, `loop.py`, and tests.",
                "Run the three cases.",
                "Run tests.",
                "Write the budget next to the case id in the output.",
            ],
            "done": [
                "A later valid attempt is returned and earlier rejects are only in the log.",
                "A valid attempt past the budget yields `unverified` and an empty answer.",
                "One-shot and retry disagree on the planted malformed-first case.",
                "Verifier call count never exceeds the budget.",
            ],
            "ahead": """
Majority vote across attempts can accept a wrong fee that is well formatted. Add a second verifier that checks the amount against a table, and compare vote-of-three to verifier-accept on a fixture where two attempts agree on a wrong amount and one attempt is right and formatted. Voting picks the wrong amount. The table verifier picks the right one or abstains. The follow-on shows a case where agreement is not evidence, and records both decisions without averaging them.
            """.strip(),
        },
        {
            "day": 92,
            "slug": "constrained-json",
            "title": "Constrained JSON Versus Repair",
            "level": "Advanced",
            "summary": "Emit a tiny JSON object under a schema you enforce during decoding, and compare it to parsing and repairing free text.",
            "concept": """
Models that are asked for JSON often add a preamble or a trailing comma. Repair functions hide that by being clever, and they also hide when the model never produced the field you needed. This project implements a tiny constrained decoder over a vocabulary of tokens you define, including braces, keys, and a closed set of values. The decoder may only emit a token the schema allows in the current state. You will also implement a repair function that strips a preamble and trailing commas. On a scripted unconstrained token stream that is almost JSON, repair succeeds. On a stream that omits the required fee key, repair must fail rather than insert a default. The constrained decoder must be unable to omit the key because the state machine never reaches done without it. The comparison is the artifact.
            """.strip(),
            "approach": """
The schema is one object with a required `code` from a fixed set and a required `amount` integer. The constrained decoder is a state machine, not a general JSON Schema validator bolted on after the fact. It chooses the only legal next token when the scripted model proposes an illegal one, and it logs the override. If you would rather have it stop on an illegal token, pick that behavior and test it, but do not silently skip a required key. The repair path is separate and is not called by the constrained path. A test feeds the repair path a missing-key string and expects an error. A test feeds the constrained decoder a proposal to emit `done` too early and expects a refusal or an inserted required key that is logged as an override. Prefer refusal if insertion feels like inventing a value. Refusal is the better default.
            """.strip(),
            "components": [
                ("Schema state machine", "Legal tokens from the current state."),
                ("Constrained decoder", "Refuses illegal tokens and logs them."),
                ("Repair function", "Strips preamble and trailing commas, and does not invent keys."),
                ("Missing-key fixture", "Repair fails, constrained decoding cannot finish early."),
            ],
            "flow": [
                "Write the state machine and a diagram of states in the notes.",
                "Decode a fully legal proposal and expect no overrides.",
                "Propose an early finish and expect refusal.",
                "Repair a trailing-comma string and expect success.",
                "Repair a missing-key string and expect failure.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "A token vocabulary you define",
                "No grammar library required",
            ],
            "setup": [
                "Create `constrained/` with `decode.py`, `repair.py`, and tests.",
                "Run both paths on the shared fixtures where both apply.",
                "Run tests.",
                "State in the notes that repair and constrained decoding are different policies.",
            ],
            "done": [
                "The constrained decoder never emits an object missing `code` or `amount`.",
                "Repair does not invent a missing key.",
                "A trailing comma is repairable and is unnecessary on the constrained path.",
                "Overrides or refusals are logged rather than dropped.",
            ],
            "ahead": """
Schemas change. Add a version field and a decoder that refuses a v1 stream when asked for v2, where v2 requires `currency`. Show a repaired v1 object, which is valid JSON, failing a v2 check. The follow-on is that valid JSON is not the same as the object your caller required, and the version is part of the contract rather than a comment in the prompt.
            """.strip(),
        },
        {
            "day": 93,
            "slug": "prefix-accounting",
            "title": "Accounting for a Shared Prefix",
            "level": "Advanced",
            "summary": "Measure how many prompt tokens a shared system prefix would reuse, and invalidate the reuse when the tool list changes.",
            "concept": """
A long system prompt that is identical across calls is work you should not pay for twice. Hosted APIs expose prefix caching. You may not have one. This project accounts for reuse without claiming to be the vendor's cache. You hash the prefix tokens. A second call with the same hash records `reused_tokens` equal to the prefix length and `new_tokens` equal to the suffix. A call with a different hash records the full prompt as new. You will show a batch of ten questions with a shared handbook preamble where the reused fraction is high, then change one tool description in the preamble and show the hash changing for every question. The study is the invalidation. A cache that ignores a tool-list edit will serve instructions you no longer mean.
            """.strip(),
            "approach": """
Tokenization can be whitespace or your byte-pair encoder. The account function does not talk to a network. It returns a record per call. The batch report sums reused and new tokens. A test runs the same prefix twice and expects the second call's reused count to equal the prefix length. A test flips one character in a tool description and expects reused tokens to be zero for the next call. Do not implement an actual KV cache. If you describe one in the notes, label it as a picture of why the hash exists, not as something you built.
            """.strip(),
            "components": [
                ("Prefix hash", "Hash of the token ids before the question."),
                ("Account record", "Reused tokens and new tokens per call."),
                ("Shared-preamble batch", "Ten questions, one prefix."),
                ("Invalidation edit", "A one-character tool-list change that zeros reuse."),
            ],
            "flow": [
                "Tokenize a preamble and ten questions.",
                "Account the batch and record the reused fraction.",
                "Edit the preamble and account again.",
                "Assert reuse collapsed.",
                "Assert a repeated identical call reuses the prefix.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Your tokenizer or a whitespace tokenizer",
                "JSON report of token accounts",
            ],
            "setup": [
                "Create `prefix-account/` with `account.py` and tests.",
                "Run both batches.",
                "Run tests.",
                "Write the reused fraction in `notes.md` and the fraction after the edit.",
            ],
            "done": [
                "Identical prefixes reuse the prefix length on the second call.",
                "A one-character preamble edit zeros reuse.",
                "The report sums match the sum of the rows.",
                "The notes do not claim you implemented a vendor cache.",
            ],
            "ahead": """
Tool results also get prepended, and caching them is wrong when the tool output changes. Extend the hash so the cached region is only the stable preamble, and tool results are always new tokens even if the text matches the previous call. Fixture two calls with the same preamble and the same tool result text and show the tool-result tokens counted as new. The follow-on draws a boundary: reused instructions, fresh observations.
            """.strip(),
        },
        {
            "day": 94,
            "slug": "narrow-small-model",
            "title": "A Small Model for a Narrow Label",
            "level": "Advanced",
            "summary": "Train a tiny local classifier on labels from a teacher script, and list the cases where the student disagrees.",
            "concept": """
A large model is an expensive way to map a dock note to `maintenance` or `billing` if a small classifier can do it. This project writes a teacher as a rule list that labels notes, trains a bag-of-words logistic model or a linear model you already built, and compares the student to the teacher on a held-out set of notes you wrote. The teacher is not a hosted model and not a synthetic-data release. It is a stand-in with known rules, so you can see the student's errors. You will report agreement, and you will list every disagreement with the note text. You will not claim the student is safe to deploy. You will say what the student is allowed to do: suggest a label next to the note, with the disagreement list as the review queue.
            """.strip(),
            "approach": """
The teacher rules are ordered and readable. The student trains only on the train split. The test split is notes the training loop never sees. Use the rider-level or note-level split you already understand, and do not let a near-duplicate sit in both splits. A test plants a duplicate and expects the splitter to keep both copies on one side. Agreement is exact label match. The disagreement file is the deliverable a person would read. If agreement is perfect, add notes the rules label for a subtle reason and the bag of words is likely to miss, such as a short negation. Do not stop at a perfect score on easy notes.
            """.strip(),
            "components": [
                ("Teacher rules", "An ordered, readable labeling function."),
                ("Student model", "A small local classifier trained on the teacher's train labels."),
                ("Held-out notes", "Written by you, disjoint from training."),
                ("Disagreement list", "Every note where student and teacher differ."),
            ],
            "flow": [
                "Write the rules and thirty notes. Split them.",
                "Label the train notes with the teacher and fit the student.",
                "Score the test notes.",
                "Write every disagreement.",
                "Assert a planted duplicate cannot land in both splits.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Your linear classifier or a few dozen lines of new code",
                "Local text only",
            ],
            "setup": [
                "Create `small-label/` with `teacher.py`, `train.py`, and tests.",
                "Run training and the report.",
                "Run the duplicate-split test.",
                "State the allowed use of the student in the first line of the notes.",
            ],
            "done": [
                "Train notes and test notes are disjoint, including near-duplicates you planted.",
                "The disagreement list is complete relative to the test set.",
                "The teacher rules are readable without running the model.",
                "The notes name what the student is not allowed to do.",
            ],
            "ahead": """
The student can be confidently wrong. Add a score, the predicted probability, and send only disagreements above a probability you choose to a `priority_review` list. Low-probability disagreements stay in the full list and out of the priority list. Fixture one high-probability miss and one low-probability miss. The follow-on is a review queue ordered by how sure the student was, not a claim that the probability is calibrated.
            """.strip(),
        },
        {
            "day": 95,
            "slug": "field-notebook-protocol",
            "title": "A Read-Only Field Notebook Protocol",
            "level": "Advanced",
            "summary": "Expose local markdown notes through two tools, search and get, with a schema and no write path.",
            "concept": """
Agents need a narrow way to read your notes. This project defines a small protocol: a process receives a JSON request and returns a JSON response. The only methods are `search` and `get`. `search` takes a query and returns heading matches with ids. `get` takes an id and returns that section's text. There is no method that writes, deletes, or shells out. A request with method `write` returns an error code `unknown-method` and does not touch the filesystem except to append a log line if you choose to log. You will implement the server in one module and a client function that sends a request dict. Transport can be in-process. The protocol shape is what you are practicing, the same shape a Model Context Protocol server uses, without building a price tracker or a review scraper.
            """.strip(),
            "approach": """
The notebook is a folder of markdown files with headings. Ids are stable: file path plus heading slug. `search` is BM25 or a simple substring scan over headings, and you document which. `get` returns the section body and refuses an id it did not issue. A test calls `get` with a path traversal such as `../secrets.md` and expects an error, not a file read outside the notebook root. Resolve ids through a table you built, not through string concatenation onto a base path. That choice is the security-relevant part of an otherwise read-only toy, and the test is required.
            """.strip(),
            "components": [
                ("Request schema", "Method name and arguments."),
                ("Search method", "Returns ids and headings from the notebook only."),
                ("Get method", "Returns a section by an issued id."),
                ("Unknown-method error", "Any other method, including write."),
            ],
            "flow": [
                "Index the notebook into an id table.",
                "Serve `search` and `get` in-process.",
                "Reject `write` without changing a source file's mtime. A test can record mtimes.",
                "Reject a traversal id.",
                "Log requests as method names only, without dumping full section bodies into the log.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Local markdown notebook",
                "JSON requests and responses",
            ],
            "setup": [
                "Create `notebook-protocol/` with `server.py`, `notebook/`, and tests.",
                "Run a scripted client session: search, then get.",
                "Run the rejection tests.",
                "Describe the two methods in `protocol.md` in a few lines a caller could implement.",
            ],
            "done": [
                "Search then get returns a real section from your notebook.",
                "`write` does not modify source files.",
                "An id outside the issued table does not read an arbitrary path.",
                "The log does not store full section bodies.",
            ],
            "ahead": """
A write path will be requested. Add a third method, `propose_edit`, that writes a patch file under `proposals/` and never modifies the notebook. The patch file contains the id and the suggested text. A test asserts the notebook file hash is unchanged and the proposal file exists. `propose_edit` on an unknown id writes nothing. The follow-on is a suggestion that cannot be confused with a saved edit.
            """.strip(),
        },
        {
            "day": 96,
            "slug": "window-versus-index",
            "title": "Window Versus Index",
            "level": "Advanced",
            "summary": "Answer the same questions from the full handbook in the prompt and from retrieval, and compare citations and cost.",
            "concept": """
If the handbook fits in the window, retrieval can look like extra machinery. It stops looking that way when the handbook grows or when the model quotes a sentence from the wrong section because the whole text was in front of it. This project runs the same ten questions two ways. The window condition pastes the full handbook into the prompt of a scripted reader that searches the pasted text with the same quote rules as the index condition. The index condition uses your BM25 stack and quotes a chunk. Both must return a quote or an abstention. You will compare exact gold-span hits and a fictional token cost: the window condition pays for the whole handbook every time, and the index condition pays for the retrieved chunks. You are not measuring a hosted model's reading skill. You are measuring the two pipelines.
            """.strip(),
            "approach": """
Use a handbook small enough to paste. Gold spans are the ones you marked earlier. The scripted reader returns the first sentence in its context that passes the coverage threshold, or abstains. Giving both conditions the same reader means the difference is the context they saw, not a different answering policy. Cost numbers are fictional and labeled. A results table has one row per question per condition. A question the index misses and the window hits is interesting, and so is the reverse if a chunk boundary is why. Write both if they occur. If they do not, say so rather than inventing a miss.
            """.strip(),
            "components": [
                ("Shared reader", "Quote-or-abstain over whatever text it was given."),
                ("Window condition", "Full handbook as context."),
                ("Index condition", "Retrieved chunks as context."),
                ("Cost model", "Fictional token prices labeled as fictional."),
            ],
            "flow": [
                "Run the ten questions under both conditions.",
                "Score gold-span hits.",
                "Sum fictional costs.",
                "List questions where the conditions disagree.",
                "Write the table and a short interpretation that cites the table.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Your handbook, BM25, and quoter",
                "A CSV comparison",
            ],
            "setup": [
                "Create `window-vs-index/` with `compare.py` and the handbook.",
                "Run both conditions.",
                "Run a test that the shared reader is the same function object or the same module path for both. Do not fork the policy.",
                "Label costs as fictional in the table header.",
            ],
            "done": [
                "Every question has two rows.",
                "Disagreements are listed or explicitly absent.",
                "Costs are reproducible from the token counts in the table.",
                "Both conditions use the same quote rule.",
            ],
            "ahead": """
Grow the handbook by duplicating background sections until the window cost exceeds a budget you set, while the index cost stays flat. Record the smallest size where the window condition is over budget and the index condition still answers. That size is the crossover in your notes. If the index starts to miss because duplicates drowned BM25, record that too. The follow-on is the point where pasting everything stops being the default, measured on your corpus rather than assumed from a blog post.
            """.strip(),
        },
        {
            "day": 97,
            "slug": "chart-peak",
            "title": "A Chart with an Expected Peak",
            "level": "Advanced",
            "summary": "Read a chart you render to SVG, answer the peak with a tolerance, and refuse a chart whose axis is cut.",
            "concept": """
People paste charts into chats and ask for the peak. The model answers with a number that is hard to audit. This project renders a tiny bar chart to SVG from a data table, then answers "what is the peak" by reading the SVG's data attributes, not by eyeballing pixels. The expected answer is the max value in the table, and the tolerance is zero because you control the source. A second chart cuts the axis so the bars start at a non-zero baseline. The required behavior is to refuse with reason `cut-axis`, because a visual comparison would mislead, even though the data attribute still holds the true value. You will test both. The point is an answer policy for a figure, not a vision-model benchmark.
            """.strip(),
            "approach": """
The SVG writer puts `data-value` and `data-baseline` on each bar. The reader refuses if any baseline is not zero. Otherwise it returns the max `data-value` and the category. A test tampers with a `data-value` so it no longer matches the source table and expects the reader to fail a consistency check you also run: every data value must appear in the source table. That check stops a chart that was edited by hand from being treated as authoritative over the table. The table remains the source of truth. The SVG is a view.
            """.strip(),
            "components": [
                ("Table source", "Categories and values."),
                ("SVG writer", "Bars with data attributes and a baseline."),
                ("Reader", "Returns the peak or a refusal."),
                ("Consistency check", "Data attributes must match the table."),
            ],
            "flow": [
                "Render a normal chart and read the peak.",
                "Assert the category and the value match the table max.",
                "Render a cut-axis chart and expect `cut-axis`.",
                "Tamper a data attribute and expect a consistency failure.",
                "Document that the table, not the picture, is authoritative.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "SVG as text",
                "No vision model and no browser",
            ],
            "setup": [
                "Create `chart-peak/` with `chart.py`, `read.py`, and tests.",
                "Write both SVGs to `out/`.",
                "Run tests.",
                "Open the SVG in a browser if you want to see it, but the tests must not require that.",
            ],
            "done": [
                "The zero-baseline chart returns the true peak category and value.",
                "The cut-axis chart is refused.",
                "A tampered attribute fails the consistency check.",
                "The notes name the table as the source of truth.",
            ],
            "ahead": """
A second question asks for the trough, and a missing category should not be treated as zero. Add a trough reader that ignores categories listed in `not_observed` rather than treating them as value zero. Fixture a week with a missing day and show the trough computed on observed days only, plus a refusal if fewer than three days were observed. The follow-on is an answer that knows the difference between a measured zero and a gap.
            """.strip(),
        },
        {
            "day": 98,
            "slug": "task-envelopes",
            "title": "Task Envelopes Between Processes",
            "level": "Advanced",
            "summary": "Pass a task envelope from a requester to a worker and return a completion receipt a third process can cancel.",
            "concept": """
Two agents that share memory are one program. Two processes that pass envelopes can fail independently. This project defines a minimal envelope: `task_id`, `deadline`, `question`, and `allowed_methods`. The worker may use only those methods and returns a receipt: `task_id`, `status`, and either a quote or an error. A monitor process can mark a task `cancelled` before the worker finishes. The worker checks the monitor before it returns and must not return `complete` for a cancelled id. You will run this in-process with three functions standing in for processes, and also across two threads or two local sockets if you want the failure to be more real. The required tests can stay in-process. The envelope is inspired by agent-to-agent handshakes and is not a full protocol implementation.
            """.strip(),
            "approach": """
Ids are generated by the requester and are unique in a test that fires two tasks. The worker's tool list is filtered by `allowed_methods`. A method outside the list errors. The monitor is a dict the worker reads at the start and at the end. A cancel that arrives after the receipt is written does not rewrite the receipt. Instead the monitor stores `cancel_after_complete`, which the test asserts. That race is the interesting one. A cancel that arrives before completion yields status `cancelled` and no quote.
            """.strip(),
            "components": [
                ("Envelope", "Task id, deadline, question, allowed methods."),
                ("Worker", "Filtered methods and a receipt."),
                ("Monitor", "Cancel flag the worker checks at the end."),
                ("Late-cancel record", "A cancel after completion does not rewrite the receipt."),
            ],
            "flow": [
                "Submit an envelope and receive a complete receipt.",
                "Submit one whose method is not allowed and expect an error receipt.",
                "Cancel before the worker finishes and expect `cancelled` with no quote.",
                "Cancel after the receipt is stored and expect the receipt unchanged plus a late-cancel note.",
                "Assert two tasks do not share an id.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "In-process functions as the required path",
                "JSON envelopes",
            ],
            "setup": [
                "Create `envelopes/` with `protocol.py` and tests.",
                "Run the four scenarios.",
                "Run tests.",
                "Describe the race in the notes in two sentences.",
            ],
            "done": [
                "A pre-completion cancel suppresses the quote.",
                "A post-completion cancel does not rewrite the receipt.",
                "Disallowed methods cannot be called by the worker.",
                "Task ids are unique across the two-task test.",
            ],
            "ahead": """
Add a deadline. If the worker's scripted clock passes the deadline before the receipt, the status is `expired` and any quote it would have returned is dropped. Fixture a slow worker and a fast worker against the same deadline. The follow-on is a receipt that can be late without being treated as success, and the monitor can tell expiry from cancellation.
            """.strip(),
        },
        {
            "day": 99,
            "slug": "cheap-confirm",
            "title": "A Cheap Proposal and a Strong Confirm",
            "level": "Advanced",
            "summary": "Let a cheap policy propose a tool and a strong policy confirm or override it, and log the override rate.",
            "concept": """
Running the expensive path on every turn is a choice, not a law. This project splits a decision. The cheap policy proposes a tool name from a small rule list. The strong policy, also scripted but allowed to see the gold tool for the fixture, confirms or overrides. In the real pattern the strong policy would be a larger model. Here it is a function you can score. The harness logs proposals, confirmations, and overrides. The override rate is overrides divided by proposals. You will fixture a set where the cheap policy is usually right and one where it proposes `quote` before any search. The strong policy must override that case. The cheap policy does not get to call the tool. Only a confirmed name is executed. This is not a human review queue and not a confidence score routed to an analyst. It is a two-policy gate in front of a tool call.
            """.strip(),
            "approach": """
Execution uses the confirmed name only. A test stubs the tools and counts calls. An overridden proposal produces zero calls under the cheap name and one call under the strong name. If the strong policy rejects both, nothing is called and the status is `no-tool`. Include that third outcome so confirmation is not forced to pick something. The report lists the override rate and the no-tool count. Do not hide overrides. They are the price of letting the cheap policy speak first.
            """.strip(),
            "components": [
                ("Cheap proposer", "A rule list that emits a tool name."),
                ("Strong confirmer", "Confirm, override, or reject."),
                ("Execution gate", "Calls only the confirmed name."),
                ("Override log", "Proposal, decision, and whether a call happened."),
            ],
            "flow": [
                "Run a batch where the cheap policy matches the fixture's expected tool.",
                "Run the premature-quote case and assert an override and a search call.",
                "Run a case the strong policy rejects and assert zero calls.",
                "Compute the override rate from the log in a test, not by hand only.",
                "Assert the cheap name was not called on the override fixture.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Scripted policies",
                "Stub tools that count calls",
            ],
            "setup": [
                "Create `cheap-confirm/` with `policies.py`, `gate.py`, and tests.",
                "Run the batch and write `out/overrides.jsonl`.",
                "Run tests.",
                "State that both policies are scripted stand-ins.",
            ],
            "done": [
                "Confirmed tools run and proposed-but-overridden tools do not.",
                "A reject runs nothing.",
                "The override rate is computed from the log.",
                "The premature quote is overridden to a search in the fixture.",
            ],
            "ahead": """
A cheap policy that is almost never overridden is paying for a confirmer it may not need on that tool. Add a per-tool tally. If `search` was confirmed ten times with zero overrides, mark it `eligible-for-autonomy` in a recommendation file that does not itself disable the confirmer. Fixture the tally and assert the file is a recommendation, by checking that the gate still confirms `search` until a separate config flag is flipped. The follow-on separates the measurement from the permission change.
            """.strip(),
        },
        {
            "day": 100,
            "slug": "handbook-field-study",
            "title": "Field Study: A Handbook Agent Under a Harness",
            "level": "Advanced",
            "summary": "Answer handbook questions with retrieval, a budget, and a cassette, and attach an evidence note to the run.",
            "concept": """
The last project uses pieces you already built, on one handbook, without turning them into a platform. A scripted agent may search notes, quote a span, and stop. It has a tool budget of four. Search is served from a cassette recorded by a fake transport or by a local function treated as a cassette: the replay run performs no new indexing side effects beyond reading files. The output for each question is an evidence note: the queries, the chunk ids returned, the quote or the abstention, the budget remaining, and the cassette key. A question with no supporting span abstains inside the budget. A question that would need a fifth search stops partial and says which checklist item was left. You will run the set twice and show the evidence notes matching. That match is the close of the atlas: a result someone else can replay.
            """.strip(),
            "approach": """
Keep the agent scripted so the replay is exact. The evidence note is JSON, one object per question, written to `out/evidence.jsonl`. The second run compares hashes of that file to the first. A mismatch fails. Do not call a hosted model in the required path. If you add one later, record it as a third run that is allowed to differ, and do not overwrite the scripted evidence. The abstention and the partial budget stop must both appear in the question set, so the field study shows a limit and not only successes. The cassette miss path should be tested with one extra question you deliberately leave unrecorded, and that question's note says `cassette-miss` rather than inventing a chunk.
            """.strip(),
            "components": [
                ("Scripted handbook agent", "Search and quote under a tool budget."),
                ("Cassette", "Recorded search results keyed by query."),
                ("Evidence note", "Queries, ids, quote or abstain, budget remaining, cassette key."),
                ("Replay check", "A second run's evidence hash matches the first."),
            ],
            "flow": [
                "Record cassettes for the answerable questions and the abstention question.",
                "Run the agent and write evidence notes.",
                "Include one question that exhausts the budget and one unrecorded query.",
                "Run again and compare hashes.",
                "Assert the unrecorded query does not produce a quote.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Your notes index, quote check, budget, and cassette",
                "JSONL evidence",
            ],
            "setup": [
                "Create `field-study/` with `agent.py`, `cassettes/`, `questions.jsonl`, and tests.",
                "Run record, then two replays.",
                "Run tests for abstain, budget stop, cassette miss, and hash match.",
                "Read one evidence note from top to bottom and confirm every id is in the cassette or explained by a miss.",
            ],
            "done": [
                "Two scripted runs produce the same evidence hash.",
                "At least one question abstains and one stops on the budget.",
                "A cassette miss does not invent a chunk.",
                "Every successful quote is an exact substring of a retrieved chunk in the note.",
            ],
            "ahead": """
Swap the scripted quoter for a second scripted quoter that is wrong on one question, and show the evidence hash changing while the cassette file's hash stays the same. The follow-on is a diff that localizes the change to the answer, not to retrieval. Write the two hashes and the question id that moved. If you cannot tell which question moved without re-reading every note, add a per-question hash to the evidence file and repeat the swap. The atlas ends when a change points at the component that moved.
            """.strip(),
        },
    ],
}
