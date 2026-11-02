"""Phase 2 — Learning Machines. Days 11–20."""

PHASE = {
    "id": "02",
    "dir": "02-learning-machines",
    "name": "Learning Machines",
    "blurb": "Train classical models on a tabular rental problem you can explain, and refuse any score that does not beat a boring baseline.",
    "outcome": "Fit, slice, and threshold a tabular model without fooling yourself.",
    "goal": "Finish this phase with a tabular model you can rerun from a config file, a baseline it had to beat, a threshold chosen from a payoff rather than from 0.5, and a written limit on what the model must not be used for.",
    "skills": [
        "Majority and mean baselines",
        "Logistic regression, scaling, and reliability bins",
        "Shallow decision trees and visible overfit",
        "Additive stumps and one-feature occlusion",
        "Precision and recall at a predeclared alert budget",
        "Clustering with names you can refuse",
        "Pairwise ranking against a popularity baseline",
        "Locked runs: seed, data hash, and a model card stub",
        "Error slices with a support floor",
        "Cost-sensitive thresholds on a report fold",
    ],
    "projects": [
        {
            "day": 11,
            "slug": "humbling-baselines",
            "title": "Baselines that Humiliate Models",
            "level": "Beginner",
            "summary": "Score a majority-class rule and a mean predictor before any learned model is allowed to look good.",
            "concept": """
Harbor Loop wants a first model for a yes-or-no question: did a booked rental overrun its slot? Ninety percent of rentals do not overrun. A classifier that always says "no" is right ninety percent of the time and useless at the dock. This project builds the dataset — a few hundred synthetic rows with a seeded generator — and the two baselines every later model has to beat. For classification, the baseline is the majority class, scored with accuracy and with balanced accuracy so the base rate cannot hide. For a companion regression, predicting overrun minutes, the baseline predicts the training mean. You will write both metrics yourself on the confusion counts. The artifact is a one-page baseline card that later days must paste their scores next to. A model that cannot beat the card does not get a paragraph in your notes.
            """.strip(),
            "approach": """
Generate rows with `random.Random(11)`. Columns: booked minutes, start hour, dock type (open or indoor), rider tenure days, weather code (clear, rain), and the label `overrun`. Plant the base rate near 0.1 by sampling the label from a rule you write down, plus noise, so the problem is learnable later and still imbalanced. Split riders, not rows, using the stable hash from the split day, even if you reimplement the ten lines here. Compute the majority baseline only from the training fold. Evaluating the majority class on data you used to pick it is a small leak; picking it on train and scoring on test is the habit. Write `baseline_card.md` with the test accuracy, balanced accuracy, and the regression mean absolute error of the mean predictor.
            """.strip(),
            "components": [
                ("Seeded generator", "Synthetic rentals with a documented labeling rule."),
                ("Rider split", "Whole riders assigned to train or test."),
                ("Majority baseline", "Train-fold mode, scored on the test fold."),
                ("Mean predictor", "Train-fold mean of overrun minutes, with test MAE."),
            ],
            "flow": [
                "Generate the table and write `data/rentals.csv` plus `data/RULE.txt` describing the labeling rule in words.",
                "Split by rider id into train and test.",
                "Compute the majority label on train only and score it on test.",
                "Compute balanced accuracy from the four confusion counts, not from a library.",
                "Fit the mean overrun on train rows that did overrun, and separately on all train rows. Document which one you are using and why.",
                "Write the baseline card. A test locks the majority label for this seed so a generator change cannot pass quietly.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library `random`, `csv`, `hashlib`",
                "Metrics implemented from counts",
            ],
            "setup": [
                "Create `baselines/` with `generate.py`, `score.py`, and tests.",
                "Run `python3 generate.py` then `python3 score.py`.",
                "Run `python3 -m unittest discover -s tests -v`.",
                "If balanced accuracy and accuracy are almost equal, your base rate is too close to one half. Push the negative rate up and regenerate.",
            ],
            "done": [
                "The baseline card quotes test numbers and names the seed and the split rule.",
                "Majority class is chosen on train, and a test would fail if it were chosen on test.",
                "Balanced accuracy is computed from TP, FP, TN, and FN in your own function.",
                "The labeling rule is written in `RULE.txt` before any later model day starts.",
            ],
        },
        {
            "day": 12,
            "slug": "readable-linear",
            "title": "A Linear Model You Can Read",
            "level": "Beginner",
            "summary": "Fit a logistic model with gradient descent, standardize inputs, and plot reliability in five bins.",
            "concept": """
A linear model earns its place when you can read a coefficient and say what would happen if that input moved. On the overrun table, tenure and rain should not share a scale: tenure is in days, weather is a code. Fit without standardizing and the steps fight each other. This project implements binary logistic regression with batch gradient descent, no scikit-learn. You will one-hot the small categories yourself, standardize numeric columns using train-fold mean and variance, and apply those same numbers to test. Then you will bin the test set by predicted probability and compare the average prediction in each bin to the observed overrun rate. That reliability table is the model's honesty check. Coefficients come after, as a sentence each: direction, rough size, and whether the feature's scale makes the size comparable.
            """.strip(),
            "approach": """
Use a learning rate you log, a fixed iteration count, and a seed only if you shuffle rows. Initialize weights at zero so the run is determined by the data. Clip the linear score before the exp in the sigmoid so a wild step cannot overflow. Hold out the test fold from standardization statistics. Reliability uses five bins of equal width on [0, 1], and bins with fewer than five test rows are reported but not trusted. Compare test log loss to the majority baseline's log loss. Accuracy alone is not the headline. If the linear model cannot beat the baseline card on log loss, say so in the notes and keep the baseline.
            """.strip(),
            "components": [
                ("Design matrix", "Numeric columns standardized, categories one-hot encoded."),
                ("Gradient step", "Batch logistic gradient with a clipped score."),
                ("Reliability table", "Five bins comparing mean prediction to observed rate."),
                ("Coefficient notes", "One sentence per weight, after scaling is explained."),
            ],
            "flow": [
                "Load the Day 11 table or regenerate it with the same seed and rule.",
                "Build the train-only scaler and apply it to train and test.",
                "Fit for a logged number of steps. Save the loss every ten steps to `loss.csv`.",
                "Predict on test and write the reliability table.",
                "Write coefficient sentences into `coefficients.md`, noting which columns were standardized.",
                "Assert test log loss is finite and that a column excluded from the scaler does not change the scaler's stored mean.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library only, including `math`",
                "CSV loss curve you can open in any spreadsheet",
            ],
            "setup": [
                "Create `linear-model/` and copy the generator or read the CSV from a relative path you document.",
                "Implement `logit.py` with `fit` and `predict_proba` separated.",
                "Run the fit and the tests.",
                "If the loss curve increases, divide the learning rate by ten and record both attempts in the notes. Do not hide the failed rate.",
            ],
            "done": [
                "Train mean and variance are not computed from test rows, and a test locks that.",
                "The reliability table has a row per non-empty bin.",
                "Test log loss is compared to the majority baseline in the written notes.",
                "You can point to one coefficient and say what scaling was applied before it was fit.",
            ],
        },
        {
            "day": 13,
            "slug": "a-tree-you-can-draw",
            "title": "A Tree You Can Draw",
            "level": "Beginner",
            "summary": "Grow a shallow decision tree, draw it, and show the overfit when you let it memorize leaves.",
            "concept": """
Trees are easy to praise because a picture of a split looks like a policy. They are also easy to overfit: a deep tree will isolate single rentals and call that structure. This project grows a classification tree for overrun with a depth limit you choose, using Gini impurity computed from counts. You will print the tree as indented text you can redraw on paper, with the train count and the train overrun rate in every node. Then you will grow the same tree with the depth limit removed, or set absurdly high, and compare train accuracy to test accuracy. The gap is the lesson. You will also name one split that matches the labeling rule you wrote on Day 11 and one split that looks like noise. If you cannot tell those apart from the picture, the picture is too deep to trust.
            """.strip(),
            "approach": """
Implement a binary tree on numeric features and on already-encoded binary categories. Candidate thresholds are midpoints between sorted unique values, capped at a small number per feature so the day stays short. Stop when depth hits the limit, when a node is pure, or when a node has fewer than a minimum count you set in a constant. Do not prune with a library. The comparison is shallow versus deep on the same split. Write `tree.txt` for the shallow model and a three-line overfit note: train accuracy, test accuracy, and the depth of the deepest leaf in the unconstrained run.
            """.strip(),
            "components": [
                ("Impurity function", "Gini from class counts, tested on a hand example."),
                ("Split search", "Midpoint thresholds with a cap on candidates."),
                ("Text tree", "Indented nodes with counts and rates."),
                ("Depth contrast", "Shallow versus unconstrained, same data, both scores."),
            ],
            "flow": [
                "Reuse the rider split and the overrun table.",
                "Fit a tree with max depth 3 and minimum node size 15.",
                "Render it to text and confirm every leaf shows a count.",
                "Fit an unconstrained tree and record train versus test accuracy.",
                "Write two sentences identifying a meaningful split and a suspicious one.",
                "Test Gini on a node with counts (3, 1) against the value you computed by hand.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library only",
                "Plain text rendering, no graphviz requirement",
            ],
            "setup": [
                "Create `tree-model/` with `tree.py` and tests.",
                "Run the shallow fit and read `tree.txt` top to bottom.",
                "Run the deep fit and append the contrast to `notes.md`.",
                "If the shallow tree and the deep tree have the same test accuracy, increase the noise in a copy of the generator or lower the minimum node size on the deep run only, and say which lever you moved.",
            ],
            "done": [
                "The text tree is complete: every internal node names a feature and a threshold.",
                "Train accuracy of the deep tree is higher than its test accuracy on your run, or you documented a dataset too small to show the gap and enlarged it.",
                "Gini matches a hand-computed example in a test.",
                "The notes name one split you would keep and one you do not trust.",
            ],
        },
        {
            "day": 14,
            "slug": "boosted-tables",
            "title": "Boosted Trees and a Local Reason",
            "level": "Beginner",
            "summary": "Fit a small gradient-boosted stumps model and explain one prediction by occluding a single feature.",
            "concept": """
Boosting is the usual next step on tabular problems, and it is also where explanations go vague. Harbor Loop does not need a leaderboard. It needs a model that beats the Day 11 card and a way to say, for one rental, which feature moved the score. This project fits additive stumps: each new tree is a depth-1 tree fit to the negative gradient of log loss. You will keep the ensemble small, on the order of twenty stumps, and you will stop if validation log loss rises. For a single test rental you will compute a local reason by occlusion: replace one feature with its train median, measure the change in predicted probability, and restore it. The largest change is the reason you write down. This is not a global importance trophy and it is not a production explainer for credit or safety decisions. It is a check you can recompute with a calculator and a median.
            """.strip(),
            "approach": """
Implement stumps, not a full boosting library. Use a learning rate of 0.1 and add each stump's contribution scaled by that rate. Hold a validation slice out of the training riders so early stopping does not look at the test riders. Log the validation loss per stump. Occlusion uses the train median for numeric features and the train mode for categories. Apply the same scaler logic you used before if features are not already on comparable scales; for stumps, raw scales are acceptable because thresholds adapt, and you should say that in the notes so you do not pretend the median swap is scale-free in meaning. Compare test log loss to the linear model and to the majority baseline.
            """.strip(),
            "components": [
                ("Stump fitter", "A depth-1 tree on the current residual."),
                ("Additive ensemble", "Learning rate times stump, with early stopping on validation riders."),
                ("Occlusion probe", "One-feature median swap and the delta in probability."),
                ("Scoreboard", "Baseline, linear, and boosted test log loss in one file."),
            ],
            "flow": [
                "Split riders into train, validation, and test. Write the counts.",
                "Fit stumps until the validation loss increases, or until you hit the cap.",
                "Score the test set once with the chosen number of stumps.",
                "Pick one test row whose predicted probability is between 0.3 and 0.7 if you have one, and occlude each feature.",
                "Write `local_reason.md` with the row id and the ordered deltas.",
                "Assert that occluding a feature and then restoring it returns the original probability within a tight tolerance.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Your own stump code from Day 13, simplified to depth 1",
                "No XGBoost requirement",
            ],
            "setup": [
                "Create `boosted-stumps/` and reuse the CSV.",
                "Implement `boost.py` and `occlude.py`.",
                "Run the fit. If it never beats the linear model, record that. A loss is an acceptable outcome if the scoreboard is honest.",
                "Run tests, including the restore-after-occlusion check.",
            ],
            "done": [
                "The scoreboard lists three test log losses: majority, linear, boosted.",
                "Early stopping uses validation riders, never test riders.",
                "The local reason names a feature, a median, and a probability delta.",
                "A test shows occlusion is side-effect free on the row.",
            ],
        },
        {
            "day": 15,
            "slug": "precision-at-the-point",
            "title": "Precision Where It Matters",
            "level": "Beginner",
            "summary": "Rank predictions and read precision and recall at the alert rate operations can actually handle.",
            "concept": """
An overrun model that flags every other rental will be switched off by the dock crew in a week. The operating point is a workload decision: how many alerts can a shift review? Accuracy at 0.5 is unrelated to that question, especially at a 10 percent base rate. This project sorts the test set by predicted probability and walks down the list, computing precision and recall after each alert. You will mark the point where the alert count matches a budget you set, such as twenty alerts per hundred rentals, and you will report precision there. You will also draw the curve as a CSV of (recall, precision) so you can plot it anywhere. A second curve on the training set will look better. You will put them side by side and refuse to quote the training curve in the baseline card.
            """.strip(),
            "approach": """
Use the boosted model's probabilities if you have them, or the linear model's if you do not. The day is about the curve, not about refitting. Implement `precision_recall_curve(labels, scores)` by sorting scores descending and accumulating true positives. Add a synthetic tie: two rows with the same score must not change the curve depending on input order. Break ties by row id so the walk is deterministic. Choose the budget in `budget.txt` before you look at the test curve. If you choose it after, you are fitting the operating point to the test set. Write both the predeclared budget precision and, separately, the best precision anywhere on the curve, labeled as exploratory.
            """.strip(),
            "components": [
                ("Ranked list", "Test rows sorted by score with a deterministic tie break."),
                ("Curve table", "Precision and recall after each additional alert."),
                ("Budget marker", "A predeclared alert rate and the precision at that rate."),
                ("Train contrast", "The same curve on train, stored so you do not quote it by mistake."),
            ],
            "flow": [
                "Write `budget.txt` with the alert rate and one sentence of operational reason.",
                "Load labels and scores for test and for train.",
                "Build both curves.",
                "Read precision at the budget on the test curve.",
                "Confirm a tie fixture produces the same curve under reversed input order.",
                "Update the baseline card with the budgeted precision, not with accuracy.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library `csv`",
                "Scores from your Day 12 or Day 14 model",
            ],
            "setup": [
                "Create `pr-curve/` with `curve.py` and a small tied fixture in tests.",
                "Run it on the real scores and write `out/test_curve.csv` and `out/train_curve.csv`.",
                "Add the budgeted number to `baseline_card.md` or a local copy of it.",
                "Run tests.",
            ],
            "done": [
                "The budget was written down before the test precision was computed, and the file's timestamp or your notes say so. If you slipped, change the budget file's reason, not the number, and recompute honestly.",
                "Ties do not depend on input order in the test.",
                "Train and test curves are separate files.",
                "The number you would tell operations is precision at the budget, and the notes say the denominator.",
            ],
        },
        {
            "day": 16,
            "slug": "clusters-with-names",
            "title": "Clusters with Names",
            "level": "Intermediate",
            "summary": "Cluster docks from usage features and name each cluster from examples, or refuse to name it.",
            "concept": """
Someone will ask what kinds of docks Harbor Loop operates. A clustering algorithm will always return groups. Names are the part you are responsible for. This project builds a dock-level table: median start hour, share of rainy rentals, median duration, and overrun rate. It runs k-means with k chosen from a small range using inertia, then tries to name each cluster from the five member docks closest to the center. A name is allowed only if you can write a sentence a teammate could falsify, such as "evening commute, indoor, short bookings." If the members do not support a sentence, the cluster is called `unlabeled-3` and the notes say what you would need to see. You will also refit with a different seed and report which docks changed cluster. Stability is part of the name. An unstable group does not deserve a product label.
            """.strip(),
            "approach": """
Standardize dock features with the mean and variance of the dock table you are clustering. That is descriptive, not a train-test model, and you should say so. Implement k-means with a fixed number of iterations and two seeds. Pick k by plotting inertia for k from 2 to 6 and choosing the smallest k after which the drop flattens; write the rule you used in a sentence so "elbow" is not a vibe. For each cluster, list the five nearest docks and their raw feature values, not just the standardized ones, because names should be in real units. The seed comparison reports the fraction of docks whose cluster assignment changed, after matching clusters by center proximity so label switching is not counted as change.
            """.strip(),
            "components": [
                ("Dock table", "One row per dock, aggregated from rentals."),
                ("k-means", "Your implementation, two seeds, inertia for several k."),
                ("Naming sheet", "Nearest members in raw units and a falsifiable sentence or an explicit refusal."),
                ("Stability note", "Share of docks that move after a seed change, with centers matched."),
            ],
            "flow": [
                "Aggregate rentals to docks. Docks with very few rentals go to an exclusion list, not into a cluster you then name.",
                "Standardize and run k-means for k from 2 to 6.",
                "Choose k and write the rule.",
                "Name or refuse each cluster using nearest members.",
                "Refit with a second seed, match centers, and compute the move rate.",
                "Test one iteration of k-means on a toy set of points you can solve by eye.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library only",
                "A naming sheet in markdown",
            ],
            "setup": [
                "Create `clusters/` with `aggregate.py`, `kmeans.py`, and `name.md`.",
                "If you are still on the synthetic generator, give docks three distinct usage patterns so a failure to separate them is informative.",
                "Run both seeds and fill in `name.md`.",
                "Run the toy-set test.",
            ],
            "done": [
                "Every cluster is either named with a falsifiable sentence or explicitly unlabeled.",
                "Excluded low-count docks are listed and are not given a name.",
                "The move rate between seeds is a number in the notes.",
                "The toy test fails if assignments on the obvious two-blob set are wrong.",
            ],
        },
        {
            "day": 17,
            "slug": "pairs-ranker",
            "title": "A Ranker from Pairs",
            "level": "Intermediate",
            "summary": "Learn to order docks for a rider from pairwise preferences, and evaluate with a rank metric.",
            "concept": """
Classification says whether a rental overran. Ranking says which dock a rider should be offered first. Harbor Loop can log a weak preference: when a rider is shown two docks and completes a rental at one of them, that dock won the pair. This project builds pairs from synthetic choice logs, fits a linear scoring function so that the winner's score exceeds the loser's, and evaluates with top-1 accuracy on held-out riders. You will use a pairwise hinge: the loss is zero when the score gap clears a margin, and linear otherwise. A constant model that always prefers the globally popular dock is the baseline. If your ranker cannot beat popularity on riders it has not seen, the features are not doing work. Do not report a classification accuracy on pairs as if it were the product metric. The product shows a list.
            """.strip(),
            "approach": """
Each candidate dock has features you already understand: distance bucket, indoor flag, historical overrun rate computed with a cutoff so the pair's own outcome is not inside the feature. That cutoff matters. Compute dock history from events before the choice time. Train with stochastic updates over pairs, seeded shuffle, fixed step size. Evaluate on riders held out entirely. Top-1 means the dock with the highest score is the one the rider completed, among the docks that were actually shown. Include a popularity baseline that ranks by prior completion count, also cutoff-safe. Write both numbers.
            """.strip(),
            "components": [
                ("Choice log", "Shown docks, chosen dock, timestamp, rider id."),
                ("Cutoff features", "Dock history strictly before the choice."),
                ("Pairwise hinge", "A linear score with a margin."),
                ("Top-1 versus popularity", "Held-out riders, both methods."),
            ],
            "flow": [
                "Generate choices with a seeded rule and a little noise.",
                "Build features with a strict time cutoff and test that the choice itself is absent from the history count.",
                "Fit the linear ranker on training riders' pairs.",
                "Score held-out riders' lists and compute top-1.",
                "Score the popularity baseline the same way.",
                "Write `rank_card.md`. If the ranker loses, keep the card anyway.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library only",
                "Held-out riders as the evaluation unit",
            ],
            "setup": [
                "Create `ranker/` with `choices.py`, `train_rank.py`, and tests.",
                "Run generation and training.",
                "Add a test that a feature builder raises or drops the current choice if someone includes it.",
                "Run the tests.",
            ],
            "done": [
                "Top-1 for the ranker and for popularity are both on the card, on held-out riders.",
                "A test rejects features that include the choice being scored.",
                "The hinge margin is a named constant.",
                "You can explain why pair accuracy would have flattered a model that only learns to pick the popular dock inside a pair of unequals.",
            ],
        },
        {
            "day": 18,
            "slug": "locked-training-runs",
            "title": "Locked Training Runs",
            "level": "Intermediate",
            "summary": "Make a training run reproducible: seed, data hash, config file, and a model card stub.",
            "concept": """
A score you cannot rerun is a rumor. This project wraps the linear model or the stumps in a single command that reads a config file, hashes the training CSV, records the seed, writes predictions, and writes a model card stub. The card is short on purpose: data hash, row counts, split rule, metric name, test number, and a list of things the model must not be used for. You will run the command twice and show that predictions match. Then you will change one config field, the learning rate or the stump cap, and show that the card's config section changed while the data hash did not. The failure you are catching is a notebook that was edited after the number was copied into a slide. The card lives next to the predictions, not in a wiki page you update later.
            """.strip(),
            "approach": """
Put hyperparameters only in `config.json`. The training script refuses to run if required keys are missing. Hash the training file bytes with SHA-256. Write `artifacts/<utc-stamp>/` containing `config.json`, `card.md`, `predictions.csv`, and `metrics.json`. Use a stamp you pass in, or a frozen stamp in tests, so tests do not depend on the clock. The reproduce check diffs predictions from two runs with the same config and stamp. Do not pickle a model unless you also store enough to recompute predictions from source. Source plus config plus data hash is the real artifact. A pickle without those is how runs go missing.
            """.strip(),
            "components": [
                ("Config file", "The only place hyperparameters are set."),
                ("Data hash", "SHA-256 of the training file bytes."),
                ("Artifact directory", "Config, card, predictions, and metrics written together."),
                ("Reproduce check", "Byte-level or value-level match of two runs."),
            ],
            "flow": [
                "Copy the chosen model into a function `train(config, csv_path, out_dir)`.",
                "Hash the CSV and store the hash in `metrics.json` and in the card.",
                "Run twice into two directories with the same stamp argument if needed, or overwrite a fixed out dir sequentially and copy outputs.",
                "Diff predictions.",
                "Change one hyperparameter, rerun, and show the hash stayed put and the metric changed or the notes say it did not.",
                "Fill the must-not-use list with two concrete prohibitions, such as pricing or disciplinary decisions.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library `hashlib`, `json`, `pathlib`",
                "Your earlier model code, imported or copied with attribution in a comment",
            ],
            "setup": [
                "Create `locked-runs/` with `config.json`, `train.py`, and `tests/test_repro.py`.",
                "Run the script twice.",
                "Run the tests, which should call `train` in a temporary directory.",
                "Read the card and delete any sentence you could not defend from `metrics.json`.",
            ],
            "done": [
                "Two runs with the same inputs write the same predictions.",
                "The card's data hash matches `hashlib` of the file on disk.",
                "A missing config key fails the run before training starts.",
                "The must-not-use list has two specific items, not a generic disclaimer.",
            ],
        },
        {
            "day": 19,
            "slug": "slice-the-errors",
            "title": "Slice the Errors",
            "level": "Intermediate",
            "summary": "Break test error down by a feature you did not train on as a target, and write what you would do next.",
            "concept": """
Average log loss can look fine while rainy outdoor docks are where the model is lost. This project slices the test set by a column, reports support and log loss per slice, and requires a minimum support before you are allowed to call a slice worse. You will predeclare the slices from the product, not from fishing: weather code, dock type, and a tenure band. Fishing is allowed only in a separate section labeled exploratory, and those slices cannot be the ones you act on today. The action is a written choice: collect more labeled rows, add a feature, or refuse to deploy the model for a slice below the support floor. You are not running a fairness audit that swaps attributes and estimates causal gaps. You are doing the earlier, plainer thing: looking at the error you already have, by a group you can define from columns.
            """.strip(),
            "approach": """
Use the locked run's test predictions so the scores are the ones the card refers to. Join them back to features by row id. For each predeclared slice, compute count, positive count, and mean log loss. A slice with fewer than thirty test rows is marked `thin` and is not ranked. Compare each eligible slice's loss to the overall test loss. Write `slice_report.md` with a table and a decision paragraph. Add one exploratory slice in a second table, and a sentence that says it did not drive the decision. A test builds a toy prediction file where one weather code has obviously worse loss and asserts the report names it, and asserts a tiny slice is marked thin.
            """.strip(),
            "components": [
                ("Joined test frame", "Predictions plus the slicing columns and the label."),
                ("Slice table", "Support, positives, and mean log loss."),
                ("Support floor", "A constant that marks thin slices."),
                ("Decision paragraph", "One next step tied to an eligible slice, or a refusal to deploy."),
            ],
            "flow": [
                "Load predictions and features. Drop rows that fail the join rather than filling them.",
                "Compute overall test log loss as the reference.",
                "Compute the predeclared slices and apply the support floor.",
                "Write the decision using only eligible slices.",
                "Append the exploratory table underneath a heading that keeps it out of the decision.",
                "Test the thin-slice rule and the obvious-bad-slice rule on toy data.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library `csv` and `math`",
                "Predictions from the locked run",
            ],
            "setup": [
                "Create `slices/` with `slice_report.py` and tests that do not need the full rental file.",
                "Run the report on the real predictions.",
                "If every eligible slice matches the overall loss, say so. Do not invent a gap.",
                "Run tests.",
            ],
            "done": [
                "Thin slices are visible and are not the subject of the decision sentence.",
                "The decision names a slice key and a support count, or explicitly says no eligible slice is worse.",
                "Exploratory slices are in a separate table.",
                "A failed join drops the row and increments a counter you print.",
            ],
        },
        {
            "day": 20,
            "slug": "payoff-thresholds",
            "title": "A Threshold from a Payoff Table",
            "level": "Intermediate",
            "summary": "Choose a classification threshold from costs you write down, then show how a different cost flips it.",
            "concept": """
Day 15 fixed a workload budget. Some decisions are better framed as costs. Suppose an overrun that is not staffed costs Harbor Loop a voucher, and a false alert costs a few minutes of crew time. Those are not the same unit until you write them in one currency. This project builds a two-by-two payoff table, sweeps thresholds on the test scores, and picks the threshold that minimizes expected cost on the test set. Then it does the dangerous version: picking the threshold on the test set is itself a use of the test set. You will split the old test riders in half, pick the threshold on the first half, and report cost on the second half. The second number is the one that goes on the card. You will also change one cost, rerun, and show the chosen threshold moving or not moving. A threshold that ignores the payoff is a default you have not earned.
            """.strip(),
            "approach": """
Write costs in `payoff.json` as four numbers: true positive, false positive, true negative, false negative. Expected cost is the sum of count times cost, divided by the number of rows, so it stays comparable across folds. Sweep thresholds from the unique predicted scores rather than from a fixed grid, so you do not miss the points where the decision actually changes. Selection fold and report fold are rider-disjoint. Document that both folds were already used to train nothing; they are carved from the original test riders only. If your test set is too small to split, regenerate a larger one with the same rule and say so. Compare the payoff-chosen threshold to 0.5 on the report fold.
            """.strip(),
            "components": [
                ("Payoff file", "Four costs in one currency, with a sentence defining the currency."),
                ("Threshold sweep", "One row per distinct score, with counts and expected cost."),
                ("Selection fold", "Where the threshold is chosen."),
                ("Report fold", "Where the cost is quoted."),
            ],
            "flow": [
                "Write `payoff.json` and the currency sentence before the sweep.",
                "Carve the original test riders into selection and report.",
                "Sweep on the selection fold and store the winning threshold.",
                "Apply that threshold to the report fold and compute cost. Also compute cost at 0.5.",
                "Edit one cost, repeat, and record whether the threshold changed.",
                "Test the sweep on a four-row hand example whose best threshold you computed on paper.",
            ],
            "stack": [
                "Python 3.11 or newer",
                "Standard library `json`",
                "Scores from the locked model",
            ],
            "setup": [
                "Create `payoff/` with `payoff.json`, `sweep.py`, and tests.",
                "Run the sweep and write `out/threshold_card.md`.",
                "Run the cost-edit as a second config, `payoff_alt.json`, not by overwriting the first result.",
                "Run tests.",
            ],
            "done": [
                "The quoted cost uses the report fold, and the selection fold is a different set of riders.",
                "Cost at the chosen threshold and cost at 0.5 are both on the card.",
                "The alternate payoff is a separate file, and the note says whether the threshold moved.",
                "The hand example in the test matches your paper calculation.",
            ],
        },
    ],
}
