# Research design

## Scope

The project connects three literatures: Indic-language coverage and evaluation (IndicXTREME / IndicBERT v2; IndicGenBench), code-switched benchmark evaluation (including *Lost in the Mix*), and tokenizer burden/fairness. The near-term study is a reviewed English-Hindi benchmark pilot measuring accuracy and token/context burden across matched English, Romanized Hindi, and Devanagari Hindi prompts. No single paper is a project blueprint. Add Marathi after the Hindi-English workflow is stable; treat Telugu, Kannada, and other Dravidian languages as a separate extension with language-specific review and sources.

## Research questions

1. How does accuracy change from English to English-matrix Romanized Hindi code-mixing (B−A)?
2. How does accuracy differ when the same Hindi spans are written in Devanagari rather than Roman script (C−B)?
3. Is model accuracy associated with Hindi-span token fertility, single-token retention, characters per token, or prompt token inflation?
4. Do these patterns vary across model families, dataset families, and task types?
5. Under a fixed context-token budget, do conditions with higher prompt token burden fit fewer in-context examples, and does accuracy differ from a fixed-number-of-exemplars comparison?

## Conditions and outcomes

- A: English baseline.
- B: English matrix with Romanized Hindi spans.
- C: matched Hindi spans in Devanagari.
- Primary outcome: item-level correctness.
- Tokenizer outcomes: complete chat input count, Hindi-span token count and fertility, single-token retention, characters per token, and token inflation versus A.
- Optional context-efficiency outcome: number of matched exemplars fitting within the same token budget, plus accuracy under fixed-token and fixed-exemplar comparisons.

The main paired contrasts are B−A, C−B, and C−A. C−B estimates a script contrast only for the matched Hindi content and English matrix used here; it is not a general script effect.

## Stimulus and analysis plan

Preserve source IDs, splits, source text, answer keys, licenses, adaptations, and Hindi-span alignment. ECT/MLF guide candidate switch locations but do not certify naturalness. Two bilingual reviewers independently assess meaning, answer preservation, naturalness, and Romanization; adjudicate before model runs.

Apply the pilot's CMI control to each base item: `CMI = 1 − max(EN, HI) / (EN + HI)`, with a target of 0.30 ± 0.02 (inclusive range 0.28–0.32). EN and HI are lexical word counts from manipulated stimulus fields only. Count whitespace-delimited tokens after stripping edge punctuation, exclude tokens containing numerals and fixed instructions/labels/answer options, and count established Hindi borrowings within designated Hindi spans as Hindi. Record counts and the CMI gate per item; do not rely on the 45-item batch mean. Match the Hindi lexical content and switch locations between B and C. This construction balance rule is distinct from tokenizer fertility and does not itself guarantee grammatical or natural switching.

The attached 10-item workbook is a construction pilot. The proposal's 45-item/135-prompt set is a feasibility batch for process and variance estimates, not a confirmatory sample. Use its estimates to plan a larger preregistered study; justify the final sample size from expected effects and item-level variance rather than carrying forward 45 by default. Report accuracy and paired item deltas by model, condition, and dataset; account for repeated items and cluster uncertainty by base item.

Measure context efficiency explicitly if it is part of the main claim: compare a fixed number of exemplars with a fixed context-token budget. Exact model-tokenizer pairs are required for token-level claims. For hosted GPT/Claude systems whose tokenizer cannot be verified, report model accuracy in a separate track and mark the tokenizer as unavailable.

Any relationship between tokenization and accuracy across unrelated pretrained models is associational because tokenizer, data, scale, architecture, instruction tuning, and language capability vary together. A causal claim requires a controlled tokenizer intervention with training conditions held constant. A well-powered matched benchmark and careful association analysis can still support a useful paper without claiming causality.

## Future extensions

After the Hindi-English workflow is stable, add Marathi with its own bilingual review and script-aware validation, then consider a separate Telugu-English, Kannada-English, or Tamil-English track. Keep controlled benchmark variants and naturalistic Hinglish as distinct experimental tracks. A separate generation study could test model-generated code-mixed answers for naturalness and meaning preservation; do not combine it with the current comprehension/accuracy outcomes without a distinct design.

