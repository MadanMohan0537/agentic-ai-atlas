# Case IDs that Never Change in Place

**Day 76** · **Advanced** · Phase 06: Proof Bench: Evals and Harnesses

Store eval cases as immutable ids, and force an edit to mint a new id instead of rewriting history.

## Concept

If you edit a gold answer and keep the case id, last month's score and today's score are not about the same question. This project stores cases in a directory of JSON files whose names are ids. A command `check` fails if a file's content hash does not match a ledger entry for that id. A command `revise` writes a new id, records `supersedes`, and leaves the old file untouched. Deleting a file is also a failure unless a tombstone entry says the id was retired. You will revise one case, run the scorer on a fake prediction file twice — once pinned to the old id set and once to the new — and show that the two score lines name their case-set hashes. The ledger is the product. The scores are there to prove you can still join them.

## Approach

The ledger is `ledger.json` mapping id to sha256 and optional `supersedes` and `retired` fields. `check` exits non-zero on a hash mismatch and prints both hashes. `revise` refuses to overwrite. A test tampers with a gold string and expects `check` to fail. Another test runs `revise` and expects the old hash to remain. The scorer accepts a `--cases` ledger slice: `all` or `current`, where current means ids that are not superseded and not retired. Document that choice. Historical comparisons use the hash, not the word "latest."

## Components

| Piece | Role |
| --- | --- |
| Case files | One JSON file per immutable id. |
| Ledger | Hashes, supersedes links, and retirements. |
| Check command | Fails when bytes drift under an existing id. |
| Revise command | Mints a new id and keeps the old file. |

## How it works

1. Write three cases and a ledger by an `add` command that refuses existing ids.
2. Tamper with one file and show `check` failing.
3. Restore it by reverting the file, not by updating the hash in place.
4. Revise one case and show both ids present.
5. Score a prediction file against `current` and against an explicit list containing the old id.

## Tech stack

- Python 3.11 or newer
- JSON ledger and case files
- Standard library `hashlib`

## Setup

1. Create `case-ids/` with `cases.py` and tests.
2. Run add, check, a failed tamper, and revise.
3. Run tests.
4. Write the rule at the top of the README you keep in that folder: ids are immutable.

## What done looks like

- Tampering fails `check` without changing the ledger.
- `revise` leaves the old file's bytes and hash intact.
- Scores name the case-set hash they used.
- `add` refuses to reuse an id.

## Step ahead

Trend lines break when an id is superseded and a dashboard silently drops it. Add a migration report that lists old id, new id, and whether any prediction file still references the old id. Fixture a prediction file that cites a superseded id and show the report naming it as `unmapped` until you add an explicit map entry. The follow-on is a map you review, so a chart does not change denominator because a gold string was edited.
