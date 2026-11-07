# English-Hindi pilot protocol, version 1

## Scope

Run a reviewed, matched English-Hindi item set before expanding to Marathi or other languages. The supplied 10-item workbook is a construction and bilingual-review batch. The proposal's 45-item/135-prompt set is the next feasibility sample, not a confirmatory sample.

## Conditions and primary contrasts

| Code | Prompt form | Primary use |
|---|---|---|
| A | English baseline, Latin script | Reference |
| B | English matrix with Romanized Hindi spans | Language-mixing contrast, B−A |
| C | Same Hindi spans as B in Devanagari | Matched script contrast, C−B |

The design estimates conditional contrasts. It does not estimate a general script main effect. A Hindi-only condition may be an additional baseline, but it does not complete the missing English-in-Devanagari cell.

## Stimulus construction and review

1. Freeze source release, split, stable item ID, source text, answer key, and license before inspecting model outputs.
2. Preserve task framing, answer options, punctuation, numerals, and source meaning across conditions wherever the task allows.
3. Record each modified Hindi span, its alignment/provenance, switch-point rationale, Romanization convention, and any English adaptation.
4. Use ECT/MLF as candidate-site constraints. Retain an English grammatical frame in B/C, avoid idioms/fixed expressions, and use aligned Hindi material rather than independent free generation where parallel text exists.
5. A model may suggest candidate switches, but the candidate is not accepted automatically. Two bilingual reviewers independently rate meaning preservation, answer preservation, naturalness, and Romanization; adjudicate disagreements and record the decision.
6. Reviewers must not validate items they materially rewrote. Do not run models until the accepted batch is frozen.
7. Apply the per-item CMI gate before release: `CMI = 1 − max(EN, HI) / (EN + HI)` on manipulated fields only, with target 0.30 ± 0.02 (0.28–0.32 inclusive). Count whitespace-delimited lexical tokens after stripping edge punctuation; exclude tokens containing numerals and fixed instructions, field labels, answer labels/options, and punctuation; count established Hindi borrowings in the designated Hindi spans as Hindi. Record EN/HI counts and CMI for every base item. The item must pass individually; a passing batch average is insufficient. Keep the Hindi lexical spans and switch locations matched between B and C. This is a construction gate, not a tokenizer metric or a naturalness guarantee.

Do not call any batch “perfect.” Report the review process and remaining limitations.

## Model and tokenizer records

Before each run, record provider, exact model ID, immutable checkpoint/revision, tokenizer revision, chat-template version, API/model version where applicable, run date, prompt template, system prompt, temperature, output limit, and normalization. Keep API keys in environment variables.

For each prompt/model pair, record:

- actual input token count after the model's chat template;
- plain prompt token count and lexical token count;
- Hindi-span token count measured by token offsets in the complete normalized prompt;
- Hindi word count, token fertility, single-token retention, and characters per token;
- token inflation from the matched A prompt;
- raw response, parsed answer, correctness, and parse status.

Keep full-prompt cost counts separate from lexical span metrics. Exclude chat-control tokens from lexical fertility. Store the normalization and tokenizer revision needed to reproduce each count.

## Evaluation and analysis

Use the same answer instructions and fixed decoding settings across models where the API permits. The primary outcome is item-level correctness. Report accuracy by model, dataset, and condition; paired deltas B−A, C−B, and C−A; and uncertainty intervals resampled by base item. Preserve unparseable/invalid outputs as explicit statuses rather than silently counting them as correct.

Relate item-level fragmentation to correctness descriptively and, if sample size permits, with a pre-specified mixed-effects logistic model. With only a few model families, treat model as a fixed effect. A tokenizer–accuracy association is not causal because pretrained models also differ in data, size, architecture, and language competence. A tokenizer-causality claim requires a controlled same-model training comparison.

## Reporting gates

- **Construction batch:** 10 items, 30 prompts; human review must pass before use.
- **Feasibility batch:** proposed 45 items, 135 prompts; use it to test procedure and estimate variability.
- **Confirmatory study:** determine item count from the pilot's variability and a power analysis; preregister exclusions, contrasts, and analysis before viewing model outputs.
- Keep optional GPT/Claude baselines separate from the primary open-model comparison unless model version, prompt, and output settings can be frozen.
