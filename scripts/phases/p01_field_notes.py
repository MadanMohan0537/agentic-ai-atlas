"""Phase 1 — Field Notes: Data & Measurement. Days 1–10."""

PHASE = {
    "id": "01",
    "dir": "01-field-notes",
    "name": "Field Notes: Data & Measurement",
    "blurb": "Say what a row means, what a metric counts, and which records you refused before any model is worth training.",
    "outcome": "Defend a dataset: grain, time, labels, uncertainty, and leakage.",
    "goal": "Finish this phase able to defend a small dataset in a review: what one row means, which rows were refused and why, which clock a daily chart uses, how a metric is computed, how uncertain a rate is, whether two annotators agreed, and whether a feature or a split peeked at the future.",
    "skills": [
        "Row contracts and explicit reject reasons",
        "Distribution diffs between extracts",
        "Join grain and double-counted measures",
        "Event time, time zones, and late arrivals",
        "Text profiling before any embedding",
        "Metric dictionaries with two agreeing implementations",
        "Seeded bootstrap intervals",
        "Double annotation and agreement",
        "Point-in-time features from event logs",
        "Train-test leakage from row splits and time order",
    ],
    "projects": [
        {
            "day": 1,
            "slug": "row-contracts",
            "title": "Row Contracts for a Messy Extract",
            "level": "Beginner",
            "summary": "Accept or reject each rental row with a reason code instead of silently coercing bad fields.",
            "concept": """
A weekly extract looks finished until you sum it. Harbor Loop Bikes, a fictional municipal operator, sends `rentals.csv` with a blank header, a dollar sign inside a duration field, a rental id that appears twice, and a station code that is not on the official list. A notebook that only prints the shape will train on whatever survived coercion. This project builds a row contract. The grain is one row per rental id. A validator either accepts the row or writes a reason code, the source line number, and the raw text. The useful artifact is the rejection report, not a smoother chart. You should be able to tell an analyst which policy removed each row and how many rentals remain. Silent drops are the bug you are hunting. If a later day cannot explain its training set, it will be because this contract was skipped.
            """.strip(),
            "approach": """
Declare the contract in a Python dictionary: required columns, python types, numeric ranges, and the set of allowed station codes. Read with the `csv` module so nothing is coerced for you. Run checks in a fixed order — structure, then type, then domain, then uniqueness — and keep the first failing reason so the counts stay interpretable. Generate the fixture yourself, with a known count of each fault, and assert those counts in a test. Write `rentals_clean.csv` and `rejects.csv`. Do not "fix" bad values inside the loader. A repair is a separate decision and belongs in the rejection note, not in an invisible fillna.
            """.strip(),
            "components": [
                ("Fixture writer", "Creates a 40-row CSV with a counted set of planted faults."),
                ("Contract spec", "Required fields, types, ranges, and the station allow-list."),
                ("Validator", "Pure function from a raw row to accept or a single reason code."),
                ("Rejection report", "Counts by reason plus three example line numbers each."),
            ],
            "flow": [
                "Write the fixture so every fault is intentional and the expected reject counts are known.",
                "Parse with `csv.DictReader`. If the field count disagrees with the header, reject the line as `bad-structure` before type checks.",
                "Coerce only after a successful type check. A `$` in a numeric field is `bad-type`, not a number you strip quietly.",
                "Reject unknown station codes and out-of-range durations with their own reason codes.",
                "Track rental ids you have already accepted. A duplicate fails even when every other field is valid.",
                "Write the clean file and the reject file, then assert the reason histogram matches the fixture plan.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library: `csv`, `pathlib`, `unittest`",
                "No third-party dataframe library on this day",
            ],
            "setup": [
                "Create a folder `row-contracts/` and a virtual environment with `python3 -m venv .venv`, then activate it. You will not install packages.",
                "Add `fixtures/build_rentals.py` that writes `fixtures/rentals.csv` and a sibling `expected_rejects.json` mapping reason codes to counts.",
                "Add `contract.py` with the station allow-list (eight codes is enough) and `validate_row(row, seen_ids) -> str | None`.",
                "Add `load.py` that reads the CSV, writes `out/rentals_clean.csv` and `out/rejects.csv`, and prints the histogram.",
                "Add `tests/test_contract.py` and run `python3 -m unittest discover -s tests -v`.",
            ],
            "done": [
                "Every planted fault appears under the reason code you named, with the right count.",
                "The clean file has unique rental ids, no currency symbols, and only allow-listed stations.",
                "A test fails if the loader skips a malformed line without recording a reason.",
                "You can state the grain in one sentence and point to the line of code that enforces it.",
            ],
        },
        {
            "day": 2,
            "slug": "extract-diff",
            "title": "Diff Two Extracts by Distribution",
            "level": "Beginner",
            "summary": "Compare two weekly rental files by quantiles and category mix, not by staring at the first rows.",
            "concept": """
Harbor Loop sends a second file, `rentals_week_b.csv`, and someone asks whether the feed "changed." Sorting both files and reading `head` will miss a duration that doubled in the tail and a station that vanished. This project compares two extracts that already passed the Day 1 contract. You will compute, for each numeric column, the min, the median, the 95th percentile, and the max, and for each category column the share of rows. Then you will emit a diff that flags a column only when a threshold you chose is crossed. The point is a reviewable change list. A human still decides whether the change is a real operational event or a broken exporter. You are not building a drift-to-retraining system. You are building the habit of comparing distributions before you trust a week-over-week chart.
            """.strip(),
            "approach": """
Reuse the clean-file schema from Day 1 so both weeks are rows you have already accepted. Implement quantiles by sorting, not by a statistics package, so you can explain the index you picked for the 95th percentile. Compare category shares with absolute percentage-point differences. Put the thresholds in a small config: for example, flag duration if the median moves by more than 15 percent, and flag a station if its share moves by more than 5 points or it disappears. Print a markdown table with week A, week B, and the delta. Include one planted change in week B so the test has something it must flag, and one tiny change it must ignore.
            """.strip(),
            "components": [
                ("Clean-week fixtures", "Two accepted extracts, one of them with planted distribution shifts."),
                ("Summary function", "Quantiles for numeric columns and shares for categories."),
                ("Threshold config", "The deltas that count as a flag, written down before you look at the result."),
                ("Diff report", "A markdown table of flagged columns and a count of unflagged ones."),
            ],
            "flow": [
                "Load both clean extracts with the Day 1 columns and refuse to compare if the headers differ.",
                "Compute numeric summaries independently for each week.",
                "Compute category shares, including categories present in only one week.",
                "Apply thresholds. A missing station is a flag even if every numeric quantile is stable.",
                "Write `out/week_diff.md` and assert that the planted shift is flagged and the tiny shift is not.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library only",
                "Markdown report you can paste into a review",
            ],
            "setup": [
                "Start a new folder so this day runs even if Day 1 is unfinished. Copy the column names, not the whole loader.",
                "Write `fixtures/week_a.csv` and `fixtures/week_b.csv` by hand or with a short generator. Keep them under 200 rows.",
                "Implement `summarize.py` and `diff.py`.",
                "Run `python3 diff.py` and then `python3 -m unittest discover -s tests -v`.",
                "Read the report out loud once. If you cannot explain a flag without looking at the code, the label is wrong.",
            ],
            "done": [
                "The report flags the planted median shift and the disappeared station.",
                "A one-percent jitter in a single row does not create a flag.",
                "Quantile code uses an explicit index on a sorted list, and a test locks that index for a known vector.",
                "Headers that differ exit non-zero with a message, rather than aligning columns by position.",
            ],
        },
        {
            "day": 3,
            "slug": "grain-and-double-counts",
            "title": "Grain, Joins, and Double-Counted Revenue",
            "level": "Beginner",
            "summary": "Show how a plausible join inflates revenue, then publish a grain checklist that would have stopped it.",
            "concept": """
Harbor Loop's finance extract has one row per rental. The maintenance extract has many rows per bike, because a bike is serviced several times a month. Join them on `bike_id` and sum `fare_cents` and you will report a fantasy. The number is large, the SQL looks ordinary, and a dashboard will happily chart it. This project builds two tiny tables and the wrong join on purpose, then the right one. You will write a grain checklist that names, for each table, what one row represents and which columns are allowed to be summed. The lesson is not "joins are hard." The lesson is that a metric without a grain is a claim you cannot audit. You will also show a safe pattern: aggregate the many-side to the join key first, then join, then sum.
            """.strip(),
            "approach": """
Use sqlite3 in the standard library so the SQL is real and the data is a file you can reopen. Create `rentals` with unique `rental_id` and `service_events` with several rows per `bike_id`. Compute three numbers side by side: the true fare sum, the inflated sum after a direct join, and the sum after pre-aggregation. They must not match by accident; pick fares so the inflation factor is obvious, such as exactly 3x on bikes with three service events. Write the checklist as `GRAIN.md` next to the SQL. Include a question the checklist forces: "If I sum this column after this join, am I still summing one row per rental?"
            """.strip(),
            "components": [
                ("SQLite schema", "Rentals at rental grain and service events at event grain."),
                ("Inflated query", "The join a hurried analysis would ship."),
                ("Safe query", "Aggregate service events to `bike_id` before joining."),
                ("Grain checklist", "One row's meaning, primary key, and which measures are summable."),
            ],
            "flow": [
                "Create the database in `build_db.py` with a fixed seed so the sums are stable.",
                "Run the true fare total from `rentals` alone and store it as the reference.",
                "Run the naive join and record the inflated total.",
                "Pre-aggregate service events to one row per bike, join, and show the fare total returning to the reference.",
                "Write `GRAIN.md` using the actual table names and keys from the schema.",
                "Test that inflated > reference and safe == reference.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library `sqlite3`",
                "SQL you can paste into any SQLite shell",
            ],
            "setup": [
                "Create `grain-lab/` and add `build_db.py`, `queries.sql`, and `tests/test_sums.py`.",
                "Insert about 20 rentals and 30 service events. Give three bikes multiple service rows.",
                "Run `python3 build_db.py` then `python3 -m unittest discover -s tests -v`.",
                "Open the database with `sqlite3 harbor.db` and run the three fare queries yourself.",
            ],
            "done": [
                "The test names all three totals and fails if the safe query drifts from the reference.",
                "`GRAIN.md` states the primary key of each table in a single line.",
                "You can point to the exact join that multiplies fare rows.",
                "A sum of service cost, which does live at event grain, is still correct after the safe pattern. Add that assert too.",
            ],
        },
        {
            "day": 4,
            "slug": "event-time",
            "title": "Event Time, Time Zones, and Late Arrivals",
            "level": "Beginner",
            "summary": "Bucket rentals by event time in one zone, and show a late event landing in yesterday's bucket.",
            "concept": """
A rental has three clocks: when the ride happened (`event_time`), when the dock emitted the record (`ingest_time`), and the zone those strings were written in. Harbor Loop's docks write local time without an offset. The warehouse job runs in UTC. A ride at 23:30 local can look like "tomorrow" or "yesterday" depending on which clock you truncate. Late arrivals make it worse: Monday's job closes Sunday, then a Sunday ride appears on Tuesday. This project picks one definition — local event time in `America/New_York`, converted to UTC for storage, bucketed by the local calendar date — and writes a test where a late event moves a closed day's count. You are practicing time literacy, not building a stream processor. The artifact is a small function and three fixtures that would have started an argument in a real standup.
            """.strip(),
            "approach": """
Store every instant as timezone-aware UTC in the data model. Parse naive local strings with an explicit zone using the standard library `zoneinfo`. Never truncate a UTC timestamp and call it a local day. Implement `local_day(event_time_utc) -> date` and `apply_arrival(daily_counts, event, arrived_at, closed_through)`. If the event's local day is already closed, record it as a late adjustment rather than silently rewriting history. Use a winter date and a summer date so a daylight-saving transition is at least one fixture, even if you only assert the offset you expect.
            """.strip(),
            "components": [
                ("Clock model", "Aware UTC instants plus the named local zone."),
                ("Day bucketer", "Converts event time to a local calendar date."),
                ("Late-arrival rule", "Closed days receive an adjustment record, not a quiet rewrite."),
                ("Fixtures", "Evening boundary, DST date, and an event that arrives after close."),
            ],
            "flow": [
                "Parse a naive local string and attach `America/New_York`.",
                "Convert to UTC and store both the UTC instant and the source zone name.",
                "Bucket by converting back to local and taking the date. Assert 23:30 local stays on that local date.",
                "Close a day, then apply an event whose local day is already closed.",
                "Check that the closed total is unchanged and an adjustment row exists with the rental id.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library `datetime` and `zoneinfo`",
                "No pandas offsets and no third-party timezone library",
            ],
            "setup": [
                "Create `event-time/` with `clocks.py` and `tests/test_clocks.py`.",
                "Hard-code three events in the test file so the cases stay visible.",
                "Run `python3 -m unittest discover -s tests -v`.",
                "Add a one-line comment above the bucketer naming the zone. If the zone is missing, the function should raise rather than assume UTC.",
            ],
            "done": [
                "A 23:30 America/New_York event buckets to that local date in both January and July.",
                "Naive timestamps are rejected, or accepted only through a function that requires a zone argument.",
                "A late event for a closed day produces an adjustment and does not change the closed total.",
                "You can explain, without notes, which clock a rides-per-day chart is using.",
            ],
        },
        {
            "day": 5,
            "slug": "text-profiles",
            "title": "Text Profiles Before Any Embedding",
            "level": "Beginner",
            "summary": "Profile a pile of support notes: length, scripts, boilerplate, and exact-duplicate rate.",
            "concept": """
Harbor Loop's support desk exports notes as text. Before you embed them or send them to a model, you need a profile that would change your plan. Some notes are three words. Some are the same macro pasted fifty times. Some mix English with Spanish station names. Some contain a phone number your later prompt would echo. This project profiles a folder of `.txt` notes you write yourself, about forty of them, including the boring cases. You will report character length quantiles, a crude script mix, the share of notes that match a boilerplate template, the exact-duplicate rate, and a count of lines that look like phone numbers. Nothing is embedded. The decision at the end is written down: which notes are worth a later retrieval corpus, and which should be excluded because they are macros.
            """.strip(),
            "approach": """
Normalize line endings and strip trailing whitespace, and count that normalization as its own step so you do not hide it. Detect boilerplate by exact match against a list of macros you author, not by a model. Detect phone-like strings with a conservative regular expression and report counts, not the numbers themselves, in the summary. Duplicate rate uses a hash of the normalized text. Keep a `decisions.md` that says "exclude macros" or "keep macros but down-weight them," with one sentence of evidence from your own report. The profile script must be rerunnable: same folder in, same JSON out.
            """.strip(),
            "components": [
                ("Note corpus", "About forty short notes, including macros, duplicates, and a few non-English tokens."),
                ("Normalizer", "Newlines and trailing whitespace, leaving a before/after length."),
                ("Profiler", "Length quantiles, boilerplate share, duplicate rate, phone-like count."),
                ("Decision note", "What you would exclude from a later corpus, tied to a number in the profile."),
            ],
            "flow": [
                "Write the notes under `corpus/`. Include five exact copies of one macro and two near-copies that differ by a ticket id.",
                "Normalize and hash. Near-copies must not count as exact duplicates. That distinction is the point of the near-copies.",
                "Compute length quantiles on normalized character length.",
                "Flag boilerplate by exact match to `macros.txt` and phone-like patterns by regex.",
                "Write `out/profile.json` and `decisions.md`. A test locks the duplicate count at five.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library `re`, `hashlib`, `pathlib`, `json`",
                "A corpus you authored, so the notes are safe to commit later if you want",
            ],
            "setup": [
                "Create `text-profiles/` and the `corpus/` folder.",
                "Add `macros.txt` with two templates.",
                "Implement `profile.py` and tests for the duplicate count and the phone-like counter.",
                "Run the profiler twice and diff the JSON. The second run should be identical.",
            ],
            "done": [
                "Exact duplicates and near-copies are counted differently, and the test shows it.",
                "The profile reports counts of phone-like strings without printing the matched text.",
                "`decisions.md` cites at least one number from `profile.json`.",
                "Re-running the script does not change the JSON.",
            ],
        },
        {
            "day": 6,
            "slug": "metric-dictionary",
            "title": "One Definition of Active",
            "level": "Beginner",
            "summary": "Write a metric dictionary entry for an active rider and compute it two ways that must agree.",
            "concept": """
"Active riders" is where Harbor Loop's weekly review goes to argue. Marketing means anyone who opened the app. Operations means anyone who completed a ride. Finance means anyone who generated a fare. All three numbers are real, and none of them is "the" active count until you pick one and show the formula. This project writes a metric dictionary entry with a name, an owner, a grain, an inclusion rule, an exclusion rule, and a worked example. Then you implement that rule twice: once as a Python function over event rows, and once as SQL over the same rows in sqlite. The two implementations must return the same rider ids on a shared fixture. A second, deliberately different definition lives in the dictionary as a rejected alternative, so you can see the trap without shipping it.
            """.strip(),
            "approach": """
Choose the operations definition and make it sharp. An active rider in a week is a `rider_id` with at least one rental whose local event day falls in that week and whose status is `completed`. Cancelled rentals do not count. Riders with only an app-open event do not count. Put the week boundary in the dictionary using the local-day rule from Day 4, described in prose even if you simplify the fixture to dates. Implement `active_riders(events, week_start, week_end) -> set[str]` and the equivalent SQL. Test equality of the sets, not of the counts alone, so a swapped rider cannot hide.
            """.strip(),
            "components": [
                ("Dictionary entry", "Name, owner, grain, inclusion, exclusion, and a worked example."),
                ("Rejected alternative", "The marketing definition, marked as not the metric."),
                ("Python implementation", "Set of rider ids over in-memory events."),
                ("SQL implementation", "The same rule in sqlite against the same rows."),
            ],
            "flow": [
                "Write `metrics/active_rider.md` before writing code. If the code is easier to write than the entry, the entry is still vague.",
                "Load a fixture with completed rides, cancelled rides, and app opens.",
                "Compute the Python set and the SQL set for one named week.",
                "Assert the sets are equal and that a cancelled-only rider is absent.",
                "Add a one-row change that flips a rental to completed and show the set gaining that rider.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library `sqlite3`",
                "Markdown for the dictionary entry",
            ],
            "setup": [
                "Create `metric-dictionary/` with `metrics/active_rider.md`, `active.py`, `active.sql`, and a test module.",
                "Keep the fixture under 30 events so you can audit it by eye.",
                "Run the tests. Then change the SQL on purpose so a cancelled ride counts, and watch the test fail.",
                "Revert that change. The failed run is the demonstration, not the final state.",
            ],
            "done": [
                "Python and SQL return the same set of rider ids on the fixture.",
                "The dictionary names an owner and a grain. The owner is a role, not the word everyone.",
                "The rejected marketing definition is present and is not what the code computes.",
                "A cancelled-only rider is excluded, and a test says so.",
            ],
        },
        {
            "day": 7,
            "slug": "bootstrap-a-rate",
            "title": "Bootstrap a Rate by Hand",
            "level": "Beginner",
            "summary": "Estimate a completion rate and a percentile interval with a seeded resample you can recompute.",
            "concept": """
Harbor Loop completed 18 rides out of 40 attempts on a rainy pilot dock. Reporting "45 percent" as if it were exact will over-commit the next staffing decision. This project estimates a completion rate and a simple uncertainty interval by resampling the 40 attempts with a fixed seed. You will implement the bootstrap yourself: draw with replacement, compute the mean, repeat, and read off percentiles. The goal is not a statistics library demo. The goal is to see that a different seed moves the interval slightly and a larger sample shrinks it. You will also write the sentence you are willing to say out loud, including what the interval is not: it does not fix a biased sample, and it does not know about next week's weather.
            """.strip(),
            "approach": """
Represent each attempt as 1 or 0. Use `random.Random(seed)` so the resample is reproducible. Implement `bootstrap_mean(xs, rounds, seed) -> list[float]` and `percentile(sorted_stats, p)`. Use 2000 rounds. Report the 2.5th and 97.5th percentiles as the interval. Add a second fixture with 400 attempts at the same underlying rate, generated from a seeded Bernoulli, and show the interval is narrower. Do not import scipy. Document the sentence in `finding.md` next to the numbers your program printed.
            """.strip(),
            "components": [
                ("Attempt vector", "Forty binary outcomes you can inspect."),
                ("Seeded resampler", "Draws with replacement from a private `random.Random`."),
                ("Percentile reader", "Reads the interval off the sorted bootstrap means."),
                ("Finding note", "One sentence a stakeholder could hear, plus one limitation."),
            ],
            "flow": [
                "Hard-code or generate the 40 outcomes and compute the point estimate.",
                "Resample 2000 times with seed 7 and store the means.",
                "Sort and read the 2.5 and 97.5 percentiles.",
                "Repeat with seed 8 and assert the point estimate is unchanged while the interval endpoints may move.",
                "Build a larger seeded sample and assert its interval width is smaller than the n=40 width.",
                "Write `finding.md` using the printed numbers.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library `random` and `statistics`",
                "No scipy and no statsmodels",
            ],
            "setup": [
                "Create `bootstrap-rate/` with `bootstrap.py` and `tests/test_bootstrap.py`.",
                "Run the script and paste the interval into `finding.md`.",
                "Run the tests. Include a test that a constant vector of ones yields an interval of exactly 1.",
                "Keep the round count at 2000 so the test runtime stays trivial.",
            ],
            "done": [
                "The same seed reproduces the same interval endpoints bit for bit on this machine.",
                "A constant vector produces a zero-width interval at that constant.",
                "The n=400 interval is narrower than the n=40 interval in the test.",
                "`finding.md` states a limitation that resampling does not cure.",
            ],
        },
        {
            "day": 8,
            "slug": "double-annotation",
            "title": "Double Annotation and Agreement",
            "level": "Beginner",
            "summary": "Label the same support notes twice, measure agreement, and fix the guideline where you disagreed.",
            "concept": """
You want a later classifier to separate `bike_issue`, `billing`, and `other` in Harbor Loop support notes. The labels are the product. If two careful readers cannot apply the guideline the same way, a model will only freeze the confusion. This project writes a one-page guideline, labels the same twenty notes twice (you can play both annotators if you wait a few minutes and hide the first pass), and computes raw agreement and Cohen's kappa by hand. Wherever you disagreed, you rewrite the guideline with an example. You do not train a model. The artifact is a guideline that got stricter because of a disagreement, plus a second labeling pass whose agreement you also report. That second number is allowed to be imperfect. Hiding a disagreement is the failure.
            """.strip(),
            "approach": """
Put notes in `notes.jsonl` with ids. Store labels in `pass1.json` and `pass2.json` mapping id to label, so you cannot silently edit pass 1 after seeing pass 2. Implement a confusion matrix among the three labels and kappa from the formula: agreement relative to chance, using the observed label margins. Where the two passes differ, append a row to `disagreements.md` with the note id, both labels, and the sentence you added to the guideline. Then label a fresh ten notes twice under the revised guideline and report that agreement separately. Do not average it into the first number.
            """.strip(),
            "components": [
                ("Guideline", "Definitions, two positive examples per class, and one near-miss."),
                ("Blind passes", "Two JSON maps that you do not edit in place."),
                ("Agreement math", "Confusion counts, raw agreement, and kappa."),
                ("Guideline patch", "A new example born from a specific disagreement."),
            ],
            "flow": [
                "Write the guideline before labeling. Keep it under a page.",
                "Label twenty notes into `pass1.json`. Start `pass2.json` only after pass 1 is written.",
                "Compute the matrix and kappa. A test can lock kappa for a fixture pair you construct, separate from your real notes.",
                "Record each disagreement and amend the guideline.",
                "Label ten new notes twice and write both agreement numbers in `report.md`.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library `json`",
                "Markdown guideline",
            ],
            "setup": [
                "Create `double-annotation/` with the notes, the guideline, and `agree.py`.",
                "Add a unit test with a hand-computed kappa on a 6-item fixture so the formula is checked without your real labels.",
                "Run `python3 agree.py --a pass1.json --b pass2.json`.",
                "If your two passes agree perfectly, you picked notes that are too easy. Add three borderline notes and label again. Perfect agreement on toys teaches nothing.",
            ],
            "done": [
                "Kappa on the hand-computed fixture matches the value you calculated on paper.",
                "At least one guideline change cites a note id and the two labels.",
                "The first-pass agreement and the revised-guideline agreement are reported separately.",
                "Label files are maps from id to label, and a test rejects a label outside the three classes.",
            ],
        },
        {
            "day": 9,
            "slug": "features-from-events",
            "title": "Features from Events Without Peeking",
            "level": "Beginner",
            "summary": "Build a rider feature table where every aggregate uses only events at or before a cutoff.",
            "concept": """
A model that predicts whether a rider will complete a ride next week is worthless if the features include next week's rides. The leak is usually boring: a "lifetime ride count" computed on the full table, then attached to a row that sits in the middle of that lifetime. This project builds a feature table for Harbor Loop riders. Each row is a rider at a decision cutoff. Features are counts and recency computed only from events at or before that cutoff. The label, if you attach one, uses only events after the cutoff. You will try to cheat on purpose — include a future ride in the count — and show a test that catches it. This is the small version of a point-in-time join. A later pipeline day goes further. Today the table fits in memory and the cutoff is a column you can point to.
            """.strip(),
            "approach": """
Events are `rider_id`, `event_time`, `event_type`. Decision rows are `rider_id`, `cutoff`. Sort events and, for each decision, scan events for that rider with `event_time <= cutoff`. Compute `rides_so_far`, `days_since_last_ride`, and `cancels_so_far`. If there is no prior ride, recency is null, not zero. Zero would claim a ride happened today. Attach a label `completed_within_7d` from events in `(cutoff, cutoff + 7 days]`. Write the honest table and a broken table that uses `<= cutoff + 7 days` for the ride count. The test asserts the broken count is greater for at least one rider and the honest function never reads an event after the cutoff.
            """.strip(),
            "components": [
                ("Event log", "Append-only rider events with timestamps."),
                ("Decision list", "Rider and cutoff pairs, including a rider with no history."),
                ("Honest aggregator", "Features from events at or before the cutoff only."),
                ("Leak detector", "A deliberately wrong aggregator and a test that separates the two."),
            ],
            "flow": [
                "Write a small event log covering three riders and two weeks.",
                "Define two cutoffs per rider so the second cutoff can see more history than the first.",
                "Compute honest features. Check by hand the first rider's `rides_so_far` at the earlier cutoff.",
                "Compute labels strictly after the cutoff.",
                "Compute the broken feature and assert it differs from the honest one on the planted future ride.",
                "Assert a rider with no prior events has null recency.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library `datetime` and `csv`",
                "No feature-store product and no training yet",
            ],
            "setup": [
                "Create `features-from-events/` with `events.csv`, `decisions.csv`, `features.py`, and tests.",
                "Run `python3 features.py --mode honest` and inspect `out/features.csv`.",
                "Run the tests, including the leak contrast.",
                "Add a comment at the cutoff comparison that states whether the cutoff instant itself is included. Pick included, and test an event exactly at the cutoff.",
            ],
            "done": [
                "An event exactly at the cutoff is included in features and excluded from the label.",
                "Null recency is preserved for riders with no prior ride.",
                "The broken aggregator fails the contrast test.",
                "You can explain the decision grain: one row per rider per cutoff, not one row per rider forever.",
            ],
        },
        {
            "day": 10,
            "slug": "split-leakage",
            "title": "Split Leakage Hunt",
            "level": "Beginner",
            "summary": "Find riders who landed in both train and test, and rebuild the split so a rider lives in only one side.",
            "concept": """
Harbor Loop trains a small classifier later in this atlas. If you split rows at random, the same rider's Monday trip can train the model and their Tuesday trip can test it. Accuracy will look like learning. It is recognition of a person you already saw. This project hunts that leak. You will implement a bad row-wise split, report the set of rider ids that appear on both sides, and then implement a rider-wise split that makes the intersection empty. You will also check a second leak that groups do not fix by themselves: sorting by time, training on the future, and testing on the past. The artifact is a split report with three numbers: overlap under the bad split, overlap under the rider split, and the earliest test time versus the latest train time under a time split. No model is trained today.
            """.strip(),
            "approach": """
Use the rental table at rental grain with `rider_id` and `event_time`. The bad split assigns each row to test with probability 0.3 using a seeded RNG. The good split hashes the rider id into buckets, or assigns whole riders after shuffling rider ids with a seed. Do not use Python's built-in `hash()`, which is salted per process. Use `hashlib` on the rider id so the split is stable. The time split sorts by `event_time` and cuts at 70 percent. Write `report.json` with the three overlap or order statistics. A test builds a tiny log where a row-wise split must overlap and the rider split must not.
            """.strip(),
            "components": [
                ("Rental rows", "Several rides per rider so a row split can leak."),
                ("Row split", "The leaky baseline, seeded."),
                ("Rider split", "A stable whole-rider assignment."),
                ("Time split check", "Compares the max train time to the min test time."),
            ],
            "flow": [
                "Load rentals and group row indexes by rider id.",
                "Run the row split and compute the intersection of rider ids.",
                "Run the rider split and assert the intersection is empty.",
                "Run the time split and record whether every train time is strictly before every test time.",
                "Write the report. If your fixture's row split happens to draw no overlap, add rides until it does, or construct the overlap explicitly in the test.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library `hashlib` and `json`",
                "No scikit-learn split helper, so the grouping stays visible",
            ],
            "setup": [
                "Create `split-leakage/` with `rides.csv`, `split.py`, and tests.",
                "Include at least eight riders with three rides each.",
                "Run `python3 split.py` and read `out/report.json`.",
                "Run the unit tests. One test should fail if someone switches the rider split back to a row split.",
            ],
            "done": [
                "The report shows a non-empty rider overlap for the row split on your fixture.",
                "The rider split overlap is empty and stable across two process runs.",
                "The time split's latest train instant is earlier than its earliest test instant.",
                "You can say which split you would use to estimate performance on a new rider, and why the time split answers a different question.",
            ],
        },
    ],
}
