# One Hop on an Entity Graph

**Day 48** · **Advanced** · Phase 04: Retrieval Studio

Link handbook chunks to entities and expand one hop to a neighbor chunk before answering.

## Concept

Some questions are paths. "Which depot services the dock that has the cargo-bike late fee" is not answered by the fee table alone and not answered by the depot page alone. This project extracts entities with a dictionary you write — docks, depots, fee codes — and links each chunk to the entities it mentions. Edges are co-mentions you define: a chunk links to an entity, and two entities link when a chunk mentions both, or when a small `relations.csv` you author says they do. Retrieval starts with the lexical hit, then walks one hop to neighboring chunks. Two hops are out of scope and a test should reject a walk that tries. You will show the cargo-bike question failing on the fee chunk alone and succeeding when the depot chunk is pulled in by the hop. You will also show a hop that pulls a distractor, and you will not hide it.

## Approach

Keep extraction dictionary-based so the graph is auditable. `relations.csv` is allowed only for relations the text does not literally co-mention, and each row has a `source` note pointing at a handbook sentence. The walker returns the seed chunks plus chunks that mention a neighboring entity, capped at a fixed number. The quoter then runs on that set. Gold for the path question lists both chunks as required, and recall uses the Day 46 definition. A distractor edge is planted on purpose: an entity shared with an unrelated anecdote chunk. The report shows that chunk arriving via the hop. Capping the walk is how you keep the distractor from becoming the whole handbook.

## Components

| Piece | Role |
| --- | --- |
| Entity dictionary | Names and aliases you listed. |
| Relation file | Hand-authored edges with a source sentence. |
| One-hop walker | Seed chunks plus neighbor chunks, with a cap. |
| Distractor report | A planted edge and the unwanted chunk it retrieves. |

## How it works

1. Tag chunks with dictionary entities.
2. Author the minimum relations to connect fee to depot.
3. Run the path question with the hop disabled and enabled.
4. Run the distractor question and list the extra chunk.
5. Test that a two-hop request raises.

## Tech stack

- Python 3.11 or newer
- CSV relations and JSON chunks
- The quoter and recall metric

## Setup

1. Create `one-hop/` with `entities.csv`, `relations.csv`, and `walk.py`.
2. Run both questions.
3. Write `graph_notes.md` with the hop-enabled quote and the distractor chunk id.
4. Run the two-hop rejection test.

## What done looks like

- The path question's required chunks are both present only when the hop is enabled, or you document an accidental direct hit and make the handbook harder.
- The distractor chunk is listed, not filtered out of the notes.
- Two hops raise, and the test covers that.
- Every relation row cites a sentence or an explicit `manual` source.

## Step ahead

One hop floods the quoter when a popular entity, the word "depot" in half the handbook, becomes a neighbor. Add a degree cap: entities mentioned in more than a threshold of chunks do not expand, and the response logs which entities were skipped as hubs. Pick the threshold from the degree histogram before you rerun the path question, and show that the cargo-bike path still returns while a hub entity adds zero chunks. If the path depended on the hub, the step-ahead is to encode that relation in `relations.csv` rather than expanding the hub.
