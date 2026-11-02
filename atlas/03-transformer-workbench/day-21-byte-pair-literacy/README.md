# Byte Pair Literacy

**Day 21** · **Intermediate** · Phase 03: Transformer Workbench

Train a byte-pair vocabulary on a tiny corpus and show the merges that hide a word boundary.

## Concept

Models do not read words. They read ids from a merge history, and the history was built to compress a corpus that may not look like your users. This project implements byte-pair encoding on a corpus you type yourself, a few kilobytes of Harbor Loop field notes are enough. You will start from characters, count adjacent pairs, merge the most frequent pair, and repeat until you hit a vocabulary budget. Then you will encode a sentence that was not in the corpus and list the tokens. The failure to catch is a merge that glues a space to a word so tightly that a rare station name shatters into noise while a boilerplate phrase becomes a single id. You will write that observation next to the actual token list. A tokenizer you have not watched merge is a dependency you cannot debug.

## Approach

Represent the corpus as a list of symbol lists, starting with characters plus an end-of-word marker if you want word-aware merges. Either choice is fine if you document it. Each merge introduces a new symbol and rewrites every occurrence. Record the merge list in order. Encoding applies merges in that same order, not by a greedy longest-match shortcut you invent later, unless you also test that the shortcut matches the ordered application on a fixture. Add one string that includes a station name appearing once. Show its tokenization before and after the final merges. Keep the corpus free of text you do not have rights to use. Your own sentences are the dataset.

## Components

| Piece | Role |
| --- | --- |
| Corpus file | Your own notes, a few kilobytes. |
| Merge trainer | Counts pairs and rewrites the corpus for each merge. |
| Merge list | Ordered rules you can replay. |
| Encode report | A held-out sentence and its token ids, plus the rare-name example. |

## How it works

1. Write `corpus.txt` and `heldout.txt`.
2. Train until the vocabulary reaches a budget you set, such as 80 tokens above the character set.
3. Save `merges.json` in order.
4. Encode the held-out text by replaying merges.
5. Encode the rare station name at an early step and at the final step and paste both into `notes.md`.
6. Test that encoding then decoding through the merge rules returns the original character string.

## Tech stack

- Python 3.11 or newer
- Standard library `json` and `collections`
- A corpus you wrote

## Setup

1. Create `bpe/` with `bpe.py`, `corpus.txt`, and tests.
2. Run training and encoding.
3. Add a test with a five-word corpus where you can hand-check the first merge.
4. Run the tests.

## What done looks like

- Decoding the encoding returns the original text on the corpus and on the held-out line.
- The first merge in the hand-checked fixture is the pair you counted by hand.
- `notes.md` shows the rare name under two vocabulary sizes.
- The merge list is ordered and is the only artifact the encoder needs besides the character inventory.
