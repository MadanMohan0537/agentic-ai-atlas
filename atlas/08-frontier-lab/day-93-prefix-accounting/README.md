# Accounting for a Shared Prefix

**Day 93** · **Advanced** · Phase 08: Frontier Lab

Measure how many prompt tokens a shared system prefix would reuse, and invalidate the reuse when the tool list changes.

## Concept

A long system prompt that is identical across calls is work you should not pay for twice. Hosted APIs expose prefix caching. You may not have one. This project accounts for reuse without claiming to be the vendor's cache. You hash the prefix tokens. A second call with the same hash records `reused_tokens` equal to the prefix length and `new_tokens` equal to the suffix. A call with a different hash records the full prompt as new. You will show a batch of ten questions with a shared handbook preamble where the reused fraction is high, then change one tool description in the preamble and show the hash changing for every question. The study is the invalidation. A cache that ignores a tool-list edit will serve instructions you no longer mean.

## Approach

Tokenization can be whitespace or your byte-pair encoder. The account function does not talk to a network. It returns a record per call. The batch report sums reused and new tokens. A test runs the same prefix twice and expects the second call's reused count to equal the prefix length. A test flips one character in a tool description and expects reused tokens to be zero for the next call. Do not implement an actual KV cache. If you describe one in the notes, label it as a picture of why the hash exists, not as something you built.

## Components

| Piece | Role |
| --- | --- |
| Prefix hash | Hash of the token ids before the question. |
| Account record | Reused tokens and new tokens per call. |
| Shared-preamble batch | Ten questions, one prefix. |
| Invalidation edit | A one-character tool-list change that zeros reuse. |

## How it works

1. Tokenize a preamble and ten questions.
2. Account the batch and record the reused fraction.
3. Edit the preamble and account again.
4. Assert reuse collapsed.
5. Assert a repeated identical call reuses the prefix.

## Tech stack

- Python 3.11 or newer
- Your tokenizer or a whitespace tokenizer
- JSON report of token accounts

## Setup

1. Create `prefix-account/` with `account.py` and tests.
2. Run both batches.
3. Run tests.
4. Write the reused fraction in `notes.md` and the fraction after the edit.

## What done looks like

- Identical prefixes reuse the prefix length on the second call.
- A one-character preamble edit zeros reuse.
- The report sums match the sum of the rows.
- The notes do not claim you implemented a vendor cache.

## Step ahead

Tool results also get prepended, and caching them is wrong when the tool output changes. Extend the hash so the cached region is only the stable preamble, and tool results are always new tokens even if the text matches the previous call. Fixture two calls with the same preamble and the same tool result text and show the tool-result tokens counted as new. The follow-on draws a boundary: reused instructions, fresh observations.
