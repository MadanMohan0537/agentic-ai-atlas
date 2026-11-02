"""Phase 4 — Retrieval Studio. Days 33–48."""

PHASE = {
    "id": "04",
    "dir": "04-retrieval-studio",
    "name": "Retrieval Studio",
    "blurb": "Index a handbook you write, retrieve with lexical and dense methods, and answer only when a span in the index supports the sentence.",
    "outcome": "Build a retrieval stack that cites, filters, and admits when the handbook does not say.",
    "goal": "Finish this phase with a handbook index you can defend: chunks tied to source offsets, lexical and dense rankings, fusion, a quote-or-abstain answer, edition filters bound to a case file, and a recall number that does not move just because a favorite example worked.",
    "skills": [
        "Chunking with source offsets and gold questions",
        "Exhaustive dense search behind one embedder interface",
        "Metadata filters applied before scoring",
        "BM25 and identifier-preserving tokenization",
        "Reciprocal rank fusion",
        "Query rewriting that keeps the original string",
        "Bounded reranking of a shortlist",
        "Exact quotes and abstention",
        "Parent-child retrieval",
        "Edition binding from a case record",
        "Table chunks that keep headers with cells",
        "Multi-query pooling and dedupe",
        "One corrective retry without moving the threshold",
        "Versioned recall-at-k evaluation",
        "Context compression that reports deleted gold spans",
        "One-hop entity graphs with a distractor you disclose",
    ],
    "projects": [
        {
            "day": 33,
            "slug": "chunks-and-questions",
            "title": "Chunks that Respect Questions",
            "level": "Intermediate",
            "summary": "Split a staff handbook into chunks and show a question that breaks when the answer straddles a cut.",
            "concept": """
Retrieval fails before search exists if the chunk boundary cuts the only sentence that answers the question. This project writes a short Harbor Loop staff handbook as eight markdown files: hours, fees, weather closures, lost-bike procedure, and so on. You will split them with a fixed character window and an overlap, then write ten questions by hand whose answers you can point to. At least two questions must require a sentence pair that a naive window separates. You will record, for each question, the chunk ids a human says are necessary. That labeled file is the gold set for the rest of the phase. Do not generate the questions with a model and then grade the model against them. You wrote the handbook, and you should write the questions. The artifact is `chunks.jsonl` plus `questions.jsonl` with the character offsets of the supporting spans.
            """.strip(),
            "approach": """
Chunk on character windows first, because the failure is easier to see than with a clever splitter. Record start and end offsets into the source file so a later citation can highlight the original text. Overlap by a fraction you declare, such as one fifth of the window. After you have seen a straddling question fail, add a second splitter that prefers markdown headings and paragraph breaks, and compare the gold chunk ids. Keep both chunk files. The heading splitter is not automatically better: a long section can still bury the answer. The comparison table is the deliverable, not a claim that semantic chunking is solved.
            """.strip(),
            "components": [
                ("Handbook", "Eight markdown files you wrote."),
                ("Window chunker", "Fixed size, overlap, source offsets."),
                ("Heading chunker", "Splits on headings and paragraphs, with a max size."),
                ("Gold questions", "Ten questions with the supporting offsets marked by you."),
            ],
            "flow": [
                "Write the handbook. Include one answer that is a pair of sentences in different paragraphs.",
                "Run both chunkers.",
                "Write ten questions and mark supporting offsets against the source, not against a chunk you hope will match.",
                "For each question, list the window chunks and the heading chunks that overlap the gold offsets.",
                "Note the questions where the window chunker splits the gold span across two chunks and the heading chunker does not, or the reverse.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library `pathlib` and `json`",
                "Markdown handbook you authored",
            ],
            "setup": [
                "Create `chunking/` with `handbook/`, `chunk.py`, and `questions.jsonl`.",
                "Run both chunkers into `out/window.jsonl` and `out/heading.jsonl`.",
                "Add a test that every chunk's text equals the source slice for its offsets.",
                "Keep questions free of answers that the handbook does not contain. Those have a later day.",
            ],
            "done": [
                "Offsets round-trip to the source text in a test.",
                "Ten questions have gold offsets.",
                "The comparison note names at least one straddling question.",
                "Both chunk files are kept, and neither is silently overwritten.",
            ],
        },
        {
            "day": 34,
            "slug": "brute-force-dense",
            "title": "Brute-Force Dense Search",
            "level": "Intermediate",
            "summary": "Embed chunks with a local bag-of-hashes or a small model and rank them by cosine, exhaustively.",
            "concept": """
Dense retrieval is a sort over similarities. An index is an optimization you add after the ranking is correct. This project embeds every chunk from Day 33 and answers a query by scoring all of them. You have two acceptable embedders. The first is a local hashing embedder: tokenize, hash each token into a fixed number of buckets, and L2-normalize the count vector. It needs no network and it is good enough to test the plumbing. The second is a small local model you already have access to, called from one function with the same output shape. The rest of the pipeline must not care which you used. You will run all ten gold questions, record the rank of the first chunk that overlaps a gold offset, and write the misses in full. A miss is a question whose gold chunk is not in the top five.
            """.strip(),
            "approach": """
Put the embedder behind `embed(texts) -> list[list[float]]` with a dimension recorded in the output file. Cosine similarity on normalized vectors is a dot product, and a test should lock that equivalence on a random vector. Search is a loop, not an index library. Save `ranking.json` with query id, top five chunk ids, and the rank of the first gold hit or null. Do not tune the embedder against the ten questions repeatedly. You may look once, change a single preprocess setting such as lowercasing, and then stop. A second change belongs in the notes as an unrun idea. Otherwise the gold set becomes training data.
            """.strip(),
            "components": [
                ("Embedder interface", "One function, hashing implementation required, model implementation optional."),
                ("Exhaustive scorer", "Dot product against every chunk vector."),
                ("Gold rank", "Rank of the first chunk that overlaps a gold span."),
                ("Miss list", "Questions where the gold chunk is outside the top five."),
            ],
            "flow": [
                "Embed all chunks and store vectors next to chunk ids.",
                "Embed each question and rank chunks.",
                "Compute gold rank using offset overlap, not string equality of the answer.",
                "Write the miss list with the top chunk's text so you can see the near miss.",
                "Test that normalized vectors have unit length and that brute-force search returns a known nearest neighbor on a toy set.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library hashing embedder",
                "Optional local embedding model behind the same function",
            ],
            "setup": [
                "Create `dense-search/` and copy the chunk and question files.",
                "Implement `hashing_embed.py` and `search.py`.",
                "Run the ten questions.",
                "Run tests, including the toy nearest-neighbor case.",
            ],
            "done": [
                "Every question has a recorded gold rank or an explicit miss.",
                "The embedder id and dimension are in the output.",
                "You changed at most one preprocess setting after seeing results, and the notes name it.",
                "The toy nearest-neighbor test passes.",
            ],
        },
        {
            "day": 35,
            "slug": "index-with-metadata",
            "title": "An Index with Metadata",
            "level": "Intermediate",
            "summary": "Persist vectors and filter by handbook version and section before similarity is computed.",
            "concept": """
Brute force hides a product bug: the search space is almost never "every chunk we have ever stored." Harbor Loop's handbook has a version and a section. A question about fees in the 2026 edition must not return the 2024 fee table just because the wording is close. This project persists vectors in a simple on-disk layout — a JSON manifest and a binary or JSON vector file — and applies metadata filters before scoring. You will plant a stale chunk with nearly identical text and a different `edition` field, and show that an unfiltered query ranks it first while a filtered query cannot see it. The index rebuilds from the manifest without leftover ids from a deleted chunk. Deleting a chunk and still returning it is the bug the test is named after.
            """.strip(),
            "approach": """
Each record has `chunk_id`, `edition`, `section`, `text`, `vector`, and `source` offsets. Filtering is a predicate over metadata, applied to candidate ids, and only then do you dot. Do not filter after you take top-k. A post-filter can return fewer hits than the user asked for and, worse, can drop the stale chunk only when you remembered to ask. The stale-chunk fixture uses the same words as a current fee chunk with one number changed. Rebuild is a pure function of the records directory: remove a file, rebuild, and assert the id is gone. You do not need a vector database server.
            """.strip(),
            "components": [
                ("Record manifest", "Ids, metadata, and where the vector lives."),
                ("Pre-filter", "Edition and section predicates applied before scoring."),
                ("Stale-edition fixture", "A near-copy that must lose under the filter."),
                ("Rebuild", "Index contents match the files on disk after a deletion."),
            ],
            "flow": [
                "Write records for the current handbook plus one stale fee chunk.",
                "Query fees with no filter and record the top id.",
                "Query with `edition=2026` and assert the stale id is absent from the candidate set, not merely absent from a truncated display.",
                "Delete a chunk file, rebuild, and assert its id does not return.",
                "Test a filter that matches nothing: the result is empty, not an error and not a fall-through to all chunks.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "JSON or a single SQLite table you create yourself",
                "The Day 34 embedder",
            ],
            "setup": [
                "Create `filtered-index/` with `index.py` and fixtures.",
                "Run the unfiltered and filtered queries.",
                "Run the deletion test.",
                "Document the candidate-count before and after the filter in `notes.md`.",
            ],
            "done": [
                "The stale chunk wins unfiltered and is invisible when the edition filter is on.",
                "An empty filter result does not fall back to the full corpus.",
                "A deleted chunk id is gone after rebuild.",
                "The notes show candidate counts before and after filtering.",
            ],
        },
        {
            "day": 36,
            "slug": "bm25-beside-vectors",
            "title": "BM25 Beside Vectors",
            "level": "Intermediate",
            "summary": "Rank the same chunks with BM25 and show a query the hashing embedder misses and BM25 hits.",
            "concept": """
Dense scores smear rare strings. A rider asks about the exact fee code `HL-FEE-14`, which appears once in the handbook. A hashing embedder may bury that chunk under generic fee language. BM25, a lexical ranker with term frequency and document length, will not, if the tokenizer keeps the code intact. This project implements BM25 over the same chunks, with a tokenizer that does not throw away identifiers. You will run the gold questions through both rankers and write a disagreement table: questions where the top lexical chunk and the top dense chunk differ. At least one query in the set should be an exact code or a rare proper name you placed in the handbook. If your gold set has no such query, add one now and mark it as added after the first dense run so the history stays honest.
            """.strip(),
            "approach": """
Implement the standard BM25 scoring formula with k1 and b as named constants. Compute inverse document frequency from the chunk collection you are searching, and keep that statistic with the index so a later chunk changes idf when you rebuild. Do not import a search engine. The point is the formula and the tokenizer. Tokenizer rules: lowercase, split on whitespace and punctuation, but keep tokens that contain digits. A test passes the fee code through as one token. Compare rankers by top-1 chunk id on each question and by gold rank.
            """.strip(),
            "components": [
                ("Tokenizer", "Keeps codes with digits as single tokens."),
                ("BM25 scorer", "Term frequency, document length, and idf, with named constants."),
                ("Disagreement table", "Questions where lexical top-1 and dense top-1 differ."),
                ("Rare-token query", "A fee code or proper name planted in the handbook."),
            ],
            "flow": [
                "Tokenize chunks and build document frequencies.",
                "Score the gold questions with BM25.",
                "Load dense rankings from Day 34 or recompute them with the hashing embedder.",
                "Write the disagreement table, including gold rank for both.",
                "Assert the fee-code query's gold chunk is in the BM25 top three.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library only",
                "The same chunk files as the dense search",
            ],
            "setup": [
                "Create `bm25/` with `bm25.py` and tests.",
                "Plant `HL-FEE-14` if the handbook does not already contain a rare code.",
                "Run both rankers and write `disagreements.md`.",
                "Run the tokenizer test on the fee code.",
            ],
            "done": [
                "BM25 constants are named and the formula is implemented in one function a test can call.",
                "The rare-token query hits its gold chunk in the BM25 top three.",
                "The disagreement table covers every gold question.",
                "A token with digits is not split into a bare number and letters.",
            ],
        },
        {
            "day": 37,
            "slug": "reciprocal-rank-fusion",
            "title": "Reciprocal Rank Fusion",
            "level": "Intermediate",
            "summary": "Fuse lexical and dense rankings with reciprocal rank fusion you recompute by hand on a toy list.",
            "concept": """
Two rankers disagree, and a product has to return one list. Averaging cosine similarity with a BM25 score mixes units nobody can explain. Reciprocal rank fusion ignores the raw scores and sums one over a constant plus the rank. This project implements that fusion for the dense list and the BM25 list, with the constant k set to 60, and also shows a one-row hand example with k set to 1 so the arithmetic fits on a page. You will fuse the gold questions and compare fused gold rank to each individual ranker. Fusion is not required to win on every question. You will count how often it matches the better of the two and how often it matches the worse. That second count is the cost of fusion, and it belongs in the notes before you make fusion the default.
            """.strip(),
            "approach": """
Ranks are 1-based. A chunk present in only one list contributes only that list's term. Do not invent a rank for a missing chunk. Sort the fused scores descending, and break ties by chunk id so the output is deterministic. The hand example uses three chunks and two lists of length two. Compute it in the test, not only in prose. On the real questions, write `fusion.md` with one line per question: dense gold rank, lexical gold rank, fused gold rank. Add a config flag to disable fusion so the earlier rankings remain reproducible.
            """.strip(),
            "components": [
                ("Rank normalizer", "1-based ranks, no raw-score mixing."),
                ("Fusion sum", "Sum of 1/(k+rank) over lists that contain the chunk."),
                ("Hand example", "Three chunks, k=1, asserted in a test."),
                ("Win/loss count", "How often fusion matches the better ranker, and how often the worse."),
            ],
            "flow": [
                "Implement fusion and the hand example test.",
                "Fuse the saved rankings for each gold question.",
                "Compute the three gold ranks.",
                "Count better-matches and worse-matches. Ties between the source rankers are excluded from both counts and listed instead.",
                "Write the notes, including a question where fusion hurt, if one exists.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library only",
                "Saved rankings from the lexical and dense days",
            ],
            "setup": [
                "Create `fusion/` with `rrf.py` and tests.",
                "Run fusion on the gold set.",
                "If you do not yet have saved rankings, recompute BM25 and the hashing embedder inside this folder and say so.",
                "Run tests.",
            ],
            "done": [
                "The hand example matches the test exactly.",
                "Ties break by chunk id, and a test swaps input order to prove it.",
                "The notes include the better-match count and the worse-match count.",
                "A missing chunk is not assigned a fictional rank.",
            ],
        },
        {
            "day": 38,
            "slug": "rewrite-keep-original",
            "title": "Rewrite, Then Keep the Original",
            "level": "Intermediate",
            "summary": "Rewrite a vague question into a handbook query and search both, because the rewrite can drop the only specific token.",
            "concept": """
Users ask "what's the deal with rain," and a rewrite step turns that into "weather closure policy." Sometimes the rewrite helps. Sometimes the user said `HL-FEE-14` in a messy sentence and the rewrite, aiming for clean prose, drops the code. This project adds a query rewriter with two backends: a deterministic template rewriter you write for the handbook's known topics, and an optional model rewriter behind the same interface. Search runs on the original query and the rewritten query. You will log both strings. A fixture query contains a rare code plus vague wording. The template rewriter must preserve unknown alphanumeric codes. You will also show a hostile template that deletes tokens it does not recognize, and a test that fails that template. Keeping the original query in the fusion set is the mitigation you will measure, not a slogan.
            """.strip(),
            "approach": """
The template rewriter maps a few keywords to handbook phrases and appends any token that matches a code pattern, rather than replacing the whole string. Search both queries with BM25, fuse the two lists with the Day 37 function, and compare gold rank to searching the original alone. The hostile rewriter is a one-liner that keeps only whitelisted words. It exists to make the failure mode obvious in a test. If you connect a model, it must be optional and the test suite must pass with the template only. Log a JSON line per question with `original`, `rewritten`, and both rankings' top ids.
            """.strip(),
            "components": [
                ("Template rewriter", "Keyword expansion that preserves code-like tokens."),
                ("Hostile rewriter", "A whitelist rewriter the test expects to drop the code."),
                ("Dual search", "Original and rewrite, fused."),
                ("Query log", "Both strings and the top ids, per question."),
            ],
            "flow": [
                "Implement the template rewriter and the code-preserving rule.",
                "Implement the hostile rewriter and test it against a sentence containing `HL-FEE-14`.",
                "Run dual search on the gold questions plus the messy code question.",
                "Compare fused dual-search gold rank to original-only gold rank.",
                "Write `rewrites.md` with one case the rewrite improved and one it would have damaged if you had dropped the original.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "BM25 and fusion from earlier days",
                "Optional model rewriter behind a flag defaulting to off",
            ],
            "setup": [
                "Create `rewrite/` with `rewrite.py` and tests.",
                "Run the messy code query with the template rewriter and with the hostile one.",
                "Run the gold set with dual search.",
                "Confirm tests pass with no network and no API key.",
            ],
            "done": [
                "The hostile rewriter drops the code, and the test asserts that drop.",
                "The template rewriter keeps the code, and the test asserts that keep.",
                "The log contains both query strings for every question.",
                "The notes include a case where dropping the original would have lost the gold chunk.",
            ],
        },
        {
            "day": 39,
            "slug": "rerank-the-shortlist",
            "title": "Rerank the Shortlist",
            "level": "Intermediate",
            "summary": "Rerank the top twenty fused hits with a lexical overlap feature and show when the new order hurts.",
            "concept": """
The first retriever is tuned to recall. A second pass can look harder at fewer chunks. A cross-encoder is the usual choice, and it is also a dependency you may not have. This project defines a reranker interface and ships a local implementation: score each candidate by the fraction of query tokens that appear in the chunk, multiplied by a saturation on chunk length so a long chapter does not win by containing every word somewhere. You may add a model cross-encoder behind the same interface later. You will rerank the top twenty from fusion and compare gold rank before and after. Publish every question the reranker made worse. A reranker without a regression list is how a demo becomes the default and quietly drops the fee-code hit below a chatty paragraph.
            """.strip(),
            "approach": """
The shortlist is exactly the fused top twenty, or fewer if the corpus is smaller. The reranker may not look outside that list. That constraint is the product: second-pass cost stays bounded, and a bug cannot "fix" recall by searching the rest of the corpus. Length saturation is a named function, such as token overlap divided by log of chunk length. Test it on two chunks with the same overlap count and different lengths. Write `rerank.md` with improved, unchanged, and regressed question ids. If you add a neural reranker, keep the lexical one as the offline default the tests use.
            """.strip(),
            "components": [
                ("Shortlist contract", "Rerank only the fused top twenty."),
                ("Lexical reranker", "Query-token overlap with a length saturation."),
                ("Regression list", "Questions whose gold rank got worse."),
                ("Interface", "A function signature a neural reranker could match later."),
            ],
            "flow": [
                "Build fused top-twenty lists for each gold question.",
                "Rerank with the lexical scorer.",
                "Compute gold rank before and after.",
                "Group question ids into improved, unchanged, and regressed.",
                "Test that a longer chunk loses to a shorter chunk when overlap counts match.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Fusion output from Day 37",
                "No required neural reranker",
            ],
            "setup": [
                "Create `rerank/` with `rerank.py` and tests.",
                "Run the gold set.",
                "Write the three groups into `rerank.md`.",
                "Add a test that a candidate outside the shortlist cannot appear in the reranked output even if you pass it accidentally. The function should ignore or reject it. Pick one behavior and test it.",
            ],
            "done": [
                "The regression list is present, even if it is empty, and emptiness is explicit.",
                "The length-saturation test passes.",
                "The reranker does not introduce chunk ids that were not in the shortlist.",
                "The notes name the shortlist size.",
            ],
        },
        {
            "day": 40,
            "slug": "quote-or-abstain",
            "title": "Quote or Abstain",
            "level": "Intermediate",
            "summary": "Answer with a quotation from a retrieved chunk, or refuse, when the handbook does not contain the fact.",
            "concept": """
A retrieval stack that always answers will invent a fee when the handbook is silent. This project draws a hard line. The answer is either a quotation copied from a retrieved chunk, plus the chunk id and offsets, or an abstention with a reason. Paraphrase is out of scope for the required path, because paraphrase makes grading mushy and makes fabrication easy. You will implement a local answerer that selects the highest-scoring sentence that covers the query tokens, and abstains when the coverage is below a threshold you set before looking at a new holdout. The holdout includes three questions whose answers are not in the handbook at all. Those must abstain. A question that quotes the wrong edition is also a failure even if the words are confident.
            """.strip(),
            "approach": """
Split candidate chunks into sentences. Score a sentence by the fraction of query tokens it contains, excluding a tiny stoplist. The threshold lives in `threshold.txt` with a one-line justification written before you run the holdout. The gold questions from earlier days are the development set. The three unanswerable questions are the holdout, and you do not tune the threshold after seeing them. If you fail them, you report the miss and adjust in a follow-up run that you label as such. Output JSON has `status` of `quote` or `abstain`, and quotes must be exact substrings of the cited chunk. A test tampers with a quote character and expects rejection.
            """.strip(),
            "components": [
                ("Sentence splitter", "Breaks a chunk without dropping the source offsets."),
                ("Coverage scorer", "Query-token fraction with a stoplist."),
                ("Threshold file", "A number justified before the holdout run."),
                ("Exact-quote check", "The returned string is a substring of the cited chunk."),
            ],
            "flow": [
                "Write the threshold and the justification.",
                "Run the ten gold questions and record quotes or abstentions.",
                "Freeze the threshold. Run the three unanswerable questions.",
                "Reject any quote that is not an exact substring.",
                "Write `answers.md` with the unanswerable outcomes called out.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Retrieved shortlists from the previous day",
                "No required generative model",
            ],
            "setup": [
                "Create `quote-or-abstain/` with `answer.py`, `threshold.txt`, and the holdout file.",
                "Run development questions, then holdout.",
                "Add the tamper test.",
                "If you optionally attach a generative model, it may only choose among sentences the retriever returned, and the exact-substring check still applies.",
            ],
            "done": [
                "Every quote passes the substring test against the cited chunk.",
                "The three unanswerable questions were not used to pick the threshold.",
                "Abstentions include a reason code, such as `low-coverage`.",
                "A tampered quote fails the test.",
            ],
        },
        {
            "day": 41,
            "slug": "parents-and-children",
            "title": "Parents and Children",
            "level": "Intermediate",
            "summary": "Search small child chunks, then expand to the parent section before you quote.",
            "concept": """
Small chunks retrieve sharply and quote poorly, because the sentence that matched is missing its condition. Large chunks quote with context and retrieve poorly, because the vector or the BM25 score is diluted. This project stores both. Child chunks are the search units. Each child points at a parent, which is the heading section that contained it. Retrieval returns children. The quoter from Day 40 reads the parent text, while the citation still records the child id that won retrieval and the parent id that supplied context. You will construct one question where the child match is a pronoun or a short rule, and the condition lives in the previous paragraph inside the parent. Quoting only the child must be incomplete, and quoting from the parent must include the condition. That pair of quotes is the artifact.
            """.strip(),
            "approach": """
Build the parent as the heading chunk from Day 33, and the children as smaller windows inside it, each storing `parent_id`. Search children with BM25. Expansion replaces the text handed to the quoter, not the id used for gold-rank calculations. Gold rank stays on the child, so you do not take credit for retrieving a giant section. Add a test that a child from edition 2024 does not expand to a parent from edition 2026 even if someone wires the ids wrong. Parent and child must share edition. Write `expansion.md` with the child-only quote and the parent quote for the pronoun question.
            """.strip(),
            "components": [
                ("Child records", "Small searchable slices with a parent id and an edition."),
                ("Parent records", "Heading sections keyed by id and edition."),
                ("Expansion step", "Quoter sees parent text; gold rank stays on the child."),
                ("Edition guard", "Refuses to expand across editions."),
            ],
            "flow": [
                "Generate parents and children from the handbook.",
                "Plant the pronoun question and mark the child offsets and the parent offsets separately.",
                "Retrieve children and expand.",
                "Run the quoter twice: once on child text, once on parent text.",
                "Assert the cross-edition expansion is rejected.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "BM25 search on children",
                "The quote checker from Day 40",
            ],
            "setup": [
                "Create `parent-child/` with `build_hierarchy.py` and tests.",
                "Write the pronoun example into the handbook if it is not there.",
                "Run both quoters and save `expansion.md`.",
                "Run the edition-guard test.",
            ],
            "done": [
                "The notes show a child quote that misses the condition and a parent quote that includes it.",
                "Gold rank is computed on child ids.",
                "Cross-edition expansion fails the test.",
                "Every child record has a parent that exists in the same edition.",
            ],
        },
        {
            "day": 42,
            "slug": "wrong-manual-version",
            "title": "The Wrong Manual Version",
            "level": "Intermediate",
            "summary": "Bind a question to a handbook edition from the conversation, and block a newer chunk the user did not ask for.",
            "concept": """
Filters are useless if the caller forgets them. A support agent asks about "the fee" while the case file says the rider's membership started under the 2024 handbook. The 2026 fee is more prominent in the index because you rewrote that page last. This project models a small case context: `edition` is a field on the case, not a guess from the question text. Retrieval receives the case and must set the filter from it. You will try to regress: a code path that ignores the case and searches all editions. A test calls that path's function, if you are tempted to keep it, and asserts it is not what `answer_case` uses. The user-visible answer cites the edition. An answer that is numerically right for the wrong year is a wrong answer.
            """.strip(),
            "approach": """
Represent a case as JSON with `case_id`, `edition`, and `question`. `answer_case` reads the edition only from the case. It does not parse years out of the question. Include a fixture where the question says "2026" but the case edition is 2024, and assert the filter follows the case. That fixture is the whole lesson: the utterance is not the system of record. Cite `edition` in the output next to the chunk id. Log the filter that was applied so a later review can see it without reading code.
            """.strip(),
            "components": [
                ("Case file", "Edition as a field, separate from the question text."),
                ("Bound retriever", "Filter comes from the case inside `answer_case`."),
                ("Hostile fixture", "Question mentions a different year than the case."),
                ("Citation", "Chunk id plus the edition that was actually searched."),
            ],
            "flow": [
                "Write three cases, including the hostile year mismatch.",
                "Implement `answer_case` and log the filter.",
                "Assert the hostile case searches 2024.",
                "Add a regression test that a helper named `search_all` is not called by `answer_case`. If you have no such helper, assert the candidate editions are a single value.",
                "Write the three answers with their cited editions.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "The filtered index",
                "JSON case files",
            ],
            "setup": [
                "Create `edition-binding/` with `cases.jsonl` and `answer_case.py`.",
                "Run the three cases.",
                "Run tests.",
                "In the notes, state which object is the system of record for edition.",
            ],
            "done": [
                "The hostile case cites 2024 and does not cite the 2026 fee chunk.",
                "The applied filter is in the log.",
                "A test locks the case field as the source of the filter.",
                "The notes name the system of record in one sentence.",
            ],
        },
        {
            "day": 43,
            "slug": "numbers-and-headers",
            "title": "Numbers that Stay with Their Headers",
            "level": "Intermediate",
            "summary": "Chunk a fee table so a cell is never separated from the column header that gives it a unit.",
            "concept": """
A markdown table of fees becomes dangerous when a chunker cuts between a header and a cell. The retriever returns "14" and the quoter says fourteen dollars, or fourteen minutes, or fourteen days. This project adds a table-aware chunker. Each row chunk includes the header row text, the row label, and the cell, and it records the column name as metadata. You will plant a question — "what is the late fee for a cargo bike" — and show a naive window that can return the cargo-bike row without the header. The table-aware chunk must contain both the column name and the number. Quoting that chunk passes an assertion that the column name is present. This is structure-aware indexing, not a spreadsheet product.
            """.strip(),
            "approach": """
Parse a simple GitHub-style markdown table yourself: header, separator, rows. Do not accept merged cells. Each data row produces one chunk per numeric cell, and the chunk text is a rendered sentence you control, such as "Late fee | cargo bike | 14 USD", built from the header and the row label. The original table is also stored so you can show it. The naive window chunker runs on the raw markdown for contrast. A test checks that every numeric chunk contains its column header string. A second test feeds a ragged row and expects a rejected table, not a shifted column.
            """.strip(),
            "components": [
                ("Table parser", "Header plus rows, rejecting ragged lines."),
                ("Cell chunks", "Header, row label, and value rendered together."),
                ("Naive contrast", "A window chunk that can isolate the bare number."),
                ("Header assertion", "Every numeric chunk contains the column name."),
            ],
            "flow": [
                "Add `fees.md` with a real markdown table, including a cargo-bike late fee.",
                "Parse it and emit cell chunks.",
                "Run the naive window chunker on the same file.",
                "Show one naive chunk that lacks the header, if the window produces one. Adjust the window on a copy of the file only for the demonstration, and label it as a constructed cut if you have to force it.",
                "Query the late fee and assert the returned table chunk contains the column name and the row label.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "A small markdown table parser you write",
                "The existing quoter's substring check",
            ],
            "setup": [
                "Create `tables/` with `fees.md`, `table_chunks.py`, and tests.",
                "Run both chunkers.",
                "Run the ragged-row test.",
                "Write `table_notes.md` with the naive chunk and the cell chunk side by side.",
            ],
            "done": [
                "A ragged table is rejected.",
                "Every numeric cell chunk includes its column header, and a test walks all of them.",
                "The cargo-bike question returns a chunk containing the row label and the column name.",
                "The notes show the contrast with a headerless fragment.",
            ],
        },
        {
            "day": 44,
            "slug": "several-queries-one-pool",
            "title": "Several Queries, One Pool",
            "level": "Intermediate",
            "summary": "Fan a question out to several lexical queries, pool the hits, and dedupe by chunk id before fusion.",
            "concept": """
One question can be several retrieval problems. "Can I leave a cargo bike out in the rain overnight, and what does it cost" needs the weather section and the fee table. A single BM25 string tends to pick one. This project splits a compound question into subqueries with a deterministic splitter: conjunctions and question marks you define, not a model. Each subquery searches. The pool is the union of hits, deduped by chunk id, keeping the best rank any subquery gave that id. You will compare gold coverage: the fraction of gold chunks hit by the single query versus the pool. On the compound question you wrote, coverage should go up. On a simple question, the pool should not pull in an unrelated second section just because the splitter was eager. Over-splitting is the failure mode you will fixture.
            """.strip(),
            "approach": """
The splitter breaks on " and " only when both sides contain a question cue you list, so a station named "Grand and Pine" does not split. That station name is the over-split fixture if you naively split on every "and". Test it. Each subquery returns a top ten. Dedupe keeps the minimum rank. Gold coverage uses the set of gold chunk ids for questions that have more than one gold span. Write `pool.md` with coverage before and after for each compound question, and the station-name fixture result.
            """.strip(),
            "components": [
                ("Guarded splitter", "Splits compounds without splitting names that contain 'and'."),
                ("Per-subquery search", "BM25 top ten for each piece."),
                ("Dedupe", "One row per chunk id, best rank kept."),
                ("Coverage comparison", "Gold chunk recall of the single string versus the pool."),
            ],
            "flow": [
                "Write two compound questions with two gold spans each.",
                "Add a question or a chunk containing `Grand and Pine` and assert it does not split.",
                "Search the full string and the pool.",
                "Compute coverage.",
                "Document a case where the splitter produced a subquery you wish it had not, if one appears. If none appears, say so.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "BM25",
                "Gold offsets from Day 33, extended",
            ],
            "setup": [
                "Create `multi-query/` with `split.py` and tests.",
                "Run the compound questions.",
                "Run the station-name test.",
                "Keep the splitter rules in a short comment that matches the test names.",
            ],
            "done": [
                "`Grand and Pine` remains one query in the test.",
                "Coverage is reported for the compound questions against both strategies.",
                "Dedupe keeps a single id with the best rank, and a test constructs a duplicate across subqueries.",
                "The splitter is deterministic: same string in, same list out.",
            ],
        },
        {
            "day": 45,
            "slug": "second-search",
            "title": "A Second Search When the First Is Empty",
            "level": "Advanced",
            "summary": "If the first query abstains for low coverage, rewrite once and search again, with a hard stop at two passes.",
            "concept": """
Day 40 abstained when coverage was low. Some of those abstentions are retrieval misses, not missing facts. A second search with a different query can recover the span. It can also thrash: a loop that rewrites forever, or a second pass that lowers the threshold until something, anything, quotes. This project allows exactly one retry. The first pass searches the original question. If the quoter would abstain for low coverage, a rewriter produces one new query, the system searches again, and the quoter runs with the same threshold as the first pass. The threshold does not move. If the second pass also abstains, the system stops and returns the abstention, plus both queries. Three searches is a bug. You will fixture a question that succeeds only on the retry, and a question that must still abstain because the fact is absent.
            """.strip(),
            "approach": """
The retry rewriter is deterministic and template-based, so the test does not need a model. For example, it appends the section name from a small keyword map. The attempt counter is an explicit integer in the response, and a test stubs the search function to count calls. A second retry path that catches a broad exception and tries again is forbidden; if you catch errors, they are not retrieval misses and they do not trigger rewrite. Log both queries even when the first pass succeeds, with the second marked `not-run`. The unanswerable holdout from Day 40 must still abstain, and its log must show two searches, not three.
            """.strip(),
            "components": [
                ("Attempt counter", "An integer capped at two, returned in the response."),
                ("Same-threshold retry", "The quoter's cutoff is identical on both passes."),
                ("Retry fixture", "A question whose gold chunk appears only after the rewritten query."),
                ("Absent-fact fixture", "Two searches, then abstain, with both queries logged."),
            ],
            "flow": [
                "Wire the first pass to the existing quote-or-abstain path.",
                "On low coverage only, rewrite once and search again.",
                "Stub the search function and assert the absent-fact question triggers two calls.",
                "Build the retry-success fixture by making the original query lexically miss and the rewritten query hit.",
                "Write `retries.md` with both fixtures' logs.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Template rewriter and the Day 40 quoter",
                "A call-counting stub in tests",
            ],
            "setup": [
                "Create `second-search/` with `retry.py` and tests.",
                "Run both fixtures.",
                "Add a test that a third search call fails the run if it happens.",
                "Confirm the threshold file is read once and reused.",
            ],
            "done": [
                "The absent-fact fixture performs two searches and abstains.",
                "The retry-success fixture quotes a span that the first query did not retrieve.",
                "The threshold value is the same in both attempts' logs.",
                "A test fails the build if search is called three times on one question.",
            ],
            "ahead": """
The next failure is a retry that succeeds by retrieving a contradictory span. Add a check between the two passes: if both passes would quote and the quotes disagree on a number, abstain with reason `conflict` rather than preferring the second pass because it ran later. Fixture two fee sentences with different amounts and a rewriter that surfaces the second one. The step-ahead behavior is to surface the conflict, not to average the numbers or to pick the more recent file unless the case edition already settled it.
            """.strip(),
        },
        {
            "day": 46,
            "slug": "recall-at-k",
            "title": "Recall at K, Written Down",
            "level": "Advanced",
            "summary": "Freeze a retrieval eval file and report recall at five and at twenty, with a denominator you can recount.",
            "concept": """
You have been watching individual questions. A phase needs a number that does not move just because you remember a favorite example. This project freezes an evaluation file: question id, question text, and the set of gold chunk ids. It runs the current retrieval stack and reports recall at 5 and recall at 20. Recall is the fraction of gold ids that appear in the top k, averaged per question and also reported as a micro average over gold ids. Those two averages answer different questions, and you will show a case where they diverge by writing one question with three gold chunks and several with one. You will not tune the stack against this file after the first measurement. If you change the stack, you add a new row to a results table rather than replacing the old number. The history is the point.
            """.strip(),
            "approach": """
Copy questions into `eval/retrieval.jsonl` and treat that file as append-only in spirit: a changed gold set is a new file version in the name, `retrieval_v2.jsonl`, not an edit. The runner reads a versioned config naming the retriever. Metrics code is separate from retrieval code so a test can score a fake ranking. Include a question with empty gold and define the metric: it is excluded from recall, and counted in a separate `no-gold` tally, because a silent zero would punish abstentions you wanted. Write `eval_report.md` with both averages, the tally, and the config name.
            """.strip(),
            "components": [
                ("Frozen eval file", "Question ids and gold chunk id sets."),
                ("Metric function", "Macro and micro recall at k, tested on a fake ranking."),
                ("No-gold tally", "Questions excluded from the denominator, counted aside."),
                ("Results table", "Append-only rows of config name and scores."),
            ],
            "flow": [
                "Assemble the eval file from the questions you trust. Drop any you are unwilling to stand behind.",
                "Score a hand-built ranking in a unit test: one hit of two gold ids is recall 0.5 on that question.",
                "Run the real stack once and append a results row.",
                "Change a single, named setting, run again, and append a second row. Do not delete the first.",
                "Note which average you would quote to a teammate and why.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "The retrieval stack you have been building",
                "JSONL eval file",
            ],
            "setup": [
                "Create `recall-eval/` with `eval/retrieval_v1.jsonl`, `metrics.py`, and `run_eval.py`.",
                "Run the unit test for the metric before the real run, so a bug in retrieval does not look like a bug in recall.",
                "Run the stack twice with two configs if you have a real knob. If you do not, run the same config twice and show the rows match.",
                "Write the report.",
            ],
            "done": [
                "Macro and micro recall are both present, and the unit test locks a hand-computed value.",
                "Questions with no gold are excluded and tallied.",
                "The results table has more than one row or a documented second run that matches the first.",
                "The eval file's version is in the report.",
            ],
            "ahead": """
Recall does not know whether the chunk that matched is the stale edition. Add an edition-conditioned recall that counts a hit only when the chunk's edition equals the case edition on the eval row. A ranking that surfaces the right words in the wrong edition must not increase the score. Put three rows in a fixture where the text matches and the edition does not, and show the conditioned recall fall while the unconditioned recall stays high. That gap is the number you would add to the results table before calling the stack ready for the casework in Day 42.
            """.strip(),
        },
        {
            "day": 47,
            "slug": "compress-before-prompt",
            "title": "Compress Before You Prompt",
            "level": "Advanced",
            "summary": "Extract the sentences that overlap the query before anything is shown to a generator, and measure what you dropped.",
            "concept": """
Stuffing five parent sections into a prompt spends the context window on instructions for docks the user did not ask about, and it gives a generator more room to stitch unrelated numbers. This project compresses each retrieved parent to the sentences that pass the Day 40 coverage score, in their original order, with offsets preserved. If no sentence passes, the parent is dropped, not replaced with a summary you invent. You will measure, on the gold questions, how many characters you removed and whether every gold offset still intersects the compressed text. A compression that deletes the gold span is a failed compression even if the remaining text looks focused. You will also run one question where the answer is the absence of a sentence — a rule that only appears as a header plus a table — and show that sentence-level compression can delete the header. That case sets up the fix.
            """.strip(),
            "approach": """
Compression is a pure function of the parent text, the query, and the threshold. It does not call a generative model. Output is a list of kept spans with offsets. The coverage metric against gold is: a gold offset range is preserved if any kept span overlaps it. Report per-question preservation and the character reduction ratio. The header-loss fixture is a table chunk from Day 43 passed through a sentence splitter that does not understand tables. You will see it fail, write the failure down, and only then special-case chunks whose metadata says `table` so they bypass sentence compression and pass through whole. The bypass is the patch. The failed run stays in the notes.
            """.strip(),
            "components": [
                ("Sentence compressor", "Keeps sentences above the coverage threshold, in order."),
                ("Preservation check", "Gold offsets still overlap a kept span."),
                ("Reduction ratio", "Characters kept divided by characters retrieved."),
                ("Table bypass", "Chunks tagged as tables skip sentence dropping, added after the fixture fails."),
            ],
            "flow": [
                "Implement compression without the table bypass.",
                "Run the gold questions and the table fixture. Record preservation.",
                "Write the table failure into `compression.md`.",
                "Add the bypass for `kind=table` and rerun. Append a second results row.",
                "Test that a non-table parent still drops a sentence below threshold.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Coverage scorer from the quoter",
                "Parent texts and gold offsets",
            ],
            "setup": [
                "Create `compress/` with `compress.py` and tests.",
                "Run the before-bypass measurement and save it.",
                "Add the bypass and run again.",
                "Do not delete the before numbers.",
            ],
            "done": [
                "Preservation and reduction are reported per question.",
                "The table-loss failure is documented before the bypass exists in the results history.",
                "A non-table low-coverage sentence is still dropped, and a test proves it.",
                "Kept spans carry source offsets.",
            ],
            "ahead": """
Sentence coverage keeps boilerplate that shares many words with the query and drops a short sentence that actually states the exception. Add a second keep rule for sentences that contain a negation cue you list, such as "unless" or "not", when they sit in a parent that already has a kept sentence. Measure how many extra characters that rule admits on the gold set and whether any gold span is saved that coverage alone dropped. If the cue list fires on every parent, the list is too broad and the step-ahead result is a narrower list, not a larger prompt.
            """.strip(),
        },
        {
            "day": 48,
            "slug": "one-hop-graph",
            "title": "One Hop on an Entity Graph",
            "level": "Advanced",
            "summary": "Link handbook chunks to entities and expand one hop to a neighbor chunk before answering.",
            "concept": """
Some questions are paths. "Which depot services the dock that has the cargo-bike late fee" is not answered by the fee table alone and not answered by the depot page alone. This project extracts entities with a dictionary you write — docks, depots, fee codes — and links each chunk to the entities it mentions. Edges are co-mentions you define: a chunk links to an entity, and two entities link when a chunk mentions both, or when a small `relations.csv` you author says they do. Retrieval starts with the lexical hit, then walks one hop to neighboring chunks. Two hops are out of scope and a test should reject a walk that tries. You will show the cargo-bike question failing on the fee chunk alone and succeeding when the depot chunk is pulled in by the hop. You will also show a hop that pulls a distractor, and you will not hide it.
            """.strip(),
            "approach": """
Keep extraction dictionary-based so the graph is auditable. `relations.csv` is allowed only for relations the text does not literally co-mention, and each row has a `source` note pointing at a handbook sentence. The walker returns the seed chunks plus chunks that mention a neighboring entity, capped at a fixed number. The quoter then runs on that set. Gold for the path question lists both chunks as required, and recall uses the Day 46 definition. A distractor edge is planted on purpose: an entity shared with an unrelated anecdote chunk. The report shows that chunk arriving via the hop. Capping the walk is how you keep the distractor from becoming the whole handbook.
            """.strip(),
            "components": [
                ("Entity dictionary", "Names and aliases you listed."),
                ("Relation file", "Hand-authored edges with a source sentence."),
                ("One-hop walker", "Seed chunks plus neighbor chunks, with a cap."),
                ("Distractor report", "A planted edge and the unwanted chunk it retrieves."),
            ],
            "flow": [
                "Tag chunks with dictionary entities.",
                "Author the minimum relations to connect fee to depot.",
                "Run the path question with the hop disabled and enabled.",
                "Run the distractor question and list the extra chunk.",
                "Test that a two-hop request raises.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "CSV relations and JSON chunks",
                "The quoter and recall metric",
            ],
            "setup": [
                "Create `one-hop/` with `entities.csv`, `relations.csv`, and `walk.py`.",
                "Run both questions.",
                "Write `graph_notes.md` with the hop-enabled quote and the distractor chunk id.",
                "Run the two-hop rejection test.",
            ],
            "done": [
                "The path question's required chunks are both present only when the hop is enabled, or you document an accidental direct hit and make the handbook harder.",
                "The distractor chunk is listed, not filtered out of the notes.",
                "Two hops raise, and the test covers that.",
                "Every relation row cites a sentence or an explicit `manual` source.",
            ],
            "ahead": """
One hop floods the quoter when a popular entity, the word "depot" in half the handbook, becomes a neighbor. Add a degree cap: entities mentioned in more than a threshold of chunks do not expand, and the response logs which entities were skipped as hubs. Pick the threshold from the degree histogram before you rerun the path question, and show that the cargo-bike path still returns while a hub entity adds zero chunks. If the path depended on the hub, the step-ahead is to encode that relation in `relations.csv` rather than expanding the hub.
            """.strip(),
        },
    ],
}
