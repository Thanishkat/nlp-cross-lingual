# Related work to read for the Hindi tokenizer study

This is a focused reading list for extending the pilot toward a publishable study. It separates the literature already cited in the proposal from additional work that can sharpen the tokenizer and Hindi-script questions.

## Highest priority

1. **Mohamed et al. (2026), “Lost in the Mix.”** Main methodological comparison: controlled benchmark variants, ECT/MLF-guided noun switching, a random replacement condition, paired accuracy deltas, direction ablations, and reviewed stimulus generation. It does not measure tokenizer fragmentation. [ACL Anthology](https://aclanthology.org/2026.acl-long.2080/)
2. **Ravikiran et al. (2026), “Do Tokenizers Fail on Informal Hindi Expressions?”** Directly relevant to script and informal-Hindi tokenization. It evaluates boundary/integrity measures, downstream identification, and robustness to romanization and spelling variation. Treat its task-specific results as motivation, not as direct evidence about reasoning benchmarks. [ACL Anthology](https://aclanthology.org/2026.loreslm-1.2/)
3. **Altıntaş et al. (2026), “TokSuite: Measuring the Impact of Tokenizer Choice on Language Model Behavior.”** Particularly useful for causal interpretation: it compares models that vary tokenizer while holding architecture, data, training budget, and initialization constant, and includes a native-annotated multilingual robustness benchmark. This is a stronger design for tokenizer causality than comparing unrelated pretrained model families. [PMLR](https://proceedings.mlr.press/v306/altintas26a.html)
4. **Ali et al. (2024), “Tokenizer Choice for LLM Training: Negligible or Crucial?”** A warning against treating fertility/parity as performance explanations by themselves: the paper reports these intrinsic measures do not always predict downstream performance. Use token counts as measured predictors and report model/condition results separately. [arXiv](https://arxiv.org/abs/2310.08754)
5. **Petrov et al. (2023), “Language Model Tokenizers Introduce Unfairness Between Languages.”** Supports the motivation that tokenizer allocation can create unequal sequence lengths, cost, latency, and context budgets across languages. [NeurIPS paper](https://proceedings.neurips.cc/paper_files/paper/2023/file/74bb24dca8334adce292883b4b651eda-Paper-Conference.pdf)

## Hindi code-mixing and Romanization

- **Kodali et al. (2022), “SyMCoM: Syntactic Measure of Code Mixing.”** Adds a syntactic-variety perspective beyond word-balance measures such as CMI. It can motivate recording switch type or part-of-speech pattern as a secondary stimulus descriptor. [ACL Anthology](https://aclanthology.org/2022.findings-acl.40/)
- **Gautam (2026), “LIPI: Transliterating Hindi the Way People Type It.”** Notes that Romanized Hindi has no single standard spelling and studies naturally typed transliterations. This supports treating Romanization convention and spelling variation as explicit factors, rather than assuming every Devanagari-to-Latin mapping is equally natural. [ACL Anthology](https://aclanthology.org/2026.wat-1.2/)
- **Winata et al. (2026), CodeMixQA.** Human-annotated parallel code-switched QA across language pairs and native/transliterated script variants; useful as a possible external comparison set. [arXiv](https://arxiv.org/abs/2601.07153)
- **Das et al. (2026), Indi-RomCoM.** Romanized Indic-English instructions with controlled mixing intensity; useful for a later density sensitivity analysis, although it is not a matched Romanized-versus-native-script Hindi reasoning set. [arXiv](https://arxiv.org/abs/2606.30790)
- **Yang & Chai (2025), CodeMixBench.** A broad multilingual code-mixing benchmark with LLM-oriented tasks; useful for external validation after the controlled pilot. [ACL Anthology](https://aclanthology.org/2025.emnlp-main.109/)

## Tokenizer measures to operationalize

- **Rust et al. (2021), “How Good Is Your Tokenizer?”** Supports fertility and multilingual tokenizer comparisons. [ACL Anthology](https://aclanthology.org/2021.acl-long.243/)
- **Chiu (2026), TokLens.** Defines a broader family of intrinsic tokenizer metrics, including fertility, characters per token, and single-token retention. [ACL Anthology](https://aclanthology.org/2026.acl-srw.18/)
- **Gambäck & Das (2016), CMI; Srivastava & Singh (2021), metric limitations.** Use CMI to describe language balance, but do not treat it as a measure of grammaticality, switch placement, naturalness, or tokenizer burden. [CMI paper](https://aclanthology.org/L16-1292/) · [metric limitations](https://aclanthology.org/2021.calcs-1.2/)

## Recommended research gap and RQs

The proposal already asks whether the B−A language-mixing contrast differs from the C−B script contrast, whether Romanized Hindi outperforms matched Devanagari, and whether fragmentation is associated with accuracy. The most defensible extension is to test these together on reviewed, item-matched prompts, then add orthographic variation and naturalistic Hinglish as a separate phase.

Potential added questions:

1. Do Romanization convention and common spelling variants change tokenizer fertility and accuracy for the same Hindi item?
2. Does fragmentation predict errors after accounting for item difficulty, condition, task type, and model family?
3. Are effects concentrated in particular lexical categories or switch patterns, beyond overall CMI?
4. Do controlled ECT/MLF-guided switches and human-naturalized Hinglish show the same relationship between tokenization and accuracy?

The current 10-item workbook is too small for confirmatory claims. The proposed 45-item batch can support a feasibility analysis and variance estimates. A larger preregistered follow-up should be sized from those estimates. A few different pretrained models cannot identify tokenizer causality because tokenizer, training data, model size, and architecture vary together; causal claims require a controlled same-model/same-training comparison such as TokSuite's design.

## Stimulus quality policy

Use ECT/MLF as constraints for candidate switch sites, not as a naturalness oracle. Keep aligned target-language text, switch-site rationale, exact Hindi span, Romanization mapping, reviewer decisions, and adjudication in the item record. A model may propose candidates, but two independent bilingual reviewers and an adjudication step decide inclusion. Preserve a separate naturalized condition instead of mixing human-authored and rule-generated prompts in one analysis.
