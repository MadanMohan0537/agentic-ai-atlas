# Phase 01: Field Notes: Data & Measurement

Days 01–10. Say what a row means, what a metric counts, and which records you refused before any model is worth training.

| Day | Level | Project | Summary |
| --- | --- | --- | --- |
| 01 | Beginner | [Row Contracts for a Messy Extract](day-01-row-contracts/README.md) | Accept or reject each rental row with a reason code instead of silently coercing bad fields. |
| 02 | Beginner | [Diff Two Extracts by Distribution](day-02-extract-diff/README.md) | Compare two weekly rental files by quantiles and category mix, not by staring at the first rows. |
| 03 | Beginner | [Grain, Joins, and Double-Counted Revenue](day-03-grain-and-double-counts/README.md) | Show how a plausible join inflates revenue, then publish a grain checklist that would have stopped it. |
| 04 | Beginner | [Event Time, Time Zones, and Late Arrivals](day-04-event-time/README.md) | Bucket rentals by event time in one zone, and show a late event landing in yesterday's bucket. |
| 05 | Beginner | [Text Profiles Before Any Embedding](day-05-text-profiles/README.md) | Profile a pile of support notes: length, scripts, boilerplate, and exact-duplicate rate. |
| 06 | Beginner | [One Definition of Active](day-06-metric-dictionary/README.md) | Write a metric dictionary entry for an active rider and compute it two ways that must agree. |
| 07 | Beginner | [Bootstrap a Rate by Hand](day-07-bootstrap-a-rate/README.md) | Estimate a completion rate and a percentile interval with a seeded resample you can recompute. |
| 08 | Beginner | [Double Annotation and Agreement](day-08-double-annotation/README.md) | Label the same support notes twice, measure agreement, and fix the guideline where you disagreed. |
| 09 | Beginner | [Features from Events Without Peeking](day-09-features-from-events/README.md) | Build a rider feature table where every aggregate uses only events at or before a cutoff. |
| 10 | Beginner | [Split Leakage Hunt](day-10-split-leakage/README.md) | Find riders who landed in both train and test, and rebuild the split so a rider lives in only one side. |
