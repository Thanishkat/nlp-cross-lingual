# Reading synthesis: Indic resources, generation, and tokenizer burden

## Purpose of this note

This note synthesizes the two ACL papers shared for this project and translates their methods and limitations into a research plan. They are complementary foundations, not instructions to reproduce either paper. The PDFs remain in the researcher’s local library; the public repository links to the official ACL Anthology records rather than redistributing copies.

## Paper 1: Indic resources, benchmark, and models

**Doddapaneni et al. (2023), “Towards Leaving No Indic Language Behind: Building Monolingual Corpora, Benchmark and Models for Indic Languages.”** The paper treats inclusive Indic NLP as a system-level gap: useful work needs language data, evaluation benchmarks, and models that cover the languages together. It contributes IndicCorp v2 (20.9B tokens across 24 languages), IndicXTREME (105 task-language evaluation sets across 20 languages, including 52 new sets), and IndicBERT v2. The benchmark spans classification, structure prediction, question answering, and retrieval; new datasets are human-supervised and include tasks created from scratch as well as carefully translated data.

The paper does more than release resources. Its experiments compare multilingual and Indic-focused models and ablate pretraining data and transfer choices. IndicBERT v2 generally outperforms its comparison systems across the suite, although no model wins every task. High-quality parallel data can help the translation-language-modeling objective, while lower-quality back-translated parallel data can hurt. In-language or in-family development data can improve model selection over English-only development data, and Hindi can serve as a stronger transfer language than English for some Indic tasks. Low-resource languages remain substantially harder, with data availability, script sharing, and related-language coverage all relevant.

**Tokenizer relevance:** the paper reports tokenizer fertility comparisons as a supporting analysis. Its tokenizer table gives a fertility value of 1.7 for IndicBERT and MuRIL, 2.2 for XLM-R, and 2.8 for mBERT in the reported comparison. The work does not make tokenizer fertility its main independent variable, nor does it isolate tokenizer effects from corpus, architecture, pretraining, and model differences. Its direct value to this project is a precedent for reporting tokenization alongside language coverage and model performance, and a warning to record script and language-family coverage rather than treating “Indic” as one homogeneous category.

## Paper 2: generation evaluation and context cost

**Singh et al. (2024), “IndicGenBench: A Multilingual Benchmark to Evaluate Generation Capabilities of LLMs on Indic Languages.”** This work addresses a different gap: multilingual language models need evaluation on user-facing generation, not only NLU. IndicGenBench extends existing sources into multi-way parallel evaluation data for 29 Indic languages, 13 scripts, and four language families. Its five settings cover cross-lingual summarization, machine translation, multilingual QA, and two cross-lingual QA directions. The authors use human curation and professional translations, then evaluate a range of proprietary and open models across one-shot, few-shot, language-transfer, and fine-tuning settings.

The study reports large gaps between English and Indic performance and performance differences across resource tiers, model families, tasks, and prompting setups. In-context examples generally help. Hindi exemplars can be more useful than English exemplars for Indic targets, while same-language examples often perform best. Their qualitative inspection also finds mixed-language outputs, incorrect inflection, hallucinated additions, omissions, and sense errors. These observations support evaluating error type and language fidelity rather than reducing every output to a single score.

**Tokenizer relevance:** Section 3.6 measures fertility with OpenAI BPE and finds large differences across languages (reported range 4.1–19.9). The paper then shows how high fertility consumes a fixed context budget, leaving room for fewer in-context examples. This motivates our context-efficiency question. However, the analysis is not a causal test that the tokenizer caused an accuracy gap: the PaLM-2 tokenizer was not public, and the reported BPE fertility is not the tokenizer of every evaluated model. Our study should make exact tokenizer-to-model correspondence explicit and mark inaccessible tokenizers as unknown rather than infer them.

The paper also states that translation extensions may miss India-specific entities and linguistic nuance, and it does not cover long-form generation or reasoning. This is relevant to our design: human review and local naturalness matter, and the current benchmark should make bounded claims about its selected tasks rather than generalize to all Indic language use.

