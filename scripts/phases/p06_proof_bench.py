"""Phase 6 — Proof Bench. Days 65–78. All advanced."""

PHASE = {
    "id": "06",
    "dir": "06-proof-bench",
    "name": "Proof Bench: Evals and Harnesses",
    "blurb": "Score agent behavior with harnesses you can rerun offline: plan fidelity, cassettes, properties, and checks that do not depend on a single judge model.",
    "outcome": "Put a number and a failing fixture on an agent behavior you care about.",
    "goal": "Finish this phase with a bench of small harnesses, each aimed at one failure mode: a tool the plan did not license, a replay that drifted, an extraction scored as a set, a slot the agent forgot, a budget curve, and a case id that never changes in place.",
    "skills": [
        "Plan-licensed tool checks",
        "Recorded HTTP cassettes and replay",
        "Property tests and shrinking for tool arguments",
        "Set-valued extraction scores",
        "Disagreement sets across scripted models",
        "Hidden-slot multi-turn scripts",
        "Cost versus quality sweeps on a frozen set",
        "Conflicts between trusted instruction sources",
        "Pinned retrieval results",
        "Structural checklists for long answers",
        "Scripted personas with a patience counter",
        "Immutable evaluation case ids",
        "Repeat-run flake budgets",
        "Accepted tool-name sequences",
    ],
    "projects": [
        {
            "day": 65,
            "slug": "plan-licensed-tools",
            "title": "Was that Tool Licensed by the Plan?",
            "level": "Advanced",
            "summary": "Score each tool call on whether the checklist named it, separate from whether the final answer was right.",
            "concept": """
An agent can reach the right fee with a tool the plan never mentioned, which means the next run can wander. This project scores a finished transcript against the checklist that was approved before any call. Each action is `licensed` if its tool name appears on the current open item, and `unlicensed` otherwise. The final-answer check is a separate boolean: did `quote` match the gold substring. You will report both numbers. A fixture with the right answer and one unlicensed lookup must fail the license score and pass the answer score. A fixture with only licensed calls and a wrong quote must do the opposite. Collapsing these into one pass mark hides which part broke. The harness reads files. It does not run the agent.
            """.strip(),
            "approach": """
Inputs are `plan.json` and `transcript.jsonl`. The scorer walks actions in order, matching them to open items as the executor would, and emits a row per action. Summary metrics are license rate and answer correctness. A missing plan file is an error, not a vacuously licensed run. Write three fixtures: clean pass, unlicensed success, licensed wrong answer. The harness prints a table and exits non-zero if license rate is below 1 or the answer is wrong, and the exit code distinguishes the two failures so a script can tell them apart.
            """.strip(),
            "components": [
                ("Plan file", "Checklist items with tool names."),
                ("Transcript file", "Actions and a final answer."),
                ("License rows", "One verdict per action."),
                ("Separate exit codes", "License failure and answer failure are different statuses."),
            ],
            "flow": [
                "Implement the scorer as a pure function of the two files.",
                "Score the three fixtures and save the tables.",
                "Assert the unlicensed-success fixture fails only the license status.",
                "Assert a missing plan raises rather than returning a perfect license rate.",
                "Document the two metrics in `score_notes.md`.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "JSON fixtures",
                "No model calls inside the harness",
            ],
            "setup": [
                "Create `plan-license/` with `score.py`, `fixtures/`, and tests.",
                "Run the three fixtures.",
                "Run tests.",
                "Confirm the harness does not import the agent loop. It only reads files the loop already wrote.",
            ],
            "done": [
                "License rate and answer correctness are both reported.",
                "The unlicensed success and the licensed failure produce different statuses.",
                "A missing plan is an error.",
                "The scorer has no network access and no model import.",
            ],
            "ahead": """
A later call can repair an earlier unlicensed lookup, and a single license rate hides the recovery. Extend the row with `repaired_by`, the later action id that produced the gold answer, and report two rates: licensed actions, and unlicensed actions that were never needed for the gold quote. Fixture a transcript where an unlicensed call's result is unused because a later licensed call quotes the gold span. The follow-on question is whether the stray call was load-bearing. If you cannot tell from the transcript, the transcript is missing the field that would say so, and that gap belongs in the notes.
            """.strip(),
        },
        {
            "day": 66,
            "slug": "http-cassettes",
            "title": "Cassettes for Tool HTTP",
            "level": "Advanced",
            "summary": "Record an HTTP tool once and replay the bytes so a later run does not touch the network.",
            "concept": """
An agent tool that calls HTTP will score differently tomorrow if the server changes, and it will fail in a classroom with no network. This project wraps one tool, `get_status(dock_id)`, in a cassette. The first run, with a flag `record`, stores the URL, the query, and the response body under a key. Later runs with `replay` never open a socket. They return the stored body or fail with `cassette-miss`. A test uses a fake transport so recording does not need a real server. Replay must not call the transport at all, which you assert by counting calls. Editing the cassette body by hand is allowed only in a file you treat as source. The harness reads it. You will also show a miss: a dock id that was not recorded fails the replay run instead of falling through to the network.
            """.strip(),
            "approach": """
The cassette is a JSON map from a canonical request key to a body. The key includes the method, path, and sorted query. It does not include timestamps. The wrapper takes a transport function. In replay mode the wrapper does not receive a live transport, or it receives one that raises if called. Prefer the raise-if-called double so a mistake is loud. Record mode calls the transport once per distinct key and writes the file. A second record of the same key compares bodies and errors on conflict rather than silently overwriting. That conflict is how you notice an upstream that is not stable enough to cassette.
            """.strip(),
            "components": [
                ("Canonical key", "Method, path, and sorted query."),
                ("Cassette file", "Map from key to response body."),
                ("Replay guard", "Transport raises if replay tries to call it."),
                ("Conflict check", "A second record with a different body errors."),
            ],
            "flow": [
                "Implement record and replay modes.",
                "Record two dock ids using a fake transport.",
                "Replay them and assert the transport call count is zero.",
                "Replay a third id and assert `cassette-miss`.",
                "Record the same key with a different body and assert conflict, leaving the file unchanged.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "JSON cassette",
                "A fake transport in tests, no real HTTP required",
            ],
            "setup": [
                "Create `cassettes/` with `cassette.py`, `fixtures/status.json`, and tests.",
                "Run record, then replay, as two commands.",
                "Run tests.",
                "Add `cassettes/` output to the folder you would commit if this were a real suite, and say so in the notes.",
            ],
            "done": [
                "Replay performs zero transport calls.",
                "An unknown key is a cassette miss, not a live call.",
                "Conflicting records do not overwrite the stored body.",
                "Request keys ignore field order in the query.",
            ],
            "ahead": """
A cassette can go stale when the server adds a field the agent starts to require. Add a schema version on the cassette and a checker that compares replayed bodies to a list of required JSON keys. A body missing `status` fails with `cassette-stale` rather than returning JSON the agent will misread as an empty dock. Fixture a recorded body from version 1 and a required-key list from version 2. The follow-on is detecting drift at replay time, before the agent treats a missing field as a real observation.
            """.strip(),
        },
        {
            "day": 67,
            "slug": "tool-properties",
            "title": "Properties of a Tool",
            "level": "Advanced",
            "summary": "Generate random valid and invalid arguments for a tool and shrink the smallest failing case.",
            "concept": """
Example calls hide the argument combination that breaks a tool. This project writes property tests for `add_minutes` and for `create_ticket`'s pure validation logic. A property is a statement: for any start minute in range and any duration in range, the end minute equals the start plus the duration modulo a day, and a second call with the same inputs returns the same result. Invalid durations outside the schema bounds never reach the function. You will generate random inputs with a seeded generator, and when a property fails you will shrink the input toward a smaller one that still fails. Shrinking is the part example tests do not do. You will plant one bug, such as an off-by-one at midnight, watch the shrinker find a small case, fix the bug, and keep the shrunk case as a regression test.
            """.strip(),
            "approach": """
The generator draws integers and strings from explicit ranges. The shrinker for integers moves toward zero or toward the lower bound, halving the distance, and stops when the smaller candidate passes. For strings it deletes characters. The property runner prints the original failing input and the shrunk input. Use a fixed seed so the run that finds the midnight bug is reproducible. Do not pull in a property-testing framework. A few dozen lines are the point. The schema validator from the agent phase is the gate: inputs that fail the schema are counted as `rejected`, not as property failures.
            """.strip(),
            "components": [
                ("Generators", "Seeded draws for ints and strings inside declared ranges."),
                ("Properties", "Pure statements about tool outputs."),
                ("Shrinker", "Searches for a smaller input that still fails."),
                ("Regression case", "The shrunk input, saved after the bug is fixed."),
            ],
            "flow": [
                "Implement generation and shrinking for integers.",
                "Plant the midnight bug and run until a failure shrinks.",
                "Save the shrunk case, fix the bug, and show the property passing.",
                "Show that out-of-range durations are rejects, not failures.",
                "Assert the shrinker does not return a larger input than it started with.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library `random`",
                "Your tool functions under test",
            ],
            "setup": [
                "Create `properties/` with `prop.py` and tests.",
                "Run the planted bug once and save the transcript of the shrink.",
                "Fix the bug and keep the regression case.",
                "Run tests on the fixed code.",
            ],
            "done": [
                "The notes show a failing input and a smaller shrunk input for the planted bug.",
                "The fixed tool passes the property at the saved seed.",
                "Schema rejects are counted apart from property failures.",
                "The shrinker unit test covers a known integer failure.",
            ],
            "ahead": """
Shrinking one argument ignores interactions. Add a shrinker for a pair of integers that tries reducing each coordinate, and fixture a bug that appears only when both the hour is 23 and the duration exceeds 60. Single-coordinate shrinking should be allowed to stop at a pair that still fails, and the notes should show the pair, not a misleading single value. The follow-on is a failure region that is not a corner of one axis.
            """.strip(),
        },
        {
            "day": 68,
            "slug": "set-equality",
            "title": "Set Equality for Extractions",
            "level": "Advanced",
            "summary": "Score extracted dock lists as sets with numeric tolerance, not as strings.",
            "concept": """
An extractor that returns docks `["B", "A"]` and a gold list `["A", "B"]` is correct, and a string equality check will say it is not. A fee of 14.0 against a gold of 14 is the same story. This project scores extraction outputs as structured values. A list field is compared as a set. A number field allows a tolerance you declare per field, defaulting to zero. Extra ids are false positives. Missing ids are false negatives. You will report precision and recall over the items, plus an exact-match rate after normalization. The harness reads JSONL of predictions and gold. It does not call a model. You will include a fixture that string-matches poorly and set-matches perfectly, and one that set-matches poorly because of a single extra dock the string check might have partially credited.
            """.strip(),
            "approach": """
Define a small target schema: `docks` as a list of strings and `fee` as a number or null. Normalization trims strings and sorts nothing in the output you store; sorting is only inside the comparison, so you do not destroy the model's order before you have scored it. Tolerance lives in `tolerances.json`. A missing field is a false negative for that field, not a crash, and it is counted. Write `score.json` with per-case notes and a micro precision and recall across dock items. Exact string match can be reported as a diagnostic and must not be the headline number.
            """.strip(),
            "components": [
                ("Normalizer", "Trim and type-check without discarding order in the stored prediction."),
                ("Set comparator", "Item precision and recall for list fields."),
                ("Numeric tolerance", "Per-field absolute tolerance."),
                ("Diagnostic string match", "Present, and not the headline."),
            ],
            "flow": [
                "Write five gold and prediction pairs, including the order swap and the extra dock.",
                "Score them and write `score.json`.",
                "Assert the order swap has item recall 1 and string match 0.",
                "Assert the extra dock reduces precision and not recall.",
                "Assert a fee of 14.0 matches gold 14 when tolerance is 0, because you normalize ints and floats that are equal.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "JSONL cases",
                "No model",
            ],
            "setup": [
                "Create `set-score/` with `score.py`, `cases.jsonl`, and tests.",
                "Run the scorer.",
                "Run tests.",
                "State in the notes which number you would quote and why the string diagnostic is not it.",
            ],
            "done": [
                "Order differences do not reduce set recall.",
                "Extra items reduce precision.",
                "Tolerances are configured per field, not hard-coded in the comparison loop.",
                "The headline metrics are item precision and recall.",
            ],
            "ahead": """
Flat sets miss nested structure. Add a path-level score for one nested field, `fees_by_dock`, a map from dock id to amount. A mismatch should name the path, such as `fees_by_dock.A`, rather than failing the whole object as one bit. Fixture a map that is right on dock A and wrong on dock B and show a score that is not zero and not one. The follow-on is a diff a person can fix from, not a single similarity float.
            """.strip(),
        },
        {
            "day": 69,
            "slug": "where-models-disagree",
            "title": "Where Three Models Disagree",
            "level": "Advanced",
            "summary": "Run one prompt through three scripted models and list the cases where their structured answers differ.",
            "concept": """
A single model output has no internal argument. Three different outputs on the same prompt show you where a human should look. This project runs a frozen prompt set through three scripted model adapters that return JSON docks and fees. The adapters are deterministic functions, so the harness is testable without keys. One adapter is correct. One swaps two docks. One abstains on rare codes. The harness groups cases by the set of distinct normalized answers and writes a disagreement file: cases where the set has more than one answer. It does not vote and it does not declare a winner. Voting would hide the abstention. You are building a queue of cases to read, not a judge of judges and not a calibration study of pairwise preferences.
            """.strip(),
            "approach": """
Each case result stores the three raw outputs and the normalized forms. Agreement means normalized equality under the Day 68 rules. The report lists disagreeing case ids and the answer set. A case where all three agree is counted and not listed in full. Include one case where two agree and one abstains, and keep it in the disagreement list. Dropping abstentions is a bug the test is named for. The adapters implement one function `complete(case) -> dict` and live in a file you can replace later with HTTP. Tests never do that replacement.
            """.strip(),
            "components": [
                ("Frozen prompts", "A handful of cases with gold, used only as a label in the report, not as a voter."),
                ("Three adapters", "Deterministic scripted models."),
                ("Disagreement list", "Cases whose normalized answer set has size greater than one."),
                ("Abstention marker", "A distinct answer value that must not be dropped."),
            ],
            "flow": [
                "Write the three adapters and five cases.",
                "Run the harness and write `disagreements.json`.",
                "Assert the all-agree case is absent from the list and present in the agree count.",
                "Assert the abstention case is present.",
                "Assert the harness does not import a voting function. If you are tempted to add one, put it in a file the default command does not call, and test that the default output has no `winner` field.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Scripted adapters",
                "The set normalizer",
            ],
            "setup": [
                "Create `disagreement/` with `adapters.py`, `harness.py`, and tests.",
                "Run the harness.",
                "Run tests.",
                "Write one sentence: this list is a reading queue, not a score.",
            ],
            "done": [
                "Agreeing cases are counted and not expanded in the disagreement list.",
                "Abstentions count as disagreements against a concrete answer.",
                "The default report has no winner field.",
                "Adapters are replaceable functions, and tests use the scripted ones.",
            ],
            "ahead": """
A long queue is not yet a way to choose the next case to read. Add a priority: cases where all three answers differ outrank cases where two agree. Sort the file that way and fixture six cases that force the order. Do not drop the lower group. The follow-on is a reading order you can explain, still without declaring which model was right.
            """.strip(),
        },
        {
            "day": 70,
            "slug": "hidden-slots",
            "title": "Hidden Slots Across Turns",
            "level": "Advanced",
            "summary": "Script a user with hidden slot values and score whether the agent fills them without re-asking a locked slot.",
            "concept": """
Multi-turn agents look fine if you read only the last turn. The failure is in the middle: the user already gave the dock, and the agent asks again, or it overwrites a locked fee code. This project is a harness around a scripted user and a scripted agent. The user has hidden slots. It reveals a slot only when asked, or when its opening line includes it. Once a slot is filled and the user has not corrected it, the slot is locked. The score penalizes a question about a locked slot and penalizes an answer that does not match the hidden value. You will run a three-turn script where the dock is given up front and the fee is asked once. A bad agent that re-asks the dock fails even if the final answer is right.
            """.strip(),
            "approach": """
The user is a function of the hidden slots and the agent question. It is not a model. The harness logs each turn's asked slot names. Locked slots are those filled and not corrected. The agent under test is also scripted so you can swap in a bad one. Metrics are: final value match, count of questions about locked slots, and turns used. Do not average these into one grade. The report lists them. A correction turn unlocks a slot on purpose, using the Day 64 rule, and a question after the correction is allowed. A fixture covers that so the harness does not punish repair.
            """.strip(),
            "components": [
                ("Hidden slot user", "Reveals values only under the script rules."),
                ("Lock set", "Filled slots that have not been corrected."),
                ("Bad agent fixture", "Re-asks the dock and still answers correctly at the end."),
                ("Separate metrics", "Match, locked-question count, and turns."),
            ],
            "flow": [
                "Implement the user and the lock rules.",
                "Run the good agent and expect zero locked questions and a value match.",
                "Run the bad agent and expect a locked question count of at least one, with the match still true.",
                "Run a correction fixture and expect the post-correction question not to count as locked.",
                "Write the three reports.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Scripted user and agents",
                "JSON reports",
            ],
            "setup": [
                "Create `hidden-slots/` with `user.py`, `harness.py`, and tests.",
                "Run the three scripts.",
                "Run tests.",
                "Keep the hidden values out of the agent's initial prompt in the good-agent fixture. The opening line may include only the values the script says were volunteered.",
            ],
            "done": [
                "The bad agent fails the locked-question metric while passing the final match.",
                "The good agent passes both.",
                "A post-correction question is not counted as a locked question.",
                "Metrics are reported separately.",
            ],
            "ahead": """
Users contradict themselves without using the correction phrases you listed. Add a fixture where turn three states a new dock id as a bare fact, not as "no, the other one." Define the harness rule you will actually enforce: either bare restatements update the slot, or they count as contradictions the agent must ask about. Pick one, fixture both an agent that follows the rule and one that does not, and write the rule in the report header. The follow-on is a contradiction policy you chose on purpose, not an accidental overwrite.
            """.strip(),
        },
        {
            "day": 71,
            "slug": "pareto-cost-quality",
            "title": "The Pareto Surface of Cost and Quality",
            "level": "Advanced",
            "summary": "Sweep a grid of retriever depth and scripted model cost and drop the configs that are worse on both axes.",
            "concept": """
A better score that costs ten times as much is not automatically the config you ship, and a cheaper config that loses one gold id may be. This project freezes a tiny retrieval eval and a scripted generator that can see only the chunks you pass it. You sweep `k` in {1, 3, 5} and a `model` label in {cheap, strong} where strong costs more per call in a price table you write. Quality is recall at k from the frozen file, or quote exact-match if you wire the quoter. Cost is the sum of a retrieval cost and a model cost you invented and documented as fictional. You plot nothing fancy: a CSV of config, quality, cost, and a flag `dominated` when another config is at least as good on quality and strictly cheaper, or strictly better and no more expensive. Dominated configs are not candidates. You do not hide them.
            """.strip(),
            "approach": """
The price table is `prices.json` with fictional units, and the report says the units are fictional in the first line. The sweep is exhaustive on the small grid. Domination is computed by a function a test can run on a hand-built three-row table, one of which is dominated. The harness does not call a hosted model. The strong scripted model returns the gold quote only if the gold chunk is in the retrieved set. The cheap one returns it only if the gold chunk is rank 1. That difference is enough to make the surface interesting. Write `frontier.csv` and a sentence naming the undominated configs.
            """.strip(),
            "components": [
                ("Price table", "Fictional costs for retrieval and for each model label."),
                ("Sweep grid", "k and model label."),
                ("Domination flag", "A config that is weakly worse on both axes."),
                ("Frontier list", "The undominated configs, named in a sentence."),
            ],
            "flow": [
                "Write prices and the two scripted models.",
                "Run the sweep on a frozen question file with known gold chunks.",
                "Compute domination.",
                "Test domination logic on a hand-built table.",
                "Write the frontier sentence from the actual CSV.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "CSV and JSON",
                "Scripted models with a price table",
            ],
            "setup": [
                "Create `pareto/` with `sweep.py`, `prices.json`, and tests.",
                "Run the sweep.",
                "Run the domination unit test.",
                "Label the units as fictional in the report's first line.",
            ],
            "done": [
                "Every grid point is a row, including dominated ones.",
                "The hand-built domination test passes.",
                "The frontier sentence names configs that exist in the CSV.",
                "No hosted model is required to reproduce the file.",
            ],
            "ahead": """
Cost is not the only second axis. Add a latency budget, also fictional, and drop any config whose scripted latency exceeds it before domination runs. Fixture a strong model that is best and over budget so it disappears from the frontier, and show the row still present with `over_budget` set. The follow-on is a constraint applied before you brag about the frontier, not a third score averaged in.
            """.strip(),
        },
        {
            "day": 72,
            "slug": "instruction-conflict",
            "title": "When Trusted Instructions Conflict",
            "level": "Advanced",
            "summary": "Score an agent on a fixture where the system instruction and the tool description disagree, using a precedence you wrote down.",
            "concept": """
Two sources you trust can disagree. The system instruction says never invent a fee, and a tool description says the tool returns a fee for every dock, including docks it has never seen. A model will follow one of them. This project does not build an attack library and does not minimize a jailbreak. It builds eight hand-written probes where a system line and a tool description conflict, plus a precedence document you write first: system instruction outranks tool description. The agent is scripted in two versions, one that obeys precedence and one that obeys the tool text. The harness scores whether a forbidden tool call happened. The probes are fixtures, not a claim about how any hosted model behaves.
            """.strip(),
            "approach": """
Each probe is a JSON object: system text, tool description, user text, and `forbidden_tool`. The runner executes a scripted policy selected by a flag. The score is the count of probes where the forbidden tool was called. Precedence lives in `precedence.md` and is written before you look at scores. The obedient policy refuses the call when the tool description promises coverage the system line forbids. The tool-following policy calls it. Tests lock both scores: obedient at zero calls, tool-following at one call per probe. Keep the probe count at eight so the fixture stays readable in one sitting.
            """.strip(),
            "components": [
                ("Precedence note", "A written order among instruction sources."),
                ("Probe file", "Eight conflicts with a named forbidden tool."),
                ("Two policies", "Obey precedence, or obey the tool description."),
                ("Call score", "Count of forbidden calls, per policy."),
            ],
            "flow": [
                "Write `precedence.md` first.",
                "Write eight probes.",
                "Run both policies and save both scores.",
                "Assert the obedient policy makes zero forbidden calls.",
                "Assert the tool-following policy makes a forbidden call on every probe.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "JSON probes",
                "Scripted policies only",
            ],
            "setup": [
                "Create `instruction-conflict/` with `probes.jsonl`, `policies.py`, and tests.",
                "Run both policies.",
                "Run tests.",
                "Do not describe the probes as a security certification. The notes should say they are a precedence fixture.",
            ],
            "done": [
                "Precedence is a file, not an unstated habit.",
                "The two policies score differently on the same probes.",
                "Eight probes are present and each names a forbidden tool.",
                "The harness makes no live model calls.",
            ],
            "ahead": """
A third trusted source is the tool result itself. Add a probe where the system line says the fee table is authoritative, the tool description agrees, and the tool result returns a different number. Extend precedence so a tool result cannot override the system line, and score an agent that quotes the tool result anyway as a failure. The follow-on is precedence that covers results, not only instructions, with one fixture where obedience means refusing the number the tool just returned.
            """.strip(),
        },
        {
            "day": 73,
            "slug": "retrieval-pins",
            "title": "Pins for a Retrieval Set",
            "level": "Advanced",
            "summary": "Hash the embedder id and the top-k chunk ids for a frozen query set, and fail when a rebuild drifts.",
            "concept": """
A retrieval change can look harmless and swap the chunk your quotes depend on. This project pins a frozen query set: for each query, store the embedder name, the index content hash, and the ordered top-k chunk ids. A later run recomputes the list and fails if the ids differ. The pin file is something you commit. Updating it is a deliberate edit, not a side effect of re-running the index. You will change one handbook sentence that should not affect a specific query and show the pin still matching, then change a sentence inside a pinned chunk and show the diff. The failure output names the query id and the first rank where the ids diverge.
            """.strip(),
            "approach": """
Use BM25 or the hashing embedder so the pin is reproducible without a downloaded model. The index content hash is a hash of the chunk texts in id order. If the hash changes and the ids do not, the report says `content-changed-ranking-stable`, which is a warning, not a pass you should ignore, and not an automatic failure. You choose failure only when the ordered ids change. A test builds a two-chunk index, pins it, edits a stopword in an unretrieved chunk, and edits a token in the retrieved chunk. Those two edits must produce different statuses.
            """.strip(),
            "components": [
                ("Pin file", "Query id, embedder name, index hash, ordered chunk ids."),
                ("Comparer", "First rank of divergence."),
                ("Content hash", "Hash of chunk texts, reported even when ranks match."),
                ("Deliberate update", "A human-edited pin, not a silent rewrite."),
            ],
            "flow": [
                "Build a tiny index and write `pins.json` by an explicit `write-pins` command.",
                "Re-run check mode and expect a match.",
                "Edit an unretrieved chunk and expect the stable-ranking warning.",
                "Edit a retrieved chunk's important token and expect a failure that names the rank.",
                "Assert check mode does not overwrite `pins.json`.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Hashing embedder or BM25",
                "JSON pin file",
            ],
            "setup": [
                "Create `pins/` with `pin.py`, a mini handbook, and tests.",
                "Run write-pins once, then check.",
                "Run the two edit tests against copies of the index.",
                "Document that updating pins is a separate command.",
            ],
            "done": [
                "Check mode never writes the pin file.",
                "A ranking change names the query and the rank.",
                "A content change with stable ranking is a warning with a distinct status.",
                "The embedder name is inside the pin file.",
            ],
            "ahead": """
Sometimes the ranking should change, because you added a paragraph on purpose. Add an allow-list file `approved_diffs.json` that names the query id and the expected new top-k. Check mode passes a diff only when it matches an approved entry, and fails if the new ranking matches neither the pin nor an approval. Fixture one approved change and one unapproved change. The follow-on is a reviewable diff, not a habit of rewriting pins whenever the check goes red.
            """.strip(),
        },
        {
            "day": 74,
            "slug": "section-checklists",
            "title": "Section Checklists for Long Answers",
            "level": "Advanced",
            "summary": "Score a long answer by required sections, forbidden claims, and numbers that must trace to a table.",
            "concept": """
Some answers are not a single span. A lost-bike reply should contain a section for what happened, a section for the fee, and no promise of a replacement bike the handbook does not make. This project scores long answers with a checklist file: required headings, forbidden phrases, and a table of numbers that must appear in both the answer and a cited table chunk. The scorer is deterministic. It does not ask a model whether the answer "covered the spirit" of a section. A missing heading is a miss. A forbidden phrase is a miss even if every heading is present. A number in the answer that is not in the cited table is a miss. You will write one gold answer that passes and two that fail for different reasons.
            """.strip(),
            "approach": """
Headings are markdown `##` lines matched to a required list. Order is required unless the checklist says `order: free`. Forbidden phrases are case-sensitive literals so you do not accidentally ban a substring of a legitimate word. Choose phrases long enough to be specific. Numbers are extracted with a regex and compared to the table chunk's numbers as a set. The report lists missing headings, forbidden hits, and unknown numbers separately. A single boolean pass is the conjunction, and the report must still show the parts when it fails.
            """.strip(),
            "components": [
                ("Checklist file", "Headings, forbidden phrases, and a cited table id."),
                ("Heading matcher", "Exact heading strings, with optional order."),
                ("Forbidden list", "Literal phrases."),
                ("Number trace", "Every number in the answer appears in the cited table."),
            ],
            "flow": [
                "Write the checklist and the table chunk.",
                "Score the passing answer.",
                "Score an answer missing a heading and one containing a forbidden promise.",
                "Score an answer whose fee number is not in the table.",
                "Assert the three failure reports name different reason groups.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Markdown answers and a JSON checklist",
                "No model judge",
            ],
            "setup": [
                "Create `checklists/` with `checklist.json`, `answers/`, and `score.py`.",
                "Run all four answers.",
                "Run tests.",
                "Keep the passing answer free of extra numbers you did not intend.",
            ],
            "done": [
                "The passing answer passes all three groups.",
                "Each planted failure trips a different group, and the report shows which.",
                "Forbidden matching is literal and covered by a test that a short token does not ban a longer innocent word.",
                "The conjunction pass is not the only field in the report.",
            ],
            "ahead": """
A missing section and a weak section are different. Add partial credit per heading: full credit when the section contains at least one number traced to the table or an explicit `not-in-handbook` token, and zero when the heading is present but the body is empty. Fixture an empty section. The follow-on score distinguishes absence from a heading with nothing under it, and the notes say you still do not grade prose quality.
            """.strip(),
        },
        {
            "day": 75,
            "slug": "patience-persona",
            "title": "A Persona with a Patience Counter",
            "level": "Advanced",
            "summary": "Simulate a user who ends the conversation after a fixed number of unhelpful turns, and score task completion.",
            "concept": """
An agent can be polite for twenty turns and never collect the dock id. This project scripts a persona with a goal, a patience counter, and a list of facts it will reveal when asked the right slot. Each agent question that does not name a missing slot decrements patience. At zero, the persona ends the conversation. The score is whether the goal slot values are filled at the end, not whether the agent said thank you. You will run a terse agent that asks the right slots and a rambling agent that asks open-ended questions. Both can be scripted. The rambling agent must hit patience zero with the goal incomplete. Completing the goal on the last remaining patience point still scores as complete. You will not add a sentiment score.
            """.strip(),
            "approach": """
The persona is a pure function. Patience starts at three. The goal is a set of slots. The agent's utterances are classified by a rule: if they contain a slot name from the missing set, the persona reveals it and patience stays. Otherwise patience drops. The harness records the turn count, the ending patience, and the unfilled slots. A test uses a persona that reveals nothing unless asked, so an agent cannot score a point from the opening line alone unless the fixture says the opening line included a slot. Put that rule in the fixture file.
            """.strip(),
            "components": [
                ("Persona", "Goal slots, patience, and a reveal rule."),
                ("Question classifier", "Whether the utterance names a missing slot."),
                ("Terse agent", "Asks only missing slots."),
                ("Rambling agent", "Never names a slot."),
            ],
            "flow": [
                "Implement the persona and the classifier.",
                "Run the terse agent and expect completion with patience at or above one.",
                "Run the rambling agent and expect an incomplete goal and patience zero.",
                "Run a terse agent that finishes on the last patience point and expect complete.",
                "Assert the report contains no sentiment or politeness field.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Scripted persona and agents",
                "JSON report",
            ],
            "setup": [
                "Create `patience/` with `persona.py`, `harness.py`, and tests.",
                "Run both agents.",
                "Run the last-point fixture.",
                "Run tests.",
            ],
            "done": [
                "The rambling agent fails by patience, not by a string match on the final answer alone.",
                "The terse agent completes the goal.",
                "Finishing on the last patience point counts as complete.",
                "The report fields are goal completion, unfilled slots, and ending patience.",
            ],
            "ahead": """
Patience is harsher when the user is underspecified and friendlier when they volunteer facts. Add a second persona config, `impatient`, with patience 1, and run the same terse agent. The terse agent should still finish if the opening line volunteers one of two slots. Fixture a terse agent that asks for the volunteered slot again and show it failing under `impatient` while passing under the original patience of three. The follow-on is a grid of persona configs, not a new agent architecture.
            """.strip(),
        },
        {
            "day": 76,
            "slug": "immutable-case-ids",
            "title": "Case IDs that Never Change in Place",
            "level": "Advanced",
            "summary": "Store eval cases as immutable ids, and force an edit to mint a new id instead of rewriting history.",
            "concept": """
If you edit a gold answer and keep the case id, last month's score and today's score are not about the same question. This project stores cases in a directory of JSON files whose names are ids. A command `check` fails if a file's content hash does not match a ledger entry for that id. A command `revise` writes a new id, records `supersedes`, and leaves the old file untouched. Deleting a file is also a failure unless a tombstone entry says the id was retired. You will revise one case, run the scorer on a fake prediction file twice — once pinned to the old id set and once to the new — and show that the two score lines name their case-set hashes. The ledger is the product. The scores are there to prove you can still join them.
            """.strip(),
            "approach": """
The ledger is `ledger.json` mapping id to sha256 and optional `supersedes` and `retired` fields. `check` exits non-zero on a hash mismatch and prints both hashes. `revise` refuses to overwrite. A test tampers with a gold string and expects `check` to fail. Another test runs `revise` and expects the old hash to remain. The scorer accepts a `--cases` ledger slice: `all` or `current`, where current means ids that are not superseded and not retired. Document that choice. Historical comparisons use the hash, not the word "latest."
            """.strip(),
            "components": [
                ("Case files", "One JSON file per immutable id."),
                ("Ledger", "Hashes, supersedes links, and retirements."),
                ("Check command", "Fails when bytes drift under an existing id."),
                ("Revise command", "Mints a new id and keeps the old file."),
            ],
            "flow": [
                "Write three cases and a ledger by an `add` command that refuses existing ids.",
                "Tamper with one file and show `check` failing.",
                "Restore it by reverting the file, not by updating the hash in place.",
                "Revise one case and show both ids present.",
                "Score a prediction file against `current` and against an explicit list containing the old id.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "JSON ledger and case files",
                "Standard library `hashlib`",
            ],
            "setup": [
                "Create `case-ids/` with `cases.py` and tests.",
                "Run add, check, a failed tamper, and revise.",
                "Run tests.",
                "Write the rule at the top of the README you keep in that folder: ids are immutable.",
            ],
            "done": [
                "Tampering fails `check` without changing the ledger.",
                "`revise` leaves the old file's bytes and hash intact.",
                "Scores name the case-set hash they used.",
                "`add` refuses to reuse an id.",
            ],
            "ahead": """
Trend lines break when an id is superseded and a dashboard silently drops it. Add a migration report that lists old id, new id, and whether any prediction file still references the old id. Fixture a prediction file that cites a superseded id and show the report naming it as `unmapped` until you add an explicit map entry. The follow-on is a map you review, so a chart does not change denominator because a gold string was edited.
            """.strip(),
        },
        {
            "day": 77,
            "slug": "flake-budget",
            "title": "A Flake Budget",
            "level": "Advanced",
            "summary": "Repeat a scripted eval many times, separate harness flake from decoder flake, and fail when the pass rate wanders too far.",
            "concept": """
A pass rate from one run is a coin flip if the decoder is stochastic. This project runs the same case set N times under two adapters. The stable adapter returns a fixed JSON answer and must produce a pass rate of 1.0 or 0.0 on every repeat, with zero variance. The shaky adapter flips a seeded coin inside the answer and produces a pass rate you can recompute. The harness records every repeat's pass bit, the mean, and the range. A flake budget says the stable adapter's range must be zero, and the shaky adapter's range must stay inside a band you set after computing the expected binomial spread for the seed. You are not building a release gate for a product and you are not estimating a confidence interval for a launch. You are measuring whether your harness itself invents noise.
            """.strip(),
            "approach": """
N is 30 so the file stays small and the binomial expectation is easy to write down. The seed is fixed. The stable adapter ignores the seed's random draws. The shaky one uses `random.Random(seed)` and you document the expected number of passes. A bug that reads the system clock inside the stable path should fail the range check. Do not use the clock. The report has two sections, harness and decoder, and a test asserts the stable section's variance is zero. If you change N, update the expected shaky count in the same commit as the code.
            """.strip(),
            "components": [
                ("Repeat runner", "N runs, fixed seed, recorded bits."),
                ("Stable adapter", "Deterministic answers."),
                ("Shaky adapter", "Seeded coin flip inside the answer."),
                ("Budget", "Zero range for the stable adapter, a named band for the shaky one."),
            ],
            "flow": [
                "Implement both adapters and the repeat runner.",
                "Run N repeats and write `flake.json`.",
                "Assert the stable range is zero.",
                "Compute the shaky pass count from the seed by hand or with a one-line replica and assert it matches.",
                "Document the budget in `budget.md` before quoting the shaky band.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library `random`",
                "JSON report",
            ],
            "setup": [
                "Create `flake/` with `adapters.py`, `repeat.py`, and tests.",
                "Run both adapters.",
                "Run tests.",
                "Keep N at 30 in one constant.",
            ],
            "done": [
                "The stable adapter's pass bits are identical across repeats.",
                "The shaky adapter's pass count matches the seeded expectation.",
                "The report separates harness variance from decoder variance.",
                "The budget file states the allowed shaky band and the value of N.",
            ],
            "ahead": """
Thirty repeats is arbitrary. Add a stopping rule that runs the shaky adapter until the running mean's Chebyshev bound, which you can compute from the observed variance without a statistics library, is inside a width you set, or until a max N of 200. Fixture a coin that is fair and show it stopping later than a coin that always passes. The follow-on is spending repeats where the bit actually moves, and the stable adapter must still stop at the minimum sample size because its variance is zero.
            """.strip(),
        },
        {
            "day": 78,
            "slug": "accepted-sequences",
            "title": "Accepted Tool Sequences",
            "level": "Advanced",
            "summary": "Score a transcript's tool names against a set of accepted sequences, ignoring argument values.",
            "concept": """
Some tasks have more than one legal procedure and many illegal ones. Looking up a fee and then quoting is fine. Quoting and then looking up is not, if the rule is that quotes must follow a lookup. This project lists accepted tool-name sequences for a task. Argument values are ignored in the required score, because a separate harness already checks values. A transcript passes if its tool-name list matches one accepted sequence exactly. A prefix of an accepted sequence is a failure labeled `incomplete`, not a pass. An extra tool in the middle is `not-accepted`. You will write three transcripts covering pass, incomplete, and an inserted tool. The harness does not run tools. It reads names in order.
            """.strip(),
            "approach": """
Accepted sequences live in `accepted.json` as a list of lists of strings. Matching is equality of the full list. You also compute the longest accepted sequence that is a prefix of the observed names, and report it, so an incomplete run is visible as "matched 2 of 3 of sequence 0" rather than as a mysterious fail. Inserted tools break every prefix at that index. Tests cover a second accepted sequence that is a different legal order, so the harness is not secretly requiring one path. Argument objects may be present in the transcript and must be ignored by the comparator. A test puts different arguments on a passing name sequence and expects a pass.
            """.strip(),
            "components": [
                ("Accepted file", "A set of tool-name sequences."),
                ("Exact matcher", "Full-list equality against any accepted sequence."),
                ("Prefix diagnostic", "How far the observed list followed some accepted sequence."),
                ("Argument blindness", "Values are not part of this score."),
            ],
            "flow": [
                "Write two accepted sequences for one task.",
                "Score a transcript for each sequence as a pass.",
                "Score a prefix and expect `incomplete` plus the prefix diagnostic.",
                "Score an inserted tool and expect `not-accepted`.",
                "Change only arguments on a passing transcript and expect the verdict to stay a pass.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "JSON transcripts",
                "No tool execution",
            ],
            "setup": [
                "Create `sequences/` with `score.py`, `accepted.json`, and tests.",
                "Run the four transcripts.",
                "Run tests.",
                "Note in the folder README that argument correctness is out of scope for this scorer.",
            ],
            "done": [
                "Both legal orders pass.",
                "A prefix is `incomplete` and not a pass.",
                "An inserted tool is `not-accepted` and the diagnostic names the index.",
                "Argument changes do not flip a pass to a fail.",
            ],
            "ahead": """
Names-only scoring still passes a lookup with an empty query. Add an argument sketch: for each step, a set of required keys that must be present and non-empty, without specifying the values. Fixture a passing order whose lookup query is an empty string and expect a new status `missing-key` that does not replace `not-accepted`. A wrong order with all keys present should still be `not-accepted`. The follow-on is a sketch of arguments, not a return to exact string match on the fee code.
            """.strip(),
        },
    ],
}
