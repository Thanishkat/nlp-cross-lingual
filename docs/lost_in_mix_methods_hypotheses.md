# Lost in the Mix: Methods and hypotheses

This note summarizes selected methods from the final ACL 2026 paper. For the full-paper review and our adaptation, see [`lost_in_mix_acl2026_review.md`](lost_in_mix_acl2026_review.md).

## Construction methods

- **Noun-token switching:** English supplies the matrix frame; selected English nouns are replaced by aligned target-language equivalents.
- **ECT and MLF constraints:** candidate switch sites should preserve compatible surface structures and the matrix-language grammatical frame. These are constraints for candidate construction, not a naturalness guarantee.
- **LLM-centric generation:** a model marks candidate slots, then aligned translations fill those slots. The paper compares this approach with an alignment-based pipeline.
- **Ratio-token control:** approximately 20% of tokens are replaced without grammatical constraints.
- **Placeholder baseline:** a neutral marker helps separate foreign-language content effects from the disruption of replacement itself.

The authors compare GPT-4o and Claude 3.5 Sonnet for stimulus generation, select Claude after bilingual naturalness judgments, and use GPT-4o to compare generation pipelines. Human sanity checks remain part of the process.

## Evaluation and results

The main evaluation uses matched benchmark items and gold answers, multiple model families, zero-shot prompts, item accuracy, and deltas against monolingual baselines. It finds that mixing direction matters: adding non-English content to English commonly lowers accuracy, while English insertions can help on some non-English matrix inputs. Prompt mitigation is inconsistent; fine-tuning gives modest recovery in the reported setup.

## Project adaptation

Our pilot uses A (English), B (English matrix with Romanized Hindi), and C (the same Hindi spans rendered in Devanagari). Its planned contrasts are B−A, C−B, and C−A. We add tokenizer fragmentation measures that the paper did not report. Because the compared pretrained models differ in training data, architecture, and scale as well as tokenizer, any fragmentation–accuracy relationship is associational, not causal.
