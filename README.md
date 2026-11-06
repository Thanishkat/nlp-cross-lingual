# Cross-Lingual Evaluation of LLMs on Indian Code-Mixed Inputs

This project studies whether Hindi-English code-mixing and script choice affect LLM benchmark accuracy, and how those outcomes relate to tokenizer fragmentation. It starts from a reviewed English-Hindi benchmark pilot; Marathi and other Indian languages are later extensions.

The starting point is an English-Hindi replication and extension of `Lost in the Mix: Evaluating LLM Understanding of Code-Switched Text` (ACL 2026, [paper](https://aclanthology.org/2026.acl-long.2080/), [official code](https://github.com/amr-mohamedd/Lost-in-the-Mix)). The paper is research context, not project instructions.

## Current Research Questions

The current A/B/C pilot asks:

- **B−A:** Does adding Romanized Hindi in an English matrix change accuracy?
- **C−B:** Does the same Hindi content in Devanagari vs Roman script change accuracy?
- **Fragmentation:** Are Hindi-span token fertility, single-token retention, characters per token, or prompt token inflation associated with item accuracy?

These are paired contrasts on the same source items, not a broad script main effect. The proposed 45-item / 135-prompt feasibility set follows the attached 10-item / 30-prompt construction pilot. Broader naturalistic Hinglish, Telugu-English, or high-volume data are future phases after review and licensing.

## Repo Map

- `docs/source_notes.md`: paper and pilot source notes, including current review status.
- `docs/lost_in_mix_methods_hypotheses.md`: ECT/MLF, noun-token, ratio-token, and project-adaptation notes.
- `docs/paper_full_reading_notes.md`: end-to-end notes on the ACL 2026 paper.
- `docs/en_hi_replication_protocol.md`: A/B/C English-Hindi pilot protocol.
- `docs/research_design.md`: research questions, metrics, and language expansion phases.
- `docs/dataset_acquisition_plan.md`: candidate datasets, provenance, and review gates.
- `data/dataset_manifest_template.csv`: schema for the large paired dataset.
- `data/prompts/seed_intent_matched_prompts.tsv`: first prompt set across English, Hindi, Hinglish, Telugu, and Telugu-English mix.
- `experiments/experiment_log_template.csv`: template for recording model outputs and scores.
- `experiments/en_hi_replication_matrix.csv`: planned English-Hindi experiment conditions.
- `docs/lost_in_mix_acl2026_review.md`: full-paper methods/results/limitations review.
- `docs/new_literature_and_novelty.md`: tokenizer, informal Hindi, code-mixing, and research-gap reading list.
- `configs/models.yaml`: candidate model registry; exact revisions must be frozen before runs.
- `src/crosslingual/`: tokenizer measurements, local inference, answer parsing, and file I/O.
- `scripts/`: command-line entry points for tokenizer measurement, local evaluation, and summary analysis.
- `scripts/analyze_tokenizer_accuracy.py`: exploratory prompt-level tokenizer/accuracy associations.
- `scripts/export_workbook_prompts.py`: exports approved condition-level prompts from the private workbook; it enforces the human-review gate.
- `data/private/Hinglish_Tokenizer_Evaluation.xlsx`: local working tracker with the attached 10-item batch and 35 clearly blank expansion slots (not committed).
- `data/private/`: local workbook and source text; excluded from Git because benchmark licenses vary.

## Immediate Next Steps

1. Complete the two independent reviewer forms and adjudicate all current items; the supplied workbook currently marks them Hold/Pending.
2. Select and pin the exact model and tokenizer revisions on the local `Model Registry` sheet.
3. Add the 35 additional feasibility items with source ID, split, source URL, license, answer key, Hindi span alignment, switch rationale, and review evidence.
4. Export approved prompts, measure tokenizer fragmentation, and only then run the frozen model comparison.
5. Expand to Marathi or other languages after this Hindi-English workflow is reviewed and stable.

## Local workflow

Install the project environment, then export only approved prompts:

```powershell
python -m pip install -e .
python scripts/export_workbook_prompts.py --workbook data/private/Hinglish_Tokenizer_Evaluation.xlsx --output data/private/stimuli.csv
python scripts/measure_tokenizers.py --input data/private/stimuli.csv --output data/private/tokenization.csv --model MODEL_ID@IMMUTABLE_SHA --model SECOND_MODEL_ID@IMMUTABLE_SHA
python scripts/run_local_models.py --input data/private/stimuli.csv --output data/private/model_runs.csv --model MODEL_ID@IMMUTABLE_SHA --model SECOND_MODEL_ID@IMMUTABLE_SHA
python scripts/analyze_results.py --input data/private/model_runs.csv --output-dir data/private/analysis
python scripts/analyze_tokenizer_accuracy.py --tokenization data/private/tokenization.csv --results data/private/model_runs.csv --output data/private/analysis/tokenizer_accuracy_associations.csv
```

The example commands require replacing each model ID and SHA with selected checkpoints. The starter candidates in `configs/models.yaml` are unselected. Hosted GPT/Claude evaluation adapters remain a follow-up decision; the model registry records the provider and model-version fields needed for a separately pinned hosted track.

## Reproducibility and data handling

The public repository should contain code, protocols, schemas, and source identifiers. Keep licensed benchmark text, local workbooks containing source questions, model outputs, and API usage logs outside version control unless each dataset's redistribution terms have been checked. Copy `.env.example` to `.env` locally; never commit credentials. Freeze immutable model and tokenizer revisions, prompt templates, decoding settings, Unicode normalization, and run dates before collecting results.