## How the papers fit with code-switching work

The project draws on three strands with different roles:

| Strand | What it contributes | What it does not establish for this study |
|---|---|---|
| Indic model/resource evaluation (Doddapaneni et al., 2023) | Language coverage, benchmark construction, tokenizer metrics as diagnostics, transfer and script considerations | A controlled tokenizer-to-accuracy causal effect |
| Indic generation/context evaluation (Singh et al., 2024) | Generation tasks, resource-tier comparisons, in-context prompt design, context-budget implications of fertility | That fertility alone explains accuracy or that generic OpenAI BPE represents every tested model |
| Code-switching evaluation (Mohamed et al., 2026, *Lost in the Mix*) | Matched multilingual items, theory-guided switch sites, code-switch accuracy contrasts, human review | A script-matched Hindi comparison or tokenizer-fragmentation analysis |

Our A/B/C design brings these together: A is English; B inserts reviewed Romanized Hindi spans into the English matrix; C uses the same Hindi content and switch sites in Devanagari. ECT/MLF can constrain candidate switch sites, while bilingual reviewers decide whether a candidate is acceptable. These procedures do not guarantee naturalness, so reviewer agreement, adjudication, and provenance remain part of the evidence.

## A publishable question and what would count as evidence

### Proposed main question

**How do language mixing and script affect LLM accuracy and context efficiency on matched English-Hindi benchmark items, and how much of the item-level variation is associated with tokenizer fragmentation?**

This question combines the controlled contrasts of code-switching evaluation with the tokenizer and context-budget concerns from Indic generation work. It avoids claiming in advance that tokenization is the cause of weaker code-switched performance.

### Research questions

1. **Accuracy:** On the same source items, what are the paired accuracy changes for B−A (Hindi insertion in Roman script), C−B (matched Devanagari vs Roman script), and C−A?
2. **Tokenizer burden:** For each exact tokenizer/model pair, how do Hindi-span fertility, single-token retention, characters per token, complete prompt tokens, and token inflation vary across A/B/C and item types?
3. **Association:** Does item-level fragmentation predict correctness after accounting for item difficulty, condition, dataset/task, and model, with uncertainty clustered at the base item?
4. **Context efficiency:** Under a fixed context-token budget, do conditions/models with higher prompt burden fit fewer matched exemplars, and does performance differ from a fixed-number-of-exemplars comparison?
5. **Error profile:** Are errors associated with code-mixed spans, script, answer parsing, or language drift, as judged with a pre-registered error taxonomy and blinded human review?

### Evidence boundary

The current 10-item/30-prompt construction batch checks workflow and reviewer materials; it is not evidence for a publishable performance claim. The planned 45-item/135-prompt set is a feasibility batch for stimulus quality, variance, and analysis plumbing. Use it to estimate uncertainty and inform a power analysis for a larger confirmatory sample. The actual sample size must be justified from pilot variance and the planned outcome model rather than chosen because 45 or 135 appeared in an earlier plan.

With unrelated pretrained models, tokenizer, pretraining corpus, model scale, architecture, instruction tuning, and language proficiency vary together. A regression or correlation can establish an association conditional on measured covariates, not a causal tokenizer effect. A causal claim requires a separate controlled experiment that changes tokenizer while holding training data, architecture, model size, optimization, and compute budget as constant as practical. If that is infeasible, describe the study as an empirical relationship between tokenizer burden and performance.

Hosted systems such as GPT or Claude should only have token metrics attached when an exact public tokenizer/model mapping is established. Otherwise keep their answer-accuracy comparison as a separate hosted-model track and label tokenizer access unavailable. For reproducibility, record model version, date, system and task prompts, decoding settings, API/provider, and raw response metadata.

## Recommended staged project

### Phase 1: Finish and report the feasibility study

