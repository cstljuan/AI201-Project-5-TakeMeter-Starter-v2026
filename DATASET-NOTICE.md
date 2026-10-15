# Dataset source and attribution

`labels.csv` contains public user posts from Arqade, the Gaming Stack Exchange site. The dataset includes the post author's display name, public source URL, and license in each row's `note` field. Answers also include their parent question URL. Post HTML was converted to plain text for classification.

Only records marked `CC BY-SA 4.0` in Stack Exchange API metadata and dated on or after 2018-05-02 were selected. The course project's labels and notes are added by the student; source post text remains attributed to its author and source. The source material's ShareAlike terms apply to adaptations. See the [Stack Exchange licensing terms](https://stackoverflow.com/help/licensing) and [Creative Commons Attribution-ShareAlike 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

AI generated the initial label suggestions in the current CSV. Juan reviewed the suggestions and confirmed or corrected each one. Rows are marked `AI-prelabel; reviewed by Juan`. A separate worksheet contains 20 posts without label suggestions for independent cold labeling.
