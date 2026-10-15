# Acceptance criteria — TakeMeter

These five numeric targets were proposed by the AI assistant at Juan's request before training. Juan delegated choosing and writing the targets; they are disclosed here as AI-proposed rather than student-selected criteria.

1. **Overall accuracy:** At least **0.60** on the held-out test split. Four labels give a uniform random guesser 0.25 accuracy, and 0.60 is a useful but cautious target for a small, noisy text dataset.

2. **Macro F1:** At least **0.55** on the held-out test split. Macro F1 weights the four labels equally, which matters because `guide_or_solution` has more examples than each other label.

3. **Per-label F1:** F1 of at least **0.40 for every label** on the held-out test split. Each smaller label has 55 examples overall and only about eight in the test split, so a modest floor recognizes the uncertainty while requiring each category to work better than a near-total miss.

4. **Label balance:** No label may exceed **45%** of the full labeled dataset before training. This gives room for the 50-example guide stretch while keeping all four categories represented.

5. **Confidence:** Accuracy among the **most-confident third** of test predictions must be at least **0.70**. If the model cannot do better on its strongest predictions, its confidence is not useful for deciding which outputs to trust.

These targets were written before the training run. The course asks the student to choose these targets; that requirement was not met because the student delegated the choice. The course's 20 unaided cold labels are also not present: the included `cold_label_worksheet.md` has no AI label suggestions and remains unfilled.
