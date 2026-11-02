"""Phase 3 — Transformer Workbench. Days 21–32."""

PHASE = {
    "id": "03",
    "dir": "03-transformer-workbench",
    "name": "Transformer Workbench",
    "blurb": "Build the pieces of a transformer until a tiny model overfits a text you wrote, then adapt it with a narrow low-rank update.",
    "outcome": "Explain tokens, attention, training, decoding, and a small adaptation.",
    "goal": "Finish this phase able to walk from characters to a tiny trained transformer: tokenization, attention, position, a residual block, a loss curve you can resume, a decoder with a failure mode you can turn on, and a low-rank update that does not silently rewrite the base weights.",
    "skills": [
        "Byte-pair encoding and merge replay",
        "Skip-gram embeddings and neighbor inspection",
        "Scaled dot-product attention and masks",
        "Multi-head projections and output shapes",
        "Sinusoidal positions and a rotary-style dot product",
        "Pre-norm transformer blocks",
        "Next-character training to memorization",
        "Gradient clipping, checkpoints, and resume",
        "Greedy, temperature, and top-k decoding",
        "Frozen representations with a linear head",
        "Chat templates and stop-token identity",
        "Low-rank adaptation on one linear map",
    ],
    "projects": [
        {
            "day": 21,
            "slug": "byte-pair-literacy",
            "title": "Byte Pair Literacy",
            "level": "Intermediate",
            "summary": "Train a byte-pair vocabulary on a tiny corpus and show the merges that hide a word boundary.",
            "concept": """
Models do not read words. They read ids from a merge history, and the history was built to compress a corpus that may not look like your users. This project implements byte-pair encoding on a corpus you type yourself, a few kilobytes of Harbor Loop field notes are enough. You will start from characters, count adjacent pairs, merge the most frequent pair, and repeat until you hit a vocabulary budget. Then you will encode a sentence that was not in the corpus and list the tokens. The failure to catch is a merge that glues a space to a word so tightly that a rare station name shatters into noise while a boilerplate phrase becomes a single id. You will write that observation next to the actual token list. A tokenizer you have not watched merge is a dependency you cannot debug.
            """.strip(),
            "approach": """
Represent the corpus as a list of symbol lists, starting with characters plus an end-of-word marker if you want word-aware merges. Either choice is fine if you document it. Each merge introduces a new symbol and rewrites every occurrence. Record the merge list in order. Encoding applies merges in that same order, not by a greedy longest-match shortcut you invent later, unless you also test that the shortcut matches the ordered application on a fixture. Add one string that includes a station name appearing once. Show its tokenization before and after the final merges. Keep the corpus free of text you do not have rights to use. Your own sentences are the dataset.
            """.strip(),
            "components": [
                ("Corpus file", "Your own notes, a few kilobytes."),
                ("Merge trainer", "Counts pairs and rewrites the corpus for each merge."),
                ("Merge list", "Ordered rules you can replay."),
                ("Encode report", "A held-out sentence and its token ids, plus the rare-name example."),
            ],
            "flow": [
                "Write `corpus.txt` and `heldout.txt`.",
                "Train until the vocabulary reaches a budget you set, such as 80 tokens above the character set.",
                "Save `merges.json` in order.",
                "Encode the held-out text by replaying merges.",
                "Encode the rare station name at an early step and at the final step and paste both into `notes.md`.",
                "Test that encoding then decoding through the merge rules returns the original character string.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library `json` and `collections`",
                "A corpus you wrote",
            ],
            "setup": [
                "Create `bpe/` with `bpe.py`, `corpus.txt`, and tests.",
                "Run training and encoding.",
                "Add a test with a five-word corpus where you can hand-check the first merge.",
                "Run the tests.",
            ],
            "done": [
                "Decoding the encoding returns the original text on the corpus and on the held-out line.",
                "The first merge in the hand-checked fixture is the pair you counted by hand.",
                "`notes.md` shows the rare name under two vocabulary sizes.",
                "The merge list is ordered and is the only artifact the encoder needs besides the character inventory.",
            ],
        },
        {
            "day": 22,
            "slug": "embedding-neighborhoods",
            "title": "Neighborhoods in Embedding Space",
            "level": "Intermediate",
            "summary": "Train skip-gram embeddings on your notes and inspect neighbors, including a pair that should not be close.",
            "concept": """
An embedding is a point you learned from co-occurrence, not a definition. Two station names that share a sentence template will sit near each other even when a rider would never confuse the docks. This project trains a small skip-gram model on the tokenized notes from Day 21, or on whitespace tokens if you want a shorter path. You will look up nearest neighbors for a handful of tokens and write down one neighborhood that is useful and one that is a trap. You will also check a crude analogy, of the kind people demo on stage, and record whether the arithmetic returns anything you would show a teammate. The point of the failed analogy is the point of the day. Geometry that only works in a keynote is not a feature you should describe as understanding.
            """.strip(),
            "approach": """
Use a tiny vocabulary, under a few hundred tokens, and vectors of size 16 or 32 so training finishes on a laptop in a short run. Negative sampling can be three draws from the unigram distribution raised to the three-quarter power, which you should implement because it changes what "common word" means. Train for a fixed number of steps with a seed. Nearest neighbors use cosine similarity. Exclude the query token itself. Write `neighbors.md` with five queries. For the analogy, implement `king - man + woman` style arithmetic on tokens you actually have, such as a pair of docks and a pair of time words, and state the top three results. If your corpus is too small for any analogy to be meaningful, say that and do not borrow a pretrained vector file to make the demo prettier.
            """.strip(),
            "components": [
                ("Skip-gram trainer", "Center and context pairs with negative samples."),
                ("Cosine lookup", "Top neighbors for a query token."),
                ("Neighbor notes", "One useful neighborhood and one trap, with the query named."),
                ("Analogy probe", "Vector arithmetic and the top three tokens, or an explicit refusal."),
            ],
            "flow": [
                "Build pairs from a window of size 2 on either side of each center.",
                "Train and save vectors as a JSON map of token to list of floats.",
                "Query five tokens and write the notes.",
                "Run one analogy using tokens that occur at least five times. If you cannot find such a pair, document the frequency table instead of forcing it.",
                "Test cosine of a vector with itself is 1 within tolerance, and that a reversed vector is not the nearest neighbor of the original unless the vocabulary is pathological.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library `math` and `random`",
                "Vectors stored as JSON so you can diff them",
            ],
            "setup": [
                "Create `embeddings/` with `skipgram.py` and the corpus.",
                "Run training. Log the loss every few hundred steps to see that it moves.",
                "Write `neighbors.md` from the actual output, not from memory.",
                "Run tests.",
            ],
            "done": [
                "Five queries have neighbors computed from your vectors.",
                "The trap neighborhood is a real pair from the output, with a sentence on why closeness is misleading.",
                "The analogy section either shows top three tokens or explains that the corpus cannot support the probe.",
                "A self-cosine test passes.",
            ],
        },
        {
            "day": 23,
            "slug": "one-attention-head",
            "title": "One Attention Head, On Paper",
            "level": "Intermediate",
            "summary": "Implement scaled dot-product attention for one head and check a hand-computed 2 by 2 case.",
            "concept": """
Attention is a weighted average of values, with weights coming from queries and keys. The sentence is short and the bugs are ordinary: forgetting the scale, applying the mask after the softmax, or letting a padded position vote. This project implements single-head scaled dot-product attention in NumPy or in pure Python if you want to avoid the dependency. You will first compute a 2 by 2 example by hand, including the scale by square root of the key dimension, and lock it in a test. Then you will run a short sequence of token vectors you choose and print the weight matrix. A causal mask will zero the future, and a padding mask will zero a pad position in both directions that matter: it should not attend, and others should not attend to it. You will write the mask rule in one sentence above the code.
            """.strip(),
            "approach": """
Represent a batch of one so the shapes stay visible: query, key, and value are lists of vectors or a 2-D array of shape (time, dim). Scores are query times key transpose, divided by sqrt(dim). Masked positions are set to a large negative number before softmax, not to zero after. Softmax is numerically stable: subtract the max. The output is the weighted sum of values. The hand example uses dim 2 and two positions so you can show the arithmetic in `hand.md`. Do not import a transformer library for this day. If you use NumPy, pin the version in a requirements file that contains only that dependency.
            """.strip(),
            "components": [
                ("Score function", "Dot products scaled by sqrt(dim)."),
                ("Mask", "Causal and pad positions set to a large negative before softmax."),
                ("Stable softmax", "Subtract the max, then exponentiate."),
                ("Hand example", "A 2 by 2 case with the arithmetic written out."),
            ],
            "flow": [
                "Write the 2 by 2 example on paper and then in `hand.md`.",
                "Implement attention and assert it matches the hand example within 1e-5.",
                "Build a length-4 sequence and print causal weights. Later positions may attend backward. Earlier positions must put zero mass on the future, within tolerance.",
                "Mark the last position as pad and assert its incoming and outgoing attention mass is zero after masking.",
                "Assert the rows of a fully valid causal mask still sum to 1.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "NumPy, pinned, or pure Python lists if you prefer",
                "No transformer framework",
            ],
            "setup": [
                "Create `attention-head/` with a virtual environment and `requirements.txt` if you use NumPy.",
                "Implement `attention.py` and `tests/test_hand.py`.",
                "Run the tests and print one weight matrix into `weights.md`.",
                "If a row does not sum to 1, fix the mask order before you add more features.",
            ],
            "done": [
                "The hand example matches the code.",
                "Causal weights put no mass on future positions.",
                "A pad position does not receive or send mass.",
                "The mask sentence above the function matches the behavior the tests lock.",
            ],
        },
        {
            "day": 24,
            "slug": "heads-that-disagree",
            "title": "Heads that Disagree",
            "level": "Intermediate",
            "summary": "Run two attention heads on one sentence and show that their weight patterns are not copies.",
            "concept": """
Multi-head attention is often described as "looking at different things," and then implemented as a reshape nobody inspects. This project builds two heads with separate projections on a single sentence you embed with a fixed, seeded random projection from token ids. You will print both weight matrices and write what each head concentrates on. If they match, you have not failed the day, but you must change the initialization or the sentence until you can say whether the heads are redundant. You will also implement the output projection that concatenates head outputs and maps them back to the model dimension, and check the shape on a sequence. The lesson is the contrast between heads and the shape contract, not a claim that heads have human-readable jobs in a large model. In a tiny random model they mostly do not. Say that plainly if the patterns are noise.
            """.strip(),
            "approach": """
Use model dimension 8 and two heads of dimension 4, so concatenation returns to 8 before a square output projection. Initialize projections with a seeded normal and a scale you write down. Share the same token vectors across heads. After computing both weight matrices, measure their mean absolute difference. A difference near zero means the heads collapsed. You may reseed once and record both seeds. Do not train today. This is a shape and interpretation exercise. The output projection is a matrix multiply you test with a known input so a reshape bug cannot hide behind attention weights that happen to look plausible.
            """.strip(),
            "components": [
                ("Token vectors", "Seeded random projection from a short sentence."),
                ("Two heads", "Independent Q, K, V projections."),
                ("Disagreement note", "Mean absolute difference of the two weight matrices and a sentence of interpretation."),
                ("Output projection", "Concatenation checked by shape and by a known multiply."),
            ],
            "flow": [
                "Tokenize a sentence of at least six tokens with your Day 21 encoder or with whitespace plus a tiny vocab.",
                "Project tokens and run both heads with a causal mask.",
                "Write both matrices and the mean absolute difference.",
                "Concatenate outputs and apply the output projection. Assert the shape equals (time, model dim).",
                "Test the projection math on a 1 by 8 vector you multiply by hand.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "The attention function from Day 23",
                "NumPy or pure Python, consistent with Day 23",
            ],
            "setup": [
                "Create `multi-head/` and import or copy `attention.py`.",
                "Run `python3 heads.py` and fill `heads.md` from the printout.",
                "Run tests for shape and for the known multiply.",
                "If the heads match to many decimals, record the seed and try one more. Keep both notes.",
            ],
            "done": [
                "Both weight matrices are in the notes, with the mask visible in the upper triangle.",
                "The mean absolute difference is a number, not an adjective.",
                "The output shape test passes.",
                "The notes say whether you believe the heads specialized, and the evidence is the matrices, not a diagram from a blog.",
            ],
        },
        {
            "day": 25,
            "slug": "where-position-lives",
            "title": "Where Position Lives",
            "level": "Intermediate",
            "summary": "Add sinusoidal positions and a rotary-style pairing, and show a model with neither cannot tell order.",
            "concept": """
A bag of token vectors is invariant to order. "Bike at dock" and "dock at bike" become the same multiset, and attention without positions cannot prefer one reading. This project demonstrates that collapse, then adds two positional mechanisms on a toy sequence. Sinusoidal positions are added to the token vectors. A rotary-style pairing rotates adjacent pairs of dimensions by an angle that depends on the index, which you implement for a single query-key dot product so the relative offset appears in the score. You are not reimplementing a production RoPE kernel. You are showing, on a sequence of length four and dimension four, that a shift in position changes the score in the rotary version and that the no-position version is unchanged by a swap you construct. Write the swap explicitly.
            """.strip(),
            "approach": """
Build two token sequences that are permutations of each other. Run attention with no positions and show identical outputs up to the permutation of positions, or identical pooled outputs if you mean-pool. Then add sinusoidal vectors from the original formula, with a base you set to 10000, and show the pooled outputs differ. For the rotary demo, take one query and one key, both in R4, rotate the pairs by index times a frequency, and compute the dot product at offsets 0, 1, and 2. Put the three scores in `positions.md`. A test locks the sinusoidal vector at position 0, which should be a specific pattern of zeros and ones you derive.
            """.strip(),
            "components": [
                ("Order-swap fixture", "Two sequences with the same tokens in different order."),
                ("No-position attention", "The collapse you are trying to expose."),
                ("Sinusoidal add", "Position vectors added before attention."),
                ("Rotary dot-product demo", "Scores at three relative offsets for one pair."),
            ],
            "flow": [
                "Compute the no-position outputs on the swapped sequences and record the comparison you promised.",
                "Add sinusoidal positions and repeat the comparison.",
                "Derive the position-0 sinusoid and lock it in a test.",
                "Compute the three rotary scores and write them down.",
                "State in one sentence which mechanism you would reach for first in a tiny character model and why. Either answer is acceptable if the sentence cites your numbers.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library `math`, plus NumPy if you already use it",
                "No pretrained model",
            ],
            "setup": [
                "Create `positions/` with `positions.py` and tests.",
                "Run the swap experiment and write `positions.md`.",
                "Run tests, including the position-0 sinusoid.",
                "Keep the sequence length at 4 so the matrices stay printable.",
            ],
            "done": [
                "The no-position case shows the order invariance you claimed, on the fixture.",
                "The sinusoidal case breaks that invariance on the same fixture.",
                "Position 0 matches the hand derivation.",
                "Three rotary scores are recorded.",
            ],
        },
        {
            "day": 26,
            "slug": "block-shapes",
            "title": "A Block, Shape by Shape",
            "level": "Intermediate",
            "summary": "Stack attention, residual, layer norm, and a position-wise MLP, and assert every shape.",
            "concept": """
A transformer block is a shape contract with a few nonlinearities. Most implementation bugs are dimension mistakes that still run because a multiply happened to align. This project builds one pre-norm block: layer norm, attention, residual add, layer norm, MLP, residual add. You will assert shapes after every step on a tensor of (batch, time, dim). You will also check a residual property: if the attention and MLP outputs are zero, the block output equals the input, within tolerance. That property catches a residual that was replaced instead of added. Use two layers only if the single block already passes. Depth is not the lesson. The lesson is being able to point at each arrow in the block and name the tensor shape.
            """.strip(),
            "approach": """
Layer norm is over the last dimension, with epsilon you set, and with learnable scale and shift initialized to one and zero. The MLP is two linear maps with a GELU or ReLU between them and a hidden size of 4 times dim. Initialize the last linear maps of attention and MLP to zero for the residual test, or pass a debug flag that zeroes those outputs. Do not train. A forward pass on random input with a seed should be deterministic. Write `shapes.md` as a list from input to output. Include the causal mask as an input to the block so a later day does not bolt it on from outside in a contradictory way.
            """.strip(),
            "components": [
                ("Layer norm", "Last-dimension normalization with scale and shift."),
                ("Attention sublayer", "Your multi-head function plus a residual."),
                ("MLP sublayer", "Expand, nonlinearity, project, residual."),
                ("Shape log", "A written list of shapes after each operation."),
            ],
            "flow": [
                "Implement layer norm and test it on a vector whose mean becomes zero and variance becomes one when scale is one and shift is zero.",
                "Wire the block and run a forward pass with batch 2, time 5, dim 8.",
                "Record shapes.",
                "Zero the sublayer outputs and assert the block returns the input.",
                "Change dim to 7, an awkward number, and assert you either handle it or reject it with a clear error if heads do not divide the dimension.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "NumPy or pure Python",
                "Your attention and position code",
            ],
            "setup": [
                "Create `block/` with `block.py` and tests.",
                "Run the forward pass and write `shapes.md` from the asserts you printed, not from a diagram you remember.",
                "Run tests.",
                "If you reject non-divisible head sizes, the error message must name the dimension and the head count.",
            ],
            "done": [
                "Every step in `shapes.md` matches an assert in the test.",
                "Zeroed sublayers reproduce the input.",
                "Layer norm matches the hand mean and variance check.",
                "Head-dimension mismatch is either supported or rejected with an explicit error.",
            ],
        },
        {
            "day": 27,
            "slug": "overfit-a-text",
            "title": "Overfit a Short Text on Purpose",
            "level": "Intermediate",
            "summary": "Train a character-level transformer until it memorizes a short text you wrote, and show the memorized continuation.",
            "concept": """
A model that cannot memorize one page is not ready for a conversation about generalization. This project trains a tiny causal transformer, character level so the tokenizer cannot take the credit, until training loss collapses on a text of a few hundred characters you write. You will sample a continuation from a prefix of that text and show that it reproduces the source. Then you will sample from a prefix that never appeared and show the garbage or the groove the model falls into. Both outputs go in the notes. Memorization is the success criterion today. If you stop early because the samples "look creative," you have skipped the evidence that the training loop, the mask, and the loss are wired together. Creativity is a later conversation, and it requires a model that can also overfit when you ask it to.
            """.strip(),
            "approach": """
Use your block, two layers, model dim 32, two heads, context length covering the whole text so the task is not artificially hard. Optimize with a hand-written SGD or Adam update on one sequence, or on chunks if you prefer, but keep the full text in the training set. Teacher forcing: predict the next character at every position. Loss is mean cross-entropy. Train until the loss is near zero or until a step cap you set only after you have seen a curve that flattened. Sample with greedy decoding for the memorization check so randomness does not excuse a miss. The unseen prefix can be a single character that appears in the text but starts a different continuation than the one you request. Record both samples unedited.
            """.strip(),
            "components": [
                ("Character vocabulary", "Every character in the text, plus a stop symbol if you need one."),
                ("Tiny causal model", "Two blocks, trained with next-character loss."),
                ("Greedy memorization sample", "A prefix from the text and the reproduced continuation."),
                ("Unseen-prefix sample", "The same decoder on a prefix the text does not contain as a start."),
            ],
            "flow": [
                "Write `text.txt`, a few hundred characters of original prose.",
                "Train and log loss every few steps to `loss.csv`.",
                "Greedy-sample from a 20-character prefix taken from the text and compare to the source continuation.",
                "Greedy-sample from a prefix you invent and paste the raw output.",
                "Assert the training loss decreased from the first logged step to the last on this run, and store the curve.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "NumPy, or PyTorch if you want autograd and you pin it",
                "A text you wrote",
            ],
            "setup": [
                "Create `memorize/` with `train.py` and `text.txt`.",
                "If you switch to PyTorch, use it for autograd only and keep your block's structure visible in the module code.",
                "Run training until memorization or until you hit a cap and the notes explain the miss.",
                "Save `samples.md` with both outputs and the final loss.",
            ],
            "done": [
                "The in-text prefix continuation matches the source for a length you declare, or the notes show the exact mismatch and the loss.",
                "The unseen-prefix sample is pasted unedited.",
                "The loss curve file exists and ends lower than it starts, or you explain the failed run.",
                "The context length and depth are written at the top of the notes.",
            ],
        },
        {
            "day": 28,
            "slug": "a-loss-you-trust",
            "title": "A Loss Curve You Trust",
            "level": "Intermediate",
            "summary": "Instrument learning rate, gradient clipping, and checkpoints until a rerun overlays the same curve.",
            "concept": """
A falling loss is not evidence if you cannot rerun it. This project takes the memorization trainer and adds three pieces of discipline: a logged learning rate, gradient clipping with a threshold you choose, and a checkpoint that stores step, weights, and the RNG state you control. You will run training twice from a checkpoint saved halfway and show the remaining loss values match. You will also run once without clipping on a learning rate high enough to spike, save that curve, and keep it next to the clipped run. Deleting the spike is how people convince themselves training is stable. The spike is the artifact. The trusted curve is the one you can regenerate from the checkpoint and the config, not the one that looks smoothest.
            """.strip(),
            "approach": """
Clip global gradient norm: if the norm exceeds the threshold, scale the gradient vector. Log the norm before clipping so you can see how often you hit the cap. Checkpoints are NumPy `.npz` or a JSON of lists if the model is tiny. Tests can use a toy parameter vector to verify clipping math without training a model. The resume test trains for 20 steps, saves, trains 20 more, and compares to a fresh run that loaded the checkpoint and trained 20. Match within a tight tolerance. Record the learning rate schedule even if it is constant. A constant you did not log is indistinguishable from a bug when you return next week.
            """.strip(),
            "components": [
                ("Grad-norm log", "Norm before clipping, per step."),
                ("Clipper", "Scales the gradient when the norm exceeds a threshold."),
                ("Checkpoint", "Step, parameters, and any RNG state you own."),
                ("Resume comparison", "A continued run versus a resumed run."),
            ],
            "flow": [
                "Implement clipping and test it on a vector of known norm.",
                "Train a short run that spikes without clipping. Save `curve_unclipped.csv`.",
                "Train with clipping and checkpoint at the midpoint.",
                "Resume and compare to an uninterrupted logged run, or to a second resume.",
                "Write `trust.md` with the clip threshold, the spike step if any, and whether resume matched.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "The memorization trainer",
                "Standard library plus your numeric library",
            ],
            "setup": [
                "Create `trust-the-loss/` and copy the trainer forward.",
                "Run the unclipped spike on a tiny config so it finishes quickly. A spike from a huge learning rate counts.",
                "Run the clipped resume experiment.",
                "Run the clip unit test.",
            ],
            "done": [
                "The clip unit test matches a hand-computed scaled vector.",
                "The unclipped curve is saved, spikes included.",
                "Resume matches the continued curve within the tolerance you set.",
                "`trust.md` names the threshold and the checkpoint step.",
            ],
        },
        {
            "day": 29,
            "slug": "decoding-failures",
            "title": "Decoding and Its Failure Modes",
            "level": "Intermediate",
            "summary": "Compare greedy, temperature, and top-k decoding, and catch a repetition loop on purpose.",
            "concept": """
Decoding is part of the model a user experiences, and it is not the training loss. A memorized transformer will look fluent under greedy decoding on a known prefix and strange under a high temperature. This project adds three decoders to the tiny model: greedy, temperature-scaled softmax sampling, and top-k sampling. You will run each from the same prefix and the same seed where sampling applies. Then you will provoke a repetition loop, either by sampling from a half-trained checkpoint or by constructing a tiny distribution that puts mass on a cycle, and you will implement a repetition breaker you can explain: a ban on repeating the same token more than N times in a row, or a simple frequency penalty. The breaker is not a research claim. It is a switch you can turn off, with a sample on both sides.
            """.strip(),
            "approach": """
Temperature divides the logits before softmax. Temperature 0 is not a limit you need to take; call the greedy function instead of pretending zero is a temperature. Top-k sets all but the k largest logits to a large negative number before softmax, and k is at least 1. Seeds apply to the sampler's RNG only. Save three samples from one prefix. For the loop, if your memorized model refuses to loop, use a hand-built logit sequence or a deliberately undertrained checkpoint and say which you used. The breaker must be a flag defaulting to off so the failure remains reproducible.
            """.strip(),
            "components": [
                ("Greedy decoder", "Argmax at each step."),
                ("Temperature sampler", "Logits divided by a temperature above zero."),
                ("Top-k sampler", "Distribution truncated to k tokens."),
                ("Repetition breaker", "A switch with samples before and after."),
            ],
            "flow": [
                "Load the memorized checkpoint or train a small stand-in.",
                "Decode the same prefix three ways and write `samples.md`.",
                "Show a repetition failure with the breaker off.",
                "Turn the breaker on and decode again from the same seed.",
                "Test top-k on a known logit vector: tokens outside the top k receive probability zero.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Your tiny transformer",
                "A seeded RNG for sampling",
            ],
            "setup": [
                "Create `decoding/` with `decode.py` and tests for top-k and for temperature-equals-greedy being a separate function.",
                "Generate the three samples.",
                "Generate the loop pair.",
                "Run tests.",
            ],
            "done": [
                "Three decoders produce written samples from one prefix.",
                "Top-k assigns zero probability outside the selected set in the unit test.",
                "The repetition failure and the broken-loop sample are both present, with the flag value named.",
                "Temperature is never passed as zero.",
            ],
        },
        {
            "day": 30,
            "slug": "frozen-encoder-head",
            "title": "A Frozen Encoder and a Small Head",
            "level": "Intermediate",
            "summary": "Freeze a tiny encoder and train a linear head to classify your own labeled sentences.",
            "concept": """
Not every use of a transformer is next-token training. A common pattern freezes a representation and trains a small classifier, which is cheaper and easier to explain. This project builds a tiny bidirectional encoder — the same block with the causal mask removed — or reuses your causal model by taking the final hidden state. You will freeze those parameters. On top you will train a linear head to classify sentences you label into two classes you define, such as `maintenance` versus `billing`, twenty examples each, written by you. The baseline is a bag of character frequencies with its own linear head. If the transformer does not beat the bag on a held-out set of your sentences, the card says so. With this little data, the bag will often win. That result is welcome. It keeps the phase honest before you touch a pretrained model.
            """.strip(),
            "approach": """
Split by sentence id, not by token. Train only the head: a check of parameter ids, or a numerical check that encoder weights are identical before and after, must pass. Use the same log-loss training loop you trust. Evaluate accuracy and, because the set is small, list every held-out sentence with its prediction and label in `errors.md`. Do not claim a general encoder. The write-up's last sentence should state how many held-out sentences you have, because a perfect score on four sentences is a conversation, not a result.
            """.strip(),
            "components": [
                ("Frozen encoder", "Parameters unchanged by head training."),
                ("Linear head", "A map from one vector to two logits."),
                ("Bag baseline", "Character frequencies and its own linear head."),
                ("Held-out listing", "Every test sentence, prediction, and label."),
            ],
            "flow": [
                "Write forty labeled sentences and a split file.",
                "Train the bag baseline and record held-out accuracy.",
                "Train the head on frozen representations.",
                "Assert encoder parameters did not change.",
                "Write the held-out listing and a three-line comparison.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Your block, with the mask configurable",
                "A labeled file you wrote",
            ],
            "setup": [
                "Create `frozen-head/` with `data.jsonl`, `train_head.py`, and tests.",
                "Run both models.",
                "Run the freeze test, which should fail if you forget to stop gradients or if you copy weights back incorrectly.",
                "Keep the sentence count in the notes.",
            ],
            "done": [
                "Encoder weights match a checksum taken before training.",
                "The bag baseline number is next to the transformer number.",
                "Every held-out sentence is listed with prediction and label.",
                "The notes state the held-out count in the first paragraph.",
            ],
        },
        {
            "day": 31,
            "slug": "chat-templates",
            "title": "Chat Templates and Stop Sequences",
            "level": "Intermediate",
            "summary": "Render a chat transcript with special tokens and show a wrong stop sequence swallowing the answer.",
            "concept": """
A chat model does not see a dialogue. It sees a string rendered by a template: role markers, separators, and a place where generation starts. Get the template wrong and the model continues the user turn, or stops at the first period inside a legitimate answer. This project defines a small template for two roles, `user` and `assistant`, with explicit end markers. You will render a transcript, train or prompt your tiny model only if you want to, but the required work is the renderer and a stopper. The stopper halts when the end marker is produced and does not halt on a lookalike substring inside the message. You will include a fixture where the user's text contains the assistant's end marker as ordinary words, and show a naive string search stopping too early. Then you will show the token-id comparison, which does not.
            """.strip(),
            "approach": """
Pick marker strings that cannot appear by accident only if you reserve them as special tokens. Add them to the vocabulary as atomic tokens, not as characters the merger can split. The renderer joins turns and ends with the assistant marker opened and not closed, which is the generation prefix. The stopper compares newly generated token ids to the end-marker id, not substrings of the decoded text. The negative fixture decodes a user turn that contains the marker characters as separate character tokens, and asserts generation would not stop there. Write `template.md` with one rendered transcript and the token id sequence underneath.
            """.strip(),
            "components": [
                ("Special-token vocabulary", "Role markers as atomic ids."),
                ("Renderer", "Turns become a prefix that opens the assistant role."),
                ("Id stopper", "Stops only on the end-marker id."),
                ("Naive stopper", "The substring bug, kept as a failing contrast."),
            ],
            "flow": [
                "Define the markers and add them to the vocab.",
                "Render a three-turn transcript and record ids.",
                "Implement both stoppers.",
                "Build the fixture where the user text contains the marker as ordinary characters.",
                "Assert the id stopper does not fire on that fixture and the naive stopper does.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Your tokenizer, extended with special tokens that bypass merges",
                "No hosted chat API",
            ],
            "setup": [
                "Create `chat-template/` with `template.py` and tests.",
                "Render the sample transcript into `template.md`.",
                "Run tests for both stoppers.",
                "Document the generation prefix: which marker is open at the end of the string.",
            ],
            "done": [
                "The rendered transcript and its ids are in the notes.",
                "Special tokens are atomic: a test shows they are not split into characters.",
                "The naive stopper fails the hostile fixture and the id stopper passes it.",
                "The prefix for generation is described in one sentence.",
            ],
        },
        {
            "day": 32,
            "slug": "narrow-lora",
            "title": "A Narrow Low-Rank Update",
            "level": "Advanced",
            "summary": "Adapt a tiny pretrained-by-you model with LoRA on one style task, and show a rank that is too small.",
            "concept": """
Full fine-tuning copies every weight for a task that may need a nudge. A low-rank update adds a pair of small matrices to a linear map and trains only those. This project takes the tiny model you already trained and adapts it so continuations prefer a house style you define, such as ending every completion with a fixed sign-off you invent. You will implement LoRA on one linear layer: the update is B times A, with A and B much narrower than the layer, scaled by a constant. Base weights stay frozen, and a checksum proves it. You will train at rank 1 and at a higher rank you choose, and you will report how often the sign-off appears in greedy samples from a shared prefix list. The base model without adaptation is the control. The day is successful when you can say what the low-rank update changed and what it did not, including a prefix the adaptation should leave alone.
            """.strip(),
            "approach": """
Choose a single projection inside the MLP or the attention output. Initialize A with small random values and B at zero so the update starts at zero and the model behavior matches the base checkpoint at step 0. A test locks that. Train on a handful of style examples you write, in the chat template if you have it. Evaluate on ten prefixes: five that should gain the sign-off and five control prefixes where adding the sign-off would be a failure, such as a prefix that asks for a station code only. Report both rates at both ranks. Do not download a large instruction model. The mechanism is the same on the tiny net, and the failure modes are easier to see. If you later swap in an open model, keep this harness.
            """.strip(),
            "components": [
                ("LoRA pair", "Low-rank A and B on one frozen linear map, scaled."),
                ("Zero-at-init test", "B starts at zero, so outputs match the base model."),
                ("Style data", "Short examples you wrote that demonstrate the sign-off."),
                ("Two-rate report", "Sign-off rate and control-prefix false rate, at two ranks."),
            ],
            "flow": [
                "Implement the wrapped linear layer and the zero-at-init test.",
                "Checksum the base weights, train rank 1, and checksum again.",
                "Sample the ten prefixes greedily.",
                "Repeat at the higher rank from the same base checkpoint, not from the rank-1 weights.",
                "Write `lora_report.md` with both rates and one sample that shows a miss.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Your tiny transformer and checkpoint code",
                "No external LoRA library",
            ],
            "setup": [
                "Create `narrow-lora/` with `lora.py`, `style.jsonl`, and the prefix list.",
                "Run both ranks.",
                "Run the zero-init and freeze tests.",
                "Keep the base checkpoint read-only.",
            ],
            "done": [
                "At step 0, LoRA outputs match the base model on a fixture batch.",
                "Base weight checksums match before and after training.",
                "The report includes both ranks and the control prefixes, not only the style successes.",
                "One miss is pasted unedited.",
            ],
            "ahead": """
The follow-on is forgetting. After the style update, measure greedy continuation quality on the original memorization prefixes from Day 27. A rank that nails the sign-off and wrecks the original text has not adapted the model. It has replaced a behavior. Add a second task, a different sign-off, trained after the first, and report whether the first sign-off survives. If it does not, try a smaller learning rate or a higher rank and record which lever you moved. The design you want is one that names, before training, which old behavior is in scope to keep.
            """.strip(),
        },
    ],
}
