# Source Notes

## Main paper

Mohamed, Amr, Yang Zhang, Michalis Vazirgiannis, and Guokan Shang. 2026. “Lost in the Mix: Evaluating LLM Understanding of Code-Switched Text.” ACL 2026. [Paper](https://aclanthology.org/2026.acl-long.2080/) · [Official implementation](https://github.com/amr-mohamedd/Lost-in-the-Mix).

The paper evaluates controlled code-switched variants of Belebele, MMLU, and XNLI in English, Arabic, German, French, and Chinese. Its central construction method replaces selected English nouns with aligned equivalents from parallel benchmark text. Equivalence Constraint Theory (ECT) and the Matrix Language Frame model (MLF) guide candidate switch positions; they do not guarantee naturalness. The authors compare this with alignment-based construction, include a roughly 20% random ratio-token condition and a placeholder baseline, and conduct human sanity checks.

The study reports directional accuracy differences between matrix-language conditions and tests prompting and fine-tuning mitigations. It does not measure tokenization or compare Romanized Hindi with Devanagari. See [`lost_in_mix_acl2026_review.md`](lost_in_mix_acl2026_review.md) and [`paper_full_reading_notes.md`](paper_full_reading_notes.md) for detailed notes.

## Current project source set

The attached pilot workbook contains 10 candidate items and 30 A/B/C prompts based on Belebele, XNLI, and MMMLU. In the attached local copy, each item is held pending two-person bilingual review and all prompts are not run. The source questions and workbook remain local; the public repository contains no benchmark prompt text.

The proposal's next feasibility target is 45 items and 135 prompts. Those 35 additional items must be sourced, licensed, constructed, and reviewed before being added. Do not treat blank workbook expansion slots as stimuli.

## Data handling

Record source dataset, release/version, split, stable item ID, license, source URL, text transformation, answer key, and reviewer decisions for every item. Keep source text and model outputs private until redistribution terms are verified. Use ECT/MLF as construction constraints and document switch points; two independent bilingual reviewers plus adjudication decide whether items are usable.
