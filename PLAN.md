# Agentic AI Atlas — Full Plan

This is the consolidated build plan for all eight phases and all 100 projects. Each project also has a folder of its own, linked below, with the same spec. Advanced projects include a step-ahead extension: the next failure the core design does not yet handle.

The catalog of links lives in [README.md](README.md). This file is the plan written out in full.

## Contents

- [Phase 01: Field Notes: Data & Measurement](#phase-01) — days 01–10
- [Phase 02: Learning Machines](#phase-02) — days 11–20
- [Phase 03: Transformer Workbench](#phase-03) — days 21–32
- [Phase 04: Retrieval Studio](#phase-04) — days 33–48
- [Phase 05: Agent Workshop](#phase-05) — days 49–64
- [Phase 06: Proof Bench: Evals and Harnesses](#phase-06) — days 65–78
- [Phase 07: Flowroom: Analytics and Pipelines](#phase-07) — days 79–90
- [Phase 08: Frontier Lab](#phase-08) — days 91–100

<a id="phase-01"></a>

## Phase 01: Field Notes: Data & Measurement

**Days 01–10.** 10 projects.

### Goal

Finish this phase able to defend a small dataset in a review: what one row means, which rows were refused and why, which clock a daily chart uses, how a metric is computed, how uncertain a rate is, whether two annotators agreed, and whether a feature or a split peeked at the future.

### Skills covered

- Row contracts and explicit reject reasons
- Distribution diffs between extracts
- Join grain and double-counted measures
- Event time, time zones, and late arrivals
- Text profiling before any embedding
- Metric dictionaries with two agreeing implementations
- Seeded bootstrap intervals
- Double annotation and agreement
- Point-in-time features from event logs
- Train-test leakage from row splits and time order

Say what a row means, what a metric counts, and which records you refused before any model is worth training.

By the end of the phase you should be able to: Defend a dataset: grain, time, labels, uncertainty, and leakage.

### Day 01 — Row Contracts for a Messy Extract

**Level:** Beginner

**Folder:** [atlas/01-field-notes/day-01-row-contracts/README.md](atlas/01-field-notes/day-01-row-contracts/README.md)

Accept or reject each rental row with a reason code instead of silently coercing bad fields.

#### Concept

A weekly extract looks finished until you sum it. Harbor Loop Bikes, a fictional municipal operator, sends `rentals.csv` with a blank header, a dollar sign inside a duration field, a rental id that appears twice, and a station code that is not on the official list. A notebook that only prints the shape will train on whatever survived coercion. This project builds a row contract. The grain is one row per rental id. A validator either accepts the row or writes a reason code, the source line number, and the raw text. The useful artifact is the rejection report, not a smoother chart. You should be able to tell an analyst which policy removed each row and how many rentals remain. Silent drops are the bug you are hunting. If a later day cannot explain its training set, it will be because this contract was skipped.

#### Approach

Declare the contract in a Python dictionary: required columns, python types, numeric ranges, and the set of allowed station codes. Read with the `csv` module so nothing is coerced for you. Run checks in a fixed order — structure, then type, then domain, then uniqueness — and keep the first failing reason so the counts stay interpretable. Generate the fixture yourself, with a known count of each fault, and assert those counts in a test. Write `rentals_clean.csv` and `rejects.csv`. Do not "fix" bad values inside the loader. A repair is a separate decision and belongs in the rejection note, not in an invisible fillna.

#### Components

| Piece | Role |
| --- | --- |
| Fixture writer | Creates a 40-row CSV with a counted set of planted faults. |
| Contract spec | Required fields, types, ranges, and the station allow-list. |
| Validator | Pure function from a raw row to accept or a single reason code. |
| Rejection report | Counts by reason plus three example line numbers each. |

#### How it works

1. Write the fixture so every fault is intentional and the expected reject counts are known.
2. Parse with `csv.DictReader`. If the field count disagrees with the header, reject the line as `bad-structure` before type checks.
3. Coerce only after a successful type check. A `$` in a numeric field is `bad-type`, not a number you strip quietly.
4. Reject unknown station codes and out-of-range durations with their own reason codes.
5. Track rental ids you have already accepted. A duplicate fails even when every other field is valid.
6. Write the clean file and the reject file, then assert the reason histogram matches the fixture plan.

#### Tech stack

- Python 3.11 or newer
- Standard library: `csv`, `pathlib`, `unittest`
- No third-party dataframe library on this day

#### Setup

1. Create a folder `row-contracts/` and a virtual environment with `python3 -m venv .venv`, then activate it. You will not install packages.
2. Add `fixtures/build_rentals.py` that writes `fixtures/rentals.csv` and a sibling `expected_rejects.json` mapping reason codes to counts.
3. Add `contract.py` with the station allow-list (eight codes is enough) and `validate_row(row, seen_ids) -> str | None`.
4. Add `load.py` that reads the CSV, writes `out/rentals_clean.csv` and `out/rejects.csv`, and prints the histogram.
5. Add `tests/test_contract.py` and run `python3 -m unittest discover -s tests -v`.

#### Deliverable

- Every planted fault appears under the reason code you named, with the right count.
- The clean file has unique rental ids, no currency symbols, and only allow-listed stations.
- A test fails if the loader skips a malformed line without recording a reason.
- You can state the grain in one sentence and point to the line of code that enforces it.

### Day 02 — Diff Two Extracts by Distribution

**Level:** Beginner

**Folder:** [atlas/01-field-notes/day-02-extract-diff/README.md](atlas/01-field-notes/day-02-extract-diff/README.md)

Compare two weekly rental files by quantiles and category mix, not by staring at the first rows.

#### Concept

Harbor Loop sends a second file, `rentals_week_b.csv`, and someone asks whether the feed "changed." Sorting both files and reading `head` will miss a duration that doubled in the tail and a station that vanished. This project compares two extracts that already passed the Day 1 contract. You will compute, for each numeric column, the min, the median, the 95th percentile, and the max, and for each category column the share of rows. Then you will emit a diff that flags a column only when a threshold you chose is crossed. The point is a reviewable change list. A human still decides whether the change is a real operational event or a broken exporter. You are not building a drift-to-retraining system. You are building the habit of comparing distributions before you trust a week-over-week chart.

#### Approach

Reuse the clean-file schema from Day 1 so both weeks are rows you have already accepted. Implement quantiles by sorting, not by a statistics package, so you can explain the index you picked for the 95th percentile. Compare category shares with absolute percentage-point differences. Put the thresholds in a small config: for example, flag duration if the median moves by more than 15 percent, and flag a station if its share moves by more than 5 points or it disappears. Print a markdown table with week A, week B, and the delta. Include one planted change in week B so the test has something it must flag, and one tiny change it must ignore.

#### Components

| Piece | Role |
| --- | --- |
| Clean-week fixtures | Two accepted extracts, one of them with planted distribution shifts. |
| Summary function | Quantiles for numeric columns and shares for categories. |
| Threshold config | The deltas that count as a flag, written down before you look at the result. |
| Diff report | A markdown table of flagged columns and a count of unflagged ones. |

#### How it works

1. Load both clean extracts with the Day 1 columns and refuse to compare if the headers differ.
2. Compute numeric summaries independently for each week.
3. Compute category shares, including categories present in only one week.
4. Apply thresholds. A missing station is a flag even if every numeric quantile is stable.
5. Write `out/week_diff.md` and assert that the planted shift is flagged and the tiny shift is not.

#### Tech stack

- Python 3.11 or newer
- Standard library only
- Markdown report you can paste into a review

#### Setup

1. Start a new folder so this day runs even if Day 1 is unfinished. Copy the column names, not the whole loader.
2. Write `fixtures/week_a.csv` and `fixtures/week_b.csv` by hand or with a short generator. Keep them under 200 rows.
3. Implement `summarize.py` and `diff.py`.
4. Run `python3 diff.py` and then `python3 -m unittest discover -s tests -v`.
5. Read the report out loud once. If you cannot explain a flag without looking at the code, the label is wrong.

#### Deliverable

- The report flags the planted median shift and the disappeared station.
- A one-percent jitter in a single row does not create a flag.
- Quantile code uses an explicit index on a sorted list, and a test locks that index for a known vector.
- Headers that differ exit non-zero with a message, rather than aligning columns by position.

### Day 03 — Grain, Joins, and Double-Counted Revenue

**Level:** Beginner

**Folder:** [atlas/01-field-notes/day-03-grain-and-double-counts/README.md](atlas/01-field-notes/day-03-grain-and-double-counts/README.md)

Show how a plausible join inflates revenue, then publish a grain checklist that would have stopped it.

#### Concept

Harbor Loop's finance extract has one row per rental. The maintenance extract has many rows per bike, because a bike is serviced several times a month. Join them on `bike_id` and sum `fare_cents` and you will report a fantasy. The number is large, the SQL looks ordinary, and a dashboard will happily chart it. This project builds two tiny tables and the wrong join on purpose, then the right one. You will write a grain checklist that names, for each table, what one row represents and which columns are allowed to be summed. The lesson is not "joins are hard." The lesson is that a metric without a grain is a claim you cannot audit. You will also show a safe pattern: aggregate the many-side to the join key first, then join, then sum.

#### Approach

Use sqlite3 in the standard library so the SQL is real and the data is a file you can reopen. Create `rentals` with unique `rental_id` and `service_events` with several rows per `bike_id`. Compute three numbers side by side: the true fare sum, the inflated sum after a direct join, and the sum after pre-aggregation. They must not match by accident; pick fares so the inflation factor is obvious, such as exactly 3x on bikes with three service events. Write the checklist as `GRAIN.md` next to the SQL. Include a question the checklist forces: "If I sum this column after this join, am I still summing one row per rental?"

#### Components

| Piece | Role |
| --- | --- |
| SQLite schema | Rentals at rental grain and service events at event grain. |
| Inflated query | The join a hurried analysis would ship. |
| Safe query | Aggregate service events to `bike_id` before joining. |
| Grain checklist | One row's meaning, primary key, and which measures are summable. |

#### How it works

1. Create the database in `build_db.py` with a fixed seed so the sums are stable.
2. Run the true fare total from `rentals` alone and store it as the reference.
3. Run the naive join and record the inflated total.
4. Pre-aggregate service events to one row per bike, join, and show the fare total returning to the reference.
5. Write `GRAIN.md` using the actual table names and keys from the schema.
6. Test that inflated > reference and safe == reference.

#### Tech stack

- Python 3.11 or newer
- Standard library `sqlite3`
- SQL you can paste into any SQLite shell

#### Setup

1. Create `grain-lab/` and add `build_db.py`, `queries.sql`, and `tests/test_sums.py`.
2. Insert about 20 rentals and 30 service events. Give three bikes multiple service rows.
3. Run `python3 build_db.py` then `python3 -m unittest discover -s tests -v`.
4. Open the database with `sqlite3 harbor.db` and run the three fare queries yourself.

#### Deliverable

- The test names all three totals and fails if the safe query drifts from the reference.
- `GRAIN.md` states the primary key of each table in a single line.
- You can point to the exact join that multiplies fare rows.
- A sum of service cost, which does live at event grain, is still correct after the safe pattern. Add that assert too.

### Day 04 — Event Time, Time Zones, and Late Arrivals

**Level:** Beginner

**Folder:** [atlas/01-field-notes/day-04-event-time/README.md](atlas/01-field-notes/day-04-event-time/README.md)

Bucket rentals by event time in one zone, and show a late event landing in yesterday's bucket.

#### Concept

A rental has three clocks: when the ride happened (`event_time`), when the dock emitted the record (`ingest_time`), and the zone those strings were written in. Harbor Loop's docks write local time without an offset. The warehouse job runs in UTC. A ride at 23:30 local can look like "tomorrow" or "yesterday" depending on which clock you truncate. Late arrivals make it worse: Monday's job closes Sunday, then a Sunday ride appears on Tuesday. This project picks one definition — local event time in `America/New_York`, converted to UTC for storage, bucketed by the local calendar date — and writes a test where a late event moves a closed day's count. You are practicing time literacy, not building a stream processor. The artifact is a small function and three fixtures that would have started an argument in a real standup.

#### Approach

Store every instant as timezone-aware UTC in the data model. Parse naive local strings with an explicit zone using the standard library `zoneinfo`. Never truncate a UTC timestamp and call it a local day. Implement `local_day(event_time_utc) -> date` and `apply_arrival(daily_counts, event, arrived_at, closed_through)`. If the event's local day is already closed, record it as a late adjustment rather than silently rewriting history. Use a winter date and a summer date so a daylight-saving transition is at least one fixture, even if you only assert the offset you expect.

#### Components

| Piece | Role |
| --- | --- |
| Clock model | Aware UTC instants plus the named local zone. |
| Day bucketer | Converts event time to a local calendar date. |
| Late-arrival rule | Closed days receive an adjustment record, not a quiet rewrite. |
| Fixtures | Evening boundary, DST date, and an event that arrives after close. |

#### How it works

1. Parse a naive local string and attach `America/New_York`.
2. Convert to UTC and store both the UTC instant and the source zone name.
3. Bucket by converting back to local and taking the date. Assert 23:30 local stays on that local date.
4. Close a day, then apply an event whose local day is already closed.
5. Check that the closed total is unchanged and an adjustment row exists with the rental id.

#### Tech stack

- Python 3.11 or newer
- Standard library `datetime` and `zoneinfo`
- No pandas offsets and no third-party timezone library

#### Setup

1. Create `event-time/` with `clocks.py` and `tests/test_clocks.py`.
2. Hard-code three events in the test file so the cases stay visible.
3. Run `python3 -m unittest discover -s tests -v`.
4. Add a one-line comment above the bucketer naming the zone. If the zone is missing, the function should raise rather than assume UTC.

#### Deliverable

- A 23:30 America/New_York event buckets to that local date in both January and July.
- Naive timestamps are rejected, or accepted only through a function that requires a zone argument.
- A late event for a closed day produces an adjustment and does not change the closed total.
- You can explain, without notes, which clock a rides-per-day chart is using.

### Day 05 — Text Profiles Before Any Embedding

**Level:** Beginner

**Folder:** [atlas/01-field-notes/day-05-text-profiles/README.md](atlas/01-field-notes/day-05-text-profiles/README.md)

Profile a pile of support notes: length, scripts, boilerplate, and exact-duplicate rate.

#### Concept

Harbor Loop's support desk exports notes as text. Before you embed them or send them to a model, you need a profile that would change your plan. Some notes are three words. Some are the same macro pasted fifty times. Some mix English with Spanish station names. Some contain a phone number your later prompt would echo. This project profiles a folder of `.txt` notes you write yourself, about forty of them, including the boring cases. You will report character length quantiles, a crude script mix, the share of notes that match a boilerplate template, the exact-duplicate rate, and a count of lines that look like phone numbers. Nothing is embedded. The decision at the end is written down: which notes are worth a later retrieval corpus, and which should be excluded because they are macros.

#### Approach

Normalize line endings and strip trailing whitespace, and count that normalization as its own step so you do not hide it. Detect boilerplate by exact match against a list of macros you author, not by a model. Detect phone-like strings with a conservative regular expression and report counts, not the numbers themselves, in the summary. Duplicate rate uses a hash of the normalized text. Keep a `decisions.md` that says "exclude macros" or "keep macros but down-weight them," with one sentence of evidence from your own report. The profile script must be rerunnable: same folder in, same JSON out.

#### Components

| Piece | Role |
| --- | --- |
| Note corpus | About forty short notes, including macros, duplicates, and a few non-English tokens. |
| Normalizer | Newlines and trailing whitespace, leaving a before/after length. |
| Profiler | Length quantiles, boilerplate share, duplicate rate, phone-like count. |
| Decision note | What you would exclude from a later corpus, tied to a number in the profile. |

#### How it works

1. Write the notes under `corpus/`. Include five exact copies of one macro and two near-copies that differ by a ticket id.
2. Normalize and hash. Near-copies must not count as exact duplicates. That distinction is the point of the near-copies.
3. Compute length quantiles on normalized character length.
4. Flag boilerplate by exact match to `macros.txt` and phone-like patterns by regex.
5. Write `out/profile.json` and `decisions.md`. A test locks the duplicate count at five.

#### Tech stack

- Python 3.11 or newer
- Standard library `re`, `hashlib`, `pathlib`, `json`
- A corpus you authored, so the notes are safe to commit later if you want

#### Setup

1. Create `text-profiles/` and the `corpus/` folder.
2. Add `macros.txt` with two templates.
3. Implement `profile.py` and tests for the duplicate count and the phone-like counter.
4. Run the profiler twice and diff the JSON. The second run should be identical.

#### Deliverable

- Exact duplicates and near-copies are counted differently, and the test shows it.
- The profile reports counts of phone-like strings without printing the matched text.
- `decisions.md` cites at least one number from `profile.json`.
- Re-running the script does not change the JSON.

### Day 06 — One Definition of Active

**Level:** Beginner

**Folder:** [atlas/01-field-notes/day-06-metric-dictionary/README.md](atlas/01-field-notes/day-06-metric-dictionary/README.md)

Write a metric dictionary entry for an active rider and compute it two ways that must agree.

#### Concept

"Active riders" is where Harbor Loop's weekly review goes to argue. Marketing means anyone who opened the app. Operations means anyone who completed a ride. Finance means anyone who generated a fare. All three numbers are real, and none of them is "the" active count until you pick one and show the formula. This project writes a metric dictionary entry with a name, an owner, a grain, an inclusion rule, an exclusion rule, and a worked example. Then you implement that rule twice: once as a Python function over event rows, and once as SQL over the same rows in sqlite. The two implementations must return the same rider ids on a shared fixture. A second, deliberately different definition lives in the dictionary as a rejected alternative, so you can see the trap without shipping it.

#### Approach

Choose the operations definition and make it sharp. An active rider in a week is a `rider_id` with at least one rental whose local event day falls in that week and whose status is `completed`. Cancelled rentals do not count. Riders with only an app-open event do not count. Put the week boundary in the dictionary using the local-day rule from Day 4, described in prose even if you simplify the fixture to dates. Implement `active_riders(events, week_start, week_end) -> set[str]` and the equivalent SQL. Test equality of the sets, not of the counts alone, so a swapped rider cannot hide.

#### Components

| Piece | Role |
| --- | --- |
| Dictionary entry | Name, owner, grain, inclusion, exclusion, and a worked example. |
| Rejected alternative | The marketing definition, marked as not the metric. |
| Python implementation | Set of rider ids over in-memory events. |
| SQL implementation | The same rule in sqlite against the same rows. |

#### How it works

1. Write `metrics/active_rider.md` before writing code. If the code is easier to write than the entry, the entry is still vague.
2. Load a fixture with completed rides, cancelled rides, and app opens.
3. Compute the Python set and the SQL set for one named week.
4. Assert the sets are equal and that a cancelled-only rider is absent.
5. Add a one-row change that flips a rental to completed and show the set gaining that rider.

#### Tech stack

- Python 3.11 or newer
- Standard library `sqlite3`
- Markdown for the dictionary entry

#### Setup

1. Create `metric-dictionary/` with `metrics/active_rider.md`, `active.py`, `active.sql`, and a test module.
2. Keep the fixture under 30 events so you can audit it by eye.
3. Run the tests. Then change the SQL on purpose so a cancelled ride counts, and watch the test fail.
4. Revert that change. The failed run is the demonstration, not the final state.

#### Deliverable

- Python and SQL return the same set of rider ids on the fixture.
- The dictionary names an owner and a grain. The owner is a role, not the word everyone.
- The rejected marketing definition is present and is not what the code computes.
- A cancelled-only rider is excluded, and a test says so.

### Day 07 — Bootstrap a Rate by Hand

**Level:** Beginner

**Folder:** [atlas/01-field-notes/day-07-bootstrap-a-rate/README.md](atlas/01-field-notes/day-07-bootstrap-a-rate/README.md)

Estimate a completion rate and a percentile interval with a seeded resample you can recompute.

#### Concept

Harbor Loop completed 18 rides out of 40 attempts on a rainy pilot dock. Reporting "45 percent" as if it were exact will over-commit the next staffing decision. This project estimates a completion rate and a simple uncertainty interval by resampling the 40 attempts with a fixed seed. You will implement the bootstrap yourself: draw with replacement, compute the mean, repeat, and read off percentiles. The goal is not a statistics library demo. The goal is to see that a different seed moves the interval slightly and a larger sample shrinks it. You will also write the sentence you are willing to say out loud, including what the interval is not: it does not fix a biased sample, and it does not know about next week's weather.

#### Approach

Represent each attempt as 1 or 0. Use `random.Random(seed)` so the resample is reproducible. Implement `bootstrap_mean(xs, rounds, seed) -> list[float]` and `percentile(sorted_stats, p)`. Use 2000 rounds. Report the 2.5th and 97.5th percentiles as the interval. Add a second fixture with 400 attempts at the same underlying rate, generated from a seeded Bernoulli, and show the interval is narrower. Do not import scipy. Document the sentence in `finding.md` next to the numbers your program printed.

#### Components

| Piece | Role |
| --- | --- |
| Attempt vector | Forty binary outcomes you can inspect. |
| Seeded resampler | Draws with replacement from a private `random.Random`. |
| Percentile reader | Reads the interval off the sorted bootstrap means. |
| Finding note | One sentence a stakeholder could hear, plus one limitation. |

#### How it works

1. Hard-code or generate the 40 outcomes and compute the point estimate.
2. Resample 2000 times with seed 7 and store the means.
3. Sort and read the 2.5 and 97.5 percentiles.
4. Repeat with seed 8 and assert the point estimate is unchanged while the interval endpoints may move.
5. Build a larger seeded sample and assert its interval width is smaller than the n=40 width.
6. Write `finding.md` using the printed numbers.

#### Tech stack

- Python 3.11 or newer
- Standard library `random` and `statistics`
- No scipy and no statsmodels

#### Setup

1. Create `bootstrap-rate/` with `bootstrap.py` and `tests/test_bootstrap.py`.
2. Run the script and paste the interval into `finding.md`.
3. Run the tests. Include a test that a constant vector of ones yields an interval of exactly 1.
4. Keep the round count at 2000 so the test runtime stays trivial.

#### Deliverable

- The same seed reproduces the same interval endpoints bit for bit on this machine.
- A constant vector produces a zero-width interval at that constant.
- The n=400 interval is narrower than the n=40 interval in the test.
- `finding.md` states a limitation that resampling does not cure.

### Day 08 — Double Annotation and Agreement

**Level:** Beginner

**Folder:** [atlas/01-field-notes/day-08-double-annotation/README.md](atlas/01-field-notes/day-08-double-annotation/README.md)

Label the same support notes twice, measure agreement, and fix the guideline where you disagreed.

#### Concept

You want a later classifier to separate `bike_issue`, `billing`, and `other` in Harbor Loop support notes. The labels are the product. If two careful readers cannot apply the guideline the same way, a model will only freeze the confusion. This project writes a one-page guideline, labels the same twenty notes twice (you can play both annotators if you wait a few minutes and hide the first pass), and computes raw agreement and Cohen's kappa by hand. Wherever you disagreed, you rewrite the guideline with an example. You do not train a model. The artifact is a guideline that got stricter because of a disagreement, plus a second labeling pass whose agreement you also report. That second number is allowed to be imperfect. Hiding a disagreement is the failure.

#### Approach

Put notes in `notes.jsonl` with ids. Store labels in `pass1.json` and `pass2.json` mapping id to label, so you cannot silently edit pass 1 after seeing pass 2. Implement a confusion matrix among the three labels and kappa from the formula: agreement relative to chance, using the observed label margins. Where the two passes differ, append a row to `disagreements.md` with the note id, both labels, and the sentence you added to the guideline. Then label a fresh ten notes twice under the revised guideline and report that agreement separately. Do not average it into the first number.

#### Components

| Piece | Role |
| --- | --- |
| Guideline | Definitions, two positive examples per class, and one near-miss. |
| Blind passes | Two JSON maps that you do not edit in place. |
| Agreement math | Confusion counts, raw agreement, and kappa. |
| Guideline patch | A new example born from a specific disagreement. |

#### How it works

1. Write the guideline before labeling. Keep it under a page.
2. Label twenty notes into `pass1.json`. Start `pass2.json` only after pass 1 is written.
3. Compute the matrix and kappa. A test can lock kappa for a fixture pair you construct, separate from your real notes.
4. Record each disagreement and amend the guideline.
5. Label ten new notes twice and write both agreement numbers in `report.md`.

#### Tech stack

- Python 3.11 or newer
- Standard library `json`
- Markdown guideline

#### Setup

1. Create `double-annotation/` with the notes, the guideline, and `agree.py`.
2. Add a unit test with a hand-computed kappa on a 6-item fixture so the formula is checked without your real labels.
3. Run `python3 agree.py --a pass1.json --b pass2.json`.
4. If your two passes agree perfectly, you picked notes that are too easy. Add three borderline notes and label again. Perfect agreement on toys teaches nothing.

#### Deliverable

- Kappa on the hand-computed fixture matches the value you calculated on paper.
- At least one guideline change cites a note id and the two labels.
- The first-pass agreement and the revised-guideline agreement are reported separately.
- Label files are maps from id to label, and a test rejects a label outside the three classes.

### Day 09 — Features from Events Without Peeking

**Level:** Beginner

**Folder:** [atlas/01-field-notes/day-09-features-from-events/README.md](atlas/01-field-notes/day-09-features-from-events/README.md)

Build a rider feature table where every aggregate uses only events at or before a cutoff.

#### Concept

A model that predicts whether a rider will complete a ride next week is worthless if the features include next week's rides. The leak is usually boring: a "lifetime ride count" computed on the full table, then attached to a row that sits in the middle of that lifetime. This project builds a feature table for Harbor Loop riders. Each row is a rider at a decision cutoff. Features are counts and recency computed only from events at or before that cutoff. The label, if you attach one, uses only events after the cutoff. You will try to cheat on purpose — include a future ride in the count — and show a test that catches it. This is the small version of a point-in-time join. A later pipeline day goes further. Today the table fits in memory and the cutoff is a column you can point to.

#### Approach

Events are `rider_id`, `event_time`, `event_type`. Decision rows are `rider_id`, `cutoff`. Sort events and, for each decision, scan events for that rider with `event_time <= cutoff`. Compute `rides_so_far`, `days_since_last_ride`, and `cancels_so_far`. If there is no prior ride, recency is null, not zero. Zero would claim a ride happened today. Attach a label `completed_within_7d` from events in `(cutoff, cutoff + 7 days]`. Write the honest table and a broken table that uses `<= cutoff + 7 days` for the ride count. The test asserts the broken count is greater for at least one rider and the honest function never reads an event after the cutoff.

#### Components

| Piece | Role |
| --- | --- |
| Event log | Append-only rider events with timestamps. |
| Decision list | Rider and cutoff pairs, including a rider with no history. |
| Honest aggregator | Features from events at or before the cutoff only. |
| Leak detector | A deliberately wrong aggregator and a test that separates the two. |

#### How it works

1. Write a small event log covering three riders and two weeks.
2. Define two cutoffs per rider so the second cutoff can see more history than the first.
3. Compute honest features. Check by hand the first rider's `rides_so_far` at the earlier cutoff.
4. Compute labels strictly after the cutoff.
5. Compute the broken feature and assert it differs from the honest one on the planted future ride.
6. Assert a rider with no prior events has null recency.

#### Tech stack

- Python 3.11 or newer
- Standard library `datetime` and `csv`
- No feature-store product and no training yet

#### Setup

1. Create `features-from-events/` with `events.csv`, `decisions.csv`, `features.py`, and tests.
2. Run `python3 features.py --mode honest` and inspect `out/features.csv`.
3. Run the tests, including the leak contrast.
4. Add a comment at the cutoff comparison that states whether the cutoff instant itself is included. Pick included, and test an event exactly at the cutoff.

#### Deliverable

- An event exactly at the cutoff is included in features and excluded from the label.
- Null recency is preserved for riders with no prior ride.
- The broken aggregator fails the contrast test.
- You can explain the decision grain: one row per rider per cutoff, not one row per rider forever.

### Day 10 — Split Leakage Hunt

**Level:** Beginner

**Folder:** [atlas/01-field-notes/day-10-split-leakage/README.md](atlas/01-field-notes/day-10-split-leakage/README.md)

Find riders who landed in both train and test, and rebuild the split so a rider lives in only one side.

#### Concept

Harbor Loop trains a small classifier later in this atlas. If you split rows at random, the same rider's Monday trip can train the model and their Tuesday trip can test it. Accuracy will look like learning. It is recognition of a person you already saw. This project hunts that leak. You will implement a bad row-wise split, report the set of rider ids that appear on both sides, and then implement a rider-wise split that makes the intersection empty. You will also check a second leak that groups do not fix by themselves: sorting by time, training on the future, and testing on the past. The artifact is a split report with three numbers: overlap under the bad split, overlap under the rider split, and the earliest test time versus the latest train time under a time split. No model is trained today.

#### Approach

Use the rental table at rental grain with `rider_id` and `event_time`. The bad split assigns each row to test with probability 0.3 using a seeded RNG. The good split hashes the rider id into buckets, or assigns whole riders after shuffling rider ids with a seed. Do not use Python's built-in `hash()`, which is salted per process. Use `hashlib` on the rider id so the split is stable. The time split sorts by `event_time` and cuts at 70 percent. Write `report.json` with the three overlap or order statistics. A test builds a tiny log where a row-wise split must overlap and the rider split must not.

#### Components

| Piece | Role |
| --- | --- |
| Rental rows | Several rides per rider so a row split can leak. |
| Row split | The leaky baseline, seeded. |
| Rider split | A stable whole-rider assignment. |
| Time split check | Compares the max train time to the min test time. |

#### How it works

1. Load rentals and group row indexes by rider id.
2. Run the row split and compute the intersection of rider ids.
3. Run the rider split and assert the intersection is empty.
4. Run the time split and record whether every train time is strictly before every test time.
5. Write the report. If your fixture's row split happens to draw no overlap, add rides until it does, or construct the overlap explicitly in the test.

#### Tech stack

- Python 3.11 or newer
- Standard library `hashlib` and `json`
- No scikit-learn split helper, so the grouping stays visible

#### Setup

1. Create `split-leakage/` with `rides.csv`, `split.py`, and tests.
2. Include at least eight riders with three rides each.
3. Run `python3 split.py` and read `out/report.json`.
4. Run the unit tests. One test should fail if someone switches the rider split back to a row split.

#### Deliverable

- The report shows a non-empty rider overlap for the row split on your fixture.
- The rider split overlap is empty and stable across two process runs.
- The time split's latest train instant is earlier than its earliest test instant.
- You can say which split you would use to estimate performance on a new rider, and why the time split answers a different question.

<a id="phase-02"></a>

## Phase 02: Learning Machines

**Days 11–20.** 10 projects.

### Goal

Finish this phase with a tabular model you can rerun from a config file, a baseline it had to beat, a threshold chosen from a payoff rather than from 0.5, and a written limit on what the model must not be used for.

### Skills covered

- Majority and mean baselines
- Logistic regression, scaling, and reliability bins
- Shallow decision trees and visible overfit
- Additive stumps and one-feature occlusion
- Precision and recall at a predeclared alert budget
- Clustering with names you can refuse
- Pairwise ranking against a popularity baseline
- Locked runs: seed, data hash, and a model card stub
- Error slices with a support floor
- Cost-sensitive thresholds on a report fold

Train classical models on a tabular rental problem you can explain, and refuse any score that does not beat a boring baseline.

By the end of the phase you should be able to: Fit, slice, and threshold a tabular model without fooling yourself.

### Day 11 — Baselines that Humiliate Models

**Level:** Beginner

**Folder:** [atlas/02-learning-machines/day-11-humbling-baselines/README.md](atlas/02-learning-machines/day-11-humbling-baselines/README.md)

Score a majority-class rule and a mean predictor before any learned model is allowed to look good.

#### Concept

Harbor Loop wants a first model for a yes-or-no question: did a booked rental overrun its slot? Ninety percent of rentals do not overrun. A classifier that always says "no" is right ninety percent of the time and useless at the dock. This project builds the dataset — a few hundred synthetic rows with a seeded generator — and the two baselines every later model has to beat. For classification, the baseline is the majority class, scored with accuracy and with balanced accuracy so the base rate cannot hide. For a companion regression, predicting overrun minutes, the baseline predicts the training mean. You will write both metrics yourself on the confusion counts. The artifact is a one-page baseline card that later days must paste their scores next to. A model that cannot beat the card does not get a paragraph in your notes.

#### Approach

Generate rows with `random.Random(11)`. Columns: booked minutes, start hour, dock type (open or indoor), rider tenure days, weather code (clear, rain), and the label `overrun`. Plant the base rate near 0.1 by sampling the label from a rule you write down, plus noise, so the problem is learnable later and still imbalanced. Split riders, not rows, using the stable hash from the split day, even if you reimplement the ten lines here. Compute the majority baseline only from the training fold. Evaluating the majority class on data you used to pick it is a small leak; picking it on train and scoring on test is the habit. Write `baseline_card.md` with the test accuracy, balanced accuracy, and the regression mean absolute error of the mean predictor.

#### Components

| Piece | Role |
| --- | --- |
| Seeded generator | Synthetic rentals with a documented labeling rule. |
| Rider split | Whole riders assigned to train or test. |
| Majority baseline | Train-fold mode, scored on the test fold. |
| Mean predictor | Train-fold mean of overrun minutes, with test MAE. |

#### How it works

1. Generate the table and write `data/rentals.csv` plus `data/RULE.txt` describing the labeling rule in words.
2. Split by rider id into train and test.
3. Compute the majority label on train only and score it on test.
4. Compute balanced accuracy from the four confusion counts, not from a library.
5. Fit the mean overrun on train rows that did overrun, and separately on all train rows. Document which one you are using and why.
6. Write the baseline card. A test locks the majority label for this seed so a generator change cannot pass quietly.

#### Tech stack

- Python 3.11 or newer
- Standard library `random`, `csv`, `hashlib`
- Metrics implemented from counts

#### Setup

1. Create `baselines/` with `generate.py`, `score.py`, and tests.
2. Run `python3 generate.py` then `python3 score.py`.
3. Run `python3 -m unittest discover -s tests -v`.
4. If balanced accuracy and accuracy are almost equal, your base rate is too close to one half. Push the negative rate up and regenerate.

#### Deliverable

- The baseline card quotes test numbers and names the seed and the split rule.
- Majority class is chosen on train, and a test would fail if it were chosen on test.
- Balanced accuracy is computed from TP, FP, TN, and FN in your own function.
- The labeling rule is written in `RULE.txt` before any later model day starts.

### Day 12 — A Linear Model You Can Read

**Level:** Beginner

**Folder:** [atlas/02-learning-machines/day-12-readable-linear/README.md](atlas/02-learning-machines/day-12-readable-linear/README.md)

Fit a logistic model with gradient descent, standardize inputs, and plot reliability in five bins.

#### Concept

A linear model earns its place when you can read a coefficient and say what would happen if that input moved. On the overrun table, tenure and rain should not share a scale: tenure is in days, weather is a code. Fit without standardizing and the steps fight each other. This project implements binary logistic regression with batch gradient descent, no scikit-learn. You will one-hot the small categories yourself, standardize numeric columns using train-fold mean and variance, and apply those same numbers to test. Then you will bin the test set by predicted probability and compare the average prediction in each bin to the observed overrun rate. That reliability table is the model's honesty check. Coefficients come after, as a sentence each: direction, rough size, and whether the feature's scale makes the size comparable.

#### Approach

Use a learning rate you log, a fixed iteration count, and a seed only if you shuffle rows. Initialize weights at zero so the run is determined by the data. Clip the linear score before the exp in the sigmoid so a wild step cannot overflow. Hold out the test fold from standardization statistics. Reliability uses five bins of equal width on [0, 1], and bins with fewer than five test rows are reported but not trusted. Compare test log loss to the majority baseline's log loss. Accuracy alone is not the headline. If the linear model cannot beat the baseline card on log loss, say so in the notes and keep the baseline.

#### Components

| Piece | Role |
| --- | --- |
| Design matrix | Numeric columns standardized, categories one-hot encoded. |
| Gradient step | Batch logistic gradient with a clipped score. |
| Reliability table | Five bins comparing mean prediction to observed rate. |
| Coefficient notes | One sentence per weight, after scaling is explained. |

#### How it works

1. Load the Day 11 table or regenerate it with the same seed and rule.
2. Build the train-only scaler and apply it to train and test.
3. Fit for a logged number of steps. Save the loss every ten steps to `loss.csv`.
4. Predict on test and write the reliability table.
5. Write coefficient sentences into `coefficients.md`, noting which columns were standardized.
6. Assert test log loss is finite and that a column excluded from the scaler does not change the scaler's stored mean.

#### Tech stack

- Python 3.11 or newer
- Standard library only, including `math`
- CSV loss curve you can open in any spreadsheet

#### Setup

1. Create `linear-model/` and copy the generator or read the CSV from a relative path you document.
2. Implement `logit.py` with `fit` and `predict_proba` separated.
3. Run the fit and the tests.
4. If the loss curve increases, divide the learning rate by ten and record both attempts in the notes. Do not hide the failed rate.

#### Deliverable

- Train mean and variance are not computed from test rows, and a test locks that.
- The reliability table has a row per non-empty bin.
- Test log loss is compared to the majority baseline in the written notes.
- You can point to one coefficient and say what scaling was applied before it was fit.

### Day 13 — A Tree You Can Draw

**Level:** Beginner

**Folder:** [atlas/02-learning-machines/day-13-a-tree-you-can-draw/README.md](atlas/02-learning-machines/day-13-a-tree-you-can-draw/README.md)

Grow a shallow decision tree, draw it, and show the overfit when you let it memorize leaves.

#### Concept

Trees are easy to praise because a picture of a split looks like a policy. They are also easy to overfit: a deep tree will isolate single rentals and call that structure. This project grows a classification tree for overrun with a depth limit you choose, using Gini impurity computed from counts. You will print the tree as indented text you can redraw on paper, with the train count and the train overrun rate in every node. Then you will grow the same tree with the depth limit removed, or set absurdly high, and compare train accuracy to test accuracy. The gap is the lesson. You will also name one split that matches the labeling rule you wrote on Day 11 and one split that looks like noise. If you cannot tell those apart from the picture, the picture is too deep to trust.

#### Approach

Implement a binary tree on numeric features and on already-encoded binary categories. Candidate thresholds are midpoints between sorted unique values, capped at a small number per feature so the day stays short. Stop when depth hits the limit, when a node is pure, or when a node has fewer than a minimum count you set in a constant. Do not prune with a library. The comparison is shallow versus deep on the same split. Write `tree.txt` for the shallow model and a three-line overfit note: train accuracy, test accuracy, and the depth of the deepest leaf in the unconstrained run.

#### Components

| Piece | Role |
| --- | --- |
| Impurity function | Gini from class counts, tested on a hand example. |
| Split search | Midpoint thresholds with a cap on candidates. |
| Text tree | Indented nodes with counts and rates. |
| Depth contrast | Shallow versus unconstrained, same data, both scores. |

#### How it works

1. Reuse the rider split and the overrun table.
2. Fit a tree with max depth 3 and minimum node size 15.
3. Render it to text and confirm every leaf shows a count.
4. Fit an unconstrained tree and record train versus test accuracy.
5. Write two sentences identifying a meaningful split and a suspicious one.
6. Test Gini on a node with counts (3, 1) against the value you computed by hand.

#### Tech stack

- Python 3.11 or newer
- Standard library only
- Plain text rendering, no graphviz requirement

#### Setup

1. Create `tree-model/` with `tree.py` and tests.
2. Run the shallow fit and read `tree.txt` top to bottom.
3. Run the deep fit and append the contrast to `notes.md`.
4. If the shallow tree and the deep tree have the same test accuracy, increase the noise in a copy of the generator or lower the minimum node size on the deep run only, and say which lever you moved.

#### Deliverable

- The text tree is complete: every internal node names a feature and a threshold.
- Train accuracy of the deep tree is higher than its test accuracy on your run, or you documented a dataset too small to show the gap and enlarged it.
- Gini matches a hand-computed example in a test.
- The notes name one split you would keep and one you do not trust.

### Day 14 — Boosted Trees and a Local Reason

**Level:** Beginner

**Folder:** [atlas/02-learning-machines/day-14-boosted-tables/README.md](atlas/02-learning-machines/day-14-boosted-tables/README.md)

Fit a small gradient-boosted stumps model and explain one prediction by occluding a single feature.

#### Concept

Boosting is the usual next step on tabular problems, and it is also where explanations go vague. Harbor Loop does not need a leaderboard. It needs a model that beats the Day 11 card and a way to say, for one rental, which feature moved the score. This project fits additive stumps: each new tree is a depth-1 tree fit to the negative gradient of log loss. You will keep the ensemble small, on the order of twenty stumps, and you will stop if validation log loss rises. For a single test rental you will compute a local reason by occlusion: replace one feature with its train median, measure the change in predicted probability, and restore it. The largest change is the reason you write down. This is not a global importance trophy and it is not a production explainer for credit or safety decisions. It is a check you can recompute with a calculator and a median.

#### Approach

Implement stumps, not a full boosting library. Use a learning rate of 0.1 and add each stump's contribution scaled by that rate. Hold a validation slice out of the training riders so early stopping does not look at the test riders. Log the validation loss per stump. Occlusion uses the train median for numeric features and the train mode for categories. Apply the same scaler logic you used before if features are not already on comparable scales; for stumps, raw scales are acceptable because thresholds adapt, and you should say that in the notes so you do not pretend the median swap is scale-free in meaning. Compare test log loss to the linear model and to the majority baseline.

#### Components

| Piece | Role |
| --- | --- |
| Stump fitter | A depth-1 tree on the current residual. |
| Additive ensemble | Learning rate times stump, with early stopping on validation riders. |
| Occlusion probe | One-feature median swap and the delta in probability. |
| Scoreboard | Baseline, linear, and boosted test log loss in one file. |

#### How it works

1. Split riders into train, validation, and test. Write the counts.
2. Fit stumps until the validation loss increases, or until you hit the cap.
3. Score the test set once with the chosen number of stumps.
4. Pick one test row whose predicted probability is between 0.3 and 0.7 if you have one, and occlude each feature.
5. Write `local_reason.md` with the row id and the ordered deltas.
6. Assert that occluding a feature and then restoring it returns the original probability within a tight tolerance.

#### Tech stack

- Python 3.11 or newer
- Your own stump code from Day 13, simplified to depth 1
- No XGBoost requirement

#### Setup

1. Create `boosted-stumps/` and reuse the CSV.
2. Implement `boost.py` and `occlude.py`.
3. Run the fit. If it never beats the linear model, record that. A loss is an acceptable outcome if the scoreboard is honest.
4. Run tests, including the restore-after-occlusion check.

#### Deliverable

- The scoreboard lists three test log losses: majority, linear, boosted.
- Early stopping uses validation riders, never test riders.
- The local reason names a feature, a median, and a probability delta.
- A test shows occlusion is side-effect free on the row.

### Day 15 — Precision Where It Matters

**Level:** Beginner

**Folder:** [atlas/02-learning-machines/day-15-precision-at-the-point/README.md](atlas/02-learning-machines/day-15-precision-at-the-point/README.md)

Rank predictions and read precision and recall at the alert rate operations can actually handle.

#### Concept

An overrun model that flags every other rental will be switched off by the dock crew in a week. The operating point is a workload decision: how many alerts can a shift review? Accuracy at 0.5 is unrelated to that question, especially at a 10 percent base rate. This project sorts the test set by predicted probability and walks down the list, computing precision and recall after each alert. You will mark the point where the alert count matches a budget you set, such as twenty alerts per hundred rentals, and you will report precision there. You will also draw the curve as a CSV of (recall, precision) so you can plot it anywhere. A second curve on the training set will look better. You will put them side by side and refuse to quote the training curve in the baseline card.

#### Approach

Use the boosted model's probabilities if you have them, or the linear model's if you do not. The day is about the curve, not about refitting. Implement `precision_recall_curve(labels, scores)` by sorting scores descending and accumulating true positives. Add a synthetic tie: two rows with the same score must not change the curve depending on input order. Break ties by row id so the walk is deterministic. Choose the budget in `budget.txt` before you look at the test curve. If you choose it after, you are fitting the operating point to the test set. Write both the predeclared budget precision and, separately, the best precision anywhere on the curve, labeled as exploratory.

#### Components

| Piece | Role |
| --- | --- |
| Ranked list | Test rows sorted by score with a deterministic tie break. |
| Curve table | Precision and recall after each additional alert. |
| Budget marker | A predeclared alert rate and the precision at that rate. |
| Train contrast | The same curve on train, stored so you do not quote it by mistake. |

#### How it works

1. Write `budget.txt` with the alert rate and one sentence of operational reason.
2. Load labels and scores for test and for train.
3. Build both curves.
4. Read precision at the budget on the test curve.
5. Confirm a tie fixture produces the same curve under reversed input order.
6. Update the baseline card with the budgeted precision, not with accuracy.

#### Tech stack

- Python 3.11 or newer
- Standard library `csv`
- Scores from your Day 12 or Day 14 model

#### Setup

1. Create `pr-curve/` with `curve.py` and a small tied fixture in tests.
2. Run it on the real scores and write `out/test_curve.csv` and `out/train_curve.csv`.
3. Add the budgeted number to `baseline_card.md` or a local copy of it.
4. Run tests.

#### Deliverable

- The budget was written down before the test precision was computed, and the file's timestamp or your notes say so. If you slipped, change the budget file's reason, not the number, and recompute honestly.
- Ties do not depend on input order in the test.
- Train and test curves are separate files.
- The number you would tell operations is precision at the budget, and the notes say the denominator.

### Day 16 — Clusters with Names

**Level:** Intermediate

**Folder:** [atlas/02-learning-machines/day-16-clusters-with-names/README.md](atlas/02-learning-machines/day-16-clusters-with-names/README.md)

Cluster docks from usage features and name each cluster from examples, or refuse to name it.

#### Concept

Someone will ask what kinds of docks Harbor Loop operates. A clustering algorithm will always return groups. Names are the part you are responsible for. This project builds a dock-level table: median start hour, share of rainy rentals, median duration, and overrun rate. It runs k-means with k chosen from a small range using inertia, then tries to name each cluster from the five member docks closest to the center. A name is allowed only if you can write a sentence a teammate could falsify, such as "evening commute, indoor, short bookings." If the members do not support a sentence, the cluster is called `unlabeled-3` and the notes say what you would need to see. You will also refit with a different seed and report which docks changed cluster. Stability is part of the name. An unstable group does not deserve a product label.

#### Approach

Standardize dock features with the mean and variance of the dock table you are clustering. That is descriptive, not a train-test model, and you should say so. Implement k-means with a fixed number of iterations and two seeds. Pick k by plotting inertia for k from 2 to 6 and choosing the smallest k after which the drop flattens; write the rule you used in a sentence so "elbow" is not a vibe. For each cluster, list the five nearest docks and their raw feature values, not just the standardized ones, because names should be in real units. The seed comparison reports the fraction of docks whose cluster assignment changed, after matching clusters by center proximity so label switching is not counted as change.

#### Components

| Piece | Role |
| --- | --- |
| Dock table | One row per dock, aggregated from rentals. |
| k-means | Your implementation, two seeds, inertia for several k. |
| Naming sheet | Nearest members in raw units and a falsifiable sentence or an explicit refusal. |
| Stability note | Share of docks that move after a seed change, with centers matched. |

#### How it works

1. Aggregate rentals to docks. Docks with very few rentals go to an exclusion list, not into a cluster you then name.
2. Standardize and run k-means for k from 2 to 6.
3. Choose k and write the rule.
4. Name or refuse each cluster using nearest members.
5. Refit with a second seed, match centers, and compute the move rate.
6. Test one iteration of k-means on a toy set of points you can solve by eye.

#### Tech stack

- Python 3.11 or newer
- Standard library only
- A naming sheet in markdown

#### Setup

1. Create `clusters/` with `aggregate.py`, `kmeans.py`, and `name.md`.
2. If you are still on the synthetic generator, give docks three distinct usage patterns so a failure to separate them is informative.
3. Run both seeds and fill in `name.md`.
4. Run the toy-set test.

#### Deliverable

- Every cluster is either named with a falsifiable sentence or explicitly unlabeled.
- Excluded low-count docks are listed and are not given a name.
- The move rate between seeds is a number in the notes.
- The toy test fails if assignments on the obvious two-blob set are wrong.

### Day 17 — A Ranker from Pairs

**Level:** Intermediate

**Folder:** [atlas/02-learning-machines/day-17-pairs-ranker/README.md](atlas/02-learning-machines/day-17-pairs-ranker/README.md)

Learn to order docks for a rider from pairwise preferences, and evaluate with a rank metric.

#### Concept

Classification says whether a rental overran. Ranking says which dock a rider should be offered first. Harbor Loop can log a weak preference: when a rider is shown two docks and completes a rental at one of them, that dock won the pair. This project builds pairs from synthetic choice logs, fits a linear scoring function so that the winner's score exceeds the loser's, and evaluates with top-1 accuracy on held-out riders. You will use a pairwise hinge: the loss is zero when the score gap clears a margin, and linear otherwise. A constant model that always prefers the globally popular dock is the baseline. If your ranker cannot beat popularity on riders it has not seen, the features are not doing work. Do not report a classification accuracy on pairs as if it were the product metric. The product shows a list.

#### Approach

Each candidate dock has features you already understand: distance bucket, indoor flag, historical overrun rate computed with a cutoff so the pair's own outcome is not inside the feature. That cutoff matters. Compute dock history from events before the choice time. Train with stochastic updates over pairs, seeded shuffle, fixed step size. Evaluate on riders held out entirely. Top-1 means the dock with the highest score is the one the rider completed, among the docks that were actually shown. Include a popularity baseline that ranks by prior completion count, also cutoff-safe. Write both numbers.

#### Components

| Piece | Role |
| --- | --- |
| Choice log | Shown docks, chosen dock, timestamp, rider id. |
| Cutoff features | Dock history strictly before the choice. |
| Pairwise hinge | A linear score with a margin. |
| Top-1 versus popularity | Held-out riders, both methods. |

#### How it works

1. Generate choices with a seeded rule and a little noise.
2. Build features with a strict time cutoff and test that the choice itself is absent from the history count.
3. Fit the linear ranker on training riders' pairs.
4. Score held-out riders' lists and compute top-1.
5. Score the popularity baseline the same way.
6. Write `rank_card.md`. If the ranker loses, keep the card anyway.

#### Tech stack

- Python 3.11 or newer
- Standard library only
- Held-out riders as the evaluation unit

#### Setup

1. Create `ranker/` with `choices.py`, `train_rank.py`, and tests.
2. Run generation and training.
3. Add a test that a feature builder raises or drops the current choice if someone includes it.
4. Run the tests.

#### Deliverable

- Top-1 for the ranker and for popularity are both on the card, on held-out riders.
- A test rejects features that include the choice being scored.
- The hinge margin is a named constant.
- You can explain why pair accuracy would have flattered a model that only learns to pick the popular dock inside a pair of unequals.

### Day 18 — Locked Training Runs

**Level:** Intermediate

**Folder:** [atlas/02-learning-machines/day-18-locked-training-runs/README.md](atlas/02-learning-machines/day-18-locked-training-runs/README.md)

Make a training run reproducible: seed, data hash, config file, and a model card stub.

#### Concept

A score you cannot rerun is a rumor. This project wraps the linear model or the stumps in a single command that reads a config file, hashes the training CSV, records the seed, writes predictions, and writes a model card stub. The card is short on purpose: data hash, row counts, split rule, metric name, test number, and a list of things the model must not be used for. You will run the command twice and show that predictions match. Then you will change one config field, the learning rate or the stump cap, and show that the card's config section changed while the data hash did not. The failure you are catching is a notebook that was edited after the number was copied into a slide. The card lives next to the predictions, not in a wiki page you update later.

#### Approach

Put hyperparameters only in `config.json`. The training script refuses to run if required keys are missing. Hash the training file bytes with SHA-256. Write `artifacts/<utc-stamp>/` containing `config.json`, `card.md`, `predictions.csv`, and `metrics.json`. Use a stamp you pass in, or a frozen stamp in tests, so tests do not depend on the clock. The reproduce check diffs predictions from two runs with the same config and stamp. Do not pickle a model unless you also store enough to recompute predictions from source. Source plus config plus data hash is the real artifact. A pickle without those is how runs go missing.

#### Components

| Piece | Role |
| --- | --- |
| Config file | The only place hyperparameters are set. |
| Data hash | SHA-256 of the training file bytes. |
| Artifact directory | Config, card, predictions, and metrics written together. |
| Reproduce check | Byte-level or value-level match of two runs. |

#### How it works

1. Copy the chosen model into a function `train(config, csv_path, out_dir)`.
2. Hash the CSV and store the hash in `metrics.json` and in the card.
3. Run twice into two directories with the same stamp argument if needed, or overwrite a fixed out dir sequentially and copy outputs.
4. Diff predictions.
5. Change one hyperparameter, rerun, and show the hash stayed put and the metric changed or the notes say it did not.
6. Fill the must-not-use list with two concrete prohibitions, such as pricing or disciplinary decisions.

#### Tech stack

- Python 3.11 or newer
- Standard library `hashlib`, `json`, `pathlib`
- Your earlier model code, imported or copied with attribution in a comment

#### Setup

1. Create `locked-runs/` with `config.json`, `train.py`, and `tests/test_repro.py`.
2. Run the script twice.
3. Run the tests, which should call `train` in a temporary directory.
4. Read the card and delete any sentence you could not defend from `metrics.json`.

#### Deliverable

- Two runs with the same inputs write the same predictions.
- The card's data hash matches `hashlib` of the file on disk.
- A missing config key fails the run before training starts.
- The must-not-use list has two specific items, not a generic disclaimer.

### Day 19 — Slice the Errors

**Level:** Intermediate

**Folder:** [atlas/02-learning-machines/day-19-slice-the-errors/README.md](atlas/02-learning-machines/day-19-slice-the-errors/README.md)

Break test error down by a feature you did not train on as a target, and write what you would do next.

#### Concept

Average log loss can look fine while rainy outdoor docks are where the model is lost. This project slices the test set by a column, reports support and log loss per slice, and requires a minimum support before you are allowed to call a slice worse. You will predeclare the slices from the product, not from fishing: weather code, dock type, and a tenure band. Fishing is allowed only in a separate section labeled exploratory, and those slices cannot be the ones you act on today. The action is a written choice: collect more labeled rows, add a feature, or refuse to deploy the model for a slice below the support floor. You are not running a fairness audit that swaps attributes and estimates causal gaps. You are doing the earlier, plainer thing: looking at the error you already have, by a group you can define from columns.

#### Approach

Use the locked run's test predictions so the scores are the ones the card refers to. Join them back to features by row id. For each predeclared slice, compute count, positive count, and mean log loss. A slice with fewer than thirty test rows is marked `thin` and is not ranked. Compare each eligible slice's loss to the overall test loss. Write `slice_report.md` with a table and a decision paragraph. Add one exploratory slice in a second table, and a sentence that says it did not drive the decision. A test builds a toy prediction file where one weather code has obviously worse loss and asserts the report names it, and asserts a tiny slice is marked thin.

#### Components

| Piece | Role |
| --- | --- |
| Joined test frame | Predictions plus the slicing columns and the label. |
| Slice table | Support, positives, and mean log loss. |
| Support floor | A constant that marks thin slices. |
| Decision paragraph | One next step tied to an eligible slice, or a refusal to deploy. |

#### How it works

1. Load predictions and features. Drop rows that fail the join rather than filling them.
2. Compute overall test log loss as the reference.
3. Compute the predeclared slices and apply the support floor.
4. Write the decision using only eligible slices.
5. Append the exploratory table underneath a heading that keeps it out of the decision.
6. Test the thin-slice rule and the obvious-bad-slice rule on toy data.

#### Tech stack

- Python 3.11 or newer
- Standard library `csv` and `math`
- Predictions from the locked run

#### Setup

1. Create `slices/` with `slice_report.py` and tests that do not need the full rental file.
2. Run the report on the real predictions.
3. If every eligible slice matches the overall loss, say so. Do not invent a gap.
4. Run tests.

#### Deliverable

- Thin slices are visible and are not the subject of the decision sentence.
- The decision names a slice key and a support count, or explicitly says no eligible slice is worse.
- Exploratory slices are in a separate table.
- A failed join drops the row and increments a counter you print.

### Day 20 — A Threshold from a Payoff Table

**Level:** Intermediate

**Folder:** [atlas/02-learning-machines/day-20-payoff-thresholds/README.md](atlas/02-learning-machines/day-20-payoff-thresholds/README.md)

Choose a classification threshold from costs you write down, then show how a different cost flips it.

#### Concept

Day 15 fixed a workload budget. Some decisions are better framed as costs. Suppose an overrun that is not staffed costs Harbor Loop a voucher, and a false alert costs a few minutes of crew time. Those are not the same unit until you write them in one currency. This project builds a two-by-two payoff table, sweeps thresholds on the test scores, and picks the threshold that minimizes expected cost on the test set. Then it does the dangerous version: picking the threshold on the test set is itself a use of the test set. You will split the old test riders in half, pick the threshold on the first half, and report cost on the second half. The second number is the one that goes on the card. You will also change one cost, rerun, and show the chosen threshold moving or not moving. A threshold that ignores the payoff is a default you have not earned.

#### Approach

Write costs in `payoff.json` as four numbers: true positive, false positive, true negative, false negative. Expected cost is the sum of count times cost, divided by the number of rows, so it stays comparable across folds. Sweep thresholds from the unique predicted scores rather than from a fixed grid, so you do not miss the points where the decision actually changes. Selection fold and report fold are rider-disjoint. Document that both folds were already used to train nothing; they are carved from the original test riders only. If your test set is too small to split, regenerate a larger one with the same rule and say so. Compare the payoff-chosen threshold to 0.5 on the report fold.

#### Components

| Piece | Role |
| --- | --- |
| Payoff file | Four costs in one currency, with a sentence defining the currency. |
| Threshold sweep | One row per distinct score, with counts and expected cost. |
| Selection fold | Where the threshold is chosen. |
| Report fold | Where the cost is quoted. |

#### How it works

1. Write `payoff.json` and the currency sentence before the sweep.
2. Carve the original test riders into selection and report.
3. Sweep on the selection fold and store the winning threshold.
4. Apply that threshold to the report fold and compute cost. Also compute cost at 0.5.
5. Edit one cost, repeat, and record whether the threshold changed.
6. Test the sweep on a four-row hand example whose best threshold you computed on paper.

#### Tech stack

- Python 3.11 or newer
- Standard library `json`
- Scores from the locked model

#### Setup

1. Create `payoff/` with `payoff.json`, `sweep.py`, and tests.
2. Run the sweep and write `out/threshold_card.md`.
3. Run the cost-edit as a second config, `payoff_alt.json`, not by overwriting the first result.
4. Run tests.

#### Deliverable

- The quoted cost uses the report fold, and the selection fold is a different set of riders.
- Cost at the chosen threshold and cost at 0.5 are both on the card.
- The alternate payoff is a separate file, and the note says whether the threshold moved.
- The hand example in the test matches your paper calculation.

<a id="phase-03"></a>

## Phase 03: Transformer Workbench

**Days 21–32.** 12 projects.

### Goal

Finish this phase able to walk from characters to a tiny trained transformer: tokenization, attention, position, a residual block, a loss curve you can resume, a decoder with a failure mode you can turn on, and a low-rank update that does not silently rewrite the base weights.

### Skills covered

- Byte-pair encoding and merge replay
- Skip-gram embeddings and neighbor inspection
- Scaled dot-product attention and masks
- Multi-head projections and output shapes
- Sinusoidal positions and a rotary-style dot product
- Pre-norm transformer blocks
- Next-character training to memorization
- Gradient clipping, checkpoints, and resume
- Greedy, temperature, and top-k decoding
- Frozen representations with a linear head
- Chat templates and stop-token identity
- Low-rank adaptation on one linear map

Build the pieces of a transformer until a tiny model overfits a text you wrote, then adapt it with a narrow low-rank update.

By the end of the phase you should be able to: Explain tokens, attention, training, decoding, and a small adaptation.

### Day 21 — Byte Pair Literacy

**Level:** Intermediate

**Folder:** [atlas/03-transformer-workbench/day-21-byte-pair-literacy/README.md](atlas/03-transformer-workbench/day-21-byte-pair-literacy/README.md)

Train a byte-pair vocabulary on a tiny corpus and show the merges that hide a word boundary.

#### Concept

Models do not read words. They read ids from a merge history, and the history was built to compress a corpus that may not look like your users. This project implements byte-pair encoding on a corpus you type yourself, a few kilobytes of Harbor Loop field notes are enough. You will start from characters, count adjacent pairs, merge the most frequent pair, and repeat until you hit a vocabulary budget. Then you will encode a sentence that was not in the corpus and list the tokens. The failure to catch is a merge that glues a space to a word so tightly that a rare station name shatters into noise while a boilerplate phrase becomes a single id. You will write that observation next to the actual token list. A tokenizer you have not watched merge is a dependency you cannot debug.

#### Approach

Represent the corpus as a list of symbol lists, starting with characters plus an end-of-word marker if you want word-aware merges. Either choice is fine if you document it. Each merge introduces a new symbol and rewrites every occurrence. Record the merge list in order. Encoding applies merges in that same order, not by a greedy longest-match shortcut you invent later, unless you also test that the shortcut matches the ordered application on a fixture. Add one string that includes a station name appearing once. Show its tokenization before and after the final merges. Keep the corpus free of text you do not have rights to use. Your own sentences are the dataset.

#### Components

| Piece | Role |
| --- | --- |
| Corpus file | Your own notes, a few kilobytes. |
| Merge trainer | Counts pairs and rewrites the corpus for each merge. |
| Merge list | Ordered rules you can replay. |
| Encode report | A held-out sentence and its token ids, plus the rare-name example. |

#### How it works

1. Write `corpus.txt` and `heldout.txt`.
2. Train until the vocabulary reaches a budget you set, such as 80 tokens above the character set.
3. Save `merges.json` in order.
4. Encode the held-out text by replaying merges.
5. Encode the rare station name at an early step and at the final step and paste both into `notes.md`.
6. Test that encoding then decoding through the merge rules returns the original character string.

#### Tech stack

- Python 3.11 or newer
- Standard library `json` and `collections`
- A corpus you wrote

#### Setup

1. Create `bpe/` with `bpe.py`, `corpus.txt`, and tests.
2. Run training and encoding.
3. Add a test with a five-word corpus where you can hand-check the first merge.
4. Run the tests.

#### Deliverable

- Decoding the encoding returns the original text on the corpus and on the held-out line.
- The first merge in the hand-checked fixture is the pair you counted by hand.
- `notes.md` shows the rare name under two vocabulary sizes.
- The merge list is ordered and is the only artifact the encoder needs besides the character inventory.

### Day 22 — Neighborhoods in Embedding Space

**Level:** Intermediate

**Folder:** [atlas/03-transformer-workbench/day-22-embedding-neighborhoods/README.md](atlas/03-transformer-workbench/day-22-embedding-neighborhoods/README.md)

Train skip-gram embeddings on your notes and inspect neighbors, including a pair that should not be close.

#### Concept

An embedding is a point you learned from co-occurrence, not a definition. Two station names that share a sentence template will sit near each other even when a rider would never confuse the docks. This project trains a small skip-gram model on the tokenized notes from Day 21, or on whitespace tokens if you want a shorter path. You will look up nearest neighbors for a handful of tokens and write down one neighborhood that is useful and one that is a trap. You will also check a crude analogy, of the kind people demo on stage, and record whether the arithmetic returns anything you would show a teammate. The point of the failed analogy is the point of the day. Geometry that only works in a keynote is not a feature you should describe as understanding.

#### Approach

Use a tiny vocabulary, under a few hundred tokens, and vectors of size 16 or 32 so training finishes on a laptop in a short run. Negative sampling can be three draws from the unigram distribution raised to the three-quarter power, which you should implement because it changes what "common word" means. Train for a fixed number of steps with a seed. Nearest neighbors use cosine similarity. Exclude the query token itself. Write `neighbors.md` with five queries. For the analogy, implement `king - man + woman` style arithmetic on tokens you actually have, such as a pair of docks and a pair of time words, and state the top three results. If your corpus is too small for any analogy to be meaningful, say that and do not borrow a pretrained vector file to make the demo prettier.

#### Components

| Piece | Role |
| --- | --- |
| Skip-gram trainer | Center and context pairs with negative samples. |
| Cosine lookup | Top neighbors for a query token. |
| Neighbor notes | One useful neighborhood and one trap, with the query named. |
| Analogy probe | Vector arithmetic and the top three tokens, or an explicit refusal. |

#### How it works

1. Build pairs from a window of size 2 on either side of each center.
2. Train and save vectors as a JSON map of token to list of floats.
3. Query five tokens and write the notes.
4. Run one analogy using tokens that occur at least five times. If you cannot find such a pair, document the frequency table instead of forcing it.
5. Test cosine of a vector with itself is 1 within tolerance, and that a reversed vector is not the nearest neighbor of the original unless the vocabulary is pathological.

#### Tech stack

- Python 3.11 or newer
- Standard library `math` and `random`
- Vectors stored as JSON so you can diff them

#### Setup

1. Create `embeddings/` with `skipgram.py` and the corpus.
2. Run training. Log the loss every few hundred steps to see that it moves.
3. Write `neighbors.md` from the actual output, not from memory.
4. Run tests.

#### Deliverable

- Five queries have neighbors computed from your vectors.
- The trap neighborhood is a real pair from the output, with a sentence on why closeness is misleading.
- The analogy section either shows top three tokens or explains that the corpus cannot support the probe.
- A self-cosine test passes.

### Day 23 — One Attention Head, On Paper

**Level:** Intermediate

**Folder:** [atlas/03-transformer-workbench/day-23-one-attention-head/README.md](atlas/03-transformer-workbench/day-23-one-attention-head/README.md)

Implement scaled dot-product attention for one head and check a hand-computed 2 by 2 case.

#### Concept

Attention is a weighted average of values, with weights coming from queries and keys. The sentence is short and the bugs are ordinary: forgetting the scale, applying the mask after the softmax, or letting a padded position vote. This project implements single-head scaled dot-product attention in NumPy or in pure Python if you want to avoid the dependency. You will first compute a 2 by 2 example by hand, including the scale by square root of the key dimension, and lock it in a test. Then you will run a short sequence of token vectors you choose and print the weight matrix. A causal mask will zero the future, and a padding mask will zero a pad position in both directions that matter: it should not attend, and others should not attend to it. You will write the mask rule in one sentence above the code.

#### Approach

Represent a batch of one so the shapes stay visible: query, key, and value are lists of vectors or a 2-D array of shape (time, dim). Scores are query times key transpose, divided by sqrt(dim). Masked positions are set to a large negative number before softmax, not to zero after. Softmax is numerically stable: subtract the max. The output is the weighted sum of values. The hand example uses dim 2 and two positions so you can show the arithmetic in `hand.md`. Do not import a transformer library for this day. If you use NumPy, pin the version in a requirements file that contains only that dependency.

#### Components

| Piece | Role |
| --- | --- |
| Score function | Dot products scaled by sqrt(dim). |
| Mask | Causal and pad positions set to a large negative before softmax. |
| Stable softmax | Subtract the max, then exponentiate. |
| Hand example | A 2 by 2 case with the arithmetic written out. |

#### How it works

1. Write the 2 by 2 example on paper and then in `hand.md`.
2. Implement attention and assert it matches the hand example within 1e-5.
3. Build a length-4 sequence and print causal weights. Later positions may attend backward. Earlier positions must put zero mass on the future, within tolerance.
4. Mark the last position as pad and assert its incoming and outgoing attention mass is zero after masking.
5. Assert the rows of a fully valid causal mask still sum to 1.

#### Tech stack

- Python 3.11 or newer
- NumPy, pinned, or pure Python lists if you prefer
- No transformer framework

#### Setup

1. Create `attention-head/` with a virtual environment and `requirements.txt` if you use NumPy.
2. Implement `attention.py` and `tests/test_hand.py`.
3. Run the tests and print one weight matrix into `weights.md`.
4. If a row does not sum to 1, fix the mask order before you add more features.

#### Deliverable

- The hand example matches the code.
- Causal weights put no mass on future positions.
- A pad position does not receive or send mass.
- The mask sentence above the function matches the behavior the tests lock.

### Day 24 — Heads that Disagree

**Level:** Intermediate

**Folder:** [atlas/03-transformer-workbench/day-24-heads-that-disagree/README.md](atlas/03-transformer-workbench/day-24-heads-that-disagree/README.md)

Run two attention heads on one sentence and show that their weight patterns are not copies.

#### Concept

Multi-head attention is often described as "looking at different things," and then implemented as a reshape nobody inspects. This project builds two heads with separate projections on a single sentence you embed with a fixed, seeded random projection from token ids. You will print both weight matrices and write what each head concentrates on. If they match, you have not failed the day, but you must change the initialization or the sentence until you can say whether the heads are redundant. You will also implement the output projection that concatenates head outputs and maps them back to the model dimension, and check the shape on a sequence. The lesson is the contrast between heads and the shape contract, not a claim that heads have human-readable jobs in a large model. In a tiny random model they mostly do not. Say that plainly if the patterns are noise.

#### Approach

Use model dimension 8 and two heads of dimension 4, so concatenation returns to 8 before a square output projection. Initialize projections with a seeded normal and a scale you write down. Share the same token vectors across heads. After computing both weight matrices, measure their mean absolute difference. A difference near zero means the heads collapsed. You may reseed once and record both seeds. Do not train today. This is a shape and interpretation exercise. The output projection is a matrix multiply you test with a known input so a reshape bug cannot hide behind attention weights that happen to look plausible.

#### Components

| Piece | Role |
| --- | --- |
| Token vectors | Seeded random projection from a short sentence. |
| Two heads | Independent Q, K, V projections. |
| Disagreement note | Mean absolute difference of the two weight matrices and a sentence of interpretation. |
| Output projection | Concatenation checked by shape and by a known multiply. |

#### How it works

1. Tokenize a sentence of at least six tokens with your Day 21 encoder or with whitespace plus a tiny vocab.
2. Project tokens and run both heads with a causal mask.
3. Write both matrices and the mean absolute difference.
4. Concatenate outputs and apply the output projection. Assert the shape equals (time, model dim).
5. Test the projection math on a 1 by 8 vector you multiply by hand.

#### Tech stack

- Python 3.11 or newer
- The attention function from Day 23
- NumPy or pure Python, consistent with Day 23

#### Setup

1. Create `multi-head/` and import or copy `attention.py`.
2. Run `python3 heads.py` and fill `heads.md` from the printout.
3. Run tests for shape and for the known multiply.
4. If the heads match to many decimals, record the seed and try one more. Keep both notes.

#### Deliverable

- Both weight matrices are in the notes, with the mask visible in the upper triangle.
- The mean absolute difference is a number, not an adjective.
- The output shape test passes.
- The notes say whether you believe the heads specialized, and the evidence is the matrices, not a diagram from a blog.

### Day 25 — Where Position Lives

**Level:** Intermediate

**Folder:** [atlas/03-transformer-workbench/day-25-where-position-lives/README.md](atlas/03-transformer-workbench/day-25-where-position-lives/README.md)

Add sinusoidal positions and a rotary-style pairing, and show a model with neither cannot tell order.

#### Concept

A bag of token vectors is invariant to order. "Bike at dock" and "dock at bike" become the same multiset, and attention without positions cannot prefer one reading. This project demonstrates that collapse, then adds two positional mechanisms on a toy sequence. Sinusoidal positions are added to the token vectors. A rotary-style pairing rotates adjacent pairs of dimensions by an angle that depends on the index, which you implement for a single query-key dot product so the relative offset appears in the score. You are not reimplementing a production RoPE kernel. You are showing, on a sequence of length four and dimension four, that a shift in position changes the score in the rotary version and that the no-position version is unchanged by a swap you construct. Write the swap explicitly.

#### Approach

Build two token sequences that are permutations of each other. Run attention with no positions and show identical outputs up to the permutation of positions, or identical pooled outputs if you mean-pool. Then add sinusoidal vectors from the original formula, with a base you set to 10000, and show the pooled outputs differ. For the rotary demo, take one query and one key, both in R4, rotate the pairs by index times a frequency, and compute the dot product at offsets 0, 1, and 2. Put the three scores in `positions.md`. A test locks the sinusoidal vector at position 0, which should be a specific pattern of zeros and ones you derive.

#### Components

| Piece | Role |
| --- | --- |
| Order-swap fixture | Two sequences with the same tokens in different order. |
| No-position attention | The collapse you are trying to expose. |
| Sinusoidal add | Position vectors added before attention. |
| Rotary dot-product demo | Scores at three relative offsets for one pair. |

#### How it works

1. Compute the no-position outputs on the swapped sequences and record the comparison you promised.
2. Add sinusoidal positions and repeat the comparison.
3. Derive the position-0 sinusoid and lock it in a test.
4. Compute the three rotary scores and write them down.
5. State in one sentence which mechanism you would reach for first in a tiny character model and why. Either answer is acceptable if the sentence cites your numbers.

#### Tech stack

- Python 3.11 or newer
- Standard library `math`, plus NumPy if you already use it
- No pretrained model

#### Setup

1. Create `positions/` with `positions.py` and tests.
2. Run the swap experiment and write `positions.md`.
3. Run tests, including the position-0 sinusoid.
4. Keep the sequence length at 4 so the matrices stay printable.

#### Deliverable

- The no-position case shows the order invariance you claimed, on the fixture.
- The sinusoidal case breaks that invariance on the same fixture.
- Position 0 matches the hand derivation.
- Three rotary scores are recorded.

### Day 26 — A Block, Shape by Shape

**Level:** Intermediate

**Folder:** [atlas/03-transformer-workbench/day-26-block-shapes/README.md](atlas/03-transformer-workbench/day-26-block-shapes/README.md)

Stack attention, residual, layer norm, and a position-wise MLP, and assert every shape.

#### Concept

A transformer block is a shape contract with a few nonlinearities. Most implementation bugs are dimension mistakes that still run because a multiply happened to align. This project builds one pre-norm block: layer norm, attention, residual add, layer norm, MLP, residual add. You will assert shapes after every step on a tensor of (batch, time, dim). You will also check a residual property: if the attention and MLP outputs are zero, the block output equals the input, within tolerance. That property catches a residual that was replaced instead of added. Use two layers only if the single block already passes. Depth is not the lesson. The lesson is being able to point at each arrow in the block and name the tensor shape.

#### Approach

Layer norm is over the last dimension, with epsilon you set, and with learnable scale and shift initialized to one and zero. The MLP is two linear maps with a GELU or ReLU between them and a hidden size of 4 times dim. Initialize the last linear maps of attention and MLP to zero for the residual test, or pass a debug flag that zeroes those outputs. Do not train. A forward pass on random input with a seed should be deterministic. Write `shapes.md` as a list from input to output. Include the causal mask as an input to the block so a later day does not bolt it on from outside in a contradictory way.

#### Components

| Piece | Role |
| --- | --- |
| Layer norm | Last-dimension normalization with scale and shift. |
| Attention sublayer | Your multi-head function plus a residual. |
| MLP sublayer | Expand, nonlinearity, project, residual. |
| Shape log | A written list of shapes after each operation. |

#### How it works

1. Implement layer norm and test it on a vector whose mean becomes zero and variance becomes one when scale is one and shift is zero.
2. Wire the block and run a forward pass with batch 2, time 5, dim 8.
3. Record shapes.
4. Zero the sublayer outputs and assert the block returns the input.
5. Change dim to 7, an awkward number, and assert you either handle it or reject it with a clear error if heads do not divide the dimension.

#### Tech stack

- Python 3.11 or newer
- NumPy or pure Python
- Your attention and position code

#### Setup

1. Create `block/` with `block.py` and tests.
2. Run the forward pass and write `shapes.md` from the asserts you printed, not from a diagram you remember.
3. Run tests.
4. If you reject non-divisible head sizes, the error message must name the dimension and the head count.

#### Deliverable

- Every step in `shapes.md` matches an assert in the test.
- Zeroed sublayers reproduce the input.
- Layer norm matches the hand mean and variance check.
- Head-dimension mismatch is either supported or rejected with an explicit error.

### Day 27 — Overfit a Short Text on Purpose

**Level:** Intermediate

**Folder:** [atlas/03-transformer-workbench/day-27-overfit-a-text/README.md](atlas/03-transformer-workbench/day-27-overfit-a-text/README.md)

Train a character-level transformer until it memorizes a short text you wrote, and show the memorized continuation.

#### Concept

A model that cannot memorize one page is not ready for a conversation about generalization. This project trains a tiny causal transformer, character level so the tokenizer cannot take the credit, until training loss collapses on a text of a few hundred characters you write. You will sample a continuation from a prefix of that text and show that it reproduces the source. Then you will sample from a prefix that never appeared and show the garbage or the groove the model falls into. Both outputs go in the notes. Memorization is the success criterion today. If you stop early because the samples "look creative," you have skipped the evidence that the training loop, the mask, and the loss are wired together. Creativity is a later conversation, and it requires a model that can also overfit when you ask it to.

#### Approach

Use your block, two layers, model dim 32, two heads, context length covering the whole text so the task is not artificially hard. Optimize with a hand-written SGD or Adam update on one sequence, or on chunks if you prefer, but keep the full text in the training set. Teacher forcing: predict the next character at every position. Loss is mean cross-entropy. Train until the loss is near zero or until a step cap you set only after you have seen a curve that flattened. Sample with greedy decoding for the memorization check so randomness does not excuse a miss. The unseen prefix can be a single character that appears in the text but starts a different continuation than the one you request. Record both samples unedited.

#### Components

| Piece | Role |
| --- | --- |
| Character vocabulary | Every character in the text, plus a stop symbol if you need one. |
| Tiny causal model | Two blocks, trained with next-character loss. |
| Greedy memorization sample | A prefix from the text and the reproduced continuation. |
| Unseen-prefix sample | The same decoder on a prefix the text does not contain as a start. |

#### How it works

1. Write `text.txt`, a few hundred characters of original prose.
2. Train and log loss every few steps to `loss.csv`.
3. Greedy-sample from a 20-character prefix taken from the text and compare to the source continuation.
4. Greedy-sample from a prefix you invent and paste the raw output.
5. Assert the training loss decreased from the first logged step to the last on this run, and store the curve.

#### Tech stack

- Python 3.11 or newer
- NumPy, or PyTorch if you want autograd and you pin it
- A text you wrote

#### Setup

1. Create `memorize/` with `train.py` and `text.txt`.
2. If you switch to PyTorch, use it for autograd only and keep your block's structure visible in the module code.
3. Run training until memorization or until you hit a cap and the notes explain the miss.
4. Save `samples.md` with both outputs and the final loss.

#### Deliverable

- The in-text prefix continuation matches the source for a length you declare, or the notes show the exact mismatch and the loss.
- The unseen-prefix sample is pasted unedited.
- The loss curve file exists and ends lower than it starts, or you explain the failed run.
- The context length and depth are written at the top of the notes.

### Day 28 — A Loss Curve You Trust

**Level:** Intermediate

**Folder:** [atlas/03-transformer-workbench/day-28-a-loss-you-trust/README.md](atlas/03-transformer-workbench/day-28-a-loss-you-trust/README.md)

Instrument learning rate, gradient clipping, and checkpoints until a rerun overlays the same curve.

#### Concept

A falling loss is not evidence if you cannot rerun it. This project takes the memorization trainer and adds three pieces of discipline: a logged learning rate, gradient clipping with a threshold you choose, and a checkpoint that stores step, weights, and the RNG state you control. You will run training twice from a checkpoint saved halfway and show the remaining loss values match. You will also run once without clipping on a learning rate high enough to spike, save that curve, and keep it next to the clipped run. Deleting the spike is how people convince themselves training is stable. The spike is the artifact. The trusted curve is the one you can regenerate from the checkpoint and the config, not the one that looks smoothest.

#### Approach

Clip global gradient norm: if the norm exceeds the threshold, scale the gradient vector. Log the norm before clipping so you can see how often you hit the cap. Checkpoints are NumPy `.npz` or a JSON of lists if the model is tiny. Tests can use a toy parameter vector to verify clipping math without training a model. The resume test trains for 20 steps, saves, trains 20 more, and compares to a fresh run that loaded the checkpoint and trained 20. Match within a tight tolerance. Record the learning rate schedule even if it is constant. A constant you did not log is indistinguishable from a bug when you return next week.

#### Components

| Piece | Role |
| --- | --- |
| Grad-norm log | Norm before clipping, per step. |
| Clipper | Scales the gradient when the norm exceeds a threshold. |
| Checkpoint | Step, parameters, and any RNG state you own. |
| Resume comparison | A continued run versus a resumed run. |

#### How it works

1. Implement clipping and test it on a vector of known norm.
2. Train a short run that spikes without clipping. Save `curve_unclipped.csv`.
3. Train with clipping and checkpoint at the midpoint.
4. Resume and compare to an uninterrupted logged run, or to a second resume.
5. Write `trust.md` with the clip threshold, the spike step if any, and whether resume matched.

#### Tech stack

- Python 3.11 or newer
- The memorization trainer
- Standard library plus your numeric library

#### Setup

1. Create `trust-the-loss/` and copy the trainer forward.
2. Run the unclipped spike on a tiny config so it finishes quickly. A spike from a huge learning rate counts.
3. Run the clipped resume experiment.
4. Run the clip unit test.

#### Deliverable

- The clip unit test matches a hand-computed scaled vector.
- The unclipped curve is saved, spikes included.
- Resume matches the continued curve within the tolerance you set.
- `trust.md` names the threshold and the checkpoint step.

### Day 29 — Decoding and Its Failure Modes

**Level:** Intermediate

**Folder:** [atlas/03-transformer-workbench/day-29-decoding-failures/README.md](atlas/03-transformer-workbench/day-29-decoding-failures/README.md)

Compare greedy, temperature, and top-k decoding, and catch a repetition loop on purpose.

#### Concept

Decoding is part of the model a user experiences, and it is not the training loss. A memorized transformer will look fluent under greedy decoding on a known prefix and strange under a high temperature. This project adds three decoders to the tiny model: greedy, temperature-scaled softmax sampling, and top-k sampling. You will run each from the same prefix and the same seed where sampling applies. Then you will provoke a repetition loop, either by sampling from a half-trained checkpoint or by constructing a tiny distribution that puts mass on a cycle, and you will implement a repetition breaker you can explain: a ban on repeating the same token more than N times in a row, or a simple frequency penalty. The breaker is not a research claim. It is a switch you can turn off, with a sample on both sides.

#### Approach

Temperature divides the logits before softmax. Temperature 0 is not a limit you need to take; call the greedy function instead of pretending zero is a temperature. Top-k sets all but the k largest logits to a large negative number before softmax, and k is at least 1. Seeds apply to the sampler's RNG only. Save three samples from one prefix. For the loop, if your memorized model refuses to loop, use a hand-built logit sequence or a deliberately undertrained checkpoint and say which you used. The breaker must be a flag defaulting to off so the failure remains reproducible.

#### Components

| Piece | Role |
| --- | --- |
| Greedy decoder | Argmax at each step. |
| Temperature sampler | Logits divided by a temperature above zero. |
| Top-k sampler | Distribution truncated to k tokens. |
| Repetition breaker | A switch with samples before and after. |

#### How it works

1. Load the memorized checkpoint or train a small stand-in.
2. Decode the same prefix three ways and write `samples.md`.
3. Show a repetition failure with the breaker off.
4. Turn the breaker on and decode again from the same seed.
5. Test top-k on a known logit vector: tokens outside the top k receive probability zero.

#### Tech stack

- Python 3.11 or newer
- Your tiny transformer
- A seeded RNG for sampling

#### Setup

1. Create `decoding/` with `decode.py` and tests for top-k and for temperature-equals-greedy being a separate function.
2. Generate the three samples.
3. Generate the loop pair.
4. Run tests.

#### Deliverable

- Three decoders produce written samples from one prefix.
- Top-k assigns zero probability outside the selected set in the unit test.
- The repetition failure and the broken-loop sample are both present, with the flag value named.
- Temperature is never passed as zero.

### Day 30 — A Frozen Encoder and a Small Head

**Level:** Intermediate

**Folder:** [atlas/03-transformer-workbench/day-30-frozen-encoder-head/README.md](atlas/03-transformer-workbench/day-30-frozen-encoder-head/README.md)

Freeze a tiny encoder and train a linear head to classify your own labeled sentences.

#### Concept

Not every use of a transformer is next-token training. A common pattern freezes a representation and trains a small classifier, which is cheaper and easier to explain. This project builds a tiny bidirectional encoder — the same block with the causal mask removed — or reuses your causal model by taking the final hidden state. You will freeze those parameters. On top you will train a linear head to classify sentences you label into two classes you define, such as `maintenance` versus `billing`, twenty examples each, written by you. The baseline is a bag of character frequencies with its own linear head. If the transformer does not beat the bag on a held-out set of your sentences, the card says so. With this little data, the bag will often win. That result is welcome. It keeps the phase honest before you touch a pretrained model.

#### Approach

Split by sentence id, not by token. Train only the head: a check of parameter ids, or a numerical check that encoder weights are identical before and after, must pass. Use the same log-loss training loop you trust. Evaluate accuracy and, because the set is small, list every held-out sentence with its prediction and label in `errors.md`. Do not claim a general encoder. The write-up's last sentence should state how many held-out sentences you have, because a perfect score on four sentences is a conversation, not a result.

#### Components

| Piece | Role |
| --- | --- |
| Frozen encoder | Parameters unchanged by head training. |
| Linear head | A map from one vector to two logits. |
| Bag baseline | Character frequencies and its own linear head. |
| Held-out listing | Every test sentence, prediction, and label. |

#### How it works

1. Write forty labeled sentences and a split file.
2. Train the bag baseline and record held-out accuracy.
3. Train the head on frozen representations.
4. Assert encoder parameters did not change.
5. Write the held-out listing and a three-line comparison.

#### Tech stack

- Python 3.11 or newer
- Your block, with the mask configurable
- A labeled file you wrote

#### Setup

1. Create `frozen-head/` with `data.jsonl`, `train_head.py`, and tests.
2. Run both models.
3. Run the freeze test, which should fail if you forget to stop gradients or if you copy weights back incorrectly.
4. Keep the sentence count in the notes.

#### Deliverable

- Encoder weights match a checksum taken before training.
- The bag baseline number is next to the transformer number.
- Every held-out sentence is listed with prediction and label.
- The notes state the held-out count in the first paragraph.

### Day 31 — Chat Templates and Stop Sequences

**Level:** Intermediate

**Folder:** [atlas/03-transformer-workbench/day-31-chat-templates/README.md](atlas/03-transformer-workbench/day-31-chat-templates/README.md)

Render a chat transcript with special tokens and show a wrong stop sequence swallowing the answer.

#### Concept

A chat model does not see a dialogue. It sees a string rendered by a template: role markers, separators, and a place where generation starts. Get the template wrong and the model continues the user turn, or stops at the first period inside a legitimate answer. This project defines a small template for two roles, `user` and `assistant`, with explicit end markers. You will render a transcript, train or prompt your tiny model only if you want to, but the required work is the renderer and a stopper. The stopper halts when the end marker is produced and does not halt on a lookalike substring inside the message. You will include a fixture where the user's text contains the assistant's end marker as ordinary words, and show a naive string search stopping too early. Then you will show the token-id comparison, which does not.

#### Approach

Pick marker strings that cannot appear by accident only if you reserve them as special tokens. Add them to the vocabulary as atomic tokens, not as characters the merger can split. The renderer joins turns and ends with the assistant marker opened and not closed, which is the generation prefix. The stopper compares newly generated token ids to the end-marker id, not substrings of the decoded text. The negative fixture decodes a user turn that contains the marker characters as separate character tokens, and asserts generation would not stop there. Write `template.md` with one rendered transcript and the token id sequence underneath.

#### Components

| Piece | Role |
| --- | --- |
| Special-token vocabulary | Role markers as atomic ids. |
| Renderer | Turns become a prefix that opens the assistant role. |
| Id stopper | Stops only on the end-marker id. |
| Naive stopper | The substring bug, kept as a failing contrast. |

#### How it works

1. Define the markers and add them to the vocab.
2. Render a three-turn transcript and record ids.
3. Implement both stoppers.
4. Build the fixture where the user text contains the marker as ordinary characters.
5. Assert the id stopper does not fire on that fixture and the naive stopper does.

#### Tech stack

- Python 3.11 or newer
- Your tokenizer, extended with special tokens that bypass merges
- No hosted chat API

#### Setup

1. Create `chat-template/` with `template.py` and tests.
2. Render the sample transcript into `template.md`.
3. Run tests for both stoppers.
4. Document the generation prefix: which marker is open at the end of the string.

#### Deliverable

- The rendered transcript and its ids are in the notes.
- Special tokens are atomic: a test shows they are not split into characters.
- The naive stopper fails the hostile fixture and the id stopper passes it.
- The prefix for generation is described in one sentence.

### Day 32 — A Narrow Low-Rank Update

**Level:** Advanced

**Folder:** [atlas/03-transformer-workbench/day-32-narrow-lora/README.md](atlas/03-transformer-workbench/day-32-narrow-lora/README.md)

Adapt a tiny pretrained-by-you model with LoRA on one style task, and show a rank that is too small.

#### Concept

Full fine-tuning copies every weight for a task that may need a nudge. A low-rank update adds a pair of small matrices to a linear map and trains only those. This project takes the tiny model you already trained and adapts it so continuations prefer a house style you define, such as ending every completion with a fixed sign-off you invent. You will implement LoRA on one linear layer: the update is B times A, with A and B much narrower than the layer, scaled by a constant. Base weights stay frozen, and a checksum proves it. You will train at rank 1 and at a higher rank you choose, and you will report how often the sign-off appears in greedy samples from a shared prefix list. The base model without adaptation is the control. The day is successful when you can say what the low-rank update changed and what it did not, including a prefix the adaptation should leave alone.

#### Approach

Choose a single projection inside the MLP or the attention output. Initialize A with small random values and B at zero so the update starts at zero and the model behavior matches the base checkpoint at step 0. A test locks that. Train on a handful of style examples you write, in the chat template if you have it. Evaluate on ten prefixes: five that should gain the sign-off and five control prefixes where adding the sign-off would be a failure, such as a prefix that asks for a station code only. Report both rates at both ranks. Do not download a large instruction model. The mechanism is the same on the tiny net, and the failure modes are easier to see. If you later swap in an open model, keep this harness.

#### Components

| Piece | Role |
| --- | --- |
| LoRA pair | Low-rank A and B on one frozen linear map, scaled. |
| Zero-at-init test | B starts at zero, so outputs match the base model. |
| Style data | Short examples you wrote that demonstrate the sign-off. |
| Two-rate report | Sign-off rate and control-prefix false rate, at two ranks. |

#### How it works

1. Implement the wrapped linear layer and the zero-at-init test.
2. Checksum the base weights, train rank 1, and checksum again.
3. Sample the ten prefixes greedily.
4. Repeat at the higher rank from the same base checkpoint, not from the rank-1 weights.
5. Write `lora_report.md` with both rates and one sample that shows a miss.

#### Tech stack

- Python 3.11 or newer
- Your tiny transformer and checkpoint code
- No external LoRA library

#### Setup

1. Create `narrow-lora/` with `lora.py`, `style.jsonl`, and the prefix list.
2. Run both ranks.
3. Run the zero-init and freeze tests.
4. Keep the base checkpoint read-only.

#### Deliverable

- At step 0, LoRA outputs match the base model on a fixture batch.
- Base weight checksums match before and after training.
- The report includes both ranks and the control prefixes, not only the style successes.
- One miss is pasted unedited.

#### Step ahead

The follow-on is forgetting. After the style update, measure greedy continuation quality on the original memorization prefixes from Day 27. A rank that nails the sign-off and wrecks the original text has not adapted the model. It has replaced a behavior. Add a second task, a different sign-off, trained after the first, and report whether the first sign-off survives. If it does not, try a smaller learning rate or a higher rank and record which lever you moved. The design you want is one that names, before training, which old behavior is in scope to keep.

<a id="phase-04"></a>

## Phase 04: Retrieval Studio

**Days 33–48.** 16 projects.

### Goal

Finish this phase with a handbook index you can defend: chunks tied to source offsets, lexical and dense rankings, fusion, a quote-or-abstain answer, edition filters bound to a case file, and a recall number that does not move just because a favorite example worked.

### Skills covered

- Chunking with source offsets and gold questions
- Exhaustive dense search behind one embedder interface
- Metadata filters applied before scoring
- BM25 and identifier-preserving tokenization
- Reciprocal rank fusion
- Query rewriting that keeps the original string
- Bounded reranking of a shortlist
- Exact quotes and abstention
- Parent-child retrieval
- Edition binding from a case record
- Table chunks that keep headers with cells
- Multi-query pooling and dedupe
- One corrective retry without moving the threshold
- Versioned recall-at-k evaluation
- Context compression that reports deleted gold spans
- One-hop entity graphs with a distractor you disclose

Index a handbook you write, retrieve with lexical and dense methods, and answer only when a span in the index supports the sentence.

By the end of the phase you should be able to: Build a retrieval stack that cites, filters, and admits when the handbook does not say.

### Day 33 — Chunks that Respect Questions

**Level:** Intermediate

**Folder:** [atlas/04-retrieval-studio/day-33-chunks-and-questions/README.md](atlas/04-retrieval-studio/day-33-chunks-and-questions/README.md)

Split a staff handbook into chunks and show a question that breaks when the answer straddles a cut.

#### Concept

Retrieval fails before search exists if the chunk boundary cuts the only sentence that answers the question. This project writes a short Harbor Loop staff handbook as eight markdown files: hours, fees, weather closures, lost-bike procedure, and so on. You will split them with a fixed character window and an overlap, then write ten questions by hand whose answers you can point to. At least two questions must require a sentence pair that a naive window separates. You will record, for each question, the chunk ids a human says are necessary. That labeled file is the gold set for the rest of the phase. Do not generate the questions with a model and then grade the model against them. You wrote the handbook, and you should write the questions. The artifact is `chunks.jsonl` plus `questions.jsonl` with the character offsets of the supporting spans.

#### Approach

Chunk on character windows first, because the failure is easier to see than with a clever splitter. Record start and end offsets into the source file so a later citation can highlight the original text. Overlap by a fraction you declare, such as one fifth of the window. After you have seen a straddling question fail, add a second splitter that prefers markdown headings and paragraph breaks, and compare the gold chunk ids. Keep both chunk files. The heading splitter is not automatically better: a long section can still bury the answer. The comparison table is the deliverable, not a claim that semantic chunking is solved.

#### Components

| Piece | Role |
| --- | --- |
| Handbook | Eight markdown files you wrote. |
| Window chunker | Fixed size, overlap, source offsets. |
| Heading chunker | Splits on headings and paragraphs, with a max size. |
| Gold questions | Ten questions with the supporting offsets marked by you. |

#### How it works

1. Write the handbook. Include one answer that is a pair of sentences in different paragraphs.
2. Run both chunkers.
3. Write ten questions and mark supporting offsets against the source, not against a chunk you hope will match.
4. For each question, list the window chunks and the heading chunks that overlap the gold offsets.
5. Note the questions where the window chunker splits the gold span across two chunks and the heading chunker does not, or the reverse.

#### Tech stack

- Python 3.11 or newer
- Standard library `pathlib` and `json`
- Markdown handbook you authored

#### Setup

1. Create `chunking/` with `handbook/`, `chunk.py`, and `questions.jsonl`.
2. Run both chunkers into `out/window.jsonl` and `out/heading.jsonl`.
3. Add a test that every chunk's text equals the source slice for its offsets.
4. Keep questions free of answers that the handbook does not contain. Those have a later day.

#### Deliverable

- Offsets round-trip to the source text in a test.
- Ten questions have gold offsets.
- The comparison note names at least one straddling question.
- Both chunk files are kept, and neither is silently overwritten.

### Day 34 — Brute-Force Dense Search

**Level:** Intermediate

**Folder:** [atlas/04-retrieval-studio/day-34-brute-force-dense/README.md](atlas/04-retrieval-studio/day-34-brute-force-dense/README.md)

Embed chunks with a local bag-of-hashes or a small model and rank them by cosine, exhaustively.

#### Concept

Dense retrieval is a sort over similarities. An index is an optimization you add after the ranking is correct. This project embeds every chunk from Day 33 and answers a query by scoring all of them. You have two acceptable embedders. The first is a local hashing embedder: tokenize, hash each token into a fixed number of buckets, and L2-normalize the count vector. It needs no network and it is good enough to test the plumbing. The second is a small local model you already have access to, called from one function with the same output shape. The rest of the pipeline must not care which you used. You will run all ten gold questions, record the rank of the first chunk that overlaps a gold offset, and write the misses in full. A miss is a question whose gold chunk is not in the top five.

#### Approach

Put the embedder behind `embed(texts) -> list[list[float]]` with a dimension recorded in the output file. Cosine similarity on normalized vectors is a dot product, and a test should lock that equivalence on a random vector. Search is a loop, not an index library. Save `ranking.json` with query id, top five chunk ids, and the rank of the first gold hit or null. Do not tune the embedder against the ten questions repeatedly. You may look once, change a single preprocess setting such as lowercasing, and then stop. A second change belongs in the notes as an unrun idea. Otherwise the gold set becomes training data.

#### Components

| Piece | Role |
| --- | --- |
| Embedder interface | One function, hashing implementation required, model implementation optional. |
| Exhaustive scorer | Dot product against every chunk vector. |
| Gold rank | Rank of the first chunk that overlaps a gold span. |
| Miss list | Questions where the gold chunk is outside the top five. |

#### How it works

1. Embed all chunks and store vectors next to chunk ids.
2. Embed each question and rank chunks.
3. Compute gold rank using offset overlap, not string equality of the answer.
4. Write the miss list with the top chunk's text so you can see the near miss.
5. Test that normalized vectors have unit length and that brute-force search returns a known nearest neighbor on a toy set.

#### Tech stack

- Python 3.11 or newer
- Standard library hashing embedder
- Optional local embedding model behind the same function

#### Setup

1. Create `dense-search/` and copy the chunk and question files.
2. Implement `hashing_embed.py` and `search.py`.
3. Run the ten questions.
4. Run tests, including the toy nearest-neighbor case.

#### Deliverable

- Every question has a recorded gold rank or an explicit miss.
- The embedder id and dimension are in the output.
- You changed at most one preprocess setting after seeing results, and the notes name it.
- The toy nearest-neighbor test passes.

### Day 35 — An Index with Metadata

**Level:** Intermediate

**Folder:** [atlas/04-retrieval-studio/day-35-index-with-metadata/README.md](atlas/04-retrieval-studio/day-35-index-with-metadata/README.md)

Persist vectors and filter by handbook version and section before similarity is computed.

#### Concept

Brute force hides a product bug: the search space is almost never "every chunk we have ever stored." Harbor Loop's handbook has a version and a section. A question about fees in the 2026 edition must not return the 2024 fee table just because the wording is close. This project persists vectors in a simple on-disk layout — a JSON manifest and a binary or JSON vector file — and applies metadata filters before scoring. You will plant a stale chunk with nearly identical text and a different `edition` field, and show that an unfiltered query ranks it first while a filtered query cannot see it. The index rebuilds from the manifest without leftover ids from a deleted chunk. Deleting a chunk and still returning it is the bug the test is named after.

#### Approach

Each record has `chunk_id`, `edition`, `section`, `text`, `vector`, and `source` offsets. Filtering is a predicate over metadata, applied to candidate ids, and only then do you dot. Do not filter after you take top-k. A post-filter can return fewer hits than the user asked for and, worse, can drop the stale chunk only when you remembered to ask. The stale-chunk fixture uses the same words as a current fee chunk with one number changed. Rebuild is a pure function of the records directory: remove a file, rebuild, and assert the id is gone. You do not need a vector database server.

#### Components

| Piece | Role |
| --- | --- |
| Record manifest | Ids, metadata, and where the vector lives. |
| Pre-filter | Edition and section predicates applied before scoring. |
| Stale-edition fixture | A near-copy that must lose under the filter. |
| Rebuild | Index contents match the files on disk after a deletion. |

#### How it works

1. Write records for the current handbook plus one stale fee chunk.
2. Query fees with no filter and record the top id.
3. Query with `edition=2026` and assert the stale id is absent from the candidate set, not merely absent from a truncated display.
4. Delete a chunk file, rebuild, and assert its id does not return.
5. Test a filter that matches nothing: the result is empty, not an error and not a fall-through to all chunks.

#### Tech stack

- Python 3.11 or newer
- JSON or a single SQLite table you create yourself
- The Day 34 embedder

#### Setup

1. Create `filtered-index/` with `index.py` and fixtures.
2. Run the unfiltered and filtered queries.
3. Run the deletion test.
4. Document the candidate-count before and after the filter in `notes.md`.

#### Deliverable

- The stale chunk wins unfiltered and is invisible when the edition filter is on.
- An empty filter result does not fall back to the full corpus.
- A deleted chunk id is gone after rebuild.
- The notes show candidate counts before and after filtering.

### Day 36 — BM25 Beside Vectors

**Level:** Intermediate

**Folder:** [atlas/04-retrieval-studio/day-36-bm25-beside-vectors/README.md](atlas/04-retrieval-studio/day-36-bm25-beside-vectors/README.md)

Rank the same chunks with BM25 and show a query the hashing embedder misses and BM25 hits.

#### Concept

Dense scores smear rare strings. A rider asks about the exact fee code `HL-FEE-14`, which appears once in the handbook. A hashing embedder may bury that chunk under generic fee language. BM25, a lexical ranker with term frequency and document length, will not, if the tokenizer keeps the code intact. This project implements BM25 over the same chunks, with a tokenizer that does not throw away identifiers. You will run the gold questions through both rankers and write a disagreement table: questions where the top lexical chunk and the top dense chunk differ. At least one query in the set should be an exact code or a rare proper name you placed in the handbook. If your gold set has no such query, add one now and mark it as added after the first dense run so the history stays honest.

#### Approach

Implement the standard BM25 scoring formula with k1 and b as named constants. Compute inverse document frequency from the chunk collection you are searching, and keep that statistic with the index so a later chunk changes idf when you rebuild. Do not import a search engine. The point is the formula and the tokenizer. Tokenizer rules: lowercase, split on whitespace and punctuation, but keep tokens that contain digits. A test passes the fee code through as one token. Compare rankers by top-1 chunk id on each question and by gold rank.

#### Components

| Piece | Role |
| --- | --- |
| Tokenizer | Keeps codes with digits as single tokens. |
| BM25 scorer | Term frequency, document length, and idf, with named constants. |
| Disagreement table | Questions where lexical top-1 and dense top-1 differ. |
| Rare-token query | A fee code or proper name planted in the handbook. |

#### How it works

1. Tokenize chunks and build document frequencies.
2. Score the gold questions with BM25.
3. Load dense rankings from Day 34 or recompute them with the hashing embedder.
4. Write the disagreement table, including gold rank for both.
5. Assert the fee-code query's gold chunk is in the BM25 top three.

#### Tech stack

- Python 3.11 or newer
- Standard library only
- The same chunk files as the dense search

#### Setup

1. Create `bm25/` with `bm25.py` and tests.
2. Plant `HL-FEE-14` if the handbook does not already contain a rare code.
3. Run both rankers and write `disagreements.md`.
4. Run the tokenizer test on the fee code.

#### Deliverable

- BM25 constants are named and the formula is implemented in one function a test can call.
- The rare-token query hits its gold chunk in the BM25 top three.
- The disagreement table covers every gold question.
- A token with digits is not split into a bare number and letters.

### Day 37 — Reciprocal Rank Fusion

**Level:** Intermediate

**Folder:** [atlas/04-retrieval-studio/day-37-reciprocal-rank-fusion/README.md](atlas/04-retrieval-studio/day-37-reciprocal-rank-fusion/README.md)

Fuse lexical and dense rankings with reciprocal rank fusion you recompute by hand on a toy list.

#### Concept

Two rankers disagree, and a product has to return one list. Averaging cosine similarity with a BM25 score mixes units nobody can explain. Reciprocal rank fusion ignores the raw scores and sums one over a constant plus the rank. This project implements that fusion for the dense list and the BM25 list, with the constant k set to 60, and also shows a one-row hand example with k set to 1 so the arithmetic fits on a page. You will fuse the gold questions and compare fused gold rank to each individual ranker. Fusion is not required to win on every question. You will count how often it matches the better of the two and how often it matches the worse. That second count is the cost of fusion, and it belongs in the notes before you make fusion the default.

#### Approach

Ranks are 1-based. A chunk present in only one list contributes only that list's term. Do not invent a rank for a missing chunk. Sort the fused scores descending, and break ties by chunk id so the output is deterministic. The hand example uses three chunks and two lists of length two. Compute it in the test, not only in prose. On the real questions, write `fusion.md` with one line per question: dense gold rank, lexical gold rank, fused gold rank. Add a config flag to disable fusion so the earlier rankings remain reproducible.

#### Components

| Piece | Role |
| --- | --- |
| Rank normalizer | 1-based ranks, no raw-score mixing. |
| Fusion sum | Sum of 1/(k+rank) over lists that contain the chunk. |
| Hand example | Three chunks, k=1, asserted in a test. |
| Win/loss count | How often fusion matches the better ranker, and how often the worse. |

#### How it works

1. Implement fusion and the hand example test.
2. Fuse the saved rankings for each gold question.
3. Compute the three gold ranks.
4. Count better-matches and worse-matches. Ties between the source rankers are excluded from both counts and listed instead.
5. Write the notes, including a question where fusion hurt, if one exists.

#### Tech stack

- Python 3.11 or newer
- Standard library only
- Saved rankings from the lexical and dense days

#### Setup

1. Create `fusion/` with `rrf.py` and tests.
2. Run fusion on the gold set.
3. If you do not yet have saved rankings, recompute BM25 and the hashing embedder inside this folder and say so.
4. Run tests.

#### Deliverable

- The hand example matches the test exactly.
- Ties break by chunk id, and a test swaps input order to prove it.
- The notes include the better-match count and the worse-match count.
- A missing chunk is not assigned a fictional rank.

### Day 38 — Rewrite, Then Keep the Original

**Level:** Intermediate

**Folder:** [atlas/04-retrieval-studio/day-38-rewrite-keep-original/README.md](atlas/04-retrieval-studio/day-38-rewrite-keep-original/README.md)

Rewrite a vague question into a handbook query and search both, because the rewrite can drop the only specific token.

#### Concept

Users ask "what's the deal with rain," and a rewrite step turns that into "weather closure policy." Sometimes the rewrite helps. Sometimes the user said `HL-FEE-14` in a messy sentence and the rewrite, aiming for clean prose, drops the code. This project adds a query rewriter with two backends: a deterministic template rewriter you write for the handbook's known topics, and an optional model rewriter behind the same interface. Search runs on the original query and the rewritten query. You will log both strings. A fixture query contains a rare code plus vague wording. The template rewriter must preserve unknown alphanumeric codes. You will also show a hostile template that deletes tokens it does not recognize, and a test that fails that template. Keeping the original query in the fusion set is the mitigation you will measure, not a slogan.

#### Approach

The template rewriter maps a few keywords to handbook phrases and appends any token that matches a code pattern, rather than replacing the whole string. Search both queries with BM25, fuse the two lists with the Day 37 function, and compare gold rank to searching the original alone. The hostile rewriter is a one-liner that keeps only whitelisted words. It exists to make the failure mode obvious in a test. If you connect a model, it must be optional and the test suite must pass with the template only. Log a JSON line per question with `original`, `rewritten`, and both rankings' top ids.

#### Components

| Piece | Role |
| --- | --- |
| Template rewriter | Keyword expansion that preserves code-like tokens. |
| Hostile rewriter | A whitelist rewriter the test expects to drop the code. |
| Dual search | Original and rewrite, fused. |
| Query log | Both strings and the top ids, per question. |

#### How it works

1. Implement the template rewriter and the code-preserving rule.
2. Implement the hostile rewriter and test it against a sentence containing `HL-FEE-14`.
3. Run dual search on the gold questions plus the messy code question.
4. Compare fused dual-search gold rank to original-only gold rank.
5. Write `rewrites.md` with one case the rewrite improved and one it would have damaged if you had dropped the original.

#### Tech stack

- Python 3.11 or newer
- BM25 and fusion from earlier days
- Optional model rewriter behind a flag defaulting to off

#### Setup

1. Create `rewrite/` with `rewrite.py` and tests.
2. Run the messy code query with the template rewriter and with the hostile one.
3. Run the gold set with dual search.
4. Confirm tests pass with no network and no API key.

#### Deliverable

- The hostile rewriter drops the code, and the test asserts that drop.
- The template rewriter keeps the code, and the test asserts that keep.
- The log contains both query strings for every question.
- The notes include a case where dropping the original would have lost the gold chunk.

### Day 39 — Rerank the Shortlist

**Level:** Intermediate

**Folder:** [atlas/04-retrieval-studio/day-39-rerank-the-shortlist/README.md](atlas/04-retrieval-studio/day-39-rerank-the-shortlist/README.md)

Rerank the top twenty fused hits with a lexical overlap feature and show when the new order hurts.

#### Concept

The first retriever is tuned to recall. A second pass can look harder at fewer chunks. A cross-encoder is the usual choice, and it is also a dependency you may not have. This project defines a reranker interface and ships a local implementation: score each candidate by the fraction of query tokens that appear in the chunk, multiplied by a saturation on chunk length so a long chapter does not win by containing every word somewhere. You may add a model cross-encoder behind the same interface later. You will rerank the top twenty from fusion and compare gold rank before and after. Publish every question the reranker made worse. A reranker without a regression list is how a demo becomes the default and quietly drops the fee-code hit below a chatty paragraph.

#### Approach

The shortlist is exactly the fused top twenty, or fewer if the corpus is smaller. The reranker may not look outside that list. That constraint is the product: second-pass cost stays bounded, and a bug cannot "fix" recall by searching the rest of the corpus. Length saturation is a named function, such as token overlap divided by log of chunk length. Test it on two chunks with the same overlap count and different lengths. Write `rerank.md` with improved, unchanged, and regressed question ids. If you add a neural reranker, keep the lexical one as the offline default the tests use.

#### Components

| Piece | Role |
| --- | --- |
| Shortlist contract | Rerank only the fused top twenty. |
| Lexical reranker | Query-token overlap with a length saturation. |
| Regression list | Questions whose gold rank got worse. |
| Interface | A function signature a neural reranker could match later. |

#### How it works

1. Build fused top-twenty lists for each gold question.
2. Rerank with the lexical scorer.
3. Compute gold rank before and after.
4. Group question ids into improved, unchanged, and regressed.
5. Test that a longer chunk loses to a shorter chunk when overlap counts match.

#### Tech stack

- Python 3.11 or newer
- Fusion output from Day 37
- No required neural reranker

#### Setup

1. Create `rerank/` with `rerank.py` and tests.
2. Run the gold set.
3. Write the three groups into `rerank.md`.
4. Add a test that a candidate outside the shortlist cannot appear in the reranked output even if you pass it accidentally. The function should ignore or reject it. Pick one behavior and test it.

#### Deliverable

- The regression list is present, even if it is empty, and emptiness is explicit.
- The length-saturation test passes.
- The reranker does not introduce chunk ids that were not in the shortlist.
- The notes name the shortlist size.

### Day 40 — Quote or Abstain

**Level:** Intermediate

**Folder:** [atlas/04-retrieval-studio/day-40-quote-or-abstain/README.md](atlas/04-retrieval-studio/day-40-quote-or-abstain/README.md)

Answer with a quotation from a retrieved chunk, or refuse, when the handbook does not contain the fact.

#### Concept

A retrieval stack that always answers will invent a fee when the handbook is silent. This project draws a hard line. The answer is either a quotation copied from a retrieved chunk, plus the chunk id and offsets, or an abstention with a reason. Paraphrase is out of scope for the required path, because paraphrase makes grading mushy and makes fabrication easy. You will implement a local answerer that selects the highest-scoring sentence that covers the query tokens, and abstains when the coverage is below a threshold you set before looking at a new holdout. The holdout includes three questions whose answers are not in the handbook at all. Those must abstain. A question that quotes the wrong edition is also a failure even if the words are confident.

#### Approach

Split candidate chunks into sentences. Score a sentence by the fraction of query tokens it contains, excluding a tiny stoplist. The threshold lives in `threshold.txt` with a one-line justification written before you run the holdout. The gold questions from earlier days are the development set. The three unanswerable questions are the holdout, and you do not tune the threshold after seeing them. If you fail them, you report the miss and adjust in a follow-up run that you label as such. Output JSON has `status` of `quote` or `abstain`, and quotes must be exact substrings of the cited chunk. A test tampers with a quote character and expects rejection.

#### Components

| Piece | Role |
| --- | --- |
| Sentence splitter | Breaks a chunk without dropping the source offsets. |
| Coverage scorer | Query-token fraction with a stoplist. |
| Threshold file | A number justified before the holdout run. |
| Exact-quote check | The returned string is a substring of the cited chunk. |

#### How it works

1. Write the threshold and the justification.
2. Run the ten gold questions and record quotes or abstentions.
3. Freeze the threshold. Run the three unanswerable questions.
4. Reject any quote that is not an exact substring.
5. Write `answers.md` with the unanswerable outcomes called out.

#### Tech stack

- Python 3.11 or newer
- Retrieved shortlists from the previous day
- No required generative model

#### Setup

1. Create `quote-or-abstain/` with `answer.py`, `threshold.txt`, and the holdout file.
2. Run development questions, then holdout.
3. Add the tamper test.
4. If you optionally attach a generative model, it may only choose among sentences the retriever returned, and the exact-substring check still applies.

#### Deliverable

- Every quote passes the substring test against the cited chunk.
- The three unanswerable questions were not used to pick the threshold.
- Abstentions include a reason code, such as `low-coverage`.
- A tampered quote fails the test.

### Day 41 — Parents and Children

**Level:** Intermediate

**Folder:** [atlas/04-retrieval-studio/day-41-parents-and-children/README.md](atlas/04-retrieval-studio/day-41-parents-and-children/README.md)

Search small child chunks, then expand to the parent section before you quote.

#### Concept

Small chunks retrieve sharply and quote poorly, because the sentence that matched is missing its condition. Large chunks quote with context and retrieve poorly, because the vector or the BM25 score is diluted. This project stores both. Child chunks are the search units. Each child points at a parent, which is the heading section that contained it. Retrieval returns children. The quoter from Day 40 reads the parent text, while the citation still records the child id that won retrieval and the parent id that supplied context. You will construct one question where the child match is a pronoun or a short rule, and the condition lives in the previous paragraph inside the parent. Quoting only the child must be incomplete, and quoting from the parent must include the condition. That pair of quotes is the artifact.

#### Approach

Build the parent as the heading chunk from Day 33, and the children as smaller windows inside it, each storing `parent_id`. Search children with BM25. Expansion replaces the text handed to the quoter, not the id used for gold-rank calculations. Gold rank stays on the child, so you do not take credit for retrieving a giant section. Add a test that a child from edition 2024 does not expand to a parent from edition 2026 even if someone wires the ids wrong. Parent and child must share edition. Write `expansion.md` with the child-only quote and the parent quote for the pronoun question.

#### Components

| Piece | Role |
| --- | --- |
| Child records | Small searchable slices with a parent id and an edition. |
| Parent records | Heading sections keyed by id and edition. |
| Expansion step | Quoter sees parent text; gold rank stays on the child. |
| Edition guard | Refuses to expand across editions. |

#### How it works

1. Generate parents and children from the handbook.
2. Plant the pronoun question and mark the child offsets and the parent offsets separately.
3. Retrieve children and expand.
4. Run the quoter twice: once on child text, once on parent text.
5. Assert the cross-edition expansion is rejected.

#### Tech stack

- Python 3.11 or newer
- BM25 search on children
- The quote checker from Day 40

#### Setup

1. Create `parent-child/` with `build_hierarchy.py` and tests.
2. Write the pronoun example into the handbook if it is not there.
3. Run both quoters and save `expansion.md`.
4. Run the edition-guard test.

#### Deliverable

- The notes show a child quote that misses the condition and a parent quote that includes it.
- Gold rank is computed on child ids.
- Cross-edition expansion fails the test.
- Every child record has a parent that exists in the same edition.

### Day 42 — The Wrong Manual Version

**Level:** Intermediate

**Folder:** [atlas/04-retrieval-studio/day-42-wrong-manual-version/README.md](atlas/04-retrieval-studio/day-42-wrong-manual-version/README.md)

Bind a question to a handbook edition from the conversation, and block a newer chunk the user did not ask for.

#### Concept

Filters are useless if the caller forgets them. A support agent asks about "the fee" while the case file says the rider's membership started under the 2024 handbook. The 2026 fee is more prominent in the index because you rewrote that page last. This project models a small case context: `edition` is a field on the case, not a guess from the question text. Retrieval receives the case and must set the filter from it. You will try to regress: a code path that ignores the case and searches all editions. A test calls that path's function, if you are tempted to keep it, and asserts it is not what `answer_case` uses. The user-visible answer cites the edition. An answer that is numerically right for the wrong year is a wrong answer.

#### Approach

Represent a case as JSON with `case_id`, `edition`, and `question`. `answer_case` reads the edition only from the case. It does not parse years out of the question. Include a fixture where the question says "2026" but the case edition is 2024, and assert the filter follows the case. That fixture is the whole lesson: the utterance is not the system of record. Cite `edition` in the output next to the chunk id. Log the filter that was applied so a later review can see it without reading code.

#### Components

| Piece | Role |
| --- | --- |
| Case file | Edition as a field, separate from the question text. |
| Bound retriever | Filter comes from the case inside `answer_case`. |
| Hostile fixture | Question mentions a different year than the case. |
| Citation | Chunk id plus the edition that was actually searched. |

#### How it works

1. Write three cases, including the hostile year mismatch.
2. Implement `answer_case` and log the filter.
3. Assert the hostile case searches 2024.
4. Add a regression test that a helper named `search_all` is not called by `answer_case`. If you have no such helper, assert the candidate editions are a single value.
5. Write the three answers with their cited editions.

#### Tech stack

- Python 3.11 or newer
- The filtered index
- JSON case files

#### Setup

1. Create `edition-binding/` with `cases.jsonl` and `answer_case.py`.
2. Run the three cases.
3. Run tests.
4. In the notes, state which object is the system of record for edition.

#### Deliverable

- The hostile case cites 2024 and does not cite the 2026 fee chunk.
- The applied filter is in the log.
- A test locks the case field as the source of the filter.
- The notes name the system of record in one sentence.

### Day 43 — Numbers that Stay with Their Headers

**Level:** Intermediate

**Folder:** [atlas/04-retrieval-studio/day-43-numbers-and-headers/README.md](atlas/04-retrieval-studio/day-43-numbers-and-headers/README.md)

Chunk a fee table so a cell is never separated from the column header that gives it a unit.

#### Concept

A markdown table of fees becomes dangerous when a chunker cuts between a header and a cell. The retriever returns "14" and the quoter says fourteen dollars, or fourteen minutes, or fourteen days. This project adds a table-aware chunker. Each row chunk includes the header row text, the row label, and the cell, and it records the column name as metadata. You will plant a question — "what is the late fee for a cargo bike" — and show a naive window that can return the cargo-bike row without the header. The table-aware chunk must contain both the column name and the number. Quoting that chunk passes an assertion that the column name is present. This is structure-aware indexing, not a spreadsheet product.

#### Approach

Parse a simple GitHub-style markdown table yourself: header, separator, rows. Do not accept merged cells. Each data row produces one chunk per numeric cell, and the chunk text is a rendered sentence you control, such as "Late fee | cargo bike | 14 USD", built from the header and the row label. The original table is also stored so you can show it. The naive window chunker runs on the raw markdown for contrast. A test checks that every numeric chunk contains its column header string. A second test feeds a ragged row and expects a rejected table, not a shifted column.

#### Components

| Piece | Role |
| --- | --- |
| Table parser | Header plus rows, rejecting ragged lines. |
| Cell chunks | Header, row label, and value rendered together. |
| Naive contrast | A window chunk that can isolate the bare number. |
| Header assertion | Every numeric chunk contains the column name. |

#### How it works

1. Add `fees.md` with a real markdown table, including a cargo-bike late fee.
2. Parse it and emit cell chunks.
3. Run the naive window chunker on the same file.
4. Show one naive chunk that lacks the header, if the window produces one. Adjust the window on a copy of the file only for the demonstration, and label it as a constructed cut if you have to force it.
5. Query the late fee and assert the returned table chunk contains the column name and the row label.

#### Tech stack

- Python 3.11 or newer
- A small markdown table parser you write
- The existing quoter's substring check

#### Setup

1. Create `tables/` with `fees.md`, `table_chunks.py`, and tests.
2. Run both chunkers.
3. Run the ragged-row test.
4. Write `table_notes.md` with the naive chunk and the cell chunk side by side.

#### Deliverable

- A ragged table is rejected.
- Every numeric cell chunk includes its column header, and a test walks all of them.
- The cargo-bike question returns a chunk containing the row label and the column name.
- The notes show the contrast with a headerless fragment.

### Day 44 — Several Queries, One Pool

**Level:** Intermediate

**Folder:** [atlas/04-retrieval-studio/day-44-several-queries-one-pool/README.md](atlas/04-retrieval-studio/day-44-several-queries-one-pool/README.md)

Fan a question out to several lexical queries, pool the hits, and dedupe by chunk id before fusion.

#### Concept

One question can be several retrieval problems. "Can I leave a cargo bike out in the rain overnight, and what does it cost" needs the weather section and the fee table. A single BM25 string tends to pick one. This project splits a compound question into subqueries with a deterministic splitter: conjunctions and question marks you define, not a model. Each subquery searches. The pool is the union of hits, deduped by chunk id, keeping the best rank any subquery gave that id. You will compare gold coverage: the fraction of gold chunks hit by the single query versus the pool. On the compound question you wrote, coverage should go up. On a simple question, the pool should not pull in an unrelated second section just because the splitter was eager. Over-splitting is the failure mode you will fixture.

#### Approach

The splitter breaks on " and " only when both sides contain a question cue you list, so a station named "Grand and Pine" does not split. That station name is the over-split fixture if you naively split on every "and". Test it. Each subquery returns a top ten. Dedupe keeps the minimum rank. Gold coverage uses the set of gold chunk ids for questions that have more than one gold span. Write `pool.md` with coverage before and after for each compound question, and the station-name fixture result.

#### Components

| Piece | Role |
| --- | --- |
| Guarded splitter | Splits compounds without splitting names that contain 'and'. |
| Per-subquery search | BM25 top ten for each piece. |
| Dedupe | One row per chunk id, best rank kept. |
| Coverage comparison | Gold chunk recall of the single string versus the pool. |

#### How it works

1. Write two compound questions with two gold spans each.
2. Add a question or a chunk containing `Grand and Pine` and assert it does not split.
3. Search the full string and the pool.
4. Compute coverage.
5. Document a case where the splitter produced a subquery you wish it had not, if one appears. If none appears, say so.

#### Tech stack

- Python 3.11 or newer
- BM25
- Gold offsets from Day 33, extended

#### Setup

1. Create `multi-query/` with `split.py` and tests.
2. Run the compound questions.
3. Run the station-name test.
4. Keep the splitter rules in a short comment that matches the test names.

#### Deliverable

- `Grand and Pine` remains one query in the test.
- Coverage is reported for the compound questions against both strategies.
- Dedupe keeps a single id with the best rank, and a test constructs a duplicate across subqueries.
- The splitter is deterministic: same string in, same list out.

### Day 45 — A Second Search When the First Is Empty

**Level:** Advanced

**Folder:** [atlas/04-retrieval-studio/day-45-second-search/README.md](atlas/04-retrieval-studio/day-45-second-search/README.md)

If the first query abstains for low coverage, rewrite once and search again, with a hard stop at two passes.

#### Concept

Day 40 abstained when coverage was low. Some of those abstentions are retrieval misses, not missing facts. A second search with a different query can recover the span. It can also thrash: a loop that rewrites forever, or a second pass that lowers the threshold until something, anything, quotes. This project allows exactly one retry. The first pass searches the original question. If the quoter would abstain for low coverage, a rewriter produces one new query, the system searches again, and the quoter runs with the same threshold as the first pass. The threshold does not move. If the second pass also abstains, the system stops and returns the abstention, plus both queries. Three searches is a bug. You will fixture a question that succeeds only on the retry, and a question that must still abstain because the fact is absent.

#### Approach

The retry rewriter is deterministic and template-based, so the test does not need a model. For example, it appends the section name from a small keyword map. The attempt counter is an explicit integer in the response, and a test stubs the search function to count calls. A second retry path that catches a broad exception and tries again is forbidden; if you catch errors, they are not retrieval misses and they do not trigger rewrite. Log both queries even when the first pass succeeds, with the second marked `not-run`. The unanswerable holdout from Day 40 must still abstain, and its log must show two searches, not three.

#### Components

| Piece | Role |
| --- | --- |
| Attempt counter | An integer capped at two, returned in the response. |
| Same-threshold retry | The quoter's cutoff is identical on both passes. |
| Retry fixture | A question whose gold chunk appears only after the rewritten query. |
| Absent-fact fixture | Two searches, then abstain, with both queries logged. |

#### How it works

1. Wire the first pass to the existing quote-or-abstain path.
2. On low coverage only, rewrite once and search again.
3. Stub the search function and assert the absent-fact question triggers two calls.
4. Build the retry-success fixture by making the original query lexically miss and the rewritten query hit.
5. Write `retries.md` with both fixtures' logs.

#### Tech stack

- Python 3.11 or newer
- Template rewriter and the Day 40 quoter
- A call-counting stub in tests

#### Setup

1. Create `second-search/` with `retry.py` and tests.
2. Run both fixtures.
3. Add a test that a third search call fails the run if it happens.
4. Confirm the threshold file is read once and reused.

#### Deliverable

- The absent-fact fixture performs two searches and abstains.
- The retry-success fixture quotes a span that the first query did not retrieve.
- The threshold value is the same in both attempts' logs.
- A test fails the build if search is called three times on one question.

#### Step ahead

The next failure is a retry that succeeds by retrieving a contradictory span. Add a check between the two passes: if both passes would quote and the quotes disagree on a number, abstain with reason `conflict` rather than preferring the second pass because it ran later. Fixture two fee sentences with different amounts and a rewriter that surfaces the second one. The step-ahead behavior is to surface the conflict, not to average the numbers or to pick the more recent file unless the case edition already settled it.

### Day 46 — Recall at K, Written Down

**Level:** Advanced

**Folder:** [atlas/04-retrieval-studio/day-46-recall-at-k/README.md](atlas/04-retrieval-studio/day-46-recall-at-k/README.md)

Freeze a retrieval eval file and report recall at five and at twenty, with a denominator you can recount.

#### Concept

You have been watching individual questions. A phase needs a number that does not move just because you remember a favorite example. This project freezes an evaluation file: question id, question text, and the set of gold chunk ids. It runs the current retrieval stack and reports recall at 5 and recall at 20. Recall is the fraction of gold ids that appear in the top k, averaged per question and also reported as a micro average over gold ids. Those two averages answer different questions, and you will show a case where they diverge by writing one question with three gold chunks and several with one. You will not tune the stack against this file after the first measurement. If you change the stack, you add a new row to a results table rather than replacing the old number. The history is the point.

#### Approach

Copy questions into `eval/retrieval.jsonl` and treat that file as append-only in spirit: a changed gold set is a new file version in the name, `retrieval_v2.jsonl`, not an edit. The runner reads a versioned config naming the retriever. Metrics code is separate from retrieval code so a test can score a fake ranking. Include a question with empty gold and define the metric: it is excluded from recall, and counted in a separate `no-gold` tally, because a silent zero would punish abstentions you wanted. Write `eval_report.md` with both averages, the tally, and the config name.

#### Components

| Piece | Role |
| --- | --- |
| Frozen eval file | Question ids and gold chunk id sets. |
| Metric function | Macro and micro recall at k, tested on a fake ranking. |
| No-gold tally | Questions excluded from the denominator, counted aside. |
| Results table | Append-only rows of config name and scores. |

#### How it works

1. Assemble the eval file from the questions you trust. Drop any you are unwilling to stand behind.
2. Score a hand-built ranking in a unit test: one hit of two gold ids is recall 0.5 on that question.
3. Run the real stack once and append a results row.
4. Change a single, named setting, run again, and append a second row. Do not delete the first.
5. Note which average you would quote to a teammate and why.

#### Tech stack

- Python 3.11 or newer
- The retrieval stack you have been building
- JSONL eval file

#### Setup

1. Create `recall-eval/` with `eval/retrieval_v1.jsonl`, `metrics.py`, and `run_eval.py`.
2. Run the unit test for the metric before the real run, so a bug in retrieval does not look like a bug in recall.
3. Run the stack twice with two configs if you have a real knob. If you do not, run the same config twice and show the rows match.
4. Write the report.

#### Deliverable

- Macro and micro recall are both present, and the unit test locks a hand-computed value.
- Questions with no gold are excluded and tallied.
- The results table has more than one row or a documented second run that matches the first.
- The eval file's version is in the report.

#### Step ahead

Recall does not know whether the chunk that matched is the stale edition. Add an edition-conditioned recall that counts a hit only when the chunk's edition equals the case edition on the eval row. A ranking that surfaces the right words in the wrong edition must not increase the score. Put three rows in a fixture where the text matches and the edition does not, and show the conditioned recall fall while the unconditioned recall stays high. That gap is the number you would add to the results table before calling the stack ready for the casework in Day 42.

### Day 47 — Compress Before You Prompt

**Level:** Advanced

**Folder:** [atlas/04-retrieval-studio/day-47-compress-before-prompt/README.md](atlas/04-retrieval-studio/day-47-compress-before-prompt/README.md)

Extract the sentences that overlap the query before anything is shown to a generator, and measure what you dropped.

#### Concept

Stuffing five parent sections into a prompt spends the context window on instructions for docks the user did not ask about, and it gives a generator more room to stitch unrelated numbers. This project compresses each retrieved parent to the sentences that pass the Day 40 coverage score, in their original order, with offsets preserved. If no sentence passes, the parent is dropped, not replaced with a summary you invent. You will measure, on the gold questions, how many characters you removed and whether every gold offset still intersects the compressed text. A compression that deletes the gold span is a failed compression even if the remaining text looks focused. You will also run one question where the answer is the absence of a sentence — a rule that only appears as a header plus a table — and show that sentence-level compression can delete the header. That case sets up the fix.

#### Approach

Compression is a pure function of the parent text, the query, and the threshold. It does not call a generative model. Output is a list of kept spans with offsets. The coverage metric against gold is: a gold offset range is preserved if any kept span overlaps it. Report per-question preservation and the character reduction ratio. The header-loss fixture is a table chunk from Day 43 passed through a sentence splitter that does not understand tables. You will see it fail, write the failure down, and only then special-case chunks whose metadata says `table` so they bypass sentence compression and pass through whole. The bypass is the patch. The failed run stays in the notes.

#### Components

| Piece | Role |
| --- | --- |
| Sentence compressor | Keeps sentences above the coverage threshold, in order. |
| Preservation check | Gold offsets still overlap a kept span. |
| Reduction ratio | Characters kept divided by characters retrieved. |
| Table bypass | Chunks tagged as tables skip sentence dropping, added after the fixture fails. |

#### How it works

1. Implement compression without the table bypass.
2. Run the gold questions and the table fixture. Record preservation.
3. Write the table failure into `compression.md`.
4. Add the bypass for `kind=table` and rerun. Append a second results row.
5. Test that a non-table parent still drops a sentence below threshold.

#### Tech stack

- Python 3.11 or newer
- Coverage scorer from the quoter
- Parent texts and gold offsets

#### Setup

1. Create `compress/` with `compress.py` and tests.
2. Run the before-bypass measurement and save it.
3. Add the bypass and run again.
4. Do not delete the before numbers.

#### Deliverable

- Preservation and reduction are reported per question.
- The table-loss failure is documented before the bypass exists in the results history.
- A non-table low-coverage sentence is still dropped, and a test proves it.
- Kept spans carry source offsets.

#### Step ahead

Sentence coverage keeps boilerplate that shares many words with the query and drops a short sentence that actually states the exception. Add a second keep rule for sentences that contain a negation cue you list, such as "unless" or "not", when they sit in a parent that already has a kept sentence. Measure how many extra characters that rule admits on the gold set and whether any gold span is saved that coverage alone dropped. If the cue list fires on every parent, the list is too broad and the step-ahead result is a narrower list, not a larger prompt.

### Day 48 — One Hop on an Entity Graph

**Level:** Advanced

**Folder:** [atlas/04-retrieval-studio/day-48-one-hop-graph/README.md](atlas/04-retrieval-studio/day-48-one-hop-graph/README.md)

Link handbook chunks to entities and expand one hop to a neighbor chunk before answering.

#### Concept

Some questions are paths. "Which depot services the dock that has the cargo-bike late fee" is not answered by the fee table alone and not answered by the depot page alone. This project extracts entities with a dictionary you write — docks, depots, fee codes — and links each chunk to the entities it mentions. Edges are co-mentions you define: a chunk links to an entity, and two entities link when a chunk mentions both, or when a small `relations.csv` you author says they do. Retrieval starts with the lexical hit, then walks one hop to neighboring chunks. Two hops are out of scope and a test should reject a walk that tries. You will show the cargo-bike question failing on the fee chunk alone and succeeding when the depot chunk is pulled in by the hop. You will also show a hop that pulls a distractor, and you will not hide it.

#### Approach

Keep extraction dictionary-based so the graph is auditable. `relations.csv` is allowed only for relations the text does not literally co-mention, and each row has a `source` note pointing at a handbook sentence. The walker returns the seed chunks plus chunks that mention a neighboring entity, capped at a fixed number. The quoter then runs on that set. Gold for the path question lists both chunks as required, and recall uses the Day 46 definition. A distractor edge is planted on purpose: an entity shared with an unrelated anecdote chunk. The report shows that chunk arriving via the hop. Capping the walk is how you keep the distractor from becoming the whole handbook.

#### Components

| Piece | Role |
| --- | --- |
| Entity dictionary | Names and aliases you listed. |
| Relation file | Hand-authored edges with a source sentence. |
| One-hop walker | Seed chunks plus neighbor chunks, with a cap. |
| Distractor report | A planted edge and the unwanted chunk it retrieves. |

#### How it works

1. Tag chunks with dictionary entities.
2. Author the minimum relations to connect fee to depot.
3. Run the path question with the hop disabled and enabled.
4. Run the distractor question and list the extra chunk.
5. Test that a two-hop request raises.

#### Tech stack

- Python 3.11 or newer
- CSV relations and JSON chunks
- The quoter and recall metric

#### Setup

1. Create `one-hop/` with `entities.csv`, `relations.csv`, and `walk.py`.
2. Run both questions.
3. Write `graph_notes.md` with the hop-enabled quote and the distractor chunk id.
4. Run the two-hop rejection test.

#### Deliverable

- The path question's required chunks are both present only when the hop is enabled, or you document an accidental direct hit and make the handbook harder.
- The distractor chunk is listed, not filtered out of the notes.
- Two hops raise, and the test covers that.
- Every relation row cites a sentence or an explicit `manual` source.

#### Step ahead

One hop floods the quoter when a popular entity, the word "depot" in half the handbook, becomes a neighbor. Add a degree cap: entities mentioned in more than a threshold of chunks do not expand, and the response logs which entities were skipped as hubs. Pick the threshold from the degree histogram before you rerun the path question, and show that the cargo-bike path still returns while a hub entity adds zero chunks. If the path depended on the hub, the step-ahead is to encode that relation in `relations.csv` rather than expanding the hub.

<a id="phase-05"></a>

## Phase 05: Agent Workshop

**Days 49–64.** 16 projects.

### Goal

Finish this phase with a small agent loop you can read end to end: tools with schemas, a transcript, a plan that the executor is not allowed to ignore, memory that names its sources, a budget that stops the loop, and a handoff that is a file rather than a shared chat.

### Skills covered

- Tool loops with pure functions and a scratchpad
- JSON schemas that reject bad arguments before the function runs
- ReAct-style transcripts
- Checklist plans and strict executors
- Sliding windows and summaries of dropped turns
- Long-term facts stored with provenance
- Routing a turn to a specialist prompt
- Handoffs by artifact
- State machines that reject illegal transitions
- Step and token budgets with partial answers
- Idempotency keys on retried tools
- A fixed action space against a local HTML fixture
- Citation-bound research over local notes
- Subagents that return structured mail
- A scored gridworld environment
- Dialogue repair after a user correction

Put a model, or a scripted stand-in, in a loop with tools, memory, and explicit state, and make every side effect visible.

By the end of the phase you should be able to: Build agents whose tools, memory, and handoffs you can replay without a hosted account.

### Day 49 — Two Pure Tools and a Scratchpad

**Level:** Intermediate

**Folder:** [atlas/05-agent-workshop/day-49-two-pure-tools/README.md](atlas/05-agent-workshop/day-49-two-pure-tools/README.md)

Run a loop that may only call two pure functions, and record every call on a scratchpad.

#### Concept

An agent that can call the network on day one teaches you nothing about the loop, because the interesting behavior is hidden in the response. This project builds the smallest loop that still deserves the name. The agent may call two pure functions: `lookup_fee(code)` reads a dictionary you wrote, and `add_minutes(start, minutes)` does arithmetic. A scripted policy, not a model, chooses the next call from the scratchpad. The scratchpad is an append-only list of calls and results. The final answer is a string that must be computable from the scratchpad alone. If you deleted the functions and kept the scratchpad, a reader could still check the answer. That is the bar. A model can replace the scripted policy later. It does not get to replace the log.

#### Approach

Represent a step as a JSON object with `tool` and `arguments`, or a final object with `answer`. The runner refuses unknown tool names and refuses a second call with the same arguments if you set a flag that the fixture uses to catch loops. The scripted policy solves one task: given a fee code and a start time, return the end time of a rental that lasts the fee's included minutes. Write three tasks in `tasks.jsonl`. One of them should omit the fee code so the policy must stop with `missing-input` rather than invent a code. Pure functions means no clock and no file writes inside the tool. The scratchpad writer is the only thing that touches disk.

#### Components

| Piece | Role |
| --- | --- |
| Tool registry | Two pure functions and a map from name to function. |
| Scratchpad | Append-only call and result records. |
| Scripted policy | Chooses the next call from the scratchpad and the task. |
| Task file | Three tasks, including one that must not invent a fee code. |

#### How it works

1. Implement the two functions and a registry that rejects unknown names.
2. Implement the runner: policy, call, append, repeat, until a final answer or a step cap of six.
3. Run the three tasks and write one scratchpad file each.
4. Assert the successful answers match a hand computation.
5. Assert the missing-code task ends with `missing-input` and an empty call list.

#### Tech stack

- Python 3.11 or newer
- Standard library `json`
- No model and no network

#### Setup

1. Create `two-tools/` with `tools.py`, `loop.py`, `tasks.jsonl`, and tests.
2. Run `python3 loop.py` and inspect `out/`.
3. Run `python3 -m unittest discover -s tests -v`.
4. Read one scratchpad aloud and confirm the answer uses only values that appear in it.

#### Deliverable

- Unknown tool names fail before any function body runs.
- The missing-input task makes zero tool calls.
- A successful answer can be recomputed from its scratchpad by a test that ignores the policy.
- The step cap is a named constant and a test exceeds it with a policy that never finishes.

### Day 50 — Schemas that Reject Arguments

**Level:** Intermediate

**Folder:** [atlas/05-agent-workshop/day-50-schemas-that-reject/README.md](atlas/05-agent-workshop/day-50-schemas-that-reject/README.md)

Validate tool arguments against a JSON schema before the function runs, and return the error as an observation.

#### Concept

A tool that accepts a string where it expected a code will either crash the loop or, worse, quietly search for nothing. This project puts a schema in front of each pure function. The schema names required fields, types, and simple bounds: a fee code matches a pattern, minutes are an integer from 1 to 240. Validation runs before the function. A failure becomes an observation the policy can see, with the schema path of the error, and the function is not called. This is argument shape checking for a local tool. It is not an authorization gateway, not an approval workflow, and not a place to encode who is allowed to move money. The question today is only: did this call match the shape the function was written for?

#### Approach

Write schemas as JSON objects you interpret yourself for a subset: object types, required keys, string patterns, integer minimum and maximum. Do not import a full JSON Schema library unless you also keep a test that shows your subset rejecting the cases you care about. The runner's order is fixed: known tool, then schema, then function. A schema error appends an observation of type `invalid-arguments` and does not increment a success counter. Add a policy that repairs one bad call: it sends minutes as a string, reads the observation, and sends an integer. Add another task that sends a fee code with a space and does not repair, so the loop stops on the observation after one attempt. Log both.

#### Components

| Piece | Role |
| --- | --- |
| Schema subset | Required keys, types, patterns, and integer bounds. |
| Validator | Returns a path and a message, or accepts. |
| Observation | Invalid arguments are data the policy can read. |
| Repair transcript | One bad call followed by a corrected call. |

#### How it works

1. Attach a schema to each tool from Day 49.
2. Reject a call before the function and record that the function body did not run. A counter inside the function makes this obvious.
3. Run the repair task and save the scratchpad.
4. Run the unrepaired bad code and assert the function call count stays zero.
5. Test a missing required field, a pattern miss, and an integer above the maximum.

#### Tech stack

- Python 3.11 or newer
- Standard library `re` and `json`
- The tool loop from Day 49

#### Setup

1. Create `schemas/` with `schema.py`, `loop.py`, and tests.
2. Run both tasks.
3. Run the unit tests for the three rejection cases.
4. Confirm in the scratchpad that the function-call counter did not move on the rejected attempt.

#### Deliverable

- Rejected calls do not execute the function, and a test locks that.
- The repair transcript shows the invalid observation and then a valid call.
- Error observations include the field path.
- The notes state that this layer checks shape, not permission to perform a side effect.

### Day 51 — A Transcript You Can Grade

**Level:** Intermediate

**Folder:** [atlas/05-agent-workshop/day-51-react-transcript/README.md](atlas/05-agent-workshop/day-51-react-transcript/README.md)

Record thought, action, and observation lines, and grade the transcript against a scripted trace.

#### Concept

A loop that only stores tool calls hides why the next call was chosen. The ReAct pattern writes a thought, then an action, then an observation, and repeats. This project implements that transcript with a scripted reasoner so you can grade the text without a model. The reasoner emits a thought that names the missing field, then an action. You will compare a run to a golden transcript: same actions in the same order, observations equal to the tool results. Thoughts may differ in wording only if you are using a model. Under the scripted reasoner they must match too, because they are part of the contract of the fixture. Grading is exact on actions and observations. A mismatched thought under the script fails the run. That strictness is what makes the later model swap measurable.

#### Approach

Each transcript line has a kind: `thought`, `action`, `observation`, or `answer`. The runner rejects two actions in a row without an observation, and rejects an observation that did not come from the tool. The golden file is a transcript you write by hand for one task. The grader reports the first diverging line index. Include a second golden file for the missing-input task that contains a thought and an answer and no action. A model backend, if you add one, is behind a flag and is not used by tests. Tests use the scripted reasoner only.

#### Components

| Piece | Role |
| --- | --- |
| Line types | Thought, action, observation, and answer, in a fixed order. |
| Scripted reasoner | Emits the next thought and action from the task state. |
| Golden transcript | A hand-written trace for one successful task. |
| Grader | Reports the first line where the run diverges. |

#### How it works

1. Define the line schema and the runner rules that forbid doubled actions.
2. Write the golden transcript for the fee-and-time task.
3. Run the scripted reasoner and grade it. It should match.
4. Mutate one action in a copy of the run and assert the grader names that line.
5. Grade the missing-input transcript and assert it contains no action lines.

#### Tech stack

- Python 3.11 or newer
- JSONL transcripts
- Scripted reasoner required, model optional and off by default

#### Setup

1. Create `react-transcript/` with `transcript.py`, `gold/`, and tests.
2. Run the match and the deliberate mismatch.
3. Run tests.
4. If you try a model, save that transcript as `out/model.jsonl` and do not overwrite the golden file when it differs.

#### Deliverable

- The scripted run matches the golden transcript exactly.
- A mutated action fails the grader at the right line index.
- The runner rejects an action that is not followed by a tool observation when another action arrives.
- Tests pass with no model key present in the environment.

### Day 52 — A Checklist the Executor Cannot Skip

**Level:** Intermediate

**Folder:** [atlas/05-agent-workshop/day-52-checklist-executor/README.md](atlas/05-agent-workshop/day-52-checklist-executor/README.md)

Separate a planner that writes a checklist from an executor that may only mark listed items done.

#### Concept

A single loop that plans and acts in the same breath will skip a step and still sound finished. This project splits the roles. The planner writes a checklist of items, each with an id and a tool call, and then it is done. The executor may run only those calls, in order, and may mark an item done only after an observation is stored. It may not add a checklist item. A final answer that arrives with an open item is rejected. You will build one hostile executor, used only in a test, that tries to mark an item done without a call, and you will show the runner refusing. The planner in the required path is scripted from the task. The lesson is the boundary, not a clever plan.

#### Approach

The checklist is JSON. Item states are `open` or `done`. The executor function takes the checklist and the scratchpad and returns the next call or a final answer. The runner checks that the call's item id exists, is open, and matches the tool the planner named. Arguments may be filled from earlier observations if the plan used placeholders such as `$item1.minutes`. Placeholders are the only flexibility. Free-form extra calls are rejected. Write a task whose plan has two items and a third tempting call that is not on the list. Assert the tempting call never runs.

#### Components

| Piece | Role |
| --- | --- |
| Planner output | A checklist of item ids and tool names. |
| Executor | Runs listed calls in order and resolves placeholders. |
| State gate | An item becomes done only after an observation. |
| Hostile executor | A test double that tries to skip the call. |

#### How it works

1. Script a planner for the fee-and-time task with two items.
2. Run the executor through the runner and save the checklist with states.
3. Assert the final answer is rejected if you force an item to stay open.
4. Assert the hostile executor's premature done mark raises.
5. Assert a call whose tool name is not on the current item is rejected.

#### Tech stack

- Python 3.11 or newer
- JSON checklist and scratchpad
- No model required

#### Setup

1. Create `checklist/` with `plan.py`, `execute.py`, and tests.
2. Run the happy path and write `out/checklist.json`.
3. Run the hostile tests.
4. Document the placeholder syntax in a short comment at the top of `execute.py`.

#### Deliverable

- The happy-path checklist ends with every item done and observations attached.
- A premature done mark fails a test.
- A tool that was not on the list does not run.
- Placeholders resolve from earlier observations, and a missing placeholder fails the item rather than calling the tool with a literal dollar string.

### Day 53 — A Summary of What Was Dropped

**Level:** Intermediate

**Folder:** [atlas/05-agent-workshop/day-53-summary-of-dropped-turns/README.md](atlas/05-agent-workshop/day-53-summary-of-dropped-turns/README.md)

Keep a sliding window of turns and a summary that names which facts were pushed out of the window.

#### Concept

Context windows fill up, and the usual fix is to delete old turns. The failure is silent: a fee code mentioned at the start is gone, and the agent asks for it again or invents one. This project keeps two stores. The window holds the last N transcript lines. The summary holds facts that were in lines you dropped, but only facts that match a small extractor: fee codes, dock names, and times. When a line leaves the window, the extractor runs on it and the summary records the fact and the line id it came from. If the extractor finds nothing, the summary records `dropped-without-fact` and the line id. You will replay a transcript long enough to force a drop and show the fee code surviving in the summary. You will also show a line whose only content is small talk, dropped without a fact, so the summary does not pretend to remember chatter.

#### Approach

N is a named constant, small enough that your fixture crosses it, such as 4 lines. The extractor is a set of regular expressions, not a model. The summary is a list of records, not a paragraph, so a test can see whether `HL-FEE-14` is present. The prompt or policy input for the next step is the summary plus the window, and a test asserts the dropped line's full text is absent from that input while the extracted code is present. Do not summarize by asking a model to "keep the important parts." That hides the exact loss this day is about.

#### Components

| Piece | Role |
| --- | --- |
| Sliding window | The last N transcript lines. |
| Extractor | Patterns for codes, docks, and times. |
| Summary records | Fact plus source line id, or an explicit drop with no fact. |
| Next-step input | Summary plus window, never the raw dropped text. |

#### How it works

1. Feed a scripted transcript longer than N that mentions a fee code early and small talk in another early line.
2. Drop lines one at a time and update the summary.
3. Assert the fee code is in the summary with the right line id.
4. Assert the small-talk line produced `dropped-without-fact`.
5. Build the next-step input and assert the raw dropped text is not in it.

#### Tech stack

- Python 3.11 or newer
- Standard library `re`
- JSONL transcript fixture

#### Setup

1. Create `window-summary/` with `memory.py` and tests.
2. Run the fixture and write `out/summary.json`.
3. Run tests.
4. Set N in one place and refer to it from the test so a change updates both.

#### Deliverable

- The fee code survives with a source line id.
- Small talk is recorded as dropped without a fact, not omitted silently.
- The next-step input excludes raw dropped lines.
- A test fails if the extractor misses a code that is still inside the window. Extraction on drop is the path under test, and in-window lines stay verbatim.

### Day 54 — Facts with Provenance

**Level:** Intermediate

**Folder:** [atlas/05-agent-workshop/day-54-facts-with-provenance/README.md](atlas/05-agent-workshop/day-54-facts-with-provenance/README.md)

Store long-term facts only with a source id, and refuse a fact the agent tries to save without one.

#### Concept

A memory note that says "the late fee is 14" is a liability if nobody can find the sentence it came from. This project is a long-term store, separate from the sliding window. A fact is admitted only with a `source_id` that exists in a catalog of handbook chunks or tool observations. The store records the fact text, the source id, and a hash of the source text at save time. On read, if the source text has changed, the fact is returned with `stale: true` and is not silently refreshed. An agent tool `remember(text, source_id)` calls this store. A call with an unknown source id is an observation of type `rejected-memory`, and nothing is written. You will try to remember a fee that does not appear in the cited chunk and, in the required design, still accept it only if the source id exists — then add a second check that the fact's numbers appear in the source text. The second check is in scope today. A memory that can attach any sentence to any id is not provenance.

#### Approach

The catalog is a JSON file of id to text, built from a few handbook chunks. `remember` verifies the id, verifies that every integer in the fact text occurs in the source text, and only then appends. This will reject some true paraphrases. That is acceptable for this day. Write the limitation down: paraphrases need a later design, and the current rule prefers false rejects over free invention. The stale flag flips when you edit the catalog text without updating the hash. A test edits the catalog and expects `stale: true` on the next read.

#### Components

| Piece | Role |
| --- | --- |
| Source catalog | Ids and texts the memory is allowed to cite. |
| Remember tool | Rejects unknown ids and facts whose numbers are not in the source. |
| Hash | SHA-256 of the source text at save time. |
| Stale read | A changed source marks the fact stale instead of rewriting it. |

#### How it works

1. Load a tiny catalog with one fee chunk and one unrelated chunk.
2. Remember a fact whose number appears in the fee chunk. Assert it is stored.
3. Attempt a fact with a number that does not appear. Assert rejection and an unchanged store.
4. Edit the catalog, reread, and assert the stale flag.
5. Attempt an unknown source id and assert rejection.

#### Tech stack

- Python 3.11 or newer
- Standard library `hashlib` and `json`
- No vector database

#### Setup

1. Create `provenance-memory/` with `store.py`, `catalog.json`, and tests.
2. Run the four cases and write `out/memory.json`.
3. Run tests.
4. Write the paraphrase limitation in `notes.md` in two sentences.

#### Deliverable

- Unknown source ids write nothing.
- A number that is not in the source blocks the write.
- A changed source marks the fact stale and does not auto-edit the fact text.
- The notes name the paraphrase limitation.

### Day 55 — A Specialist Router

**Level:** Intermediate

**Folder:** [atlas/05-agent-workshop/day-55-specialist-router/README.md](atlas/05-agent-workshop/day-55-specialist-router/README.md)

Route a user turn to a specialist prompt by rules, and log the route even when you override it.

#### Concept

One prompt that tries to be a fee clerk, a weather clerk, and a small-talk partner will follow the loudest instruction in the turn. This project routes each turn to one specialist: `fees`, `weather`, or `fallback`. Routing is a deterministic rule list you can read, plus an optional model router behind the same interface that tests do not use. The rule list looks for fee codes, weather words, and otherwise falls back. The specialist receives only its own instruction block and the turn, not the other specialists' instructions. You will include a turn that matches two rules and show that the first matching rule wins, and that the log records both the winner and the rules that also matched. An override argument exists for tests and must be logged as `override`, not as if the rules had chosen it.

#### Approach

Rules are an ordered list of objects with a name, a pattern, and a specialist id. First match wins. The log line contains the turn id, the specialist, the winning rule name, the other matching rule names, and whether an override was used. A test sends "late fee in the rain" and expects `fees` if that rule is first, with `weather` listed as also matched. Swapping rule order changes the winner, and a second test locks the swapped order so the priority is data, not an accident of if-statements scattered in code. The fallback specialist has a short instruction that says it cannot look up fees. Assert that the fee instruction text is absent from the fallback prompt.

#### Components

| Piece | Role |
| --- | --- |
| Ordered rules | Patterns and specialist ids, first match wins. |
| Specialist prompts | Separate instruction blocks. |
| Route log | Winner, also-matched rules, and override flag. |
| Prompt assembly | Only the chosen specialist's instructions are included. |

#### How it works

1. Write three specialist instruction files.
2. Route a fee turn, a weather turn, an ambiguous turn, and a turn that matches nothing.
3. Assert the ambiguous turn logs the runner-up rule.
4. Override the fallback turn to `fees` and assert the log says override.
5. Assert the assembled prompt for fallback does not contain the fee instruction.

#### Tech stack

- Python 3.11 or newer
- JSON rules and plain text instruction files
- Model router off unless a flag is set

#### Setup

1. Create `router/` with `rules.json`, `specialists/`, `route.py`, and tests.
2. Run the four turns and write `out/routes.jsonl`.
3. Run tests, including the swapped-order test.
4. Read the assembled fallback prompt and confirm it is short.

#### Deliverable

- Ambiguous turns log the winner and the also-matched rules.
- Rule order is data, and a test proves a swap changes the winner.
- Overrides are labeled as overrides in the log.
- Unchosen specialist instructions are not in the assembled prompt.

### Day 56 — Handoff by Artifact

**Level:** Intermediate

**Folder:** [atlas/05-agent-workshop/day-56-handoff-by-artifact/README.md](atlas/05-agent-workshop/day-56-handoff-by-artifact/README.md)

Pass work from a researcher role to a writer role only as a file with required fields, never as a shared transcript.

#### Concept

Two roles that share a chat will each assume the other noticed the fee code. This project forbids the shared transcript. The researcher reads the handbook chunks and writes `handoff.json` with required fields: `question`, `quotes` (each an exact substring plus chunk id), and `open_questions`. The writer may read only that file. It produces an answer that quotes only from `quotes`, or it returns `incomplete` if `open_questions` is non-empty. You will run one task where the researcher fills a real quote and an empty open-question list, and one where it sets an open question and leaves quotes empty. The writer must not "helpfully" answer the second task from the handbook, because the writer is not given the handbook path. A test that points the writer at the handbook folder should fail code review in the sense that your writer function's signature does not accept a handbook path.

#### Approach

Define the handoff schema and validate it before the writer runs. Extra fields are rejected so the researcher cannot smuggle a draft answer the writer will paste. The writer function signature is `write_answer(handoff: dict) -> dict`. Tests pass a handoff whose quote does not contain a number the researcher hoped to sneak into an extra field. Assert the extra field is rejected at validation, before the writer. For the successful task, assert the answer text contains the quote and the chunk id. For the incomplete task, assert the status is `incomplete` and the answer text is empty.

#### Components

| Piece | Role |
| --- | --- |
| Handoff schema | Question, quotes, and open questions. Extra fields rejected. |
| Researcher | A scripted function that fills the handoff from fixture chunks. |
| Writer | Reads only the handoff object. |
| Incomplete path | Non-empty open questions block the answer. |

#### How it works

1. Implement validation, including rejection of unknown fields.
2. Run the researcher on a fixture question and write `handoff.json`.
3. Run the writer on that file.
4. Run the open-question fixture and assert `incomplete`.
5. Assert the writer source does not take a handbook directory argument. A small test can inspect the signature with `inspect`.

#### Tech stack

- Python 3.11 or newer
- JSON handoff file
- Standard library `inspect` for the signature test

#### Setup

1. Create `handoff/` with `schema.py`, `roles.py`, and tests.
2. Run both fixtures.
3. Run tests.
4. Open `handoff.json` and confirm every quote is a substring of the fixture chunk you point at in the test.

#### Deliverable

- Unknown handoff fields fail validation.
- The writer signature accepts the handoff and nothing else.
- A non-empty open-question list yields an empty answer and status `incomplete`.
- The successful answer cites a chunk id that is inside the handoff.

### Day 57 — Illegal Transitions

**Level:** Intermediate

**Folder:** [atlas/05-agent-workshop/day-57-illegal-transitions/README.md](atlas/05-agent-workshop/day-57-illegal-transitions/README.md)

Model the agent as a state machine and reject any event that the current state does not allow.

#### Concept

Loops get into impossible states: an answer before any retrieval, a second handoff, a tool call after the answer. This project names the states and the events. States are `idle`, `planned`, `acting`, `handoff`, and `answered`. Events are `plan`, `act`, `observe`, `submit_handoff`, and `answer`. A table maps state and event to the next state or to `illegal`. The runner consults the table and refuses illegal events with the state name and the event name in the error. It does not catch the error and continue. You will drive a happy path and three illegal paths: answering from idle, acting after answered, and submitting two handoffs. The table is data, so a test can add a temporary transition without editing the runner.

#### Approach

Store the table as a dictionary of pairs. The runner holds one current state and appends every accepted event to a log. Illegal events raise `IllegalTransition` and leave the state unchanged. A test attempts the illegal event and then a legal one and asserts the legal one still sees the pre-illegal state. Do not encode the table as a chain of if statements inside the runner. The runner should look up the pair and follow it. Print the reachable states from `idle` by a small walk so you notice a state you cannot enter.

#### Components

| Piece | Role |
| --- | --- |
| Transition table | Pairs of state and event, stored as data. |
| Runner | Looks up the table and refuses misses. |
| Event log | Accepted events only. |
| Illegal paths | Three fixture sequences that must raise. |

#### How it works

1. Write the table and a function that lists states unreachable from idle.
2. Drive the happy path through answer and save the log.
3. Attempt each illegal path and record the exception message.
4. Assert state is unchanged after a rejected event.
5. Assert every named state is reachable, or remove the state from the machine.

#### Tech stack

- Python 3.11 or newer
- Standard library only
- No model

#### Setup

1. Create `state-machine/` with `machine.py` and tests.
2. Run the happy path and the three failures.
3. Run tests.
4. If a state is unreachable, fix the table before you call the day done.

#### Deliverable

- Three illegal sequences raise and name both the state and the event.
- State does not change on a rejected event.
- The transition table is data the runner looks up.
- Every state is reachable from idle, and a test walks the table to prove it.

### Day 58 — Budgets and Partial Answers

**Level:** Advanced

**Folder:** [atlas/05-agent-workshop/day-58-budgets-and-partial-answers/README.md](atlas/05-agent-workshop/day-58-budgets-and-partial-answers/README.md)

Stop the loop at a step budget and return a partial answer that lists unfinished checklist items.

#### Concept

An agent that runs until it feels done will run until someone kills the process. This project adds a budget: a maximum number of tool calls and a maximum number of transcript lines. When either limit is hit, the runner does not raise a generic timeout and discard the work. It returns a structured partial answer: status `partial`, the observations so far, and the checklist item ids still open. A complete answer is illegal if the budget is already exhausted. You will fixture a planner that emits four items and a budget of two calls, and show the partial result containing the two finished observations and the two open ids. You will also fixture a task that finishes inside the budget and show status `complete` with an empty open list. The budget is part of the task file so a test can tighten it without editing code.

#### Approach

Count tool calls, not thoughts. A thought does not spend the tool budget. Transcript-line budget counts every line. Hitting either budget triggers the same partial response shape so callers do not special-case the reason, but the response includes `stop_reason` of `tool-budget` or `line-budget`. A test sets the tool budget to zero and expects a partial answer with every item open and zero observations. The runner must check the budget before the call, not after, so a zero budget does not sneak one execution through. Write `budget_notes.md` with both fixture outputs.

#### Components

| Piece | Role |
| --- | --- |
| Tool budget | Checked before a call is dispatched. |
| Line budget | Checked before a line is appended. |
| Partial response | Observations so far and open item ids. |
| Stop reason | Which budget fired, on the response. |

#### How it works

1. Add budgets to the checklist runner from Day 52.
2. Run the four-item plan with a tool budget of two.
3. Run a two-item plan inside the budget and expect `complete`.
4. Run a zero tool budget and expect no function executions.
5. Hit the line budget with a talkative scripted policy and expect `line-budget` without a tool call that would exceed the tool budget. Keep the fixture simple: a line budget of one.

#### Tech stack

- Python 3.11 or newer
- The checklist runner
- JSON task files that include budgets

#### Setup

1. Create `budgets/` with `budget_loop.py` and tests.
2. Run the three fixtures and save their responses.
3. Run tests, including the zero-budget case.
4. Confirm a function-body counter stays at zero when the tool budget is zero.

#### Deliverable

- Partial responses list finished observations and open ids.
- A zero tool budget executes nothing.
- `stop_reason` distinguishes the two budgets.
- A task that finishes inside budget has status `complete` and no open ids.

#### Step ahead

A partial answer can still be mistaken for a fee quote if a reader looks only at the observations. Add a renderer that refuses to print a currency number unless status is `complete`, and otherwise prints the open item ids first. Fixture a partial run whose observations already contain a fee amount, and assert the rendered text does not contain that amount. The follow-on failure you are preventing is a UI that shows the observation log as if it were the answer.

### Day 59 — Idempotency Keys on Retried Tools

**Level:** Advanced

**Folder:** [atlas/05-agent-workshop/day-59-idempotency-keys/README.md](atlas/05-agent-workshop/day-59-idempotency-keys/README.md)

Retry a tool that appends a ledger row without appending it twice, using a key the caller supplies.

#### Concept

The pure tools from earlier days can be repeated safely. A tool that appends a maintenance ticket cannot. This project adds one effectful tool, `create_ticket`, backed by an in-memory ledger. Each call carries an idempotency key chosen by the agent, not by the tool. The first call with a key appends a row and stores the result. A second call with the same key and the same body returns the stored result and does not append. A second call with the same key and a different body is an error `key-reused-with-different-body`, and the ledger stays as it was. Retries are how you survive a crash after the tool succeeded but before the observation was written. You will simulate that crash by invoking the tool, discarding the observation, and invoking it again. The ledger length must stay one.

#### Approach

The ledger is a list and a dict from key to stored result. Body equality is JSON canonical form: sorted keys, no whitespace surprises. Do not use the key as a substitute for identity of the ticket only; store the body hash next to the key. A missing key is a schema error from Day 50's rules, and the tool does not run. This is not a permission system and not an approval chain. The only question is whether a retry duplicates a row. Include a test where two different keys with the same body create two tickets, because idempotency is not deduplication of intent. Write that distinction in `notes.md` so you do not collapse the two ideas later.

#### Components

| Piece | Role |
| --- | --- |
| Ledger | Append-only ticket rows in memory. |
| Key store | Maps a key to a body hash and a result. |
| Retry simulation | Two calls, one discarded observation, one row. |
| Conflict error | Same key, different body, no new row. |

#### How it works

1. Implement `create_ticket` with required `idempotency_key` and a body.
2. Call it twice with the same key and body. Assert one row.
3. Call it with the same key and a changed summary. Assert the error and an unchanged ledger.
4. Call it with two keys and the same body. Assert two rows.
5. Omit the key and assert the function body does not run.

#### Tech stack

- Python 3.11 or newer
- Standard library `json`
- In-memory ledger, no database server

#### Setup

1. Create `idempotency/` with `ledger.py` and tests.
2. Run the four cases as a script that prints ledger lengths.
3. Run tests.
4. Write the distinction between retry identity and content dedupe in `notes.md`.

#### Deliverable

- A retry with the same key and body does not append a second row.
- The same key with a different body errors and does not append.
- Two keys create two rows even if the bodies match.
- A missing key never reaches the ledger code, and a test covers it.

#### Step ahead

The key store lives in the same process as the crash you simulated, so a real crash would forget the key and the retry would duplicate the ticket. Persist the key store to a file before you append the ledger row, and persist the row after. Fixture a crash between the two writes by stopping after the key file is written and before the ledger append, then resume. The follow-on behavior is: resume sees the key with status `pending`, completes the single append, and a later retry returns that row. If resume appends twice, the order of the two writes is wrong.

### Day 60 — A Fixed Action Space on a Local Form

**Level:** Advanced

**Folder:** [atlas/05-agent-workshop/day-60-fixed-action-form/README.md](atlas/05-agent-workshop/day-60-fixed-action-form/README.md)

Drive a local HTML form with click, type, and read actions, and reject any action outside that set.

#### Concept

A browser agent that can run arbitrary scripts is a shell with extra steps. This project hosts a single HTML form on localhost — a lost-bike report with fields for dock id, fee code, and a submit button — and allows exactly three actions: `click(id)`, `type(id, text)`, and `read(id)`. The fixture page uses stable element ids. The agent is scripted. It reads the dock label, types a dock id and a fee code, clicks submit, and reads a confirmation element. There is no action for evaluating a string as code, and a test rejects `eval` and `navigate` if someone adds them to the action enum. The page is a file you wrote. You are practicing a bounded action space, not building a general computer-use product.

#### Approach

Serve the file with `http.server` or parse it with `html.parser` and apply actions to a small DOM you implement for the three element types you need: input, button, and output. A full browser is optional. The required path is a tiny DOM so tests do not need a browser binary. Submit copies the input values into the confirmation text only if both fields match patterns you set on the form. The scripted agent reads the confirmation and stops. An agent that types into an unknown id gets an observation `unknown-target` and does not change state. Log every action. Assert the log contains no action names outside the three.

#### Components

| Piece | Role |
| --- | --- |
| Fixture form | Local HTML with stable ids and a confirmation element. |
| Tiny DOM | Inputs, a button, and text output. |
| Action enum | Click, type, and read only. |
| Scripted agent | A fixed sequence that fills and submits the form. |

#### How it works

1. Write `form.html` and the tiny DOM that loads it.
2. Implement the three actions and the unknown-target observation.
3. Run the scripted agent and assert the confirmation text contains the dock id.
4. Attempt a disallowed action name and assert rejection.
5. Attempt a type into an unknown id and assert the inputs are unchanged.

#### Tech stack

- Python 3.11 or newer
- Standard library `html.parser`
- A local HTML fixture you wrote

#### Setup

1. Create `form-agent/` with `form.html`, `dom.py`, `agent.py`, and tests.
2. Run the scripted agent.
3. Run tests.
4. Do not add Selenium or a browser dependency on the required path.

#### Deliverable

- The confirmation text contains the values the agent typed.
- Action names outside the three are rejected, and a test lists the rejected names it tried.
- Unknown targets do not mutate inputs.
- The action log is complete for the successful run.

#### Step ahead

The form gains a second page after submit, with a new confirmation id and a hidden field the agent did not type. Extend the tiny DOM with one page transition triggered by submit, and require the agent to `read` the new page's id before it is allowed to answer. A script that answers from the first page's confirmation alone must fail. The follow-on is carrying state across a transition without adding a new action type.

### Day 61 — A Notes Researcher that Cites

**Level:** Advanced

**Folder:** [atlas/05-agent-workshop/day-61-notes-researcher/README.md](atlas/05-agent-workshop/day-61-notes-researcher/README.md)

Answer a question from local markdown notes with the quote-or-abstain rule wired into the tool loop.

#### Concept

The retrieval stack can quote, and the agent loop can call tools. This project connects them without loosening either rule. The only retrieval tool is `search_notes(query)`, which returns chunk ids and texts from a notes folder using BM25. The only answer tool is `quote(chunk_id, text)` which succeeds only if text is an exact substring of that chunk. A final answer must be one of those successful quotes or an abstention. A scripted policy handles two questions: one answerable from the notes, one not. The unanswerable question must end in abstain even if a chunk shares several words. You will not add a free-text `finish` tool that bypasses `quote`. If the policy tries, the runner rejects it. The point is to make the citation check a tool result, not a convention the model is asked to respect.

#### Approach

Reuse a small BM25 implementation and a handful of notes you write. `quote` looks up the chunk by id from the same index `search_notes` uses, so the policy cannot quote a chunk it invented an id for unless that id exists, and cannot quote text that is not there. The runner's terminal states are `quoted` and `abstained`. Anything else is an error. Log the search results and the quote attempts. A test calls `quote` with a near-miss string that differs by one word and expects failure. Another test omits search and calls `quote` with a real pair, which is allowed if the id exists: search is how the agent discovers ids, not a permission check. Do not confuse the two. Write that down so the citation rule stays about text, not about a ritual of having searched first.

#### Components

| Piece | Role |
| --- | --- |
| Notes index | Local markdown chunked and scored with BM25. |
| Search tool | Returns ids and texts. |
| Quote tool | Exact substring check against the indexed chunk. |
| Terminal states | Quoted or abstained, with no free-text finish path. |

#### How it works

1. Index four short notes, one of which contains a fee sentence.
2. Run the answerable question and assert the quote tool succeeded.
3. Run the unanswerable question and assert abstention and zero successful quotes.
4. Reject a `finish` tool name.
5. Fail a one-word-off quote in a unit test.

#### Tech stack

- Python 3.11 or newer
- BM25 over local markdown
- Scripted policy, model optional and off in tests

#### Setup

1. Create `notes-researcher/` with `notes/`, `index.py`, `loop.py`, and tests.
2. Run both questions.
3. Run tests.
4. Write `notes.md` explaining that search is discovery and quote is the check.

#### Deliverable

- The answerable run ends `quoted` with a substring of a real chunk.
- The unanswerable run ends `abstained` with no successful quote.
- A free-text finish tool is rejected.
- A one-word-off quote fails.

#### Step ahead

A quote can be exact and still be the wrong edition if notes from two years share a sentence frame. Add an `edition` field on each note and a required `edition` argument on `quote` that must match the chunk. Fixture two notes with the same sentence and different editions, and show that quoting the 2024 sentence while asking for 2026 fails. The follow-on keeps the substring check and adds a second predicate the tool enforces, rather than hoping the policy prefers the right file.

### Day 62 — A Mailbox for Subagents

**Level:** Advanced

**Folder:** [atlas/05-agent-workshop/day-62-subagent-mailbox/README.md](atlas/05-agent-workshop/day-62-subagent-mailbox/README.md)

Let a parent post a task to a child and accept only a structured reply on a mailbox, not a shared scratchpad.

#### Concept

A parent agent that calls a child as a function and reads the child's scratchpad will depend on private details. This project gives the child a mailbox. The parent writes a task message with an id, a question, and the chunk ids the child is allowed to read. The child may use only those ids. It posts a reply message with the same task id, a status, and either a quote or an error code. The parent is not given a function that reads the child's tool log. A test asserts the parent's visible state after the reply does not contain the child's intermediate search strings. You will run one successful delegation and one where the child is asked about a chunk id that was not in the allow-list. That reply is an error, and the parent must surface the error rather than retry the child with a widened list. Widening is a different task with a different id.

#### Approach

Messages are JSON records on two lists: inbox and outbox. The child function receives one task and returns one reply. It does not receive a callback into the parent. The allow-list is checked inside the child's search tool, which is a filtered view of the index. A reply that cites a chunk outside the list is rejected by the mailbox validator before the parent sees it, and replaced with an error reply. This keeps a buggy child from laundering a citation. The parent policy is scripted: post, wait, stop. No recursive delegation. A test that tries to post a second child task while the first is open fails, so mailboxes do not become an unbounded tree on this day.

#### Components

| Piece | Role |
| --- | --- |
| Task message | Id, question, and allowed chunk ids. |
| Child view | Search restricted to the allow-list. |
| Reply validator | Rejects citations outside the list before the parent reads them. |
| Parent state | Sees the reply and not the child's scratchpad. |

#### How it works

1. Implement the mailbox and the allow-list filter.
2. Run a task whose answer is inside the allow-list.
3. Run a task whose only supporting chunk is outside the list and expect an error reply.
4. Assert the parent state lacks the child's query strings.
5. Assert a second open task is rejected.

#### Tech stack

- Python 3.11 or newer
- Local notes index
- JSON messages

#### Setup

1. Create `mailbox/` with `mail.py`, `child.py`, `parent.py`, and tests.
2. Run both delegations.
3. Run tests.
4. Keep the child's log on disk for you to debug, but do not pass that path into the parent function.

#### Deliverable

- A citation outside the allow-list never appears in the parent's reply object.
- The parent function signature does not accept a child log path.
- Two open tasks are rejected.
- The successful reply quotes a chunk that was on the list.

#### Step ahead

The parent currently stops on the first error. Add a single, explicit follow-up task id that may cite one extra chunk id, chosen from the error's `blocked_ids` field, and no others. The follow-up must reference the original task id. A parent that opens a follow-up without that reference, or that adds two extra ids, is rejected. The step-ahead is a bounded widening you can see in the mailbox, not a retry with a fresh unrestricted child.

### Day 63 — A Scored Gridworld

**Level:** Advanced

**Folder:** [atlas/05-agent-workshop/day-63-scored-gridworld/README.md](atlas/05-agent-workshop/day-63-scored-gridworld/README.md)

Put an agent in a tiny grid, score a task, and show a script that loops without progress.

#### Concept

Tool-using transcripts are hard to score because the world is implicit. A grid is a world you can score. This project builds a 5 by 5 grid with a dock, a bike, and a goal cell. The agent may `move` in four directions and `pickup`. Walls and the edge reject the move with an observation and do not change position. The score is 1 when the bike reaches the goal in at most 12 actions, otherwise 0. A scripted policy solves it. A second policy chases a loop: move left, move right, forever. The runner's budget stops it, and the score is 0. You will log positions after every action. This is an environment and a score, not a trace debugger and not a failure-taxonomy product. You do not need to classify why the loop happened beyond showing that position did not change across a full cycle.

#### Approach

The environment is a pure function from state and action to state and observation, plus a reward of 0 until the goal condition, then 1, and the episode ends. Illegal moves return the same state. The loop policy is deterministic. The progress check in the required path is simple: if the position set of the last four actions has size 1, stop early with score 0 and reason `no-progress`. That check is local to this environment. Do not generalize it into a library of agent failure types. Seed nothing unless you add an obstacle that is random. The grid is fixed so the successful action list is a test fixture.

#### Components

| Piece | Role |
| --- | --- |
| Grid state | Agent position, bike position, goal, and whether the bike is held. |
| Action set | Four moves and pickup, with rejected moves leaving state unchanged. |
| Score | 1 only if the bike is on the goal within the action cap. |
| Loop policy | A policy the no-progress rule stops. |

#### How it works

1. Implement the transition function and a test that an illegal move does not change state.
2. Run the solving script and assert score 1 and a known action count.
3. Run the loop policy and assert score 0 and reason `no-progress`.
4. Assert the position log length matches the action count for the solver.
5. Assert pickup off the bike cell is a no-op observation and does not set the held flag.

#### Tech stack

- Python 3.11 or newer
- Standard library only
- No game engine

#### Setup

1. Create `gridworld/` with `env.py`, `policies.py`, and tests.
2. Run both policies and write `out/trace.json` for each.
3. Run tests.
4. Draw the grid in the notes with the goal marked, so a reader can replay the solver by hand.

#### Deliverable

- The solver scores 1 on the fixed grid.
- The loop policy scores 0 with `no-progress`.
- Illegal moves do not change state.
- The notes include the grid and the solver's action list.

#### Step ahead

The no-progress rule misses a policy that walks in a large square and never picks up the bike. Add a second stagnation rule: if `pickup` has not succeeded and the Manhattan distance to the bike has not decreased for six moves, stop with reason `no-approach`. Fixture a square-walk policy that stays far from the bike and assert that reason. Keep the original no-progress rule for the left-right loop. The follow-on is two stopping rules with different fixtures, not one vague notion of being stuck.

### Day 64 — Repair After a Correction

**Level:** Advanced

**Folder:** [atlas/05-agent-workshop/day-64-repair-after-correction/README.md](atlas/05-agent-workshop/day-64-repair-after-correction/README.md)

When the user says the other dock was meant, revise the slot you filled and do not defend the first one.

#### Concept

A form-filling agent stores a dock id from the first user turn. The user then says "no, the other one, the indoor dock." A brittle agent repeats the first id because it is already in the scratchpad. This project models dialogue state as slots: `dock_id` and `fee_code`, each with a value and a `source_turn`. A correction pattern clears the slot the pattern names and sets it from the next resolvable description. "Indoor dock" resolves through a table of dock attributes, not through the previous slot. If two docks are indoor, the agent must ask which, and it must not keep the previous dock id while it asks. You will script the user with two turns and assert the slot after turn two is the indoor dock, and that the first dock id is recorded only as a superseded value, not as the current one.

#### Approach

The resolver maps attributes to dock ids. Corrections match a small set of phrases you list, including "the other one" and "no". A correction without a resolvable replacement clears the slot and sets status `needs-clarification`. It does not leave the old value in place with a note. Superseded values go to a history list the answer renderer ignores. The answer renderer reads current slots only. A test renders the answer after the correction and asserts the first dock id is absent. Another test has two indoor docks and asserts the current slot is empty and the question names the attribute, not the old id.

#### Components

| Piece | Role |
| --- | --- |
| Slots | Value, source turn, and status. |
| History | Superseded values that the answer renderer does not read. |
| Attribute resolver | A table from attributes to dock ids. |
| Clarification | Empty slot when the correction is ambiguous. |

#### How it works

1. Fill `dock_id` from turn one with an outdoor dock.
2. Apply the correction turn that says indoor.
3. Assert the current value is the indoor dock and history holds the outdoor id.
4. Render the answer and assert the outdoor id is absent.
5. Run the two-indoor-docks fixture and assert clarification with an empty current value.

#### Tech stack

- Python 3.11 or newer
- JSON dialogue scripts
- No model required

#### Setup

1. Create `repair/` with `slots.py`, `dialogues.jsonl`, and tests.
2. Run both dialogues.
3. Run tests.
4. Write one sentence in the notes: the current slot is the only value the answer may use.

#### Deliverable

- After a clear correction, the answer text contains the new dock and not the old one.
- The old value is still in history for audit.
- An ambiguous correction clears the current slot.
- The renderer has no parameter that passes history into the answer, and a signature test can lock that.

#### Step ahead

A second correction can refer to history: "go back to the first one." Add an explicit undo command that pops history into the current slot, and reject it when history is empty. Do not make ordinary noun phrases search history. Fixture "go back to the first one" succeeding once and a second undo failing with `empty-history`. The follow-on keeps undo as a named command so a vague sentence cannot resurrect a superseded fee code by accident.

<a id="phase-06"></a>

## Phase 06: Proof Bench: Evals and Harnesses

**Days 65–78.** 14 projects.

### Goal

Finish this phase with a bench of small harnesses, each aimed at one failure mode: a tool the plan did not license, a replay that drifted, an extraction scored as a set, a slot the agent forgot, a budget curve, and a case id that never changes in place.

### Skills covered

- Plan-licensed tool checks
- Recorded HTTP cassettes and replay
- Property tests and shrinking for tool arguments
- Set-valued extraction scores
- Disagreement sets across scripted models
- Hidden-slot multi-turn scripts
- Cost versus quality sweeps on a frozen set
- Conflicts between trusted instruction sources
- Pinned retrieval results
- Structural checklists for long answers
- Scripted personas with a patience counter
- Immutable evaluation case ids
- Repeat-run flake budgets
- Accepted tool-name sequences

Score agent behavior with harnesses you can rerun offline: plan fidelity, cassettes, properties, and checks that do not depend on a single judge model.

By the end of the phase you should be able to: Put a number and a failing fixture on an agent behavior you care about.

### Day 65 — Was that Tool Licensed by the Plan?

**Level:** Advanced

**Folder:** [atlas/06-proof-bench/day-65-plan-licensed-tools/README.md](atlas/06-proof-bench/day-65-plan-licensed-tools/README.md)

Score each tool call on whether the checklist named it, separate from whether the final answer was right.

#### Concept

An agent can reach the right fee with a tool the plan never mentioned, which means the next run can wander. This project scores a finished transcript against the checklist that was approved before any call. Each action is `licensed` if its tool name appears on the current open item, and `unlicensed` otherwise. The final-answer check is a separate boolean: did `quote` match the gold substring. You will report both numbers. A fixture with the right answer and one unlicensed lookup must fail the license score and pass the answer score. A fixture with only licensed calls and a wrong quote must do the opposite. Collapsing these into one pass mark hides which part broke. The harness reads files. It does not run the agent.

#### Approach

Inputs are `plan.json` and `transcript.jsonl`. The scorer walks actions in order, matching them to open items as the executor would, and emits a row per action. Summary metrics are license rate and answer correctness. A missing plan file is an error, not a vacuously licensed run. Write three fixtures: clean pass, unlicensed success, licensed wrong answer. The harness prints a table and exits non-zero if license rate is below 1 or the answer is wrong, and the exit code distinguishes the two failures so a script can tell them apart.

#### Components

| Piece | Role |
| --- | --- |
| Plan file | Checklist items with tool names. |
| Transcript file | Actions and a final answer. |
| License rows | One verdict per action. |
| Separate exit codes | License failure and answer failure are different statuses. |

#### How it works

1. Implement the scorer as a pure function of the two files.
2. Score the three fixtures and save the tables.
3. Assert the unlicensed-success fixture fails only the license status.
4. Assert a missing plan raises rather than returning a perfect license rate.
5. Document the two metrics in `score_notes.md`.

#### Tech stack

- Python 3.11 or newer
- JSON fixtures
- No model calls inside the harness

#### Setup

1. Create `plan-license/` with `score.py`, `fixtures/`, and tests.
2. Run the three fixtures.
3. Run tests.
4. Confirm the harness does not import the agent loop. It only reads files the loop already wrote.

#### Deliverable

- License rate and answer correctness are both reported.
- The unlicensed success and the licensed failure produce different statuses.
- A missing plan is an error.
- The scorer has no network access and no model import.

#### Step ahead

A later call can repair an earlier unlicensed lookup, and a single license rate hides the recovery. Extend the row with `repaired_by`, the later action id that produced the gold answer, and report two rates: licensed actions, and unlicensed actions that were never needed for the gold quote. Fixture a transcript where an unlicensed call's result is unused because a later licensed call quotes the gold span. The follow-on question is whether the stray call was load-bearing. If you cannot tell from the transcript, the transcript is missing the field that would say so, and that gap belongs in the notes.

### Day 66 — Cassettes for Tool HTTP

**Level:** Advanced

**Folder:** [atlas/06-proof-bench/day-66-http-cassettes/README.md](atlas/06-proof-bench/day-66-http-cassettes/README.md)

Record an HTTP tool once and replay the bytes so a later run does not touch the network.

#### Concept

An agent tool that calls HTTP will score differently tomorrow if the server changes, and it will fail in a classroom with no network. This project wraps one tool, `get_status(dock_id)`, in a cassette. The first run, with a flag `record`, stores the URL, the query, and the response body under a key. Later runs with `replay` never open a socket. They return the stored body or fail with `cassette-miss`. A test uses a fake transport so recording does not need a real server. Replay must not call the transport at all, which you assert by counting calls. Editing the cassette body by hand is allowed only in a file you treat as source. The harness reads it. You will also show a miss: a dock id that was not recorded fails the replay run instead of falling through to the network.

#### Approach

The cassette is a JSON map from a canonical request key to a body. The key includes the method, path, and sorted query. It does not include timestamps. The wrapper takes a transport function. In replay mode the wrapper does not receive a live transport, or it receives one that raises if called. Prefer the raise-if-called double so a mistake is loud. Record mode calls the transport once per distinct key and writes the file. A second record of the same key compares bodies and errors on conflict rather than silently overwriting. That conflict is how you notice an upstream that is not stable enough to cassette.

#### Components

| Piece | Role |
| --- | --- |
| Canonical key | Method, path, and sorted query. |
| Cassette file | Map from key to response body. |
| Replay guard | Transport raises if replay tries to call it. |
| Conflict check | A second record with a different body errors. |

#### How it works

1. Implement record and replay modes.
2. Record two dock ids using a fake transport.
3. Replay them and assert the transport call count is zero.
4. Replay a third id and assert `cassette-miss`.
5. Record the same key with a different body and assert conflict, leaving the file unchanged.

#### Tech stack

- Python 3.11 or newer
- JSON cassette
- A fake transport in tests, no real HTTP required

#### Setup

1. Create `cassettes/` with `cassette.py`, `fixtures/status.json`, and tests.
2. Run record, then replay, as two commands.
3. Run tests.
4. Add `cassettes/` output to the folder you would commit if this were a real suite, and say so in the notes.

#### Deliverable

- Replay performs zero transport calls.
- An unknown key is a cassette miss, not a live call.
- Conflicting records do not overwrite the stored body.
- Request keys ignore field order in the query.

#### Step ahead

A cassette can go stale when the server adds a field the agent starts to require. Add a schema version on the cassette and a checker that compares replayed bodies to a list of required JSON keys. A body missing `status` fails with `cassette-stale` rather than returning JSON the agent will misread as an empty dock. Fixture a recorded body from version 1 and a required-key list from version 2. The follow-on is detecting drift at replay time, before the agent treats a missing field as a real observation.

### Day 67 — Properties of a Tool

**Level:** Advanced

**Folder:** [atlas/06-proof-bench/day-67-tool-properties/README.md](atlas/06-proof-bench/day-67-tool-properties/README.md)

Generate random valid and invalid arguments for a tool and shrink the smallest failing case.

#### Concept

Example calls hide the argument combination that breaks a tool. This project writes property tests for `add_minutes` and for `create_ticket`'s pure validation logic. A property is a statement: for any start minute in range and any duration in range, the end minute equals the start plus the duration modulo a day, and a second call with the same inputs returns the same result. Invalid durations outside the schema bounds never reach the function. You will generate random inputs with a seeded generator, and when a property fails you will shrink the input toward a smaller one that still fails. Shrinking is the part example tests do not do. You will plant one bug, such as an off-by-one at midnight, watch the shrinker find a small case, fix the bug, and keep the shrunk case as a regression test.

#### Approach

The generator draws integers and strings from explicit ranges. The shrinker for integers moves toward zero or toward the lower bound, halving the distance, and stops when the smaller candidate passes. For strings it deletes characters. The property runner prints the original failing input and the shrunk input. Use a fixed seed so the run that finds the midnight bug is reproducible. Do not pull in a property-testing framework. A few dozen lines are the point. The schema validator from the agent phase is the gate: inputs that fail the schema are counted as `rejected`, not as property failures.

#### Components

| Piece | Role |
| --- | --- |
| Generators | Seeded draws for ints and strings inside declared ranges. |
| Properties | Pure statements about tool outputs. |
| Shrinker | Searches for a smaller input that still fails. |
| Regression case | The shrunk input, saved after the bug is fixed. |

#### How it works

1. Implement generation and shrinking for integers.
2. Plant the midnight bug and run until a failure shrinks.
3. Save the shrunk case, fix the bug, and show the property passing.
4. Show that out-of-range durations are rejects, not failures.
5. Assert the shrinker does not return a larger input than it started with.

#### Tech stack

- Python 3.11 or newer
- Standard library `random`
- Your tool functions under test

#### Setup

1. Create `properties/` with `prop.py` and tests.
2. Run the planted bug once and save the transcript of the shrink.
3. Fix the bug and keep the regression case.
4. Run tests on the fixed code.

#### Deliverable

- The notes show a failing input and a smaller shrunk input for the planted bug.
- The fixed tool passes the property at the saved seed.
- Schema rejects are counted apart from property failures.
- The shrinker unit test covers a known integer failure.

#### Step ahead

Shrinking one argument ignores interactions. Add a shrinker for a pair of integers that tries reducing each coordinate, and fixture a bug that appears only when both the hour is 23 and the duration exceeds 60. Single-coordinate shrinking should be allowed to stop at a pair that still fails, and the notes should show the pair, not a misleading single value. The follow-on is a failure region that is not a corner of one axis.

### Day 68 — Set Equality for Extractions

**Level:** Advanced

**Folder:** [atlas/06-proof-bench/day-68-set-equality/README.md](atlas/06-proof-bench/day-68-set-equality/README.md)

Score extracted dock lists as sets with numeric tolerance, not as strings.

#### Concept

An extractor that returns docks `["B", "A"]` and a gold list `["A", "B"]` is correct, and a string equality check will say it is not. A fee of 14.0 against a gold of 14 is the same story. This project scores extraction outputs as structured values. A list field is compared as a set. A number field allows a tolerance you declare per field, defaulting to zero. Extra ids are false positives. Missing ids are false negatives. You will report precision and recall over the items, plus an exact-match rate after normalization. The harness reads JSONL of predictions and gold. It does not call a model. You will include a fixture that string-matches poorly and set-matches perfectly, and one that set-matches poorly because of a single extra dock the string check might have partially credited.

#### Approach

Define a small target schema: `docks` as a list of strings and `fee` as a number or null. Normalization trims strings and sorts nothing in the output you store; sorting is only inside the comparison, so you do not destroy the model's order before you have scored it. Tolerance lives in `tolerances.json`. A missing field is a false negative for that field, not a crash, and it is counted. Write `score.json` with per-case notes and a micro precision and recall across dock items. Exact string match can be reported as a diagnostic and must not be the headline number.

#### Components

| Piece | Role |
| --- | --- |
| Normalizer | Trim and type-check without discarding order in the stored prediction. |
| Set comparator | Item precision and recall for list fields. |
| Numeric tolerance | Per-field absolute tolerance. |
| Diagnostic string match | Present, and not the headline. |

#### How it works

1. Write five gold and prediction pairs, including the order swap and the extra dock.
2. Score them and write `score.json`.
3. Assert the order swap has item recall 1 and string match 0.
4. Assert the extra dock reduces precision and not recall.
5. Assert a fee of 14.0 matches gold 14 when tolerance is 0, because you normalize ints and floats that are equal.

#### Tech stack

- Python 3.11 or newer
- JSONL cases
- No model

#### Setup

1. Create `set-score/` with `score.py`, `cases.jsonl`, and tests.
2. Run the scorer.
3. Run tests.
4. State in the notes which number you would quote and why the string diagnostic is not it.

#### Deliverable

- Order differences do not reduce set recall.
- Extra items reduce precision.
- Tolerances are configured per field, not hard-coded in the comparison loop.
- The headline metrics are item precision and recall.

#### Step ahead

Flat sets miss nested structure. Add a path-level score for one nested field, `fees_by_dock`, a map from dock id to amount. A mismatch should name the path, such as `fees_by_dock.A`, rather than failing the whole object as one bit. Fixture a map that is right on dock A and wrong on dock B and show a score that is not zero and not one. The follow-on is a diff a person can fix from, not a single similarity float.

### Day 69 — Where Three Models Disagree

**Level:** Advanced

**Folder:** [atlas/06-proof-bench/day-69-where-models-disagree/README.md](atlas/06-proof-bench/day-69-where-models-disagree/README.md)

Run one prompt through three scripted models and list the cases where their structured answers differ.

#### Concept

A single model output has no internal argument. Three different outputs on the same prompt show you where a human should look. This project runs a frozen prompt set through three scripted model adapters that return JSON docks and fees. The adapters are deterministic functions, so the harness is testable without keys. One adapter is correct. One swaps two docks. One abstains on rare codes. The harness groups cases by the set of distinct normalized answers and writes a disagreement file: cases where the set has more than one answer. It does not vote and it does not declare a winner. Voting would hide the abstention. You are building a queue of cases to read, not a judge of judges and not a calibration study of pairwise preferences.

#### Approach

Each case result stores the three raw outputs and the normalized forms. Agreement means normalized equality under the Day 68 rules. The report lists disagreeing case ids and the answer set. A case where all three agree is counted and not listed in full. Include one case where two agree and one abstains, and keep it in the disagreement list. Dropping abstentions is a bug the test is named for. The adapters implement one function `complete(case) -> dict` and live in a file you can replace later with HTTP. Tests never do that replacement.

#### Components

| Piece | Role |
| --- | --- |
| Frozen prompts | A handful of cases with gold, used only as a label in the report, not as a voter. |
| Three adapters | Deterministic scripted models. |
| Disagreement list | Cases whose normalized answer set has size greater than one. |
| Abstention marker | A distinct answer value that must not be dropped. |

#### How it works

1. Write the three adapters and five cases.
2. Run the harness and write `disagreements.json`.
3. Assert the all-agree case is absent from the list and present in the agree count.
4. Assert the abstention case is present.
5. Assert the harness does not import a voting function. If you are tempted to add one, put it in a file the default command does not call, and test that the default output has no `winner` field.

#### Tech stack

- Python 3.11 or newer
- Scripted adapters
- The set normalizer

#### Setup

1. Create `disagreement/` with `adapters.py`, `harness.py`, and tests.
2. Run the harness.
3. Run tests.
4. Write one sentence: this list is a reading queue, not a score.

#### Deliverable

- Agreeing cases are counted and not expanded in the disagreement list.
- Abstentions count as disagreements against a concrete answer.
- The default report has no winner field.
- Adapters are replaceable functions, and tests use the scripted ones.

#### Step ahead

A long queue is not yet a way to choose the next case to read. Add a priority: cases where all three answers differ outrank cases where two agree. Sort the file that way and fixture six cases that force the order. Do not drop the lower group. The follow-on is a reading order you can explain, still without declaring which model was right.

### Day 70 — Hidden Slots Across Turns

**Level:** Advanced

**Folder:** [atlas/06-proof-bench/day-70-hidden-slots/README.md](atlas/06-proof-bench/day-70-hidden-slots/README.md)

Script a user with hidden slot values and score whether the agent fills them without re-asking a locked slot.

#### Concept

Multi-turn agents look fine if you read only the last turn. The failure is in the middle: the user already gave the dock, and the agent asks again, or it overwrites a locked fee code. This project is a harness around a scripted user and a scripted agent. The user has hidden slots. It reveals a slot only when asked, or when its opening line includes it. Once a slot is filled and the user has not corrected it, the slot is locked. The score penalizes a question about a locked slot and penalizes an answer that does not match the hidden value. You will run a three-turn script where the dock is given up front and the fee is asked once. A bad agent that re-asks the dock fails even if the final answer is right.

#### Approach

The user is a function of the hidden slots and the agent question. It is not a model. The harness logs each turn's asked slot names. Locked slots are those filled and not corrected. The agent under test is also scripted so you can swap in a bad one. Metrics are: final value match, count of questions about locked slots, and turns used. Do not average these into one grade. The report lists them. A correction turn unlocks a slot on purpose, using the Day 64 rule, and a question after the correction is allowed. A fixture covers that so the harness does not punish repair.

#### Components

| Piece | Role |
| --- | --- |
| Hidden slot user | Reveals values only under the script rules. |
| Lock set | Filled slots that have not been corrected. |
| Bad agent fixture | Re-asks the dock and still answers correctly at the end. |
| Separate metrics | Match, locked-question count, and turns. |

#### How it works

1. Implement the user and the lock rules.
2. Run the good agent and expect zero locked questions and a value match.
3. Run the bad agent and expect a locked question count of at least one, with the match still true.
4. Run a correction fixture and expect the post-correction question not to count as locked.
5. Write the three reports.

#### Tech stack

- Python 3.11 or newer
- Scripted user and agents
- JSON reports

#### Setup

1. Create `hidden-slots/` with `user.py`, `harness.py`, and tests.
2. Run the three scripts.
3. Run tests.
4. Keep the hidden values out of the agent's initial prompt in the good-agent fixture. The opening line may include only the values the script says were volunteered.

#### Deliverable

- The bad agent fails the locked-question metric while passing the final match.
- The good agent passes both.
- A post-correction question is not counted as a locked question.
- Metrics are reported separately.

#### Step ahead

Users contradict themselves without using the correction phrases you listed. Add a fixture where turn three states a new dock id as a bare fact, not as "no, the other one." Define the harness rule you will actually enforce: either bare restatements update the slot, or they count as contradictions the agent must ask about. Pick one, fixture both an agent that follows the rule and one that does not, and write the rule in the report header. The follow-on is a contradiction policy you chose on purpose, not an accidental overwrite.

### Day 71 — The Pareto Surface of Cost and Quality

**Level:** Advanced

**Folder:** [atlas/06-proof-bench/day-71-pareto-cost-quality/README.md](atlas/06-proof-bench/day-71-pareto-cost-quality/README.md)

Sweep a grid of retriever depth and scripted model cost and drop the configs that are worse on both axes.

#### Concept

A better score that costs ten times as much is not automatically the config you ship, and a cheaper config that loses one gold id may be. This project freezes a tiny retrieval eval and a scripted generator that can see only the chunks you pass it. You sweep `k` in {1, 3, 5} and a `model` label in {cheap, strong} where strong costs more per call in a price table you write. Quality is recall at k from the frozen file, or quote exact-match if you wire the quoter. Cost is the sum of a retrieval cost and a model cost you invented and documented as fictional. You plot nothing fancy: a CSV of config, quality, cost, and a flag `dominated` when another config is at least as good on quality and strictly cheaper, or strictly better and no more expensive. Dominated configs are not candidates. You do not hide them.

#### Approach

The price table is `prices.json` with fictional units, and the report says the units are fictional in the first line. The sweep is exhaustive on the small grid. Domination is computed by a function a test can run on a hand-built three-row table, one of which is dominated. The harness does not call a hosted model. The strong scripted model returns the gold quote only if the gold chunk is in the retrieved set. The cheap one returns it only if the gold chunk is rank 1. That difference is enough to make the surface interesting. Write `frontier.csv` and a sentence naming the undominated configs.

#### Components

| Piece | Role |
| --- | --- |
| Price table | Fictional costs for retrieval and for each model label. |
| Sweep grid | k and model label. |
| Domination flag | A config that is weakly worse on both axes. |
| Frontier list | The undominated configs, named in a sentence. |

#### How it works

1. Write prices and the two scripted models.
2. Run the sweep on a frozen question file with known gold chunks.
3. Compute domination.
4. Test domination logic on a hand-built table.
5. Write the frontier sentence from the actual CSV.

#### Tech stack

- Python 3.11 or newer
- CSV and JSON
- Scripted models with a price table

#### Setup

1. Create `pareto/` with `sweep.py`, `prices.json`, and tests.
2. Run the sweep.
3. Run the domination unit test.
4. Label the units as fictional in the report's first line.

#### Deliverable

- Every grid point is a row, including dominated ones.
- The hand-built domination test passes.
- The frontier sentence names configs that exist in the CSV.
- No hosted model is required to reproduce the file.

#### Step ahead

Cost is not the only second axis. Add a latency budget, also fictional, and drop any config whose scripted latency exceeds it before domination runs. Fixture a strong model that is best and over budget so it disappears from the frontier, and show the row still present with `over_budget` set. The follow-on is a constraint applied before you brag about the frontier, not a third score averaged in.

### Day 72 — When Trusted Instructions Conflict

**Level:** Advanced

**Folder:** [atlas/06-proof-bench/day-72-instruction-conflict/README.md](atlas/06-proof-bench/day-72-instruction-conflict/README.md)

Score an agent on a fixture where the system instruction and the tool description disagree, using a precedence you wrote down.

#### Concept

Two sources you trust can disagree. The system instruction says never invent a fee, and a tool description says the tool returns a fee for every dock, including docks it has never seen. A model will follow one of them. This project does not build an attack library and does not minimize a jailbreak. It builds eight hand-written probes where a system line and a tool description conflict, plus a precedence document you write first: system instruction outranks tool description. The agent is scripted in two versions, one that obeys precedence and one that obeys the tool text. The harness scores whether a forbidden tool call happened. The probes are fixtures, not a claim about how any hosted model behaves.

#### Approach

Each probe is a JSON object: system text, tool description, user text, and `forbidden_tool`. The runner executes a scripted policy selected by a flag. The score is the count of probes where the forbidden tool was called. Precedence lives in `precedence.md` and is written before you look at scores. The obedient policy refuses the call when the tool description promises coverage the system line forbids. The tool-following policy calls it. Tests lock both scores: obedient at zero calls, tool-following at one call per probe. Keep the probe count at eight so the fixture stays readable in one sitting.

#### Components

| Piece | Role |
| --- | --- |
| Precedence note | A written order among instruction sources. |
| Probe file | Eight conflicts with a named forbidden tool. |
| Two policies | Obey precedence, or obey the tool description. |
| Call score | Count of forbidden calls, per policy. |

#### How it works

1. Write `precedence.md` first.
2. Write eight probes.
3. Run both policies and save both scores.
4. Assert the obedient policy makes zero forbidden calls.
5. Assert the tool-following policy makes a forbidden call on every probe.

#### Tech stack

- Python 3.11 or newer
- JSON probes
- Scripted policies only

#### Setup

1. Create `instruction-conflict/` with `probes.jsonl`, `policies.py`, and tests.
2. Run both policies.
3. Run tests.
4. Do not describe the probes as a security certification. The notes should say they are a precedence fixture.

#### Deliverable

- Precedence is a file, not an unstated habit.
- The two policies score differently on the same probes.
- Eight probes are present and each names a forbidden tool.
- The harness makes no live model calls.

#### Step ahead

A third trusted source is the tool result itself. Add a probe where the system line says the fee table is authoritative, the tool description agrees, and the tool result returns a different number. Extend precedence so a tool result cannot override the system line, and score an agent that quotes the tool result anyway as a failure. The follow-on is precedence that covers results, not only instructions, with one fixture where obedience means refusing the number the tool just returned.

### Day 73 — Pins for a Retrieval Set

**Level:** Advanced

**Folder:** [atlas/06-proof-bench/day-73-retrieval-pins/README.md](atlas/06-proof-bench/day-73-retrieval-pins/README.md)

Hash the embedder id and the top-k chunk ids for a frozen query set, and fail when a rebuild drifts.

#### Concept

A retrieval change can look harmless and swap the chunk your quotes depend on. This project pins a frozen query set: for each query, store the embedder name, the index content hash, and the ordered top-k chunk ids. A later run recomputes the list and fails if the ids differ. The pin file is something you commit. Updating it is a deliberate edit, not a side effect of re-running the index. You will change one handbook sentence that should not affect a specific query and show the pin still matching, then change a sentence inside a pinned chunk and show the diff. The failure output names the query id and the first rank where the ids diverge.

#### Approach

Use BM25 or the hashing embedder so the pin is reproducible without a downloaded model. The index content hash is a hash of the chunk texts in id order. If the hash changes and the ids do not, the report says `content-changed-ranking-stable`, which is a warning, not a pass you should ignore, and not an automatic failure. You choose failure only when the ordered ids change. A test builds a two-chunk index, pins it, edits a stopword in an unretrieved chunk, and edits a token in the retrieved chunk. Those two edits must produce different statuses.

#### Components

| Piece | Role |
| --- | --- |
| Pin file | Query id, embedder name, index hash, ordered chunk ids. |
| Comparer | First rank of divergence. |
| Content hash | Hash of chunk texts, reported even when ranks match. |
| Deliberate update | A human-edited pin, not a silent rewrite. |

#### How it works

1. Build a tiny index and write `pins.json` by an explicit `write-pins` command.
2. Re-run check mode and expect a match.
3. Edit an unretrieved chunk and expect the stable-ranking warning.
4. Edit a retrieved chunk's important token and expect a failure that names the rank.
5. Assert check mode does not overwrite `pins.json`.

#### Tech stack

- Python 3.11 or newer
- Hashing embedder or BM25
- JSON pin file

#### Setup

1. Create `pins/` with `pin.py`, a mini handbook, and tests.
2. Run write-pins once, then check.
3. Run the two edit tests against copies of the index.
4. Document that updating pins is a separate command.

#### Deliverable

- Check mode never writes the pin file.
- A ranking change names the query and the rank.
- A content change with stable ranking is a warning with a distinct status.
- The embedder name is inside the pin file.

#### Step ahead

Sometimes the ranking should change, because you added a paragraph on purpose. Add an allow-list file `approved_diffs.json` that names the query id and the expected new top-k. Check mode passes a diff only when it matches an approved entry, and fails if the new ranking matches neither the pin nor an approval. Fixture one approved change and one unapproved change. The follow-on is a reviewable diff, not a habit of rewriting pins whenever the check goes red.

### Day 74 — Section Checklists for Long Answers

**Level:** Advanced

**Folder:** [atlas/06-proof-bench/day-74-section-checklists/README.md](atlas/06-proof-bench/day-74-section-checklists/README.md)

Score a long answer by required sections, forbidden claims, and numbers that must trace to a table.

#### Concept

Some answers are not a single span. A lost-bike reply should contain a section for what happened, a section for the fee, and no promise of a replacement bike the handbook does not make. This project scores long answers with a checklist file: required headings, forbidden phrases, and a table of numbers that must appear in both the answer and a cited table chunk. The scorer is deterministic. It does not ask a model whether the answer "covered the spirit" of a section. A missing heading is a miss. A forbidden phrase is a miss even if every heading is present. A number in the answer that is not in the cited table is a miss. You will write one gold answer that passes and two that fail for different reasons.

#### Approach

Headings are markdown `##` lines matched to a required list. Order is required unless the checklist says `order: free`. Forbidden phrases are case-sensitive literals so you do not accidentally ban a substring of a legitimate word. Choose phrases long enough to be specific. Numbers are extracted with a regex and compared to the table chunk's numbers as a set. The report lists missing headings, forbidden hits, and unknown numbers separately. A single boolean pass is the conjunction, and the report must still show the parts when it fails.

#### Components

| Piece | Role |
| --- | --- |
| Checklist file | Headings, forbidden phrases, and a cited table id. |
| Heading matcher | Exact heading strings, with optional order. |
| Forbidden list | Literal phrases. |
| Number trace | Every number in the answer appears in the cited table. |

#### How it works

1. Write the checklist and the table chunk.
2. Score the passing answer.
3. Score an answer missing a heading and one containing a forbidden promise.
4. Score an answer whose fee number is not in the table.
5. Assert the three failure reports name different reason groups.

#### Tech stack

- Python 3.11 or newer
- Markdown answers and a JSON checklist
- No model judge

#### Setup

1. Create `checklists/` with `checklist.json`, `answers/`, and `score.py`.
2. Run all four answers.
3. Run tests.
4. Keep the passing answer free of extra numbers you did not intend.

#### Deliverable

- The passing answer passes all three groups.
- Each planted failure trips a different group, and the report shows which.
- Forbidden matching is literal and covered by a test that a short token does not ban a longer innocent word.
- The conjunction pass is not the only field in the report.

#### Step ahead

A missing section and a weak section are different. Add partial credit per heading: full credit when the section contains at least one number traced to the table or an explicit `not-in-handbook` token, and zero when the heading is present but the body is empty. Fixture an empty section. The follow-on score distinguishes absence from a heading with nothing under it, and the notes say you still do not grade prose quality.

### Day 75 — A Persona with a Patience Counter

**Level:** Advanced

**Folder:** [atlas/06-proof-bench/day-75-patience-persona/README.md](atlas/06-proof-bench/day-75-patience-persona/README.md)

Simulate a user who ends the conversation after a fixed number of unhelpful turns, and score task completion.

#### Concept

An agent can be polite for twenty turns and never collect the dock id. This project scripts a persona with a goal, a patience counter, and a list of facts it will reveal when asked the right slot. Each agent question that does not name a missing slot decrements patience. At zero, the persona ends the conversation. The score is whether the goal slot values are filled at the end, not whether the agent said thank you. You will run a terse agent that asks the right slots and a rambling agent that asks open-ended questions. Both can be scripted. The rambling agent must hit patience zero with the goal incomplete. Completing the goal on the last remaining patience point still scores as complete. You will not add a sentiment score.

#### Approach

The persona is a pure function. Patience starts at three. The goal is a set of slots. The agent's utterances are classified by a rule: if they contain a slot name from the missing set, the persona reveals it and patience stays. Otherwise patience drops. The harness records the turn count, the ending patience, and the unfilled slots. A test uses a persona that reveals nothing unless asked, so an agent cannot score a point from the opening line alone unless the fixture says the opening line included a slot. Put that rule in the fixture file.

#### Components

| Piece | Role |
| --- | --- |
| Persona | Goal slots, patience, and a reveal rule. |
| Question classifier | Whether the utterance names a missing slot. |
| Terse agent | Asks only missing slots. |
| Rambling agent | Never names a slot. |

#### How it works

1. Implement the persona and the classifier.
2. Run the terse agent and expect completion with patience at or above one.
3. Run the rambling agent and expect an incomplete goal and patience zero.
4. Run a terse agent that finishes on the last patience point and expect complete.
5. Assert the report contains no sentiment or politeness field.

#### Tech stack

- Python 3.11 or newer
- Scripted persona and agents
- JSON report

#### Setup

1. Create `patience/` with `persona.py`, `harness.py`, and tests.
2. Run both agents.
3. Run the last-point fixture.
4. Run tests.

#### Deliverable

- The rambling agent fails by patience, not by a string match on the final answer alone.
- The terse agent completes the goal.
- Finishing on the last patience point counts as complete.
- The report fields are goal completion, unfilled slots, and ending patience.

#### Step ahead

Patience is harsher when the user is underspecified and friendlier when they volunteer facts. Add a second persona config, `impatient`, with patience 1, and run the same terse agent. The terse agent should still finish if the opening line volunteers one of two slots. Fixture a terse agent that asks for the volunteered slot again and show it failing under `impatient` while passing under the original patience of three. The follow-on is a grid of persona configs, not a new agent architecture.

### Day 76 — Case IDs that Never Change in Place

**Level:** Advanced

**Folder:** [atlas/06-proof-bench/day-76-immutable-case-ids/README.md](atlas/06-proof-bench/day-76-immutable-case-ids/README.md)

Store eval cases as immutable ids, and force an edit to mint a new id instead of rewriting history.

#### Concept

If you edit a gold answer and keep the case id, last month's score and today's score are not about the same question. This project stores cases in a directory of JSON files whose names are ids. A command `check` fails if a file's content hash does not match a ledger entry for that id. A command `revise` writes a new id, records `supersedes`, and leaves the old file untouched. Deleting a file is also a failure unless a tombstone entry says the id was retired. You will revise one case, run the scorer on a fake prediction file twice — once pinned to the old id set and once to the new — and show that the two score lines name their case-set hashes. The ledger is the product. The scores are there to prove you can still join them.

#### Approach

The ledger is `ledger.json` mapping id to sha256 and optional `supersedes` and `retired` fields. `check` exits non-zero on a hash mismatch and prints both hashes. `revise` refuses to overwrite. A test tampers with a gold string and expects `check` to fail. Another test runs `revise` and expects the old hash to remain. The scorer accepts a `--cases` ledger slice: `all` or `current`, where current means ids that are not superseded and not retired. Document that choice. Historical comparisons use the hash, not the word "latest."

#### Components

| Piece | Role |
| --- | --- |
| Case files | One JSON file per immutable id. |
| Ledger | Hashes, supersedes links, and retirements. |
| Check command | Fails when bytes drift under an existing id. |
| Revise command | Mints a new id and keeps the old file. |

#### How it works

1. Write three cases and a ledger by an `add` command that refuses existing ids.
2. Tamper with one file and show `check` failing.
3. Restore it by reverting the file, not by updating the hash in place.
4. Revise one case and show both ids present.
5. Score a prediction file against `current` and against an explicit list containing the old id.

#### Tech stack

- Python 3.11 or newer
- JSON ledger and case files
- Standard library `hashlib`

#### Setup

1. Create `case-ids/` with `cases.py` and tests.
2. Run add, check, a failed tamper, and revise.
3. Run tests.
4. Write the rule at the top of the README you keep in that folder: ids are immutable.

#### Deliverable

- Tampering fails `check` without changing the ledger.
- `revise` leaves the old file's bytes and hash intact.
- Scores name the case-set hash they used.
- `add` refuses to reuse an id.

#### Step ahead

Trend lines break when an id is superseded and a dashboard silently drops it. Add a migration report that lists old id, new id, and whether any prediction file still references the old id. Fixture a prediction file that cites a superseded id and show the report naming it as `unmapped` until you add an explicit map entry. The follow-on is a map you review, so a chart does not change denominator because a gold string was edited.

### Day 77 — A Flake Budget

**Level:** Advanced

**Folder:** [atlas/06-proof-bench/day-77-flake-budget/README.md](atlas/06-proof-bench/day-77-flake-budget/README.md)

Repeat a scripted eval many times, separate harness flake from decoder flake, and fail when the pass rate wanders too far.

#### Concept

A pass rate from one run is a coin flip if the decoder is stochastic. This project runs the same case set N times under two adapters. The stable adapter returns a fixed JSON answer and must produce a pass rate of 1.0 or 0.0 on every repeat, with zero variance. The shaky adapter flips a seeded coin inside the answer and produces a pass rate you can recompute. The harness records every repeat's pass bit, the mean, and the range. A flake budget says the stable adapter's range must be zero, and the shaky adapter's range must stay inside a band you set after computing the expected binomial spread for the seed. You are not building a release gate for a product and you are not estimating a confidence interval for a launch. You are measuring whether your harness itself invents noise.

#### Approach

N is 30 so the file stays small and the binomial expectation is easy to write down. The seed is fixed. The stable adapter ignores the seed's random draws. The shaky one uses `random.Random(seed)` and you document the expected number of passes. A bug that reads the system clock inside the stable path should fail the range check. Do not use the clock. The report has two sections, harness and decoder, and a test asserts the stable section's variance is zero. If you change N, update the expected shaky count in the same commit as the code.

#### Components

| Piece | Role |
| --- | --- |
| Repeat runner | N runs, fixed seed, recorded bits. |
| Stable adapter | Deterministic answers. |
| Shaky adapter | Seeded coin flip inside the answer. |
| Budget | Zero range for the stable adapter, a named band for the shaky one. |

#### How it works

1. Implement both adapters and the repeat runner.
2. Run N repeats and write `flake.json`.
3. Assert the stable range is zero.
4. Compute the shaky pass count from the seed by hand or with a one-line replica and assert it matches.
5. Document the budget in `budget.md` before quoting the shaky band.

#### Tech stack

- Python 3.11 or newer
- Standard library `random`
- JSON report

#### Setup

1. Create `flake/` with `adapters.py`, `repeat.py`, and tests.
2. Run both adapters.
3. Run tests.
4. Keep N at 30 in one constant.

#### Deliverable

- The stable adapter's pass bits are identical across repeats.
- The shaky adapter's pass count matches the seeded expectation.
- The report separates harness variance from decoder variance.
- The budget file states the allowed shaky band and the value of N.

#### Step ahead

Thirty repeats is arbitrary. Add a stopping rule that runs the shaky adapter until the running mean's Chebyshev bound, which you can compute from the observed variance without a statistics library, is inside a width you set, or until a max N of 200. Fixture a coin that is fair and show it stopping later than a coin that always passes. The follow-on is spending repeats where the bit actually moves, and the stable adapter must still stop at the minimum sample size because its variance is zero.

### Day 78 — Accepted Tool Sequences

**Level:** Advanced

**Folder:** [atlas/06-proof-bench/day-78-accepted-sequences/README.md](atlas/06-proof-bench/day-78-accepted-sequences/README.md)

Score a transcript's tool names against a set of accepted sequences, ignoring argument values.

#### Concept

Some tasks have more than one legal procedure and many illegal ones. Looking up a fee and then quoting is fine. Quoting and then looking up is not, if the rule is that quotes must follow a lookup. This project lists accepted tool-name sequences for a task. Argument values are ignored in the required score, because a separate harness already checks values. A transcript passes if its tool-name list matches one accepted sequence exactly. A prefix of an accepted sequence is a failure labeled `incomplete`, not a pass. An extra tool in the middle is `not-accepted`. You will write three transcripts covering pass, incomplete, and an inserted tool. The harness does not run tools. It reads names in order.

#### Approach

Accepted sequences live in `accepted.json` as a list of lists of strings. Matching is equality of the full list. You also compute the longest accepted sequence that is a prefix of the observed names, and report it, so an incomplete run is visible as "matched 2 of 3 of sequence 0" rather than as a mysterious fail. Inserted tools break every prefix at that index. Tests cover a second accepted sequence that is a different legal order, so the harness is not secretly requiring one path. Argument objects may be present in the transcript and must be ignored by the comparator. A test puts different arguments on a passing name sequence and expects a pass.

#### Components

| Piece | Role |
| --- | --- |
| Accepted file | A set of tool-name sequences. |
| Exact matcher | Full-list equality against any accepted sequence. |
| Prefix diagnostic | How far the observed list followed some accepted sequence. |
| Argument blindness | Values are not part of this score. |

#### How it works

1. Write two accepted sequences for one task.
2. Score a transcript for each sequence as a pass.
3. Score a prefix and expect `incomplete` plus the prefix diagnostic.
4. Score an inserted tool and expect `not-accepted`.
5. Change only arguments on a passing transcript and expect the verdict to stay a pass.

#### Tech stack

- Python 3.11 or newer
- JSON transcripts
- No tool execution

#### Setup

1. Create `sequences/` with `score.py`, `accepted.json`, and tests.
2. Run the four transcripts.
3. Run tests.
4. Note in the folder README that argument correctness is out of scope for this scorer.

#### Deliverable

- Both legal orders pass.
- A prefix is `incomplete` and not a pass.
- An inserted tool is `not-accepted` and the diagnostic names the index.
- Argument changes do not flip a pass to a fail.

#### Step ahead

Names-only scoring still passes a lookup with an empty query. Add an argument sketch: for each step, a set of required keys that must be present and non-empty, without specifying the values. Fixture a passing order whose lookup query is an empty string and expect a new status `missing-key` that does not replace `not-accepted`. A wrong order with all keys present should still be `not-accepted`. The follow-on is a sketch of arguments, not a return to exact string match on the fee code.

<a id="phase-07"></a>

## Phase 07: Flowroom: Analytics and Pipelines

**Days 79–90.** 12 projects.

### Goal

Finish this phase able to sessionize an event log, keep a rerunnable mart, track history, put labels next to features as of a cutoff, and backfill an embedding table without rewriting unchanged text.

### Skills covered

- Sessionization with late events
- Path analysis over help documents
- Cohort retention triangles
- Idempotent staging and marts in SQLite
- Slowly changing catalog history
- Tumbling window aggregates
- Freshness checks and backfill
- Point-in-time label joins
- Content-hashed embedding backfills
- Seasonal residual alerts
- Entity resolution with a review file
- Structured logs and an error budget

Turn raw events into sessions, marts, and features that can be rebuilt, with late data and stale rows called out instead of smoothed over.

By the end of the phase you should be able to: Build a small warehouse path you can rerun without double-counting or leaking the future.

### Day 79 — Sessions and Late Events

**Level:** Intermediate

**Folder:** [atlas/07-flowroom/day-79-sessions-and-late-events/README.md](atlas/07-flowroom/day-79-sessions-and-late-events/README.md)

Build rider sessions from an inactivity gap and show a late event that should extend a closed session.

#### Concept

A session is a decision about a gap, not a column in the source. Harbor Loop's app emits `app_open`, `search`, and `rental_complete` with event time and ingest time. Two events from the same rider belong to the same session when the gap is under 30 minutes. A job that closes the day at midnight will miss a 23:50 event that arrives the next morning and should have extended the last session. This project builds sessions from a fixture, writes session ids, and then applies a late event. You will show two outputs: the premature close, and the rebuilt sessions after the late event is included. The late event must change a session end time rather than becoming a new one-event session. Rebuilding from the full log is allowed. Mutating a closed session in place without a rebuild record is not.

#### Approach

Sort by rider and event time. Assign session ids with a counter that increments when the gap exceeds the threshold. The threshold is a constant. Late events are applied by concatenating them with the original log and recomputing, then writing a diff of session end times. A test plants a 20-minute-late completion after a search and expects the same session id. A test plants a 2-hour-late event and expects a new session. Use ingest time only to decide lateness relative to a close timestamp, not to order the session. Ordering uses event time. Write both clocks into the output so a reader can see which one you used.

#### Components

| Piece | Role |
| --- | --- |
| Event fixture | Rider events with event time and ingest time. |
| Gap rule | A named inactivity threshold. |
| Session builder | Deterministic ids from the sorted log. |
| Late diff | End times before and after the late event is included. |

#### How it works

1. Write a log with two riders and a known gap pattern.
2. Build sessions and lock the ids in a test.
3. Add a late in-gap event and recompute.
4. Assert the session count does not increase for that rider.
5. Add a late out-of-gap event and assert the session count increases.

#### Tech stack

- Python 3.11 or newer
- Standard library `csv` and `datetime`
- No warehouse server

#### Setup

1. Create `sessions/` with `events.csv`, `sessions.py`, and tests.
2. Run the builder twice, before and after the late file.
3. Run tests.
4. Record the threshold and the close timestamp in `notes.md`.

#### Deliverable

- In-gap late events extend a session.
- Out-of-gap late events start a new session.
- Ordering uses event time, and a test swaps ingest order to prove it.
- The diff file shows the end-time change rather than overwriting silently.

### Day 80 — Paths Through the Help Docs

**Level:** Intermediate

**Folder:** [atlas/07-flowroom/day-80-help-doc-paths/README.md](atlas/07-flowroom/day-80-help-doc-paths/README.md)

Count which help-doc sequences precede a resolved event, and ignore paths that never resolve.

#### Concept

Pageview counts flatter articles that people open and abandon. Harbor Loop's help center emits doc views and a `resolved` event when the rider marks the issue done. This project builds paths: ordered doc ids inside a session, ending at the first resolved, or ending unfinished if the session never resolves. You will report the top resolved paths and, separately, the top unfinished paths. A doc that appears in both is not "successful" just because it is popular. You will also refuse to count a path that skips across sessions. The fixture includes one doc that is common in unfinished paths and rare in resolved ones, and the report must not rank it as a success. This is path analysis, not a feature-adoption dashboard and not a model of whether the doc caused the resolution.

#### Approach

Start from the session ids you know how to build, or from a fixture that already has session ids so this day stays about paths. Collapse consecutive duplicate doc views. End a path at the first `resolved` inside the session. Docs after resolved are ignored and counted in a `tail` tally so you notice a tagging bug if the tail is large. Rank paths by resolved count with a minimum support of two so a unique path does not become a recommendation. Unfinished paths have their own table and are not used as the denominator of a success rate unless you also print the denominator. Write both tables.

#### Components

| Piece | Role |
| --- | --- |
| Session events | Doc views and resolved markers. |
| Path cutter | Stops at the first resolved event. |
| Resolved ranking | Paths with support at least two. |
| Unfinished ranking | A separate table, including the planted dead-end doc. |

#### How it works

1. Write a fixture with a dead-end doc and a short path that resolves.
2. Build paths per session.
3. Assert events after resolved do not extend the path.
4. Rank both tables.
5. Assert the dead-end doc is absent from the resolved ranking and present in the unfinished ranking.

#### Tech stack

- Python 3.11 or newer
- CSV fixtures
- No visualization library required

#### Setup

1. Create `paths/` with `events.csv`, `paths.py`, and tests.
2. Run the report and write `out/resolved.csv` and `out/unfinished.csv`.
3. Run tests.
4. State in the notes that the tables are descriptive, not causal.

#### Deliverable

- Resolved and unfinished paths are different files.
- The dead-end doc is not listed as a resolved success.
- Events after the first resolved marker do not change the path, and the tail count is reported.
- A path cannot contain events from two session ids, and a test mixes them to prove the cut.

### Day 81 — Retention Triangles

**Level:** Intermediate

**Folder:** [atlas/07-flowroom/day-81-retention-triangles/README.md](atlas/07-flowroom/day-81-retention-triangles/README.md)

Build a cohort retention triangle from signup week and activity week, and do not fill future weeks.

#### Concept

A retention chart that shows every cohort at week 4, including the cohort that signed up last week, is fiction. This project builds a triangle. Rows are signup cohorts by week. Columns are week 0 through week 4. A cell is the fraction of the cohort with at least one rental in that activity week. Cells in the future, relative to a `as_of` date you set, are null, not zero. Zero would say the riders churned. Null says the week has not happened. You will compute the triangle from a fixture that includes a cohort with a full history and a cohort that started near `as_of`. The report prints nulls as blank. A test expects a blank, and it fails if you write 0.

#### Approach

Signup week is the week of the rider's first event in a signup file, not the first event you happened to load if the file is filtered. Use the signup file as the source of the cohort so a late first rental does not move the rider. Activity is a set of weeks per rider. Cohort size is the number of riders in the signup week, including those with no later rentals. They count in the denominator. Week 0 includes the signup week itself. Document that. Pick ISO weeks and a single time zone, and parse every timestamp as aware UTC converted to that zone before you take the week.

#### Components

| Piece | Role |
| --- | --- |
| Signup file | Rider id and signup timestamp, the cohort source. |
| Activity file | Rentals after signup. |
| Triangle | Cohort by relative week, with nulls for the future. |
| As-of date | The clock the null rule uses. |

#### How it works

1. Build cohorts from the signup file.
2. Mark activity weeks per rider.
3. Fill cells up to the last completed week relative to `as_of`.
4. Leave future cells null and test one of them.
5. Include a rider with no activity and assert they remain in the denominator.

#### Tech stack

- Python 3.11 or newer
- Standard library `datetime` and `csv`
- A printed triangle in markdown or CSV

#### Setup

1. Create `retention/` with the two CSV files, `triangle.py`, and tests.
2. Run the triangle at a fixed `as_of` you store in `as_of.txt`.
3. Run tests.
4. Read the triangle and confirm the newest cohort has blanks on the right.

#### Deliverable

- Future cells are null, and a test rejects zeros in those cells.
- Inactive signups stay in the denominator.
- The as-of date is a file, not today's date from the clock.
- Week boundaries use one named time zone.

### Day 82 — Rerun-Safe Marts

**Level:** Intermediate

**Folder:** [atlas/07-flowroom/day-82-rerun-safe-marts/README.md](atlas/07-flowroom/day-82-rerun-safe-marts/README.md)

Load raw events into staging and a mart in SQLite so running the job twice does not double the totals.

#### Concept

A pipeline that inserts into a reporting table every time it runs will double last week's rentals the moment someone retries a failure. This project creates three layers in SQLite: `raw`, `staging`, and `mart_daily`. Raw is append-only and keyed by an event id. A second load of the same file inserts zero new raw rows. Staging is rebuilt from raw for the dates in the batch, deleting that date range inside the transaction and inserting again. The mart is rebuilt from staging for the same range. You will run the job twice and assert the daily totals match the first run. You will also add one new event and show only that day's total changing. The range delete is the whole trick. A job that only inserts cannot be retried.

#### Approach

Use the standard library `sqlite3`. Wrap the rebuild in a transaction. The batch range is an argument, not `select min(date), max(date)` from the whole raw table, because that would rebuild history you did not intend to touch. A test loads a file, loads it again, and checks a count. A second test extends the range and checks that an untouched day still has the same total. Primary keys on event id make the raw insert use `INSERT OR IGNORE`. Document that ignore is acceptable for exact duplicate ids and wrong for two different payloads with the same id. A test sends a conflicting payload and expects a recorded conflict, not a silent ignore. You may handle that second case by comparing a hash before ignore.

#### Components

| Piece | Role |
| --- | --- |
| Raw table | Append-only events with a primary key and a payload hash. |
| Staging rebuild | Delete-and-insert for a date range, inside a transaction. |
| Daily mart | Totals rebuilt from staging for the same range. |
| Conflict check | Same id with a different hash is reported, not ignored. |

#### How it works

1. Create the three tables.
2. Load a file and record daily totals.
3. Load the same file and assert totals are unchanged and raw row count is unchanged.
4. Load a new event on one date and assert other dates are unchanged.
5. Attempt a conflicting payload and assert it is rejected and counted.

#### Tech stack

- Python 3.11 or newer
- Standard library `sqlite3`
- SQL visible in the repository as strings or `.sql` files

#### Setup

1. Create `marts/` with `pipeline.py`, `schema.sql`, and tests.
2. Run the pipeline twice.
3. Run tests.
4. Point the notes at the transaction that deletes the range.

#### Deliverable

- A rerun does not change totals.
- A new event changes only its date.
- A conflicting duplicate id is not silently ignored.
- The batch date range is an explicit argument.

### Day 83 — Catalog History

**Level:** Intermediate

**Folder:** [atlas/07-flowroom/day-83-catalog-history/README.md](atlas/07-flowroom/day-83-catalog-history/README.md)

Store fee-code changes as dated rows so a question about last March does not see today's price.

#### Concept

A fee table with one row per code shows the price now. A support question about a rental in March needs the price that was in force in March. This project implements a small slowly changing dimension. Each fee code has rows with `valid_from` and `valid_to`. The current row has a null `valid_to`. When the price changes, you close the open row by setting `valid_to` to the change time and insert a new open row. You never update the price in place. A query function `fee_as_of(code, when)` returns the row whose interval contains `when`. You will change a fee twice and show three answers: before the first change, between the changes, and after the second. A test queries exactly at a boundary and documents whether `valid_from` is inclusive. Pick inclusive start and exclusive end, and test both sides of the boundary.

#### Approach

Do this in SQLite or in plain data structures backed by a CSV you can diff. The close-and-insert operation is one function. It rejects a change that would open a second current row. It rejects a `valid_from` earlier than the current row's `valid_from`. Historical rows are immutable: a test that tries to update an old price in SQL should not be part of the API. If you are tempted to add an update method, make it raise. Querying a time before the first row returns `unknown`, not the earliest price.

#### Components

| Piece | Role |
| --- | --- |
| Interval rows | `valid_from` inclusive, `valid_to` exclusive, one open row. |
| Change function | Closes the open row and inserts the new price. |
| As-of query | Returns the row containing a timestamp. |
| Boundary tests | Both sides of a change instant. |

#### How it works

1. Insert an initial fee.
2. Change it twice at known timestamps.
3. Query three times and lock the three prices.
4. Query exactly at `valid_to` of the first row and expect the second price.
5. Attempt a retroactive edit and expect a rejection.

#### Tech stack

- Python 3.11 or newer
- SQLite or CSV with a tiny query function
- Aware timestamps

#### Setup

1. Create `catalog-history/` with `fees.py` and tests.
2. Run the two changes and print the three as-of answers.
3. Run tests.
4. Write the inclusivity rule in one line at the top of `fees.py`.

#### Deliverable

- Three as-of queries return three prices.
- The boundary instant follows the inclusive-start exclusive-end rule.
- A second open row cannot be inserted for the same code.
- Times before the first version return `unknown`.

### Day 84 — Tumbling Windows on a File

**Level:** Intermediate

**Folder:** [atlas/07-flowroom/day-84-tumbling-windows/README.md](atlas/07-flowroom/day-84-tumbling-windows/README.md)

Aggregate an event file into fixed five-minute windows and put late events in a side bucket.

#### Concept

Streaming systems tumble, and so can a file if you are explicit about watermarks. This project reads dock events ordered by ingest time and assigns each event to a five-minute window on event time. A window closes when you have seen an ingest time more than ten minutes past the window end. Events for a closed window do not update the aggregate. They go to a late bucket with a count. You will fixture an event that arrives in order and one that arrives after its window has closed. The closed aggregate must stay fixed. This is not a distributed stream processor. It is the watermark rule, which is the part people skip when they copy a diagram.

#### Approach

Windows are aligned to epoch minutes so two runs agree. The watermark is the max ingest time seen so far minus the allowed lateness. An event is late when its window end is less than or equal to the watermark at the time it is processed. Processing order is ingest order, which the fixture should not make identical to event order. Print the open aggregates and the late count. A test processes a late event and asserts the window sum is unchanged and the late count increased by one. A second test puts an event inside the lateness allowance and asserts the sum increased.

#### Components

| Piece | Role |
| --- | --- |
| Aligned windows | Five-minute buckets with a defined origin. |
| Watermark | Max ingest time minus allowed lateness. |
| Aggregate | A count or a sum per window that freezes when the window closes. |
| Late bucket | Events that missed the watermark, counted and stored. |

#### How it works

1. Write events whose ingest order differs from event order.
2. Process them one by one, updating the watermark.
3. Close a window and then deliver a late event.
4. Assert the frozen sum and the late count.
5. Assert an event inside the allowance still updates the sum.

#### Tech stack

- Python 3.11 or newer
- Standard library only
- A fixture file, not a broker

#### Setup

1. Create `windows/` with `events.csv`, `tumble.py`, and tests.
2. Run the processor and write `out/windows.csv` and `out/late.csv`.
3. Run tests.
4. Document the window size and the lateness in one place.

#### Deliverable

- Late events do not change a closed window.
- Events inside the lateness allowance do change the open window.
- Window bounds are deterministic across two runs.
- The late file contains the late event id.

### Day 85 — Freshness and a Backfill

**Level:** Intermediate

**Folder:** [atlas/07-flowroom/day-85-freshness-backfill/README.md](atlas/07-flowroom/day-85-freshness-backfill/README.md)

Mark a mart table stale when its newest event is too old, then backfill a date without touching the others.

#### Concept

A dashboard that refreshes on open will still show Tuesday if the job has been failing since Tuesday. This project writes a freshness check for `mart_daily`: the maximum event date must be at least the as-of date minus one day. If it is older, the check fails with the observed maximum and the expected minimum. It does not fill the gap with zeros. You will then run a backfill for the missing date only, using the range rebuild from the mart day, and show the freshness check passing afterward. A backfill that rebuilds every historical day is a bug in this fixture, and a test counts how many dates were deleted. The allowed count is one.

#### Approach

Freshness is a function of the mart and an as-of date, returning a record with `ok`, `observed_max`, and `expected_min`. The job log records which dates were rebuilt. The test runs a pipeline that skipped a date, expects `ok` false, runs the backfill command with that date, and expects `ok` true. It also expects the other dates' totals to be byte-identical, which you can check by storing a hash of the untouched rows before and after. Do not implement alerting to a chat system. Print the record. The product is the check and the narrow backfill.

#### Components

| Piece | Role |
| --- | --- |
| Freshness function | Compares max event date to the as-of date. |
| Failure record | Observed max and expected min, no invented zeros. |
| Backfill command | Rebuilds one date range. |
| Untouched-row hash | Proves other dates did not change. |

#### How it works

1. Load a mart with a missing latest date.
2. Run freshness and expect failure.
3. Backfill that date only.
4. Hash the other dates before and after and assert equality.
5. Run freshness again and expect success.

#### Tech stack

- Python 3.11 or newer
- SQLite mart from the previous pipeline day, or a smaller stand-in
- JSON freshness record

#### Setup

1. Create `freshness/` with `fresh.py` and tests.
2. Run the fail, the backfill, and the pass.
3. Run tests.
4. Write the expected lag, one day, as a named constant.

#### Deliverable

- A stale mart fails the check and does not gain zero rows from the check itself.
- Backfill rebuilds one date.
- Hashes of untouched dates match.
- The success record still includes the observed max, not only a boolean.

### Day 86 — Labels Joined as Of

**Level:** Intermediate

**Folder:** [atlas/07-flowroom/day-86-labels-as-of/README.md](atlas/07-flowroom/day-86-labels-as-of/README.md)

Attach a training label to a feature row using only events inside a window that starts after the cutoff.

#### Concept

Day 9 built features that do not peek. This project is the join you would actually schedule. Each decision row has a rider and a cutoff. Features are aggregates of events at or before the cutoff. The label is 1 if any `overrun` event occurs in `(cutoff, cutoff + 7 days]`. The SQL or the Python join must not use a label window that overlaps the feature window. You will write the query, explain the inequality, and plant one overrun exactly at the cutoff and one a second after. The first is a feature event, not a positive label. The second is a positive label and not a feature. A sloppy `<=` on both sides double-counts that second. A sloppy pair of `<=` on the cutoff double-counts the first. Tests cover both edges.

#### Approach

Prefer SQLite so the predicate is visible in one query with two joins or two subqueries. Name the predicates in comments. The output table contains `rider_id`, `cutoff`, feature columns, and `label`. A rider with no events before the cutoff still gets a row if they are in the decision list, with null features, and can still have a positive label. Dropping them biases the set toward riders you already know. Assert a decision row with only a future overrun survives with null `rides_so_far` and label 1.

#### Components

| Piece | Role |
| --- | --- |
| Decision list | Rider and cutoff pairs, including a rider with no history. |
| Feature predicate | Events at or before the cutoff. |
| Label predicate | Events strictly after the cutoff and at or before cutoff plus seven days. |
| Edge fixtures | An event exactly at the cutoff and an event one second later. |

#### How it works

1. Load events and decisions into SQLite.
2. Run the feature query and the label query as two named SQL strings.
3. Join them on rider and cutoff.
4. Assert the two edge events land in different columns.
5. Assert the history-free rider remains in the output.

#### Tech stack

- Python 3.11 or newer
- SQLite
- SQL files you can read without running Python

#### Setup

1. Create `as-of-labels/` with `label.sql`, `features.sql`, `join.py`, and tests.
2. Run the join and inspect `out/training_rows.csv`.
3. Run tests.
4. Add a one-line comment on each inequality.

#### Deliverable

- The event at the cutoff affects features and not the label.
- The event one second later affects the label and not the features.
- A decision row with no history is kept.
- The SQL files contain the predicates the tests are about.

### Day 87 — An Embedding Job that Skips Unchanged Text

**Level:** Advanced

**Folder:** [atlas/07-flowroom/day-87-embedding-backfill/README.md](atlas/07-flowroom/day-87-embedding-backfill/README.md)

Backfill chunk embeddings keyed by content hash and model id, and skip rows whose hash is already stored.

#### Concept

Re-embedding a handbook on every build burns time and, when the model is hosted, money. It also mixes vectors from two models in one column if you are not careful. This project stores embeddings in a table keyed by chunk id, content hash, and model id. The job embeds a chunk only when that triple is missing. A text change changes the hash and produces a new row. The old row stays so you can compare. A model id change produces a new row even if the text is identical. The search path must filter to one model id, and a test expects it to ignore the other model's vector. You will run the job twice and show the second run embedding zero chunks. This is a batch data job. It is not a vector database product pitch.

#### Approach

Use the hashing embedder so the job runs offline. The hash is SHA-256 of the chunk text bytes. The job writes a log line per chunk: `embedded` or `skipped`, with the reason. A test changes one character, expects one `embedded` and the rest `skipped`, and expects two rows for that chunk id. The reader function `vectors_for(model_id)` returns only that model. If the caller omits the model id, it raises. Silent mixing is the bug. Keep the log. The skip decision should be testable without re-reading the whole table by eye.

#### Components

| Piece | Role |
| --- | --- |
| Embedding table | Chunk id, content hash, model id, vector. |
| Skip rule | Do nothing when the triple already exists. |
| Append-on-change | New hash or new model id adds a row and keeps the old one. |
| Reader filter | Requires a model id and will not mix. |

#### How it works

1. Embed a three-chunk handbook with model id `hash-v1`.
2. Run the job again and assert zero embeds.
3. Edit one chunk and assert a single embed and two stored rows for that id.
4. Run with model id `hash-v2` and assert three new rows.
5. Assert a reader call without a model id raises, and a call with `hash-v1` does not return `hash-v2` vectors.

#### Tech stack

- Python 3.11 or newer
- SQLite and the hashing embedder
- A job log of embedded versus skipped

#### Setup

1. Create `embed-backfill/` with `job.py` and tests.
2. Run the sequence of four job states.
3. Run tests.
4. Record the model id naming rule in the notes: changing the hash function means a new model id.

#### Deliverable

- The second run skips every chunk.
- A one-character edit embeds one chunk and retains the previous row.
- Two model ids never appear in one reader result.
- Omitting the model id raises.

#### Step ahead

A chunk that disappears from the handbook should not remain searchable forever. Add a tombstone step: after a run, rows whose chunk id is absent from the current source and whose model id is the one you are building are marked `retired` with a timestamp, not deleted. The reader skips retired rows. Fixture a deleted chunk and show that its vector is still in the table and absent from search results. The follow-on is reversible retirement, so you can explain a missing hit, rather than a silent delete.

### Day 88 — Seasonal Residuals

**Level:** Advanced

**Folder:** [atlas/07-flowroom/day-88-seasonal-residuals/README.md](atlas/07-flowroom/day-88-seasonal-residuals/README.md)

Alert when a daily rental count departs from a weekday baseline, and suppress dates you listed in advance.

#### Concept

A raw spike on Saturday is not news if Saturdays are always busy. This project builds a baseline for daily completed rentals: the median of the same weekday over the previous eight weeks, computed only from dates before the day you are scoring. The residual is the day's count minus that median. An alert fires when the residual exceeds a threshold you set in advance. You will plant one holiday that looks like an alert and, in the step that is still the core project, let it alert. The suppression list comes in the follow-on. For the core, you will also plant a true quiet Tuesday that should alert, and a normal Saturday that should not. This is a residual check on a metric series. It is not a feature-drift monitor and it does not recommend retraining a model.

#### Approach

The series is a CSV of date and count that you generate with a weekday pattern plus two anomalies. The baseline function refuses to use the current day or any later day. A test passes future dates into the frame and asserts the baseline for a Wednesday does not change when a later Wednesday is huge. The threshold is a constant in `threshold.txt`. Alerts are rows in `alerts.csv` with the date, the median, the count, and the residual. No alert row means no alert. Do not emit a score for every day and call them all alerts.

#### Components

| Piece | Role |
| --- | --- |
| Weekday median | Eight prior matching weekdays, looking only backward. |
| Residual | Count minus median. |
| Threshold file | Written before you interpret alerts. |
| Alert file | Only the days that crossed the threshold. |

#### How it works

1. Generate eight weeks of patterned counts plus a quiet Tuesday and a busy holiday Monday.
2. Compute baselines and assert a future leak does not change an earlier baseline.
3. Write alerts using the threshold.
4. Assert the normal Saturday is absent and the quiet Tuesday is present.
5. Leave the holiday in the alert file for the core project and mention it in the notes as the known nuisance.

#### Tech stack

- Python 3.11 or newer
- Standard library `statistics` and `datetime`
- CSV inputs and outputs

#### Setup

1. Create `residuals/` with `series.csv`, `baseline.py`, and tests.
2. Set the threshold before running alerts.
3. Run the job and the leak test.
4. Run tests.

#### Deliverable

- The baseline for a day does not depend on later days.
- The quiet Tuesday alerts and a normal Saturday does not.
- The holiday Monday is listed as a nuisance in the notes, and it does alert in the core output.
- Non-alerting days are absent from `alerts.csv`.

#### Step ahead

Add `calendar.csv` of dates that should not alert, written before you rerun, and suppress those dates with a reason `calendar` stored in a separate file from the real alerts. The quiet Tuesday must remain a real alert. A date on the calendar that would not have alerted anyway should not appear as a suppression, so you do not inflate how useful the calendar is. The follow-on is a suppression log you can audit, not a deleted residual.

### Day 89 — Borderline Entity Matches

**Level:** Advanced

**Folder:** [atlas/07-flowroom/day-89-borderline-matches/README.md](atlas/07-flowroom/day-89-borderline-matches/README.md)

Match rider records across two files with a score, and send only the borderline band to a review sheet.

#### Concept

Two exports call the same rider different names. A greedy match will either merge strangers or drop true pairs. This project scores candidate pairs from two files using rules you can read: exact email, exact phone, and a normalized name similarity you implement with a simple token Jaccard. High scores auto-link. Low scores are ignored. A middle band is written to `review.csv` with the two ids, the score, and the reason codes that fired. You do not auto-link the middle. You will plant one true pair that differs by a nickname and one false pair that shares a last name only. The true pair should land in review or in auto-link according to thresholds you set before seeing the result, and the false pair must not auto-link. The review file is the product. A silent merge is the failure.

#### Approach

Blocking: only compare pairs that share a phone, an email, or a last-name token, so you do not score the full cross product. Say so, because blocking can miss a pair with no shared token. Plant one true pair with no shared block key and show it absent from review. That miss belongs in the notes. Thresholds live in `thresholds.json` with `auto` and `review` cutoffs. Auto requires the score to be greater than or equal to `auto`. Review is the half-open band `[review, auto)`. Below `review` is drop. A test constructs three scores and expects three different destinations.

#### Components

| Piece | Role |
| --- | --- |
| Blocker | Candidate pairs that share a strong token. |
| Scorer | Email, phone, and token Jaccard, combined by rules you write down. |
| Thresholds | Auto, review, and drop. |
| Review sheet | Borderline pairs only. |

#### How it works

1. Write two small files with the planted pairs, including the unblockable true pair.
2. Generate candidates and scores.
3. Route each candidate to auto, review, or drop.
4. Assert the last-name-only pair is not auto-linked.
5. Assert the unblockable true pair appears in a `missed_blocks` note and not in the review sheet.

#### Tech stack

- Python 3.11 or newer
- CSV and JSON
- No external matching library

#### Setup

1. Create `entities/` with `left.csv`, `right.csv`, `match.py`, and tests.
2. Set thresholds before the run you will quote.
3. Run the matcher.
4. Run tests.

#### Deliverable

- The three destinations are tested with constructed scores.
- The false pair is not auto-linked.
- The review sheet contains only the middle band.
- The unblockable true pair is reported as a block miss, not quietly dropped.

#### Step ahead

Review decisions should feed the next run. Add `decisions.csv` with pair id and `link` or `reject`, and make the matcher honor a decision even when the score would have routed the pair differently. A later score change must not auto-link a pair a human rejected. Fixture a rejected pair whose score rises above the auto threshold and assert it stays unlinked, with reason `human-reject`. The follow-on is a decision that outranks the score.

### Day 90 — Logs and an Error Budget

**Level:** Advanced

**Folder:** [atlas/07-flowroom/day-90-error-budget-logs/README.md](atlas/07-flowroom/day-90-error-budget-logs/README.md)

Parse structured logs into typed events and compute an error budget for a single route.

#### Concept

Free-text logs do not become a reliability number by being searched. This project defines a log line schema: timestamp, level, route, status, and request id. A parser accepts lines that match and sends the rest to `rejected.log` with a reason. You will compute, for one route, the fraction of requests with status 500 over a day, and compare it to a budget of one percent. A day over budget is a row in `budget_breach.csv`. A day with too few requests, under a minimum you set, is `insufficient`, not a breach and not a success. You will fixture both a breach and a quiet day. This is a log mart for one service. It is not a tracing product and it does not join spans across services yet.

#### Approach

Write the parser so a line with an extra field is rejected rather than partially used, or accept extra fields and document which. Pick one. A missing status is a reject. Counts group by route and date. The budget comparison runs only when the request count is at least the minimum. Use integers and a ratio you compute from counts, and store the counts in the output so a reader can recompute the ratio. A test with 1 failure out of 10 requests is a breach if the minimum is 10 and the budget is one percent... that would be 10 percent, which breaches. Also test 0 failures out of 5 as insufficient when the minimum is 10.

#### Components

| Piece | Role |
| --- | --- |
| Line parser | Typed fields and a reject file. |
| Route-day counts | Requests and errors from accepted lines only. |
| Minimum sample | Days below it are insufficient. |
| Breach file | Days over the error budget, with counts. |

#### How it works

1. Parse a fixture containing one bad line and several good lines.
2. Assert the bad line is in the reject file and not in the counts.
3. Compute two days: one breach and one insufficient sample.
4. Assert the quiet small day is not a breach.
5. Recompute the ratio from the stored counts in a test.

#### Tech stack

- Python 3.11 or newer
- Plain text logs and CSV outputs
- No log vendor SDK

#### Setup

1. Create `error-budget/` with `app.log`, `parse.py`, and tests.
2. Run the parser and the budget step.
3. Run tests.
4. Write the budget and the minimum sample at the top of the report.

#### Deliverable

- Malformed lines are excluded from the ratio.
- A small sample is `insufficient`, not healthy and not a breach.
- A breach row contains the counts needed to recompute the ratio.
- The route filter is explicit, and another route's errors do not enter the ratio.

#### Step ahead

A request that fails and is retried under a new request id inflates the error rate. Add an optional `root_request_id` field. When it is present, count unique root ids rather than lines. Fixture three lines that share a root id, two of them errors, and show the line-based rate and the root-based rate side by side. The follow-on does not delete the line-based rate. It shows how a retry policy changes the budget math, and days without root ids keep the line-based definition.

<a id="phase-08"></a>

## Phase 08: Frontier Lab

**Days 91–100.** 10 projects.

### Goal

Finish this phase with a capstone handbook agent that retrieves, spends a budget, and replays from a cassette, plus a set of small studies: verifiers, schemas, prefix cost, a narrow small model, a read-only tool protocol, and a comparison of full context against retrieval.

### Skills covered

- Test-time retries gated by a verifier
- Schema-constrained output versus parse-and-repair
- Prefix-reuse accounting
- A small local classifier compared with a teacher
- A read-only tool protocol over local notes
- Long-context prompts versus retrieval on one corpus
- Reading a chart fixture against an expected number
- Task envelopes between processes
- A cheap proposer and a strong confirmer
- A capstone run with evidence attached

Practice the system patterns that showed up after plain chat: verifiers, constrained output, prefix reuse, small models, tool protocols, and a capstone that cites its own evidence.

By the end of the phase you should be able to: Explain a recent system pattern by building a small, testable version of it.

### Day 91 — Retry Under a Verifier

**Level:** Advanced

**Folder:** [atlas/08-frontier-lab/day-91-retry-under-a-verifier/README.md](atlas/08-frontier-lab/day-91-retry-under-a-verifier/README.md)

Let a scripted model retry until a verifier accepts the format, and stop when the budget is spent.

#### Concept

Spending more inference on a hard question only helps if you can reject a bad attempt. This project defines a verifier that accepts a string only when it is a single fee line matching a pattern: a code, an amount, and a unit. A scripted generator produces a sequence of attempts, some malformed. The loop keeps the first accepted attempt and records how many tries it used. If the budget runs out, it returns `unverified` and does not return the last bad string as if it were an answer. You will compare that policy to a one-shot policy that returns the first attempt even when the verifier would fail it. On a fixture where the first attempt is malformed and the second is valid, the retry policy must be the only one that answers. This is test-time compute with an explicit budget, not a claim that a larger model would have gotten the fee right.

#### Approach

The generator is a list of strings per question, which stands in for successive samples. The verifier is a pure function. The budget is an integer on the case. The loop never calls the verifier more times than the budget, and a test uses a generator longer than the budget whose only valid line sits past the budget. That case must end `unverified`. Log every attempt and the verifier's reason. Do not add a model. The lesson is the control flow: generate, check, stop.

#### Components

| Piece | Role |
| --- | --- |
| Verifier | A pure accept or reject with a reason. |
| Attempt list | Scripted stand-in for successive samples. |
| Budget | Maximum verifier calls. |
| One-shot contrast | Returns the first attempt without verification. |

#### How it works

1. Implement the verifier and test it on a valid and an invalid line.
2. Run the retry loop on a case that succeeds on attempt two.
3. Run a case whose only valid attempt is past the budget.
4. Compare to one-shot on the first case and assert the outputs differ.
5. Assert the unverified case does not include the rejected strings in the answer field.

#### Tech stack

- Python 3.11 or newer
- Scripted attempt lists
- No hosted model

#### Setup

1. Create `verifier-retry/` with `verify.py`, `loop.py`, and tests.
2. Run the three cases.
3. Run tests.
4. Write the budget next to the case id in the output.

#### Deliverable

- A later valid attempt is returned and earlier rejects are only in the log.
- A valid attempt past the budget yields `unverified` and an empty answer.
- One-shot and retry disagree on the planted malformed-first case.
- Verifier call count never exceeds the budget.

#### Step ahead

Majority vote across attempts can accept a wrong fee that is well formatted. Add a second verifier that checks the amount against a table, and compare vote-of-three to verifier-accept on a fixture where two attempts agree on a wrong amount and one attempt is right and formatted. Voting picks the wrong amount. The table verifier picks the right one or abstains. The follow-on shows a case where agreement is not evidence, and records both decisions without averaging them.

### Day 92 — Constrained JSON Versus Repair

**Level:** Advanced

**Folder:** [atlas/08-frontier-lab/day-92-constrained-json/README.md](atlas/08-frontier-lab/day-92-constrained-json/README.md)

Emit a tiny JSON object under a schema you enforce during decoding, and compare it to parsing and repairing free text.

#### Concept

Models that are asked for JSON often add a preamble or a trailing comma. Repair functions hide that by being clever, and they also hide when the model never produced the field you needed. This project implements a tiny constrained decoder over a vocabulary of tokens you define, including braces, keys, and a closed set of values. The decoder may only emit a token the schema allows in the current state. You will also implement a repair function that strips a preamble and trailing commas. On a scripted unconstrained token stream that is almost JSON, repair succeeds. On a stream that omits the required fee key, repair must fail rather than insert a default. The constrained decoder must be unable to omit the key because the state machine never reaches done without it. The comparison is the artifact.

#### Approach

The schema is one object with a required `code` from a fixed set and a required `amount` integer. The constrained decoder is a state machine, not a general JSON Schema validator bolted on after the fact. It chooses the only legal next token when the scripted model proposes an illegal one, and it logs the override. If you would rather have it stop on an illegal token, pick that behavior and test it, but do not silently skip a required key. The repair path is separate and is not called by the constrained path. A test feeds the repair path a missing-key string and expects an error. A test feeds the constrained decoder a proposal to emit `done` too early and expects a refusal or an inserted required key that is logged as an override. Prefer refusal if insertion feels like inventing a value. Refusal is the better default.

#### Components

| Piece | Role |
| --- | --- |
| Schema state machine | Legal tokens from the current state. |
| Constrained decoder | Refuses illegal tokens and logs them. |
| Repair function | Strips preamble and trailing commas, and does not invent keys. |
| Missing-key fixture | Repair fails, constrained decoding cannot finish early. |

#### How it works

1. Write the state machine and a diagram of states in the notes.
2. Decode a fully legal proposal and expect no overrides.
3. Propose an early finish and expect refusal.
4. Repair a trailing-comma string and expect success.
5. Repair a missing-key string and expect failure.

#### Tech stack

- Python 3.11 or newer
- A token vocabulary you define
- No grammar library required

#### Setup

1. Create `constrained/` with `decode.py`, `repair.py`, and tests.
2. Run both paths on the shared fixtures where both apply.
3. Run tests.
4. State in the notes that repair and constrained decoding are different policies.

#### Deliverable

- The constrained decoder never emits an object missing `code` or `amount`.
- Repair does not invent a missing key.
- A trailing comma is repairable and is unnecessary on the constrained path.
- Overrides or refusals are logged rather than dropped.

#### Step ahead

Schemas change. Add a version field and a decoder that refuses a v1 stream when asked for v2, where v2 requires `currency`. Show a repaired v1 object, which is valid JSON, failing a v2 check. The follow-on is that valid JSON is not the same as the object your caller required, and the version is part of the contract rather than a comment in the prompt.

### Day 93 — Accounting for a Shared Prefix

**Level:** Advanced

**Folder:** [atlas/08-frontier-lab/day-93-prefix-accounting/README.md](atlas/08-frontier-lab/day-93-prefix-accounting/README.md)

Measure how many prompt tokens a shared system prefix would reuse, and invalidate the reuse when the tool list changes.

#### Concept

A long system prompt that is identical across calls is work you should not pay for twice. Hosted APIs expose prefix caching. You may not have one. This project accounts for reuse without claiming to be the vendor's cache. You hash the prefix tokens. A second call with the same hash records `reused_tokens` equal to the prefix length and `new_tokens` equal to the suffix. A call with a different hash records the full prompt as new. You will show a batch of ten questions with a shared handbook preamble where the reused fraction is high, then change one tool description in the preamble and show the hash changing for every question. The study is the invalidation. A cache that ignores a tool-list edit will serve instructions you no longer mean.

#### Approach

Tokenization can be whitespace or your byte-pair encoder. The account function does not talk to a network. It returns a record per call. The batch report sums reused and new tokens. A test runs the same prefix twice and expects the second call's reused count to equal the prefix length. A test flips one character in a tool description and expects reused tokens to be zero for the next call. Do not implement an actual KV cache. If you describe one in the notes, label it as a picture of why the hash exists, not as something you built.

#### Components

| Piece | Role |
| --- | --- |
| Prefix hash | Hash of the token ids before the question. |
| Account record | Reused tokens and new tokens per call. |
| Shared-preamble batch | Ten questions, one prefix. |
| Invalidation edit | A one-character tool-list change that zeros reuse. |

#### How it works

1. Tokenize a preamble and ten questions.
2. Account the batch and record the reused fraction.
3. Edit the preamble and account again.
4. Assert reuse collapsed.
5. Assert a repeated identical call reuses the prefix.

#### Tech stack

- Python 3.11 or newer
- Your tokenizer or a whitespace tokenizer
- JSON report of token accounts

#### Setup

1. Create `prefix-account/` with `account.py` and tests.
2. Run both batches.
3. Run tests.
4. Write the reused fraction in `notes.md` and the fraction after the edit.

#### Deliverable

- Identical prefixes reuse the prefix length on the second call.
- A one-character preamble edit zeros reuse.
- The report sums match the sum of the rows.
- The notes do not claim you implemented a vendor cache.

#### Step ahead

Tool results also get prepended, and caching them is wrong when the tool output changes. Extend the hash so the cached region is only the stable preamble, and tool results are always new tokens even if the text matches the previous call. Fixture two calls with the same preamble and the same tool result text and show the tool-result tokens counted as new. The follow-on draws a boundary: reused instructions, fresh observations.

### Day 94 — A Small Model for a Narrow Label

**Level:** Advanced

**Folder:** [atlas/08-frontier-lab/day-94-narrow-small-model/README.md](atlas/08-frontier-lab/day-94-narrow-small-model/README.md)

Train a tiny local classifier on labels from a teacher script, and list the cases where the student disagrees.

#### Concept

A large model is an expensive way to map a dock note to `maintenance` or `billing` if a small classifier can do it. This project writes a teacher as a rule list that labels notes, trains a bag-of-words logistic model or a linear model you already built, and compares the student to the teacher on a held-out set of notes you wrote. The teacher is not a hosted model and not a synthetic-data release. It is a stand-in with known rules, so you can see the student's errors. You will report agreement, and you will list every disagreement with the note text. You will not claim the student is safe to deploy. You will say what the student is allowed to do: suggest a label next to the note, with the disagreement list as the review queue.

#### Approach

The teacher rules are ordered and readable. The student trains only on the train split. The test split is notes the training loop never sees. Use the rider-level or note-level split you already understand, and do not let a near-duplicate sit in both splits. A test plants a duplicate and expects the splitter to keep both copies on one side. Agreement is exact label match. The disagreement file is the deliverable a person would read. If agreement is perfect, add notes the rules label for a subtle reason and the bag of words is likely to miss, such as a short negation. Do not stop at a perfect score on easy notes.

#### Components

| Piece | Role |
| --- | --- |
| Teacher rules | An ordered, readable labeling function. |
| Student model | A small local classifier trained on the teacher's train labels. |
| Held-out notes | Written by you, disjoint from training. |
| Disagreement list | Every note where student and teacher differ. |

#### How it works

1. Write the rules and thirty notes. Split them.
2. Label the train notes with the teacher and fit the student.
3. Score the test notes.
4. Write every disagreement.
5. Assert a planted duplicate cannot land in both splits.

#### Tech stack

- Python 3.11 or newer
- Your linear classifier or a few dozen lines of new code
- Local text only

#### Setup

1. Create `small-label/` with `teacher.py`, `train.py`, and tests.
2. Run training and the report.
3. Run the duplicate-split test.
4. State the allowed use of the student in the first line of the notes.

#### Deliverable

- Train notes and test notes are disjoint, including near-duplicates you planted.
- The disagreement list is complete relative to the test set.
- The teacher rules are readable without running the model.
- The notes name what the student is not allowed to do.

#### Step ahead

The student can be confidently wrong. Add a score, the predicted probability, and send only disagreements above a probability you choose to a `priority_review` list. Low-probability disagreements stay in the full list and out of the priority list. Fixture one high-probability miss and one low-probability miss. The follow-on is a review queue ordered by how sure the student was, not a claim that the probability is calibrated.

### Day 95 — A Read-Only Field Notebook Protocol

**Level:** Advanced

**Folder:** [atlas/08-frontier-lab/day-95-field-notebook-protocol/README.md](atlas/08-frontier-lab/day-95-field-notebook-protocol/README.md)

Expose local markdown notes through two tools, search and get, with a schema and no write path.

#### Concept

Agents need a narrow way to read your notes. This project defines a small protocol: a process receives a JSON request and returns a JSON response. The only methods are `search` and `get`. `search` takes a query and returns heading matches with ids. `get` takes an id and returns that section's text. There is no method that writes, deletes, or shells out. A request with method `write` returns an error code `unknown-method` and does not touch the filesystem except to append a log line if you choose to log. You will implement the server in one module and a client function that sends a request dict. Transport can be in-process. The protocol shape is what you are practicing, the same shape a Model Context Protocol server uses, without building a price tracker or a review scraper.

#### Approach

The notebook is a folder of markdown files with headings. Ids are stable: file path plus heading slug. `search` is BM25 or a simple substring scan over headings, and you document which. `get` returns the section body and refuses an id it did not issue. A test calls `get` with a path traversal such as `../secrets.md` and expects an error, not a file read outside the notebook root. Resolve ids through a table you built, not through string concatenation onto a base path. That choice is the security-relevant part of an otherwise read-only toy, and the test is required.

#### Components

| Piece | Role |
| --- | --- |
| Request schema | Method name and arguments. |
| Search method | Returns ids and headings from the notebook only. |
| Get method | Returns a section by an issued id. |
| Unknown-method error | Any other method, including write. |

#### How it works

1. Index the notebook into an id table.
2. Serve `search` and `get` in-process.
3. Reject `write` without changing a source file's mtime. A test can record mtimes.
4. Reject a traversal id.
5. Log requests as method names only, without dumping full section bodies into the log.

#### Tech stack

- Python 3.11 or newer
- Local markdown notebook
- JSON requests and responses

#### Setup

1. Create `notebook-protocol/` with `server.py`, `notebook/`, and tests.
2. Run a scripted client session: search, then get.
3. Run the rejection tests.
4. Describe the two methods in `protocol.md` in a few lines a caller could implement.

#### Deliverable

- Search then get returns a real section from your notebook.
- `write` does not modify source files.
- An id outside the issued table does not read an arbitrary path.
- The log does not store full section bodies.

#### Step ahead

A write path will be requested. Add a third method, `propose_edit`, that writes a patch file under `proposals/` and never modifies the notebook. The patch file contains the id and the suggested text. A test asserts the notebook file hash is unchanged and the proposal file exists. `propose_edit` on an unknown id writes nothing. The follow-on is a suggestion that cannot be confused with a saved edit.

### Day 96 — Window Versus Index

**Level:** Advanced

**Folder:** [atlas/08-frontier-lab/day-96-window-versus-index/README.md](atlas/08-frontier-lab/day-96-window-versus-index/README.md)

Answer the same questions from the full handbook in the prompt and from retrieval, and compare citations and cost.

#### Concept

If the handbook fits in the window, retrieval can look like extra machinery. It stops looking that way when the handbook grows or when the model quotes a sentence from the wrong section because the whole text was in front of it. This project runs the same ten questions two ways. The window condition pastes the full handbook into the prompt of a scripted reader that searches the pasted text with the same quote rules as the index condition. The index condition uses your BM25 stack and quotes a chunk. Both must return a quote or an abstention. You will compare exact gold-span hits and a fictional token cost: the window condition pays for the whole handbook every time, and the index condition pays for the retrieved chunks. You are not measuring a hosted model's reading skill. You are measuring the two pipelines.

#### Approach

Use a handbook small enough to paste. Gold spans are the ones you marked earlier. The scripted reader returns the first sentence in its context that passes the coverage threshold, or abstains. Giving both conditions the same reader means the difference is the context they saw, not a different answering policy. Cost numbers are fictional and labeled. A results table has one row per question per condition. A question the index misses and the window hits is interesting, and so is the reverse if a chunk boundary is why. Write both if they occur. If they do not, say so rather than inventing a miss.

#### Components

| Piece | Role |
| --- | --- |
| Shared reader | Quote-or-abstain over whatever text it was given. |
| Window condition | Full handbook as context. |
| Index condition | Retrieved chunks as context. |
| Cost model | Fictional token prices labeled as fictional. |

#### How it works

1. Run the ten questions under both conditions.
2. Score gold-span hits.
3. Sum fictional costs.
4. List questions where the conditions disagree.
5. Write the table and a short interpretation that cites the table.

#### Tech stack

- Python 3.11 or newer
- Your handbook, BM25, and quoter
- A CSV comparison

#### Setup

1. Create `window-vs-index/` with `compare.py` and the handbook.
2. Run both conditions.
3. Run a test that the shared reader is the same function object or the same module path for both. Do not fork the policy.
4. Label costs as fictional in the table header.

#### Deliverable

- Every question has two rows.
- Disagreements are listed or explicitly absent.
- Costs are reproducible from the token counts in the table.
- Both conditions use the same quote rule.

#### Step ahead

Grow the handbook by duplicating background sections until the window cost exceeds a budget you set, while the index cost stays flat. Record the smallest size where the window condition is over budget and the index condition still answers. That size is the crossover in your notes. If the index starts to miss because duplicates drowned BM25, record that too. The follow-on is the point where pasting everything stops being the default, measured on your corpus rather than assumed from a blog post.

### Day 97 — A Chart with an Expected Peak

**Level:** Advanced

**Folder:** [atlas/08-frontier-lab/day-97-chart-peak/README.md](atlas/08-frontier-lab/day-97-chart-peak/README.md)

Read a chart you render to SVG, answer the peak with a tolerance, and refuse a chart whose axis is cut.

#### Concept

People paste charts into chats and ask for the peak. The model answers with a number that is hard to audit. This project renders a tiny bar chart to SVG from a data table, then answers "what is the peak" by reading the SVG's data attributes, not by eyeballing pixels. The expected answer is the max value in the table, and the tolerance is zero because you control the source. A second chart cuts the axis so the bars start at a non-zero baseline. The required behavior is to refuse with reason `cut-axis`, because a visual comparison would mislead, even though the data attribute still holds the true value. You will test both. The point is an answer policy for a figure, not a vision-model benchmark.

#### Approach

The SVG writer puts `data-value` and `data-baseline` on each bar. The reader refuses if any baseline is not zero. Otherwise it returns the max `data-value` and the category. A test tampers with a `data-value` so it no longer matches the source table and expects the reader to fail a consistency check you also run: every data value must appear in the source table. That check stops a chart that was edited by hand from being treated as authoritative over the table. The table remains the source of truth. The SVG is a view.

#### Components

| Piece | Role |
| --- | --- |
| Table source | Categories and values. |
| SVG writer | Bars with data attributes and a baseline. |
| Reader | Returns the peak or a refusal. |
| Consistency check | Data attributes must match the table. |

#### How it works

1. Render a normal chart and read the peak.
2. Assert the category and the value match the table max.
3. Render a cut-axis chart and expect `cut-axis`.
4. Tamper a data attribute and expect a consistency failure.
5. Document that the table, not the picture, is authoritative.

#### Tech stack

- Python 3.11 or newer
- SVG as text
- No vision model and no browser

#### Setup

1. Create `chart-peak/` with `chart.py`, `read.py`, and tests.
2. Write both SVGs to `out/`.
3. Run tests.
4. Open the SVG in a browser if you want to see it, but the tests must not require that.

#### Deliverable

- The zero-baseline chart returns the true peak category and value.
- The cut-axis chart is refused.
- A tampered attribute fails the consistency check.
- The notes name the table as the source of truth.

#### Step ahead

A second question asks for the trough, and a missing category should not be treated as zero. Add a trough reader that ignores categories listed in `not_observed` rather than treating them as value zero. Fixture a week with a missing day and show the trough computed on observed days only, plus a refusal if fewer than three days were observed. The follow-on is an answer that knows the difference between a measured zero and a gap.

### Day 98 — Task Envelopes Between Processes

**Level:** Advanced

**Folder:** [atlas/08-frontier-lab/day-98-task-envelopes/README.md](atlas/08-frontier-lab/day-98-task-envelopes/README.md)

Pass a task envelope from a requester to a worker and return a completion receipt a third process can cancel.

#### Concept

Two agents that share memory are one program. Two processes that pass envelopes can fail independently. This project defines a minimal envelope: `task_id`, `deadline`, `question`, and `allowed_methods`. The worker may use only those methods and returns a receipt: `task_id`, `status`, and either a quote or an error. A monitor process can mark a task `cancelled` before the worker finishes. The worker checks the monitor before it returns and must not return `complete` for a cancelled id. You will run this in-process with three functions standing in for processes, and also across two threads or two local sockets if you want the failure to be more real. The required tests can stay in-process. The envelope is inspired by agent-to-agent handshakes and is not a full protocol implementation.

#### Approach

Ids are generated by the requester and are unique in a test that fires two tasks. The worker's tool list is filtered by `allowed_methods`. A method outside the list errors. The monitor is a dict the worker reads at the start and at the end. A cancel that arrives after the receipt is written does not rewrite the receipt. Instead the monitor stores `cancel_after_complete`, which the test asserts. That race is the interesting one. A cancel that arrives before completion yields status `cancelled` and no quote.

#### Components

| Piece | Role |
| --- | --- |
| Envelope | Task id, deadline, question, allowed methods. |
| Worker | Filtered methods and a receipt. |
| Monitor | Cancel flag the worker checks at the end. |
| Late-cancel record | A cancel after completion does not rewrite the receipt. |

#### How it works

1. Submit an envelope and receive a complete receipt.
2. Submit one whose method is not allowed and expect an error receipt.
3. Cancel before the worker finishes and expect `cancelled` with no quote.
4. Cancel after the receipt is stored and expect the receipt unchanged plus a late-cancel note.
5. Assert two tasks do not share an id.

#### Tech stack

- Python 3.11 or newer
- In-process functions as the required path
- JSON envelopes

#### Setup

1. Create `envelopes/` with `protocol.py` and tests.
2. Run the four scenarios.
3. Run tests.
4. Describe the race in the notes in two sentences.

#### Deliverable

- A pre-completion cancel suppresses the quote.
- A post-completion cancel does not rewrite the receipt.
- Disallowed methods cannot be called by the worker.
- Task ids are unique across the two-task test.

#### Step ahead

Add a deadline. If the worker's scripted clock passes the deadline before the receipt, the status is `expired` and any quote it would have returned is dropped. Fixture a slow worker and a fast worker against the same deadline. The follow-on is a receipt that can be late without being treated as success, and the monitor can tell expiry from cancellation.

### Day 99 — A Cheap Proposal and a Strong Confirm

**Level:** Advanced

**Folder:** [atlas/08-frontier-lab/day-99-cheap-confirm/README.md](atlas/08-frontier-lab/day-99-cheap-confirm/README.md)

Let a cheap policy propose a tool and a strong policy confirm or override it, and log the override rate.

#### Concept

Running the expensive path on every turn is a choice, not a law. This project splits a decision. The cheap policy proposes a tool name from a small rule list. The strong policy, also scripted but allowed to see the gold tool for the fixture, confirms or overrides. In the real pattern the strong policy would be a larger model. Here it is a function you can score. The harness logs proposals, confirmations, and overrides. The override rate is overrides divided by proposals. You will fixture a set where the cheap policy is usually right and one where it proposes `quote` before any search. The strong policy must override that case. The cheap policy does not get to call the tool. Only a confirmed name is executed. This is not a human review queue and not a confidence score routed to an analyst. It is a two-policy gate in front of a tool call.

#### Approach

Execution uses the confirmed name only. A test stubs the tools and counts calls. An overridden proposal produces zero calls under the cheap name and one call under the strong name. If the strong policy rejects both, nothing is called and the status is `no-tool`. Include that third outcome so confirmation is not forced to pick something. The report lists the override rate and the no-tool count. Do not hide overrides. They are the price of letting the cheap policy speak first.

#### Components

| Piece | Role |
| --- | --- |
| Cheap proposer | A rule list that emits a tool name. |
| Strong confirmer | Confirm, override, or reject. |
| Execution gate | Calls only the confirmed name. |
| Override log | Proposal, decision, and whether a call happened. |

#### How it works

1. Run a batch where the cheap policy matches the fixture's expected tool.
2. Run the premature-quote case and assert an override and a search call.
3. Run a case the strong policy rejects and assert zero calls.
4. Compute the override rate from the log in a test, not by hand only.
5. Assert the cheap name was not called on the override fixture.

#### Tech stack

- Python 3.11 or newer
- Scripted policies
- Stub tools that count calls

#### Setup

1. Create `cheap-confirm/` with `policies.py`, `gate.py`, and tests.
2. Run the batch and write `out/overrides.jsonl`.
3. Run tests.
4. State that both policies are scripted stand-ins.

#### Deliverable

- Confirmed tools run and proposed-but-overridden tools do not.
- A reject runs nothing.
- The override rate is computed from the log.
- The premature quote is overridden to a search in the fixture.

#### Step ahead

A cheap policy that is almost never overridden is paying for a confirmer it may not need on that tool. Add a per-tool tally. If `search` was confirmed ten times with zero overrides, mark it `eligible-for-autonomy` in a recommendation file that does not itself disable the confirmer. Fixture the tally and assert the file is a recommendation, by checking that the gate still confirms `search` until a separate config flag is flipped. The follow-on separates the measurement from the permission change.

### Day 100 — Field Study: A Handbook Agent Under a Harness

**Level:** Advanced

**Folder:** [atlas/08-frontier-lab/day-100-handbook-field-study/README.md](atlas/08-frontier-lab/day-100-handbook-field-study/README.md)

Answer handbook questions with retrieval, a budget, and a cassette, and attach an evidence note to the run.

#### Concept

The last project uses pieces you already built, on one handbook, without turning them into a platform. A scripted agent may search notes, quote a span, and stop. It has a tool budget of four. Search is served from a cassette recorded by a fake transport or by a local function treated as a cassette: the replay run performs no new indexing side effects beyond reading files. The output for each question is an evidence note: the queries, the chunk ids returned, the quote or the abstention, the budget remaining, and the cassette key. A question with no supporting span abstains inside the budget. A question that would need a fifth search stops partial and says which checklist item was left. You will run the set twice and show the evidence notes matching. That match is the close of the atlas: a result someone else can replay.

#### Approach

Keep the agent scripted so the replay is exact. The evidence note is JSON, one object per question, written to `out/evidence.jsonl`. The second run compares hashes of that file to the first. A mismatch fails. Do not call a hosted model in the required path. If you add one later, record it as a third run that is allowed to differ, and do not overwrite the scripted evidence. The abstention and the partial budget stop must both appear in the question set, so the field study shows a limit and not only successes. The cassette miss path should be tested with one extra question you deliberately leave unrecorded, and that question's note says `cassette-miss` rather than inventing a chunk.

#### Components

| Piece | Role |
| --- | --- |
| Scripted handbook agent | Search and quote under a tool budget. |
| Cassette | Recorded search results keyed by query. |
| Evidence note | Queries, ids, quote or abstain, budget remaining, cassette key. |
| Replay check | A second run's evidence hash matches the first. |

#### How it works

1. Record cassettes for the answerable questions and the abstention question.
2. Run the agent and write evidence notes.
3. Include one question that exhausts the budget and one unrecorded query.
4. Run again and compare hashes.
5. Assert the unrecorded query does not produce a quote.

#### Tech stack

- Python 3.11 or newer
- Your notes index, quote check, budget, and cassette
- JSONL evidence

#### Setup

1. Create `field-study/` with `agent.py`, `cassettes/`, `questions.jsonl`, and tests.
2. Run record, then two replays.
3. Run tests for abstain, budget stop, cassette miss, and hash match.
4. Read one evidence note from top to bottom and confirm every id is in the cassette or explained by a miss.

#### Deliverable

- Two scripted runs produce the same evidence hash.
- At least one question abstains and one stops on the budget.
- A cassette miss does not invent a chunk.
- Every successful quote is an exact substring of a retrieved chunk in the note.

#### Step ahead

Swap the scripted quoter for a second scripted quoter that is wrong on one question, and show the evidence hash changing while the cassette file's hash stays the same. The follow-on is a diff that localizes the change to the answer, not to retrieval. Write the two hashes and the question id that moved. If you cannot tell which question moved without re-reading every note, add a per-question hash to the evidence file and repeat the swap. The atlas ends when a change points at the component that moved.
