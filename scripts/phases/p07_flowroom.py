"""Phase 7 — Flowroom. Days 79–90."""

PHASE = {
    "id": "07",
    "dir": "07-flowroom",
    "name": "Flowroom: Analytics and Pipelines",
    "blurb": "Turn raw events into sessions, marts, and features that can be rebuilt, with late data and stale rows called out instead of smoothed over.",
    "outcome": "Build a small warehouse path you can rerun without double-counting or leaking the future.",
    "goal": "Finish this phase able to sessionize an event log, keep a rerunnable mart, track history, put labels next to features as of a cutoff, and backfill an embedding table without rewriting unchanged text.",
    "skills": [
        "Sessionization with late events",
        "Path analysis over help documents",
        "Cohort retention triangles",
        "Idempotent staging and marts in SQLite",
        "Slowly changing catalog history",
        "Tumbling window aggregates",
        "Freshness checks and backfill",
        "Point-in-time label joins",
        "Content-hashed embedding backfills",
        "Seasonal residual alerts",
        "Entity resolution with a review file",
        "Structured logs and an error budget",
    ],
    "projects": [
        {
            "day": 79,
            "slug": "sessions-and-late-events",
            "title": "Sessions and Late Events",
            "level": "Intermediate",
            "summary": "Build rider sessions from an inactivity gap and show a late event that should extend a closed session.",
            "concept": """
A session is a decision about a gap, not a column in the source. Harbor Loop's app emits `app_open`, `search`, and `rental_complete` with event time and ingest time. Two events from the same rider belong to the same session when the gap is under 30 minutes. A job that closes the day at midnight will miss a 23:50 event that arrives the next morning and should have extended the last session. This project builds sessions from a fixture, writes session ids, and then applies a late event. You will show two outputs: the premature close, and the rebuilt sessions after the late event is included. The late event must change a session end time rather than becoming a new one-event session. Rebuilding from the full log is allowed. Mutating a closed session in place without a rebuild record is not.
            """.strip(),
            "approach": """
Sort by rider and event time. Assign session ids with a counter that increments when the gap exceeds the threshold. The threshold is a constant. Late events are applied by concatenating them with the original log and recomputing, then writing a diff of session end times. A test plants a 20-minute-late completion after a search and expects the same session id. A test plants a 2-hour-late event and expects a new session. Use ingest time only to decide lateness relative to a close timestamp, not to order the session. Ordering uses event time. Write both clocks into the output so a reader can see which one you used.
            """.strip(),
            "components": [
                ("Event fixture", "Rider events with event time and ingest time."),
                ("Gap rule", "A named inactivity threshold."),
                ("Session builder", "Deterministic ids from the sorted log."),
                ("Late diff", "End times before and after the late event is included."),
            ],
            "flow": [
                "Write a log with two riders and a known gap pattern.",
                "Build sessions and lock the ids in a test.",
                "Add a late in-gap event and recompute.",
                "Assert the session count does not increase for that rider.",
                "Add a late out-of-gap event and assert the session count increases.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library `csv` and `datetime`",
                "No warehouse server",
            ],
            "setup": [
                "Create `sessions/` with `events.csv`, `sessions.py`, and tests.",
                "Run the builder twice, before and after the late file.",
                "Run tests.",
                "Record the threshold and the close timestamp in `notes.md`.",
            ],
            "done": [
                "In-gap late events extend a session.",
                "Out-of-gap late events start a new session.",
                "Ordering uses event time, and a test swaps ingest order to prove it.",
                "The diff file shows the end-time change rather than overwriting silently.",
            ],
        },
        {
            "day": 80,
            "slug": "help-doc-paths",
            "title": "Paths Through the Help Docs",
            "level": "Intermediate",
            "summary": "Count which help-doc sequences precede a resolved event, and ignore paths that never resolve.",
            "concept": """
Pageview counts flatter articles that people open and abandon. Harbor Loop's help center emits doc views and a `resolved` event when the rider marks the issue done. This project builds paths: ordered doc ids inside a session, ending at the first resolved, or ending unfinished if the session never resolves. You will report the top resolved paths and, separately, the top unfinished paths. A doc that appears in both is not "successful" just because it is popular. You will also refuse to count a path that skips across sessions. The fixture includes one doc that is common in unfinished paths and rare in resolved ones, and the report must not rank it as a success. This is path analysis, not a feature-adoption dashboard and not a model of whether the doc caused the resolution.
            """.strip(),
            "approach": """
Start from the session ids you know how to build, or from a fixture that already has session ids so this day stays about paths. Collapse consecutive duplicate doc views. End a path at the first `resolved` inside the session. Docs after resolved are ignored and counted in a `tail` tally so you notice a tagging bug if the tail is large. Rank paths by resolved count with a minimum support of two so a unique path does not become a recommendation. Unfinished paths have their own table and are not used as the denominator of a success rate unless you also print the denominator. Write both tables.
            """.strip(),
            "components": [
                ("Session events", "Doc views and resolved markers."),
                ("Path cutter", "Stops at the first resolved event."),
                ("Resolved ranking", "Paths with support at least two."),
                ("Unfinished ranking", "A separate table, including the planted dead-end doc."),
            ],
            "flow": [
                "Write a fixture with a dead-end doc and a short path that resolves.",
                "Build paths per session.",
                "Assert events after resolved do not extend the path.",
                "Rank both tables.",
                "Assert the dead-end doc is absent from the resolved ranking and present in the unfinished ranking.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "CSV fixtures",
                "No visualization library required",
            ],
            "setup": [
                "Create `paths/` with `events.csv`, `paths.py`, and tests.",
                "Run the report and write `out/resolved.csv` and `out/unfinished.csv`.",
                "Run tests.",
                "State in the notes that the tables are descriptive, not causal.",
            ],
            "done": [
                "Resolved and unfinished paths are different files.",
                "The dead-end doc is not listed as a resolved success.",
                "Events after the first resolved marker do not change the path, and the tail count is reported.",
                "A path cannot contain events from two session ids, and a test mixes them to prove the cut.",
            ],
        },
        {
            "day": 81,
            "slug": "retention-triangles",
            "title": "Retention Triangles",
            "level": "Intermediate",
            "summary": "Build a cohort retention triangle from signup week and activity week, and do not fill future weeks.",
            "concept": """
A retention chart that shows every cohort at week 4, including the cohort that signed up last week, is fiction. This project builds a triangle. Rows are signup cohorts by week. Columns are week 0 through week 4. A cell is the fraction of the cohort with at least one rental in that activity week. Cells in the future, relative to a `as_of` date you set, are null, not zero. Zero would say the riders churned. Null says the week has not happened. You will compute the triangle from a fixture that includes a cohort with a full history and a cohort that started near `as_of`. The report prints nulls as blank. A test expects a blank, and it fails if you write 0.
            """.strip(),
            "approach": """
Signup week is the week of the rider's first event in a signup file, not the first event you happened to load if the file is filtered. Use the signup file as the source of the cohort so a late first rental does not move the rider. Activity is a set of weeks per rider. Cohort size is the number of riders in the signup week, including those with no later rentals. They count in the denominator. Week 0 includes the signup week itself. Document that. Pick ISO weeks and a single time zone, and parse every timestamp as aware UTC converted to that zone before you take the week.
            """.strip(),
            "components": [
                ("Signup file", "Rider id and signup timestamp, the cohort source."),
                ("Activity file", "Rentals after signup."),
                ("Triangle", "Cohort by relative week, with nulls for the future."),
                ("As-of date", "The clock the null rule uses."),
            ],
            "flow": [
                "Build cohorts from the signup file.",
                "Mark activity weeks per rider.",
                "Fill cells up to the last completed week relative to `as_of`.",
                "Leave future cells null and test one of them.",
                "Include a rider with no activity and assert they remain in the denominator.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library `datetime` and `csv`",
                "A printed triangle in markdown or CSV",
            ],
            "setup": [
                "Create `retention/` with the two CSV files, `triangle.py`, and tests.",
                "Run the triangle at a fixed `as_of` you store in `as_of.txt`.",
                "Run tests.",
                "Read the triangle and confirm the newest cohort has blanks on the right.",
            ],
            "done": [
                "Future cells are null, and a test rejects zeros in those cells.",
                "Inactive signups stay in the denominator.",
                "The as-of date is a file, not today's date from the clock.",
                "Week boundaries use one named time zone.",
            ],
        },
        {
            "day": 82,
            "slug": "rerun-safe-marts",
            "title": "Rerun-Safe Marts",
            "level": "Intermediate",
            "summary": "Load raw events into staging and a mart in SQLite so running the job twice does not double the totals.",
            "concept": """
A pipeline that inserts into a reporting table every time it runs will double last week's rentals the moment someone retries a failure. This project creates three layers in SQLite: `raw`, `staging`, and `mart_daily`. Raw is append-only and keyed by an event id. A second load of the same file inserts zero new raw rows. Staging is rebuilt from raw for the dates in the batch, deleting that date range inside the transaction and inserting again. The mart is rebuilt from staging for the same range. You will run the job twice and assert the daily totals match the first run. You will also add one new event and show only that day's total changing. The range delete is the whole trick. A job that only inserts cannot be retried.
            """.strip(),
            "approach": """
Use the standard library `sqlite3`. Wrap the rebuild in a transaction. The batch range is an argument, not `select min(date), max(date)` from the whole raw table, because that would rebuild history you did not intend to touch. A test loads a file, loads it again, and checks a count. A second test extends the range and checks that an untouched day still has the same total. Primary keys on event id make the raw insert use `INSERT OR IGNORE`. Document that ignore is acceptable for exact duplicate ids and wrong for two different payloads with the same id. A test sends a conflicting payload and expects a recorded conflict, not a silent ignore. You may handle that second case by comparing a hash before ignore.
            """.strip(),
            "components": [
                ("Raw table", "Append-only events with a primary key and a payload hash."),
                ("Staging rebuild", "Delete-and-insert for a date range, inside a transaction."),
                ("Daily mart", "Totals rebuilt from staging for the same range."),
                ("Conflict check", "Same id with a different hash is reported, not ignored."),
            ],
            "flow": [
                "Create the three tables.",
                "Load a file and record daily totals.",
                "Load the same file and assert totals are unchanged and raw row count is unchanged.",
                "Load a new event on one date and assert other dates are unchanged.",
                "Attempt a conflicting payload and assert it is rejected and counted.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library `sqlite3`",
                "SQL visible in the repository as strings or `.sql` files",
            ],
            "setup": [
                "Create `marts/` with `pipeline.py`, `schema.sql`, and tests.",
                "Run the pipeline twice.",
                "Run tests.",
                "Point the notes at the transaction that deletes the range.",
            ],
            "done": [
                "A rerun does not change totals.",
                "A new event changes only its date.",
                "A conflicting duplicate id is not silently ignored.",
                "The batch date range is an explicit argument.",
            ],
        },
        {
            "day": 83,
            "slug": "catalog-history",
            "title": "Catalog History",
            "level": "Intermediate",
            "summary": "Store fee-code changes as dated rows so a question about last March does not see today's price.",
            "concept": """
A fee table with one row per code shows the price now. A support question about a rental in March needs the price that was in force in March. This project implements a small slowly changing dimension. Each fee code has rows with `valid_from` and `valid_to`. The current row has a null `valid_to`. When the price changes, you close the open row by setting `valid_to` to the change time and insert a new open row. You never update the price in place. A query function `fee_as_of(code, when)` returns the row whose interval contains `when`. You will change a fee twice and show three answers: before the first change, between the changes, and after the second. A test queries exactly at a boundary and documents whether `valid_from` is inclusive. Pick inclusive start and exclusive end, and test both sides of the boundary.
            """.strip(),
            "approach": """
Do this in SQLite or in plain data structures backed by a CSV you can diff. The close-and-insert operation is one function. It rejects a change that would open a second current row. It rejects a `valid_from` earlier than the current row's `valid_from`. Historical rows are immutable: a test that tries to update an old price in SQL should not be part of the API. If you are tempted to add an update method, make it raise. Querying a time before the first row returns `unknown`, not the earliest price.
            """.strip(),
            "components": [
                ("Interval rows", "`valid_from` inclusive, `valid_to` exclusive, one open row."),
                ("Change function", "Closes the open row and inserts the new price."),
                ("As-of query", "Returns the row containing a timestamp."),
                ("Boundary tests", "Both sides of a change instant."),
            ],
            "flow": [
                "Insert an initial fee.",
                "Change it twice at known timestamps.",
                "Query three times and lock the three prices.",
                "Query exactly at `valid_to` of the first row and expect the second price.",
                "Attempt a retroactive edit and expect a rejection.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "SQLite or CSV with a tiny query function",
                "Aware timestamps",
            ],
            "setup": [
                "Create `catalog-history/` with `fees.py` and tests.",
                "Run the two changes and print the three as-of answers.",
                "Run tests.",
                "Write the inclusivity rule in one line at the top of `fees.py`.",
            ],
            "done": [
                "Three as-of queries return three prices.",
                "The boundary instant follows the inclusive-start exclusive-end rule.",
                "A second open row cannot be inserted for the same code.",
                "Times before the first version return `unknown`.",
            ],
        },
        {
            "day": 84,
            "slug": "tumbling-windows",
            "title": "Tumbling Windows on a File",
            "level": "Intermediate",
            "summary": "Aggregate an event file into fixed five-minute windows and put late events in a side bucket.",
            "concept": """
Streaming systems tumble, and so can a file if you are explicit about watermarks. This project reads dock events ordered by ingest time and assigns each event to a five-minute window on event time. A window closes when you have seen an ingest time more than ten minutes past the window end. Events for a closed window do not update the aggregate. They go to a late bucket with a count. You will fixture an event that arrives in order and one that arrives after its window has closed. The closed aggregate must stay fixed. This is not a distributed stream processor. It is the watermark rule, which is the part people skip when they copy a diagram.
            """.strip(),
            "approach": """
Windows are aligned to epoch minutes so two runs agree. The watermark is the max ingest time seen so far minus the allowed lateness. An event is late when its window end is less than or equal to the watermark at the time it is processed. Processing order is ingest order, which the fixture should not make identical to event order. Print the open aggregates and the late count. A test processes a late event and asserts the window sum is unchanged and the late count increased by one. A second test puts an event inside the lateness allowance and asserts the sum increased.
            """.strip(),
            "components": [
                ("Aligned windows", "Five-minute buckets with a defined origin."),
                ("Watermark", "Max ingest time minus allowed lateness."),
                ("Aggregate", "A count or a sum per window that freezes when the window closes."),
                ("Late bucket", "Events that missed the watermark, counted and stored."),
            ],
            "flow": [
                "Write events whose ingest order differs from event order.",
                "Process them one by one, updating the watermark.",
                "Close a window and then deliver a late event.",
                "Assert the frozen sum and the late count.",
                "Assert an event inside the allowance still updates the sum.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library only",
                "A fixture file, not a broker",
            ],
            "setup": [
                "Create `windows/` with `events.csv`, `tumble.py`, and tests.",
                "Run the processor and write `out/windows.csv` and `out/late.csv`.",
                "Run tests.",
                "Document the window size and the lateness in one place.",
            ],
            "done": [
                "Late events do not change a closed window.",
                "Events inside the lateness allowance do change the open window.",
                "Window bounds are deterministic across two runs.",
                "The late file contains the late event id.",
            ],
        },
        {
            "day": 85,
            "slug": "freshness-backfill",
            "title": "Freshness and a Backfill",
            "level": "Intermediate",
            "summary": "Mark a mart table stale when its newest event is too old, then backfill a date without touching the others.",
            "concept": """
A dashboard that refreshes on open will still show Tuesday if the job has been failing since Tuesday. This project writes a freshness check for `mart_daily`: the maximum event date must be at least the as-of date minus one day. If it is older, the check fails with the observed maximum and the expected minimum. It does not fill the gap with zeros. You will then run a backfill for the missing date only, using the range rebuild from the mart day, and show the freshness check passing afterward. A backfill that rebuilds every historical day is a bug in this fixture, and a test counts how many dates were deleted. The allowed count is one.
            """.strip(),
            "approach": """
Freshness is a function of the mart and an as-of date, returning a record with `ok`, `observed_max`, and `expected_min`. The job log records which dates were rebuilt. The test runs a pipeline that skipped a date, expects `ok` false, runs the backfill command with that date, and expects `ok` true. It also expects the other dates' totals to be byte-identical, which you can check by storing a hash of the untouched rows before and after. Do not implement alerting to a chat system. Print the record. The product is the check and the narrow backfill.
            """.strip(),
            "components": [
                ("Freshness function", "Compares max event date to the as-of date."),
                ("Failure record", "Observed max and expected min, no invented zeros."),
                ("Backfill command", "Rebuilds one date range."),
                ("Untouched-row hash", "Proves other dates did not change."),
            ],
            "flow": [
                "Load a mart with a missing latest date.",
                "Run freshness and expect failure.",
                "Backfill that date only.",
                "Hash the other dates before and after and assert equality.",
                "Run freshness again and expect success.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "SQLite mart from the previous pipeline day, or a smaller stand-in",
                "JSON freshness record",
            ],
            "setup": [
                "Create `freshness/` with `fresh.py` and tests.",
                "Run the fail, the backfill, and the pass.",
                "Run tests.",
                "Write the expected lag, one day, as a named constant.",
            ],
            "done": [
                "A stale mart fails the check and does not gain zero rows from the check itself.",
                "Backfill rebuilds one date.",
                "Hashes of untouched dates match.",
                "The success record still includes the observed max, not only a boolean.",
            ],
        },
        {
            "day": 86,
            "slug": "labels-as-of",
            "title": "Labels Joined as Of",
            "level": "Intermediate",
            "summary": "Attach a training label to a feature row using only events inside a window that starts after the cutoff.",
            "concept": """
Day 9 built features that do not peek. This project is the join you would actually schedule. Each decision row has a rider and a cutoff. Features are aggregates of events at or before the cutoff. The label is 1 if any `overrun` event occurs in `(cutoff, cutoff + 7 days]`. The SQL or the Python join must not use a label window that overlaps the feature window. You will write the query, explain the inequality, and plant one overrun exactly at the cutoff and one a second after. The first is a feature event, not a positive label. The second is a positive label and not a feature. A sloppy `<=` on both sides double-counts that second. A sloppy pair of `<=` on the cutoff double-counts the first. Tests cover both edges.
            """.strip(),
            "approach": """
Prefer SQLite so the predicate is visible in one query with two joins or two subqueries. Name the predicates in comments. The output table contains `rider_id`, `cutoff`, feature columns, and `label`. A rider with no events before the cutoff still gets a row if they are in the decision list, with null features, and can still have a positive label. Dropping them biases the set toward riders you already know. Assert a decision row with only a future overrun survives with null `rides_so_far` and label 1.
            """.strip(),
            "components": [
                ("Decision list", "Rider and cutoff pairs, including a rider with no history."),
                ("Feature predicate", "Events at or before the cutoff."),
                ("Label predicate", "Events strictly after the cutoff and at or before cutoff plus seven days."),
                ("Edge fixtures", "An event exactly at the cutoff and an event one second later."),
            ],
            "flow": [
                "Load events and decisions into SQLite.",
                "Run the feature query and the label query as two named SQL strings.",
                "Join them on rider and cutoff.",
                "Assert the two edge events land in different columns.",
                "Assert the history-free rider remains in the output.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "SQLite",
                "SQL files you can read without running Python",
            ],
            "setup": [
                "Create `as-of-labels/` with `label.sql`, `features.sql`, `join.py`, and tests.",
                "Run the join and inspect `out/training_rows.csv`.",
                "Run tests.",
                "Add a one-line comment on each inequality.",
            ],
            "done": [
                "The event at the cutoff affects features and not the label.",
                "The event one second later affects the label and not the features.",
                "A decision row with no history is kept.",
                "The SQL files contain the predicates the tests are about.",
            ],
        },
        {
            "day": 87,
            "slug": "embedding-backfill",
            "title": "An Embedding Job that Skips Unchanged Text",
            "level": "Advanced",
            "summary": "Backfill chunk embeddings keyed by content hash and model id, and skip rows whose hash is already stored.",
            "concept": """
Re-embedding a handbook on every build burns time and, when the model is hosted, money. It also mixes vectors from two models in one column if you are not careful. This project stores embeddings in a table keyed by chunk id, content hash, and model id. The job embeds a chunk only when that triple is missing. A text change changes the hash and produces a new row. The old row stays so you can compare. A model id change produces a new row even if the text is identical. The search path must filter to one model id, and a test expects it to ignore the other model's vector. You will run the job twice and show the second run embedding zero chunks. This is a batch data job. It is not a vector database product pitch.
            """.strip(),
            "approach": """
Use the hashing embedder so the job runs offline. The hash is SHA-256 of the chunk text bytes. The job writes a log line per chunk: `embedded` or `skipped`, with the reason. A test changes one character, expects one `embedded` and the rest `skipped`, and expects two rows for that chunk id. The reader function `vectors_for(model_id)` returns only that model. If the caller omits the model id, it raises. Silent mixing is the bug. Keep the log. The skip decision should be testable without re-reading the whole table by eye.
            """.strip(),
            "components": [
                ("Embedding table", "Chunk id, content hash, model id, vector."),
                ("Skip rule", "Do nothing when the triple already exists."),
                ("Append-on-change", "New hash or new model id adds a row and keeps the old one."),
                ("Reader filter", "Requires a model id and will not mix."),
            ],
            "flow": [
                "Embed a three-chunk handbook with model id `hash-v1`.",
                "Run the job again and assert zero embeds.",
                "Edit one chunk and assert a single embed and two stored rows for that id.",
                "Run with model id `hash-v2` and assert three new rows.",
                "Assert a reader call without a model id raises, and a call with `hash-v1` does not return `hash-v2` vectors.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "SQLite and the hashing embedder",
                "A job log of embedded versus skipped",
            ],
            "setup": [
                "Create `embed-backfill/` with `job.py` and tests.",
                "Run the sequence of four job states.",
                "Run tests.",
                "Record the model id naming rule in the notes: changing the hash function means a new model id.",
            ],
            "done": [
                "The second run skips every chunk.",
                "A one-character edit embeds one chunk and retains the previous row.",
                "Two model ids never appear in one reader result.",
                "Omitting the model id raises.",
            ],
            "ahead": """
A chunk that disappears from the handbook should not remain searchable forever. Add a tombstone step: after a run, rows whose chunk id is absent from the current source and whose model id is the one you are building are marked `retired` with a timestamp, not deleted. The reader skips retired rows. Fixture a deleted chunk and show that its vector is still in the table and absent from search results. The follow-on is reversible retirement, so you can explain a missing hit, rather than a silent delete.
            """.strip(),
        },
        {
            "day": 88,
            "slug": "seasonal-residuals",
            "title": "Seasonal Residuals",
            "level": "Advanced",
            "summary": "Alert when a daily rental count departs from a weekday baseline, and suppress dates you listed in advance.",
            "concept": """
A raw spike on Saturday is not news if Saturdays are always busy. This project builds a baseline for daily completed rentals: the median of the same weekday over the previous eight weeks, computed only from dates before the day you are scoring. The residual is the day's count minus that median. An alert fires when the residual exceeds a threshold you set in advance. You will plant one holiday that looks like an alert and, in the step that is still the core project, let it alert. The suppression list comes in the follow-on. For the core, you will also plant a true quiet Tuesday that should alert, and a normal Saturday that should not. This is a residual check on a metric series. It is not a feature-drift monitor and it does not recommend retraining a model.
            """.strip(),
            "approach": """
The series is a CSV of date and count that you generate with a weekday pattern plus two anomalies. The baseline function refuses to use the current day or any later day. A test passes future dates into the frame and asserts the baseline for a Wednesday does not change when a later Wednesday is huge. The threshold is a constant in `threshold.txt`. Alerts are rows in `alerts.csv` with the date, the median, the count, and the residual. No alert row means no alert. Do not emit a score for every day and call them all alerts.
            """.strip(),
            "components": [
                ("Weekday median", "Eight prior matching weekdays, looking only backward."),
                ("Residual", "Count minus median."),
                ("Threshold file", "Written before you interpret alerts."),
                ("Alert file", "Only the days that crossed the threshold."),
            ],
            "flow": [
                "Generate eight weeks of patterned counts plus a quiet Tuesday and a busy holiday Monday.",
                "Compute baselines and assert a future leak does not change an earlier baseline.",
                "Write alerts using the threshold.",
                "Assert the normal Saturday is absent and the quiet Tuesday is present.",
                "Leave the holiday in the alert file for the core project and mention it in the notes as the known nuisance.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library `statistics` and `datetime`",
                "CSV inputs and outputs",
            ],
            "setup": [
                "Create `residuals/` with `series.csv`, `baseline.py`, and tests.",
                "Set the threshold before running alerts.",
                "Run the job and the leak test.",
                "Run tests.",
            ],
            "done": [
                "The baseline for a day does not depend on later days.",
                "The quiet Tuesday alerts and a normal Saturday does not.",
                "The holiday Monday is listed as a nuisance in the notes, and it does alert in the core output.",
                "Non-alerting days are absent from `alerts.csv`.",
            ],
            "ahead": """
Add `calendar.csv` of dates that should not alert, written before you rerun, and suppress those dates with a reason `calendar` stored in a separate file from the real alerts. The quiet Tuesday must remain a real alert. A date on the calendar that would not have alerted anyway should not appear as a suppression, so you do not inflate how useful the calendar is. The follow-on is a suppression log you can audit, not a deleted residual.
            """.strip(),
        },
        {
            "day": 89,
            "slug": "borderline-matches",
            "title": "Borderline Entity Matches",
            "level": "Advanced",
            "summary": "Match rider records across two files with a score, and send only the borderline band to a review sheet.",
            "concept": """
Two exports call the same rider different names. A greedy match will either merge strangers or drop true pairs. This project scores candidate pairs from two files using rules you can read: exact email, exact phone, and a normalized name similarity you implement with a simple token Jaccard. High scores auto-link. Low scores are ignored. A middle band is written to `review.csv` with the two ids, the score, and the reason codes that fired. You do not auto-link the middle. You will plant one true pair that differs by a nickname and one false pair that shares a last name only. The true pair should land in review or in auto-link according to thresholds you set before seeing the result, and the false pair must not auto-link. The review file is the product. A silent merge is the failure.
            """.strip(),
            "approach": """
Blocking: only compare pairs that share a phone, an email, or a last-name token, so you do not score the full cross product. Say so, because blocking can miss a pair with no shared token. Plant one true pair with no shared block key and show it absent from review. That miss belongs in the notes. Thresholds live in `thresholds.json` with `auto` and `review` cutoffs. Auto requires the score to be greater than or equal to `auto`. Review is the half-open band `[review, auto)`. Below `review` is drop. A test constructs three scores and expects three different destinations.
            """.strip(),
            "components": [
                ("Blocker", "Candidate pairs that share a strong token."),
                ("Scorer", "Email, phone, and token Jaccard, combined by rules you write down."),
                ("Thresholds", "Auto, review, and drop."),
                ("Review sheet", "Borderline pairs only."),
            ],
            "flow": [
                "Write two small files with the planted pairs, including the unblockable true pair.",
                "Generate candidates and scores.",
                "Route each candidate to auto, review, or drop.",
                "Assert the last-name-only pair is not auto-linked.",
                "Assert the unblockable true pair appears in a `missed_blocks` note and not in the review sheet.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "CSV and JSON",
                "No external matching library",
            ],
            "setup": [
                "Create `entities/` with `left.csv`, `right.csv`, `match.py`, and tests.",
                "Set thresholds before the run you will quote.",
                "Run the matcher.",
                "Run tests.",
            ],
            "done": [
                "The three destinations are tested with constructed scores.",
                "The false pair is not auto-linked.",
                "The review sheet contains only the middle band.",
                "The unblockable true pair is reported as a block miss, not quietly dropped.",
            ],
            "ahead": """
Review decisions should feed the next run. Add `decisions.csv` with pair id and `link` or `reject`, and make the matcher honor a decision even when the score would have routed the pair differently. A later score change must not auto-link a pair a human rejected. Fixture a rejected pair whose score rises above the auto threshold and assert it stays unlinked, with reason `human-reject`. The follow-on is a decision that outranks the score.
            """.strip(),
        },
        {
            "day": 90,
            "slug": "error-budget-logs",
            "title": "Logs and an Error Budget",
            "level": "Advanced",
            "summary": "Parse structured logs into typed events and compute an error budget for a single route.",
            "concept": """
Free-text logs do not become a reliability number by being searched. This project defines a log line schema: timestamp, level, route, status, and request id. A parser accepts lines that match and sends the rest to `rejected.log` with a reason. You will compute, for one route, the fraction of requests with status 500 over a day, and compare it to a budget of one percent. A day over budget is a row in `budget_breach.csv`. A day with too few requests, under a minimum you set, is `insufficient`, not a breach and not a success. You will fixture both a breach and a quiet day. This is a log mart for one service. It is not a tracing product and it does not join spans across services yet.
            """.strip(),
            "approach": """
Write the parser so a line with an extra field is rejected rather than partially used, or accept extra fields and document which. Pick one. A missing status is a reject. Counts group by route and date. The budget comparison runs only when the request count is at least the minimum. Use integers and a ratio you compute from counts, and store the counts in the output so a reader can recompute the ratio. A test with 1 failure out of 10 requests is a breach if the minimum is 10 and the budget is one percent... that would be 10 percent, which breaches. Also test 0 failures out of 5 as insufficient when the minimum is 10.
            """.strip(),
            "components": [
                ("Line parser", "Typed fields and a reject file."),
                ("Route-day counts", "Requests and errors from accepted lines only."),
                ("Minimum sample", "Days below it are insufficient."),
                ("Breach file", "Days over the error budget, with counts."),
            ],
            "flow": [
                "Parse a fixture containing one bad line and several good lines.",
                "Assert the bad line is in the reject file and not in the counts.",
                "Compute two days: one breach and one insufficient sample.",
                "Assert the quiet small day is not a breach.",
                "Recompute the ratio from the stored counts in a test.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Plain text logs and CSV outputs",
                "No log vendor SDK",
            ],
            "setup": [
                "Create `error-budget/` with `app.log`, `parse.py`, and tests.",
                "Run the parser and the budget step.",
                "Run tests.",
                "Write the budget and the minimum sample at the top of the report.",
            ],
            "done": [
                "Malformed lines are excluded from the ratio.",
                "A small sample is `insufficient`, not healthy and not a breach.",
                "A breach row contains the counts needed to recompute the ratio.",
                "The route filter is explicit, and another route's errors do not enter the ratio.",
            ],
            "ahead": """
A request that fails and is retried under a new request id inflates the error rate. Add an optional `root_request_id` field. When it is present, count unique root ids rather than lines. Fixture three lines that share a root id, two of them errors, and show the line-based rate and the root-based rate side by side. The follow-on does not delete the line-based rate. It shows how a retry policy changes the budget math, and days without root ids keep the line-based definition.
            """.strip(),
        },
    ],
}
