# Lost in the Mix: Full-paper review

**Paper:** Amr Mohamed, Yang Zhang, Michalis Vazirgiannis, and Guokan Shang. 2026. “Lost in the Mix: Evaluating LLM Understanding of Code-Switched Text.” ACL 2026, pages 44922–44938. [ACL Anthology](https://aclanthology.org/2026.acl-long.2080/) · [PDF](https://aclanthology.org/2026.acl-long.2080.pdf) · [official implementation](https://github.com/amr-mohamedd/Lost-in-the-Mix).

## What the paper asks

The paper tests whether LLMs understand reasoning and comprehension inputs when languages are mixed inside the same benchmark item. It adapts parallel versions of Belebele, MMLU, and XNLI so that the source item, answer choices, and gold label remain aligned. It asks how the direction and linguistic structure of mixing affect accuracy, and whether prompting or fine-tuning can reduce any loss.

The study covers English, Arabic, German, French, and Chinese. Its evaluated models are Llama 3.2 Instruct 3B; Llama 3.1 Instruct 8B and 70B; Qwen 2.5 Instruct 3B, 7B, and 72B; Mistral 7B Instruct v0.3; and ALLaM 7B. The main evaluation is zero-shot with matched task prompts using a modified EleutherAI Language Model Evaluation Harness.

## How it constructs the mixed-language items

The main method is **noun-token switching**. English remains the matrix language, and selected English nouns are replaced with aligned equivalents from the official parallel-language item. The authors use Equivalence Constraint Theory (ECT) and the Matrix Language Frame (MLF) model as constraints on candidate switch points: the English grammatical frame should remain intact, switches should occur at compatible boundaries, and fixed expressions or idioms should be avoided.

Their LLM-centric pipeline has two stages:

1. Ask a language model to mark switchable English nouns with placeholders, while preserving the matrix-language frame.
2. Fill those placeholders from aligned target-language text, adjusting inflection where needed and preserving meaning.

They compare that pipeline with an alignment-based method using automatic alignment, POS information, and generation. In their quality-selection study, bilingual annotators preferred Claude 3.5 Sonnet over GPT-4o for naturalness by modest margins. GPT-4o preferred the LLM-centric pipeline over the alignment-based version in pairwise judgments. Human spot checks were still used to check naturalness and ECT/MLF adherence. So the paper uses theory-guided generation plus review; it does not claim that a prompt alone guarantees perfect switches.

The paper also evaluates a separate **ratio-token** condition, replacing about 20% of tokens without syntactic constraints. A placeholder baseline replaces switch sites with a neutral marker, helping distinguish foreign-language content from disruption caused by replacing text at all.

## Evaluation and main findings

The paper reports item accuracy, benchmark-size-weighted accuracy, and accuracy deltas against the matching monolingual baseline. It finds a directional asymmetry: inserting non-English material into English generally lowers accuracy, while inserting English into some non-English matrix texts can help. Larger models are often more robust, but model family, language coverage, and scale all matter. The random 20% condition also lowers accuracy; its losses are broadly comparable to the linguistically constrained condition, suggesting that grammatical plausibility alone does not remove the difficulty.

Additional experiments reverse the matrix-language direction, mix multiple embedded languages, prepend a short instruction that the input is code-switched, and fine-tune Llama 3.1 8B on synthetic code-switched generation data. Prompt-based mitigation is inconsistent across models. Fine-tuning produces modest, more consistent recovery in their setup.

## What it does not answer

The paper does **not** measure tokenizer fertility, single-token retention, characters per token, or any other tokenizer fragmentation metric. It studies the relationship between code-switching and comprehension, not whether a particular tokenizer explains an accuracy change. The English-matrix noun-switch design also does not isolate a script contrast between Romanized Hindi and Devanagari Hindi.

The paper names important limits: noun substitution is only one relatively simple form of natural switching; its random replacement rate is fixed at 20%; and synthetic, reviewed stimuli do not represent every feature of spontaneous bilingual speech.

## How our project can extend it

The current pilot's A/B/C design adds a Hindi script comparison:

- A: English baseline.
- B: English matrix with Romanized Hindi.
- C: the same Hindi spans in Devanagari.

The B−A contrast estimates the effect of adding Hindi while retaining Latin script. The C−B contrast compares script renderings of matched Hindi content. The workbook's 10-item batch is a validation pilot; the proposal's 45-item plan is the later feasibility sample. The pilot should not be described as a reproduction of every experiment in the ACL paper.

The tokenizer extension should record exact tokenizer/checkpoint revisions, normalization, plain prompt and chat-formatted token counts, lexical span counts, token fertility, single-token retention, characters per token, and token inflation versus A. The same submitted text should be tokenized with the exact tokenizer belonging to each evaluated model. Compare these measures with item-level correctness, but describe any relationship as an association: models also differ in training data, architecture, scale, and Hindi ability.

Keep the paper's useful controls in view: aligned source meaning and gold answers, fixed prompting/decoding, item pairing, an optional placeholder control, and human review before the stimuli are frozen. A local pilot with a few dozen items should be framed as feasibility evidence with estimates and uncertainty, not as a definitive causal claim.
