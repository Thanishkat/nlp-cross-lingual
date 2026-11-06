# Full reading notes: Lost in the Mix (ACL 2026)

**Primary source:** Mohamed, Zhang, Vazirgiannis, and Shang (2026), [ACL Anthology](https://aclanthology.org/2026.acl-long.2080/), [PDF](https://aclanthology.org/2026.acl-long.2080.pdf). The authors' [implementation repository](https://github.com/amr-mohamedd/Lost-in-the-Mix) contains dataset-processing and evaluation scripts.

## Research problem and contribution

The paper asks how language mixing changes LLM comprehension on established benchmark tasks. It creates controlled code-switched variants of Belebele, MMLU, and XNLI using parallel benchmark translations, then compares them with matching monolingual baselines. The tasks cover passage reading comprehension, broad-domain multiple-choice knowledge/reasoning, and natural-language inference.

The paper contributes a theory-guided construction pipeline, a multi-model/multi-language accuracy study, and mitigation experiments. It evaluates English, Arabic, German, French, and Chinese with Llama 3.2 3B; Llama 3.1 8B/70B; Qwen 2.5 3B/7B/72B; Mistral 7B Instruct v0.3; and ALLaM 7B. Main evaluation is zero-shot with standardized prompts and a modified LM Evaluation Harness.

## Linguistic design

English is the matrix language in the primary experiments. The matrix language supplies the clause's grammatical frame; an embedded language contributes inserted words or phrases.

For the main **noun-token** condition, selected English nouns are replaced with aligned nouns from official parallel-language versions of the same benchmark item. Candidate switch points follow the core insights of:

- **Equivalence Constraint Theory (ECT):** a switch is placed where the surface structures of the two languages are compatible.
- **Matrix Language Frame (MLF):** the matrix language remains the grammatical frame; insertions should not force the clause into an unintended second grammar.

The paper's LLM-centric construction uses two steps. First, a generator marks switchable nouns with placeholders while preserving the English frame and avoiding idioms/fixed expressions. Second, it fills those positions from the aligned target-language text, adjusting inflection if necessary and preserving meaning. The paper compares this with an alignment-based pipeline.

The paper also reports a **ratio-token** condition that replaces about 20% of tokens without enforcing syntax. A neutral-placeholder condition helps distinguish effects of meaningful foreign words from effects caused by replacing text with markers.

## Quality controls

Claude 3.5 Sonnet and GPT-4o were compared as stimulus generators. Bilingual annotators conducted blind pairwise naturalness preferences; Claude was selected after modest preference margins. The authors also compared generation pipelines using GPT-4o as a judge, then performed manual sanity checks for naturalness and ECT/MLF adherence. The paper does not claim that ECT/MLF prompting makes a stimulus perfect or eliminates human review.

For a Hindi extension, use ECT/MLF to constrain candidates, preserve aligned source content, and record the rationale. Then require two independent bilingual reviews and documented adjudication. Keep human-naturalized Hinglish distinct from controlled noun-token stimuli.

## Metrics and results

The core measures are accuracy, benchmark-size-weighted accuracy, and accuracy delta from the corresponding monolingual baseline. Negative deltas indicate degradation.

The main result is directional asymmetry: inserting non-English material into English generally lowers accuracy, while embedding English into some non-English matrix-language inputs can improve it. Larger models are often more robust, but effects vary by family and language coverage. Random token replacement also degrades accuracy, with losses broadly comparable to linguistically constrained switching. Prompt-based mitigation is inconsistent; fine-tuning on synthetic code-switched generation data gives modest, more consistent recovery in their setup.

## What the paper does not study

It does not measure tokenizer fragmentation. It reports no fertility, characters-per-token, single-token-retention, or prompt-token inflation analysis. It also does not compare Romanized Hindi with Devanagari Hindi while holding the Hindi content constant. Those are the direct extensions in this project.

The authors note that noun replacement is only one relatively simple switching pattern, the random replacement rate is fixed at 20%, and synthetic reviewed stimuli do not capture all spontaneous bilingual speech.

## Direct implications for our pilot

The current A/B/C pilot is related to the paper but is not a full reproduction:

- **A:** English baseline.
- **B:** English matrix with Romanized Hindi spans.
- **C:** the same Hindi spans rendered in Devanagari.

`B − A` estimates the effect of adding Hindi while the writing system remains Latin. `C − B` estimates the script-rendering difference for matched Hindi content. The A/B/C design does not identify a general script main effect because it lacks an English-in-Devanagari cell. The optional monolingual-Hindi condition does not fill that cell.

Tokenization should be measured with the exact tokenizer revision belonging to each model. Record normalized prompt text, model/checkpoint SHA, tokenizer revision, chat-template version, full submitted input-token count, manipulated-span token count, token fertility, single-token retention, characters per token, and token inflation relative to A. Report performance and tokenization together, but treat the relationship as correlational: models differ in training data, architecture, size, and language competence as well as tokenizer.

The attached workbook is a 10-item construction/validation batch (30 prompts). The proposal's later 45-item plan is a separate feasibility sample. The 10-item batch must pass bilingual review and adjudication before model runs; its current local copy shows those gates as pending.
