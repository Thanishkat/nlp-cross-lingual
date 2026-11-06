# Research design

## Scope

Begin with a reviewed English-Hindi benchmark pilot and measure how model accuracy and tokenizer fragmentation vary across matched English, Romanized Hindi, and Devanagari Hindi prompts. Add Marathi after this workflow is stable; treat Telugu, Kannada, and other Dravidian languages as a separate extension with language-specific review and sources.

## Research questions

1. How does accuracy change from English to English-matrix Romanized Hindi code-mixing (B−A)?
2. How does accuracy differ when the same Hindi spans are written in Devanagari rather than Roman script (C−B)?
3. Is model accuracy associated with Hindi-span token fertility, single-token retention, characters per token, or prompt token inflation?
4. Do these patterns vary across model families, dataset families, and task types?

## Conditions and outcomes

- A: English baseline.
- B: English matrix with Romanized Hindi spans.
- C: matched Hindi spans in Devanagari.
- Primary outcome: item-level correctness.
- Tokenizer outcomes: complete chat input count, Hindi-span token count and fertility, single-token retention, characters per token, and token inflation versus A.

The main paired contrasts are B−A, C−B, and C−A. C−B estimates a script contrast only for the matched Hindi content and English matrix used here; it is not a general script effect.

## Stimulus and analysis plan

Preserve source IDs, splits, source text, answer keys, licenses, adaptations, and Hindi-span alignment. ECT/MLF guide candidate switch locations but do not certify naturalness. Two bilingual reviewers independently assess meaning, answer preservation, naturalness, and Romanization; adjudicate before model runs.

The attached 10-item workbook is a construction pilot. The proposal's 45-item set is a feasibility batch for process and variance estimates, not a confirmatory sample. Report accuracy and paired item deltas by model, condition, and dataset; use item-level resampling for uncertainty. Any relationship between tokenization and accuracy across different pretrained models is associational because tokenizer, data, scale, and architecture vary together.

## Future extensions

After the Hindi-English workflow is stable, add Marathi as the next closely related language, then a separate Telugu-English, Kannada-English, or Tamil-English track with appropriate bilingual reviewers. Keep controlled benchmark variants and naturalistic Hinglish as distinct experimental tracks. A tokenizer-causality study requires controlled training runs that vary tokenizer while holding the rest of the training setup constant.
