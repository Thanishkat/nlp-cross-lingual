# English-Hindi pilot protocol

## Design

Use the same source item and answer key across three prompt conditions:

| Condition | Prompt form | Contrast |
|---|---|---|
| A | English baseline | Reference |
| B | English matrix with Romanized Hindi spans | B−A estimates adding Hindi in Latin script |
| C | Same Hindi spans in Devanagari | C−B compares matched script renderings |

C−A is also reported as the total difference from the English baseline. This design does not estimate a general script main effect because there is no English-in-Devanagari comparison cell.

## Current and planned samples

The attached construction workbook has 10 items and 30 prompts: four Belebele, three XNLI, and three MMMLU items. The attached copy marks human review pending and all model runs not started. Treat these as draft stimuli, not evaluated or accepted data.

The proposal's next feasibility batch is 45 items/135 prompts, subject to sourcing, license review, construction, and bilingual validation. The local spreadsheet reserves 35 empty item slots. Select new records from suitable splits and preserve their stable source IDs, source text locally, gold answers, licenses, and transformation history.

## Stimulus quality gate

Apply ECT/MLF to identify candidate switch sites and preserve aligned meaning. Record each switch point, Hindi span, transliteration, source adaptation, and answer key. Two bilingual reviewers independently rate meaning preservation, answer preservation, naturalness, and Romanization. Adjudicate disagreements. Do not run model evaluations until the batch is frozen.

## Tokenizer and model records

Pin exact model and tokenizer revisions. Apply each model's chat template and record both actual chat input token count and lexical span tokenization. For Hindi spans report token fertility, single-token retention, characters per token, and matched-prompt token inflation. Normalize Unicode consistently and record the normalization form.

For model results, retain provider/model version, revision, prompt/system template, decoding parameters, run timestamp, raw output, parsed answer, and correctness. Keep unparseable outputs missing with an explicit status.

## Analysis

Report item-paired accuracy and B−A, C−B, and C−A deltas by model, dataset, and condition. Resample by base item for uncertainty intervals. Relate fragmentation to item correctness descriptively; model-family differences are confounds. A causal tokenizer claim requires a controlled same-model training experiment with tokenizer as the manipulated factor.
