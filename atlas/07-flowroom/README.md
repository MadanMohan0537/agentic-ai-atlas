# Phase 07: Flowroom: Analytics and Pipelines

Days 79–90. Turn raw events into sessions, marts, and features that can be rebuilt, with late data and stale rows called out instead of smoothed over.

| Day | Level | Project | Summary |
| --- | --- | --- | --- |
| 79 | Intermediate | [Sessions and Late Events](day-79-sessions-and-late-events/README.md) | Build rider sessions from an inactivity gap and show a late event that should extend a closed session. |
| 80 | Intermediate | [Paths Through the Help Docs](day-80-help-doc-paths/README.md) | Count which help-doc sequences precede a resolved event, and ignore paths that never resolve. |
| 81 | Intermediate | [Retention Triangles](day-81-retention-triangles/README.md) | Build a cohort retention triangle from signup week and activity week, and do not fill future weeks. |
| 82 | Intermediate | [Rerun-Safe Marts](day-82-rerun-safe-marts/README.md) | Load raw events into staging and a mart in SQLite so running the job twice does not double the totals. |
| 83 | Intermediate | [Catalog History](day-83-catalog-history/README.md) | Store fee-code changes as dated rows so a question about last March does not see today's price. |
| 84 | Intermediate | [Tumbling Windows on a File](day-84-tumbling-windows/README.md) | Aggregate an event file into fixed five-minute windows and put late events in a side bucket. |
| 85 | Intermediate | [Freshness and a Backfill](day-85-freshness-backfill/README.md) | Mark a mart table stale when its newest event is too old, then backfill a date without touching the others. |
| 86 | Intermediate | [Labels Joined as Of](day-86-labels-as-of/README.md) | Attach a training label to a feature row using only events inside a window that starts after the cutoff. |
| 87 | Advanced | [An Embedding Job that Skips Unchanged Text](day-87-embedding-backfill/README.md) | Backfill chunk embeddings keyed by content hash and model id, and skip rows whose hash is already stored. |
| 88 | Advanced | [Seasonal Residuals](day-88-seasonal-residuals/README.md) | Alert when a daily rental count departs from a weekday baseline, and suppress dates you listed in advance. |
| 89 | Advanced | [Borderline Entity Matches](day-89-borderline-matches/README.md) | Match rider records across two files with a score, and send only the borderline band to a review sheet. |
| 90 | Advanced | [Logs and an Error Budget](day-90-error-budget-logs/README.md) | Parse structured logs into typed events and compute an error budget for a single route. |
