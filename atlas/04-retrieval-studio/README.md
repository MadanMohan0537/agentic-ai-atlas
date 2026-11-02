# Phase 04: Retrieval Studio

Days 33–48. Index a handbook you write, retrieve with lexical and dense methods, and answer only when a span in the index supports the sentence.

| Day | Level | Project | Summary |
| --- | --- | --- | --- |
| 33 | Intermediate | [Chunks that Respect Questions](day-33-chunks-and-questions/README.md) | Split a staff handbook into chunks and show a question that breaks when the answer straddles a cut. |
| 34 | Intermediate | [Brute-Force Dense Search](day-34-brute-force-dense/README.md) | Embed chunks with a local bag-of-hashes or a small model and rank them by cosine, exhaustively. |
| 35 | Intermediate | [An Index with Metadata](day-35-index-with-metadata/README.md) | Persist vectors and filter by handbook version and section before similarity is computed. |
| 36 | Intermediate | [BM25 Beside Vectors](day-36-bm25-beside-vectors/README.md) | Rank the same chunks with BM25 and show a query the hashing embedder misses and BM25 hits. |
| 37 | Intermediate | [Reciprocal Rank Fusion](day-37-reciprocal-rank-fusion/README.md) | Fuse lexical and dense rankings with reciprocal rank fusion you recompute by hand on a toy list. |
| 38 | Intermediate | [Rewrite, Then Keep the Original](day-38-rewrite-keep-original/README.md) | Rewrite a vague question into a handbook query and search both, because the rewrite can drop the only specific token. |
| 39 | Intermediate | [Rerank the Shortlist](day-39-rerank-the-shortlist/README.md) | Rerank the top twenty fused hits with a lexical overlap feature and show when the new order hurts. |
| 40 | Intermediate | [Quote or Abstain](day-40-quote-or-abstain/README.md) | Answer with a quotation from a retrieved chunk, or refuse, when the handbook does not contain the fact. |
| 41 | Intermediate | [Parents and Children](day-41-parents-and-children/README.md) | Search small child chunks, then expand to the parent section before you quote. |
| 42 | Intermediate | [The Wrong Manual Version](day-42-wrong-manual-version/README.md) | Bind a question to a handbook edition from the conversation, and block a newer chunk the user did not ask for. |
| 43 | Intermediate | [Numbers that Stay with Their Headers](day-43-numbers-and-headers/README.md) | Chunk a fee table so a cell is never separated from the column header that gives it a unit. |
| 44 | Intermediate | [Several Queries, One Pool](day-44-several-queries-one-pool/README.md) | Fan a question out to several lexical queries, pool the hits, and dedupe by chunk id before fusion. |
| 45 | Advanced | [A Second Search When the First Is Empty](day-45-second-search/README.md) | If the first query abstains for low coverage, rewrite once and search again, with a hard stop at two passes. |
| 46 | Advanced | [Recall at K, Written Down](day-46-recall-at-k/README.md) | Freeze a retrieval eval file and report recall at five and at twenty, with a denominator you can recount. |
| 47 | Advanced | [Compress Before You Prompt](day-47-compress-before-prompt/README.md) | Extract the sentences that overlap the query before anything is shown to a generator, and measure what you dropped. |
| 48 | Advanced | [One Hop on an Entity Graph](day-48-one-hop-graph/README.md) | Link handbook chunks to entities and expand one hop to a neighbor chunk before answering. |
