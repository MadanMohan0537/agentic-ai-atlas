# Chat Templates and Stop Sequences

**Day 31** · **Intermediate** · Phase 03: Transformer Workbench

Render a chat transcript with special tokens and show a wrong stop sequence swallowing the answer.

## Concept

A chat model does not see a dialogue. It sees a string rendered by a template: role markers, separators, and a place where generation starts. Get the template wrong and the model continues the user turn, or stops at the first period inside a legitimate answer. This project defines a small template for two roles, `user` and `assistant`, with explicit end markers. You will render a transcript, train or prompt your tiny model only if you want to, but the required work is the renderer and a stopper. The stopper halts when the end marker is produced and does not halt on a lookalike substring inside the message. You will include a fixture where the user's text contains the assistant's end marker as ordinary words, and show a naive string search stopping too early. Then you will show the token-id comparison, which does not.

## Approach

Pick marker strings that cannot appear by accident only if you reserve them as special tokens. Add them to the vocabulary as atomic tokens, not as characters the merger can split. The renderer joins turns and ends with the assistant marker opened and not closed, which is the generation prefix. The stopper compares newly generated token ids to the end-marker id, not substrings of the decoded text. The negative fixture decodes a user turn that contains the marker characters as separate character tokens, and asserts generation would not stop there. Write `template.md` with one rendered transcript and the token id sequence underneath.

## Components

| Piece | Role |
| --- | --- |
| Special-token vocabulary | Role markers as atomic ids. |
| Renderer | Turns become a prefix that opens the assistant role. |
| Id stopper | Stops only on the end-marker id. |
| Naive stopper | The substring bug, kept as a failing contrast. |

## How it works

1. Define the markers and add them to the vocab.
2. Render a three-turn transcript and record ids.
3. Implement both stoppers.
4. Build the fixture where the user text contains the marker as ordinary characters.
5. Assert the id stopper does not fire on that fixture and the naive stopper does.

## Tech stack

- Python 3.11 or newer
- Your tokenizer, extended with special tokens that bypass merges
- No hosted chat API

## Setup

1. Create `chat-template/` with `template.py` and tests.
2. Render the sample transcript into `template.md`.
3. Run tests for both stoppers.
4. Document the generation prefix: which marker is open at the end of the string.

## What done looks like

- The rendered transcript and its ids are in the notes.
- Special tokens are atomic: a test shows they are not split into characters.
- The naive stopper fails the hostile fixture and the id stopper passes it.
- The prefix for generation is described in one sentence.
