# Text Profiles Before Any Embedding

**Day 05** · **Beginner** · Phase 01: Field Notes: Data & Measurement

Profile a pile of support notes: length, scripts, boilerplate, and exact-duplicate rate.

## Concept

Harbor Loop's support desk exports notes as text. Before you embed them or send them to a model, you need a profile that would change your plan. Some notes are three words. Some are the same macro pasted fifty times. Some mix English with Spanish station names. Some contain a phone number your later prompt would echo. This project profiles a folder of `.txt` notes you write yourself, about forty of them, including the boring cases. You will report character length quantiles, a crude script mix, the share of notes that match a boilerplate template, the exact-duplicate rate, and a count of lines that look like phone numbers. Nothing is embedded. The decision at the end is written down: which notes are worth a later retrieval corpus, and which should be excluded because they are macros.

## Approach

Normalize line endings and strip trailing whitespace, and count that normalization as its own step so you do not hide it. Detect boilerplate by exact match against a list of macros you author, not by a model. Detect phone-like strings with a conservative regular expression and report counts, not the numbers themselves, in the summary. Duplicate rate uses a hash of the normalized text. Keep a `decisions.md` that says "exclude macros" or "keep macros but down-weight them," with one sentence of evidence from your own report. The profile script must be rerunnable: same folder in, same JSON out.

## Components

| Piece | Role |
| --- | --- |
| Note corpus | About forty short notes, including macros, duplicates, and a few non-English tokens. |
| Normalizer | Newlines and trailing whitespace, leaving a before/after length. |
| Profiler | Length quantiles, boilerplate share, duplicate rate, phone-like count. |
| Decision note | What you would exclude from a later corpus, tied to a number in the profile. |

## How it works

1. Write the notes under `corpus/`. Include five exact copies of one macro and two near-copies that differ by a ticket id.
2. Normalize and hash. Near-copies must not count as exact duplicates. That distinction is the point of the near-copies.
3. Compute length quantiles on normalized character length.
4. Flag boilerplate by exact match to `macros.txt` and phone-like patterns by regex.
5. Write `out/profile.json` and `decisions.md`. A test locks the duplicate count at five.

## Tech stack

- Python 3.11 or newer
- Standard library `re`, `hashlib`, `pathlib`, `json`
- A corpus you authored, so the notes are safe to commit later if you want

## Setup

1. Create `text-profiles/` and the `corpus/` folder.
2. Add `macros.txt` with two templates.
3. Implement `profile.py` and tests for the duplicate count and the phone-like counter.
4. Run the profiler twice and diff the JSON. The second run should be identical.

## What done looks like

- Exact duplicates and near-copies are counted differently, and the test shows it.
- The profile reports counts of phone-like strings without printing the matched text.
- `decisions.md` cites at least one number from `profile.json`.
- Re-running the script does not change the JSON.
