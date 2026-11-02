# Window Versus Index

**Day 96** · **Advanced** · Phase 08: Frontier Lab

Answer the same questions from the full handbook in the prompt and from retrieval, and compare citations and cost.

## Concept

If the handbook fits in the window, retrieval can look like extra machinery. It stops looking that way when the handbook grows or when the model quotes a sentence from the wrong section because the whole text was in front of it. This project runs the same ten questions two ways. The window condition pastes the full handbook into the prompt of a scripted reader that searches the pasted text with the same quote rules as the index condition. The index condition uses your BM25 stack and quotes a chunk. Both must return a quote or an abstention. You will compare exact gold-span hits and a fictional token cost: the window condition pays for the whole handbook every time, and the index condition pays for the retrieved chunks. You are not measuring a hosted model's reading skill. You are measuring the two pipelines.

## Approach

Use a handbook small enough to paste. Gold spans are the ones you marked earlier. The scripted reader returns the first sentence in its context that passes the coverage threshold, or abstains. Giving both conditions the same reader means the difference is the context they saw, not a different answering policy. Cost numbers are fictional and labeled. A results table has one row per question per condition. A question the index misses and the window hits is interesting, and so is the reverse if a chunk boundary is why. Write both if they occur. If they do not, say so rather than inventing a miss.

## Components

| Piece | Role |
| --- | --- |
| Shared reader | Quote-or-abstain over whatever text it was given. |
| Window condition | Full handbook as context. |
| Index condition | Retrieved chunks as context. |
| Cost model | Fictional token prices labeled as fictional. |

## How it works

1. Run the ten questions under both conditions.
2. Score gold-span hits.
3. Sum fictional costs.
4. List questions where the conditions disagree.
5. Write the table and a short interpretation that cites the table.

## Tech stack

- Python 3.11 or newer
- Your handbook, BM25, and quoter
- A CSV comparison

## Setup

1. Create `window-vs-index/` with `compare.py` and the handbook.
2. Run both conditions.
3. Run a test that the shared reader is the same function object or the same module path for both. Do not fork the policy.
4. Label costs as fictional in the table header.

## What done looks like

- Every question has two rows.
- Disagreements are listed or explicitly absent.
- Costs are reproducible from the token counts in the table.
- Both conditions use the same quote rule.

## Step ahead

Grow the handbook by duplicating background sections until the window cost exceeds a budget you set, while the index cost stays flat. Record the smallest size where the window condition is over budget and the index condition still answers. That size is the crossover in your notes. If the index starts to miss because duplicates drowned BM25, record that too. The follow-on is the point where pasting everything stops being the default, measured on your corpus rather than assumed from a blog post.
