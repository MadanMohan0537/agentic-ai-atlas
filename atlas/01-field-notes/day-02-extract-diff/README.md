# Diff Two Extracts by Distribution

**Day 02** · **Beginner** · Phase 01: Field Notes: Data & Measurement

Compare two weekly rental files by quantiles and category mix, not by staring at the first rows.

## Concept

Harbor Loop sends a second file, `rentals_week_b.csv`, and someone asks whether the feed "changed." Sorting both files and reading `head` will miss a duration that doubled in the tail and a station that vanished. This project compares two extracts that already passed the Day 1 contract. You will compute, for each numeric column, the min, the median, the 95th percentile, and the max, and for each category column the share of rows. Then you will emit a diff that flags a column only when a threshold you chose is crossed. The point is a reviewable change list. A human still decides whether the change is a real operational event or a broken exporter. You are not building a drift-to-retraining system. You are building the habit of comparing distributions before you trust a week-over-week chart.

## Approach

Reuse the clean-file schema from Day 1 so both weeks are rows you have already accepted. Implement quantiles by sorting, not by a statistics package, so you can explain the index you picked for the 95th percentile. Compare category shares with absolute percentage-point differences. Put the thresholds in a small config: for example, flag duration if the median moves by more than 15 percent, and flag a station if its share moves by more than 5 points or it disappears. Print a markdown table with week A, week B, and the delta. Include one planted change in week B so the test has something it must flag, and one tiny change it must ignore.

## Components

| Piece | Role |
| --- | --- |
| Clean-week fixtures | Two accepted extracts, one of them with planted distribution shifts. |
| Summary function | Quantiles for numeric columns and shares for categories. |
| Threshold config | The deltas that count as a flag, written down before you look at the result. |
| Diff report | A markdown table of flagged columns and a count of unflagged ones. |

## How it works

1. Load both clean extracts with the Day 1 columns and refuse to compare if the headers differ.
2. Compute numeric summaries independently for each week.
3. Compute category shares, including categories present in only one week.
4. Apply thresholds. A missing station is a flag even if every numeric quantile is stable.
5. Write `out/week_diff.md` and assert that the planted shift is flagged and the tiny shift is not.

## Tech stack

- Python 3.11 or newer
- Standard library only
- Markdown report you can paste into a review

## Setup

1. Start a new folder so this day runs even if Day 1 is unfinished. Copy the column names, not the whole loader.
2. Write `fixtures/week_a.csv` and `fixtures/week_b.csv` by hand or with a short generator. Keep them under 200 rows.
3. Implement `summarize.py` and `diff.py`.
4. Run `python3 diff.py` and then `python3 -m unittest discover -s tests -v`.
5. Read the report out loud once. If you cannot explain a flag without looking at the code, the label is wrong.

## What done looks like

- The report flags the planted median shift and the disappeared station.
- A one-percent jitter in a single row does not create a flag.
- Quantile code uses an explicit index on a sorted list, and a test locks that index for a known vector.
- Headers that differ exit non-zero with a message, rather than aligning columns by position.
