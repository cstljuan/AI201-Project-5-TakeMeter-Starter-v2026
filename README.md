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

**Base model:**

**Settings:** <!-- epochs, learning rate, batch size, seed -->

**Anything I changed from the defaults, and why:**

**Split sizes:** <!-- train / val / test, and per-label counts in the test
split. If a label had fewer than about 8 in test, say so — it explains a lot
of next unit's variance. -->



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
- *What I changed:* Juan reviewed all 270 candidate labels against the taxonomy and confirmed or corrected them. The separate cold-label worksheet has no suggestions and remains for independent labeling.

**Acceptance criteria disclosure:** At Juan's request, AI proposed the five numeric targets in [criteria.md](criteria.md) before training. The course's requirement that the student choose those targets was not met.

**Pre-labelling disclosure:** AI generated initial label suggestions for the Arqade dataset; Juan reviewed all suggestions and confirmed or corrected them. Each row is marked `AI-prelabel; reviewed by Juan`. Those labels are not cold. The separate 20-post cold-label worksheet has no label suggestions and remains unfilled, so the course's cold-label requirement was not met.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy |  |  |  |
| Macro F1 |  |  |  |
| F1 — `label_one` |  |  |  |
| F1 — `label_two` |  |  |  |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

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

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



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
