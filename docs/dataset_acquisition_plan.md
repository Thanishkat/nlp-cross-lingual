# Dataset Acquisition Plan

## Current Constraint

The current English-Hindi pilot uses three matched conditions: English (A), English matrix with Romanized Hindi (B), and the same Hindi spans in Devanagari (C). Telugu-English is a later track and should begin with its own reviewed, language-specific design.

This matters because code-mixed text can look obviously wrong to a fluent reader. The dataset must therefore prioritize naturalness and semantic equivalence over raw size.

## Dataset Requirements

For the main evaluation set, each item should have:

- A Roman-script code-mixed input.
- A clean English equivalent or gloss.
- Optional metadata: language tags, matrix language, domain, source, annotator status.
- A quality flag showing whether it is human-authored, human-translated, manually refined, synthetic, or unverified.

Do not use unverified LLM-generated code-mixed sentences as final evaluation data. They can be used only for pilot stress tests or model fine-tuning experiments, and must be labeled as synthetic.

## Recommended Source Priority

### Tier 1: Use First

1. COMI-LINGUA
   - Hindi-English code-mixed text.
   - 181,463 expert-annotated instances.
   - Includes MT data with English, Romanized Hindi, and Devanagari Hindi fields.
   - Good fit for large-scale Roman-script Hinglish/English-equivalent evaluation.
   - Caveat: some fields are LLM-generated then manually refined, so keep the provenance column.

2. PHINC
   - 13,738 Hinglish-English parallel social-media sentences.
   - Hinglish and English are Roman-script.
   - Good fit for natural Hinglish with English equivalents.
   - Caveat: the paper itself notes that some translations require correction, so it needs a quality audit before final evaluation.

3. WMT22 MixMT / HinglishEval / HinGE
   - Useful for monolingual-to-code-mixed and code-mixed-to-English evaluation.
   - Prefer human-generated splits over synthetic splits.
   - Good for extra Hinglish scale and comparison with prior shared-task work.

### Tier 2: Useful But Not Enough Alone

4. GLUECoS
   - Hindi-English code-switched benchmark covering LID, POS, NER, sentiment, QA, and NLI.
   - Useful for benchmark-style tasks, but not necessarily a large open-ended prompt source.

5. Telugu-English LID corpora
   - Existing work includes manually annotated Telugu-English code-mixed Twitter/blog datasets.
   - Useful for studying Roman-script Telugu-English naturalness and token-level language ID.
   - Caveat: these are generally not large parallel prompt datasets with clean English equivalents.

## Telugu-English Strategy

For Telugu-English, do not assume there is a ready PHINC-scale public dataset with clean English equivalents.

Recommended approach:

1. Start with a smaller Telugu-English pilot from manually annotated code-mixed corpora if accessible.
2. Build a controlled evaluation set from English seed prompts.
3. Have bilingual Telugu-English speakers rewrite each prompt naturally in Roman-script Telugu-English.
4. Add a second bilingual reviewer for semantic equivalence and naturalness.
5. Keep Telugu-English as a smaller but higher-quality track until more data is found or created.

Target sizes:

- Construction batch: the attached 10-item/30-prompt batch, after independent review.
- Feasibility batch: the proposal's 45 items/135 prompts, after source and license checks and independent review.
- Confirmatory sample: choose only after estimating item-level variability and completing an appropriate power analysis; do not infer it from a generic corpus-size target.

## Quality Gates

Each example should pass these checks before entering the final eval set:

- `roman_only`: no native-script text in Phase 1.
- `not_pure_english`: exclude examples that are basically English unless used as the English baseline.
- `has_english_equivalent`: must have a clean English meaning.
- `semantic_match`: code-mixed input and English equivalent mean the same thing.
- `naturalness_score`: fluent bilingual reviewer score, recommended 1-5.
- `domain_label`: social, assistant query, factual, advice, reasoning, local context, etc.
- `length_bucket`: short, medium, long.
- `toxicity_or_privacy_flag`: remove unsafe personal data and handle abusive content deliberately.

## Sampling Plan

Build balanced subsets instead of taking the first N rows:

- Domains: social, practical advice, factual, local/cultural, reasoning, task/instruction.
- Length: short, medium, long.
- Mixing density: low, medium, high.
- Matrix language: English-dominant, Hindi/Telugu-dominant, balanced.
- Named entities: with and without names/places/products.

For the first large run:

- 5,000 Hinglish-English pairs from COMI-LINGUA.
- 5,000 Hinglish-English pairs from PHINC after filtering.
- 1,000 Telugu-English pairs if a reviewed source or bilingual annotation pass is available.
- 1,000 English-only baseline prompts matched by domain and length.

## Annotation Columns To Create

Use a manifest with these fields:

- `example_id`
- `source_dataset`
- `source_split`
- `language_pair`
- `script_condition`
- `code_mixed_text`
- `english_equivalent`
- `domain`
- `mixing_density`
- `matrix_language`
- `naturalness_score`
- `semantic_equivalence_score`
- `quality_status`
- `reviewer_id`
- `notes`

## Decision

For now, the project should focus on Roman-script Hinglish at scale, while building Telugu-English as a smaller curated track. This gives enough data for thousands of prompts without sacrificing the credibility of the evaluation.