- Freeze the 45 matched items only after source/license checks, two independent bilingual reviews, adjudication, per-item CMI gate, and answer-preservation checks.
- Balance 15 items per benchmark only if source quality and item eligibility allow it; preserve benchmark identity and report counts honestly if balance changes.
- Select exact models from distinct families only after resource, inference, and tokenizer availability checks. A compact set of well-documented open-weight model/tokenizer pairs is more informative than a long list of unpinned model names.
- Run the same frozen prompt templates and scoring procedure across A/B/C. Separate local open-weight runs (with tokenizer access) from hosted proprietary runs (where tokenization may be unavailable).
- Report per-item paired contrasts, confidence intervals, reviewer agreement, token burden, and error cases. Label results exploratory.

### Phase 2: Confirm the main finding

- Use Phase 1 estimates to plan a larger, preregistered sample with enough items per dataset/task and balanced language/script conditions.
- Where feasible, compare a context-budget condition (same token budget) with a fixed-exemplar-count condition. This tests the mechanism suggested by IndicGenBench more directly than token counts alone.
- Fit an item-level model that accounts for repeated measurements (same item across conditions and models); report model-family and task interactions, and use item-clustered uncertainty.
- Include blinded output evaluation and a compact, pre-defined error taxonomy. Report inter-rater agreement and adjudication rather than only consensus scores.

### Phase 3: Decide whether a tokenizer-causal paper is warranted

If Phase 1–2 show a stable association and there is compute/modeling support, design a controlled tokenizer intervention or retraining comparison. Otherwise the association study plus a carefully constructed matched benchmark can still be a research contribution, provided claims are narrow, comparisons are powered, and the dataset/code are reproducible and licensable.

### Extensions after the first study

- **Marathi:** a natural next language given the Indo-Aryan relationship, but it requires its own reviewer pool, script-aware construction, and answer-preserving validation; linguistic relatedness does not mean Hindi rules transfer unchanged.
- **Tamil/Telugu/Kannada:** a separate Dravidian-language research track with its own language expertise and sampling; do not treat these as mere substitutions into the Hindi protocol.
- **Naturalistic Hinglish:** analyze separately from controlled benchmark edits. Use naturally produced or reviewed examples and preserve source/provenance. Do not pool these with ECT/MLF-constrained item transformations without an explicit design.
- **Generation:** a future task could test whether models can produce natural, meaning-preserving code-mixed answers, evaluated by bilingual raters. This is distinct from the current comprehension/benchmark-accuracy question and should be a separate study aim.

## Practical takeaway

The strongest near-term contribution is not “tokenization causes poor code-switching.” It is a transparent, human-reviewed, matched evaluation of English, Romanized Hindi mixing, and Devanagari Hindi, reporting accuracy and exact token/context burden together. If the accuracy gaps persist and fragmentation predicts item errors under a careful analysis, that provides evidence for a focused follow-up. If token burden does not explain performance, that is also informative: it directs attention toward language competence, prompt behavior, model training, or stimulus difficulty instead.

## References

- Doddapaneni, S., Aralikatte, R., Ramesh, G., Goyal, S., Khapra, M. M., Kunchukuttan, A., & Kumar, P. (2023). Towards Leaving No Indic Language Behind: Building Monolingual Corpora, Benchmark and Models for Indic Languages. *Proceedings of ACL 2023*, 12402–12426. https://aclanthology.org/2023.acl-long.693/
- Singh, H., Gupta, N., Bharadwaj, S., Tewari, D., & Talukdar, P. (2024). IndicGenBench: A Multilingual Benchmark to Evaluate Generation Capabilities of LLMs on Indic Languages. *Proceedings of ACL 2024*, 11047–11073. https://aclanthology.org/2024.acl-long.595/
- Mohamed, A., Zhang, Y., Vazirgiannis, M., & Shang, G. (2026). Lost in the Mix: Evaluating LLM Understanding of Code-Switched Text. *Proceedings of ACL 2026*. https://aclanthology.org/2026.acl-long.2080/

