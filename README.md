# TakeMeter

## Planned stretch work

Before starting the stretch work, I plan to add a fourth label, `guide_or_solution`, for posts that provide actionable game-related steps or explanations. I will also run a second training experiment with learning rate changed from `2e-5` to `1e-5` while keeping the other settings fixed, and add 50 examples to the thinnest label while keeping every label at or below 70% of the dataset. I will report the measured effect of the second run and the final label counts below.

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

TakeMeter classifies English posts from Arqade, the public Gaming Stack Exchange community. It separates help requests, unsupported claims, evidence-backed claims, and actionable guides or solutions. The sample is drawn from the Arqade Q&A site, not its separate Meta site.
<!-- Your community, and what your classifier sorts posts into. Three or four
     sentences. -->



---

## Label Taxonomy

### `supported_claim`

**Definition:** A factual explanation or claim that includes a specific, checkable detail, example, source, or test in the post.

**Example 1:** An answer supports its conclusion with a character's level-90 base stat and named equipment. [Answer by pinckerman](https://gaming.stackexchange.com/a/419667)

**Example 2:** An answer compares the stated system requirements for Hades and Hades II to support its compatibility conclusion. [Answer by Larnu](https://gaming.stackexchange.com/a/419644)

### `unsupported_claim`

**Definition:** A factual or evaluative assertion presented without a specific reason, example, source, or checkable detail in the post.

**Example 1:** An answer tentatively names a voice actor while saying it has not found confirmation. [Answer by Somebody](https://gaming.stackexchange.com/a/419683)

**Example 2:** A short answer states what RadAway does to radiation and HP without giving a source or explanation. [Answer by Dave](https://gaming.stackexchange.com/a/418859)

### `help_request`

**Definition:** A post whose main purpose is to ask for gameplay information, advice, explanation, or troubleshooting.

**Example 1:** The author describes getting stuck on a Genshin Impact floor and asks for a working strategy. [Question by pinckerman](https://gaming.stackexchange.com/questions/419682/how-to-beat-this-abyss-floor-11-1-iteration)

**Example 2:** The author asks who voiced new characters in a Warcraft III expansion after not finding credits or an online listing. [Question by TreeSpawned](https://gaming.stackexchange.com/questions/419660/who-are-the-voice-actors-for-warcraft-3-forsaken-kingdom)

### `guide_or_solution`

**Definition:** A post whose main purpose is to provide actionable steps or a method that answers a gameplay question or solves a problem.

**Example 1:** An answer says to use Oatchi's rush and strike both walls beside the platform to dislodge Pikmin. [Answer by Nutella](https://gaming.stackexchange.com/a/419669)

**Example 2:** An answer recommends building a Multi-Purpose Room at the base of a Bloodvine, with rebuilding as a fallback. [Answer by voided](https://gaming.stackexchange.com/a/419657)

### The hardest boundary

**Which two labels:** `supported_claim` and `guide_or_solution`

**The decision rule I used every time:** If the post's main purpose is an actionable procedure the reader can follow, label it `guide_or_solution`. If its main purpose is to establish or explain a factual claim with checkable detail, label it `supported_claim`, even when it ends with an optional check. An Arqade answer about an achievement cites the game's mechanics and tells readers where to verify them; I label it `supported_claim` because the answer primarily explains the rule rather than walking the reader through a sequence of actions. [Answer by voided](https://gaming.stackexchange.com/a/419649)

**Taxonomy stress test:** Eight fictional boundary examples were generated and classified before full collection. The examples and results are in [taxonomy_stress_test.md](taxonomy_stress_test.md).

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:** Public Arqade questions and answers returned by the Stack Exchange API. Posts were limited to `CC BY-SA 4.0` and English text. Each dataset row records the post author and link, the license, and the HTML-to-text conversion. The 20 Steam candidates in `steam_label_review_worksheet.md` are excluded.

**How I labelled them:** AI-assisted candidate labels were generated from the taxonomy and text patterns. Juan reviewed all 270 suggestions and confirmed or corrected them. Each row records that review and includes source attribution. This workflow is not cold labeling. The 20-post unaided set is separate and still needs Juan's labels; see [cold_label_worksheet.md](cold_label_worksheet.md). The counts below cover the 270 reviewed rows only.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `help_request` | 55 | 20.4% |
| `supported_claim` | 55 | 20.4% |
| `guide_or_solution` | 105 | 38.9% |
| `unsupported_claim` | 55 | 20.4% |
| **Total** | **270** | **100%** |

The first 220 rows form the base collection (55 per label). The 50 additional `guide_or_solution` posts implement the planned dataset-size stretch feature. The counts reflect the reviewed labels. Each row includes author and source links with the post's `CC BY-SA 4.0` license attribution.

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

**1.**
> *The post:* The Genshin Impact question calls a mechanic the worst and then asks how to clear a specific floor.
>
> *Could have been:* `unsupported_claim` or `help_request`
>
> *I chose, because:* The main purpose is to get a working strategy, so it is `help_request`. [Question](https://gaming.stackexchange.com/questions/419682/how-to-beat-this-abyss-floor-11-1-iteration)

**2.**
> *The post:* An answer explains an achievement requirement using a linked game reference and tells readers how to check enemy entries.
>
> *Could have been:* `supported_claim` or `guide_or_solution`
>
> *I chose, because:* The answer mainly substantiates what the achievement requires; the lookup step is secondary. [Answer](https://gaming.stackexchange.com/a/419649)

**3.**
> *The post:* An answer proposes building a room at the Bloodvine base, with removing and rebuilding the existing room as another path.
>
> *Could have been:* `supported_claim` or `guide_or_solution`
>
> *I chose, because:* The central purpose is to give the player concrete steps to fix the problem. [Answer](https://gaming.stackexchange.com/a/419657)

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:** `distilbert-base-uncased`.

**Settings:** 3 epochs, learning rate `2e-5`, batch size 8, maximum 128 tokens per post, seed 42. Device: CPU; PyTorch 2.14.1+cpu.

**Anything I changed from the defaults, and why:** Batch size was reduced from 16 to 8 because this device has 5.7 GiB total RAM and the initial default-size run exited before producing results. The lower batch size reduces memory demand; all other base settings stay at the defaults.

**Split sizes:** 188 train / 41 validation / 41 test. Test counts: `supported_claim` 8, `unsupported_claim` 9, `help_request` 8, `guide_or_solution` 16. Metrics for the first three labels may be jumpy because they have only 8–9 test examples.

**Second training experiment (stretch):** I changed only the learning rate from `2e-5` to `1e-5`; epochs, batch size, seed, token length, data, and split stayed fixed. `results.json` is the `2e-5` run, and [results_second_experiment.json](results_second_experiment.json) is the `1e-5` run.

| Learning rate | Accuracy | Macro F1 |
|---:|---:|---:|
| `2e-5` | 0.634 | 0.500 |
| `1e-5` | 0.390 | 0.140 |

On this seed and split, the lower learning rate reduced accuracy by 0.244 and macro F1 by 0.360. This is one run per setting, so it describes this experiment rather than a general effect.



---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:* Eight fictional posts at the boundaries of the four labels, to check whether the definitions separated them.
- *What came back:* The examples separated into the four labels. One circular opinion, “the map is boring because it is boring,” showed that “a stated reason” was too broad.
- *What I changed:* I required a specific reason, concrete example, or checkable detail for `supported_claim`. I also included unresolved problem reports in `help_request` because a short failure report can be a request for troubleshooting without a question mark.

**Moment 2**

- *What I asked for:* Initial label suggestions for Arqade posts under the written taxonomy, then rechecked each suggestion against the taxonomy.
- *What came back:* Pattern-based candidates included borderline answers across the evidence-backed and actionable categories.
- *What I changed:* Juan reviewed all 270 candidate labels against the taxonomy and confirmed or corrected them. Later, Juan requested AI suggestions for the separate 20-post worksheet; these are not independent cold labels and remain outside the training dataset.

**Acceptance criteria disclosure:** At Juan's request, AI proposed the five numeric targets in [criteria.md](criteria.md) before training. The course's requirement that the student choose those targets was not met.

**Pre-labelling disclosure:** AI generated initial label suggestions for the Arqade dataset; Juan reviewed all suggestions and confirmed or corrected them. Each row is marked `AI-prelabel; reviewed by Juan`. Those labels are not cold. The separate 20-post worksheet now contains AI suggestions, not unaided labels, so the course's cold-label requirement remains unmet. The historical statement in criteria.md describes the state when that file was committed.

**Unit 6 AI disclosure:** At Juan's request, Codex suggested the 20 worksheet labels and the 30 staff-set labels, prepared the local experiment runner, measured the token-length distribution, ran the trials, and drafted the analysis. The staff suggestions are not independent student annotations. Juan has not reviewed or confirmed those suggestions.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.293 | 0.634 | +0.341 |
| Macro F1 | 0.175 | 0.500 | +0.325 |
| F1: guide_or_solution | 0.316 | 0.711 | +0.395 |
| F1: help_request | 0.000 | 0.889 | +0.889 |
| F1: supported_claim | 0.000 | 0.400 | +0.400 |
| F1: unsupported_claim | 0.383 | 0.000 | -0.383 |

Both models were scored on the same 41 posts in the committed test_split.csv. The baseline used the original label_definitions.txt and facebook/bart-large-mnli on CPU. baseline_results.json records held_out=true, used_definitions=true and all predictions.

**Prediction chronology:** The baseline was launched as environment preparation before a new written prediction was committed. There is no valid pre-run prediction for this setup run; no retrospective prediction is claimed.

**What the gap means:** On this single held-out split, the fine-tuned model beats the definitions-only baseline on overall accuracy, macro F1 and three labels. It performs worse on unsupported_claim. This is not yet the required three-seed result and does not establish that the advantage generalizes across random splits.




---

**Worksheet disclosure:** At Juan's request, Codex suggested labels for the 20-post worksheet; the local Unit 5 and Unit 6 copies contain the same suggestions. They are not independent cold labels and are not in the training dataset.

## Run Log - Before

Data: the original 270 reviewed, AI-prelabelled Arqade posts. Each seed independently trains DistilBERT for three epochs at learning rate 2e-5, batch 8 and 128 tokens. Device: Apple Silicon GPU (MPS), PyTorch 2.14.1. Each test split contains 41 posts; seed 42 uses the same held-out texts as the original Unit 5 result. Metrics and the source dataset hash are in `results_three_seeds_before.json`. No AI-suggested worksheet rows were added.

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---:|---:|---:|---|
| Overall accuracy | at least 0.60 | 0.610 | 0.561 | 0.585 | MISSED |
| Macro F1 | at least 0.55 | 0.461 | 0.399 | 0.364 | MISSED |
| Lowest label F1 | each at least 0.40 | 0.000 | 0.000 | 0.000 | MISSED |
| Largest label share | at most 0.45 | 0.389 | 0.389 | 0.389 | MET |
| Most-confident-third accuracy | at least 0.70 | 0.769 | 0.769 | 0.846 | MET |

The per-label criterion requires every label to meet its floor, so the table shows the lowest F1 for each seed. The balance row is the same across seeds because the underlying dataset does not change.

| Label F1 | Seed 42 | Seed 7 | Seed 2024 |
|---|---:|---:|---:|
| `supported_claim` | 0.222 | 0.000 | 0.000 |
| `unsupported_claim` | 0.000 | 0.222 | 0.000 |
| `help_request` | 0.941 | 0.706 | 0.727 |
| `guide_or_solution` | 0.681 | 0.667 | 0.727 |

### Seed 42 confusion matrix

| True label / predicted | supported_claim | unsupported_claim | help_request | guide_or_solution |
|---|---:|---:|---:|---:|
| supported_claim | 1 | 0 | 0 | 7 |
| unsupported_claim | 0 | 0 | 1 | 8 |
| help_request | 0 | 0 | 8 | 0 |
| guide_or_solution | 0 | 0 | 0 | 16 |

The largest error is eight true `unsupported_claim` posts predicted as `guide_or_solution`; the reverse happened zero times. Seven of eight true `supported_claim` posts were also predicted as guides. In this split the model favors the larger guide category and misses the evidence distinction, although the matrix alone cannot prove why.

### Confidence check

| Seed | Most-confident third accuracy | Least-confident third accuracy | Difference | Posts in each group |
|---|---:|---:|---:|---:|
| 42 | 0.769 | 0.231 | +0.538 | 13 |
| 7 | 0.769 | 0.308 | +0.462 | 13 |
| 2024 | 0.846 | 0.154 | +0.692 | 13 |

This ranks the predictions by model confidence; it is not a probability calibration test. Groups contain only 13 posts each.

## Verdicts and Diagnoses

Accuracy misses its target because seed 7 is below 0.60. Macro F1 misses on all three seeds, and the per-label floor misses in every seed. The label-balance and most-confident-third criteria meet their thresholds in all three trials. These criteria were proposed by AI before the original training run; they have not been changed.

The three claim-label F1 scores are low across trials while the guide label has 105 examples and the other labels have 55 each. The seed 42 matrix shows claim posts often classified as guides. The small test supports of 8 or 9 for each claim label make the scores volatile; label imbalance and overlap in how posts explain or give steps are plausible contributors, not established causes. Agreement evidence is pending, so inconsistent annotation cannot yet be assessed from the staff exercise. A token audit found 145 of 270 posts exceed the 128-token limit: 40/55 supported claims, 28/55 help requests, 77/105 guides, and 0/55 unsupported claims. This truncates different proportions by class and could conceal relevant context or encourage reliance on length; the counts alone do not establish its effect on accuracy. At 256 tokens, 82 posts still exceed the limit. Full counts are in `token_length_audit.json`.

### Worst-label examples

By lowest recall in the seed 42 matrix, `unsupported_claim` is the worst: 0 of 9 recovered, F1 0.000. Eight were classified as guides and one as a help request; no true guide was classified as an unsupported claim. Two guide-predicted errors include [this siren-control answer](https://gaming.stackexchange.com/a/419440) and [this explanation of meditation](https://gaming.stackexchange.com/a/418407). Both discuss actions a player can take, a possible overlap with the guide boundary. These are observations about the text, not proof of why the model erred. The complete actual predictions and confidences are in `predictions_three_seeds_before.json`; source attribution is retained in `labels.csv`.

---

## Agreement Report

**Status:** At Juan's request, Codex suggested the 30 labels in `my_staff_labels.csv` and explained them in `staff_label_worksheet.md`. They are AI-assisted, not independent student annotations. The staff reference labels have not been obtained or opened; no agreement rate or adjudications are available yet.

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

### First experiment: more training epochs

The original trials showed low claim-label F1 and improving validation loss over the original three epochs. As a test of undertraining, the first experiment changes the epoch count from 3 to 5; the initial learning rate remains 2e-5, batch size 8, maximum length 128, dataset and seeds are unchanged. The scheduler decays across the total training steps, so changing epoch count also changes its schedule over time. This is a training hypothesis, not proof of the cause of errors.

### Run Log - After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---:|---:|---:|---|
| Overall accuracy | at least 0.60 | 0.780 | 0.780 | 0.707 | MET |
| Macro F1 | at least 0.55 | 0.748 | 0.734 | 0.663 | MET |
| Lowest label F1 | each at least 0.40 | 0.615 | 0.364 | 0.429 | MISSED |
| Largest label share | at most 0.45 | 0.389 | 0.389 | 0.389 | MET |
| Most-confident-third accuracy | at least 0.70 | 0.846 | 0.769 | 0.923 | MET |

### Second experiment: longer inputs

The token audit found that 145/270 posts exceed 128 tokens, including 40/55 supported claims and 77/105 guides, compared with 0/55 unsupported claims. To test whether more context helps, this cumulative experiment keeps the first experiment's five epochs and changes the input limit from 128 to 256 tokens. At the new limit, 82/270 posts still exceed the limit. All other settings and the same seed-specific train, validation and test posts are held fixed.

### Run Log - After Second

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---:|---:|---:|---|
| Overall accuracy | at least 0.60 | 0.829 | 0.756 | 0.805 | MET |
| Macro F1 | at least 0.55 | 0.814 | 0.681 | 0.767 | MET |
| Lowest label F1 | each at least 0.40 | 0.615 | 0.200 | 0.615 | MISSED |
| Largest label share | at most 0.45 | 0.389 | 0.389 | 0.389 | MET |
| Most-confident-third accuracy | at least 0.70 | 0.846 | 0.769 | 0.923 | MET |

### Paired comparison

| Seed | Before accuracy | Five epochs accuracy | Five epochs + 256 tokens accuracy | Before macro F1 | Five epochs macro F1 | Five epochs + 256 tokens macro F1 |
|---|---:|---:|---:|---:|---:|---:|
| 42 | 0.610 | 0.780 | 0.829 | 0.461 | 0.748 | 0.814 |
| 7 | 0.561 | 0.780 | 0.756 | 0.399 | 0.734 | 0.681 |
| 2024 | 0.585 | 0.707 | 0.805 | 0.364 | 0.663 | 0.767 |

### Confidence comparison in the new runs

| Run | Seed | Most-confident third | Least-confident third | Difference | Posts per group |
|---|---:|---:|---:|---:|---:|
| after | 42 | 0.846 | 0.692 | +0.154 | 13 |
| after | 7 | 0.769 | 0.692 | +0.077 | 13 |
| after | 2024 | 0.923 | 0.462 | +0.462 | 13 |
| after_second | 42 | 0.846 | 0.923 | -0.077 | 13 |
| after_second | 7 | 0.769 | 0.692 | +0.077 | 13 |
| after_second | 2024 | 0.923 | 0.615 | +0.308 | 13 |

The same held-out texts are paired across configurations for each seed; different seeds use different test splits. These experiments were chosen after examining earlier results and reuse those held-out examples, so their comparisons are exploratory and should not be treated as an unbiased final estimate. The original Unit 5 results and test split remain unchanged. Each result JSON records settings, device and dataset hash; the corresponding predictions JSON records actual examples and confidence.

Five epochs versus three improved macro F1 in all three paired trials; per-seed changes were +0.287, +0.335, +0.299.
The 256-token limit versus 128 had mixed or unchanged macro F1 across the paired trials; per-seed changes were +0.066, -0.053, +0.105.

---

## What's Still Broken

The final experiment still misses the all-seed target for per-label F1: `supported_claim` scores 0.200 on seed 7, below the 0.40 floor. More independently reviewed examples for the weak categories and a fresh held-out evaluation would be useful next steps; the current evidence does not establish which intervention will work.

The original taxonomy was intended to distinguish claims by evidence and separate them from actionable guides. The initial seed 42 matrix instead sent 15 of 17 claim posts to the guide category, so the model did not reliably capture that boundary in the starting run. The pending staff reference and AI-assisted staff suggestions cannot independently verify Juan's labeling consistency. Further work stopped here because the staff reference file is unavailable and the original evaluation split has already been reused.

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**

# Unit 6 experiment plan

Declared before Unit 6 experiments: complete the confidence check, the worst-label error analysis, and a second measured improvement. The confidence check, worst-label analysis, and second measured experiment are recorded above with numerical evidence; staff agreement remains pending.

Keep the original criteria, Unit 5 outputs, taxonomy and baseline test split. Record three seeds (42, 7, 2024) before any improvement. Make one diagnosis-driven change, measure it on the same three seeds, then isolate and measure the second change in a third run log. Do not overwrite the first two result files.

The staff agreement exercise is pending the answer file provided by the TF. Juan requested AI-suggested labels, documented above, so any comparison describes AI-assisted agreement rather than his independent annotation. Do not fabricate adjudications.
