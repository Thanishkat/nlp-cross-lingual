"""Measure each prompt with explicitly selected, revision-pinned HF tokenizers.

Example:
  python scripts/measure_tokenizers.py --input data/private/stimuli.csv \
    --output data/private/tokenization.csv \
    --model meta-llama/Llama-3.1-8B-Instruct@<commit-sha>
"""

from __future__ import annotations

import argparse
import os

from huggingface_hub import HfApi
from transformers import AutoTokenizer

from crosslingual.io import read_stimuli, write_records
from crosslingual.tokenization import measure_prompt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Local CSV/TSV of condition-level prompts")
    parser.add_argument("--output", required=True, help="Private CSV path for tokenizer measurements")
    parser.add_argument(
        "--model", action="append", required=True,
        help="Hugging Face model id and immutable SHA, formatted model-id@sha; repeat per model",
    )
    parser.add_argument("--normalization", default="NFC", choices=["NFC", "NFD", "NFKC", "NFKD"])
    parser.add_argument(
        "--system-prompt",
        default="Answer the task directly. For multiple choice, return only the answer label.",
    )
    args = parser.parse_args()
    rows = read_stimuli(args.input)
    hf_token = os.getenv("HF_TOKEN") or None
    measurements = []
    api = HfApi(token=hf_token)
    for model_spec in args.model:
        if "@" not in model_spec:
            raise SystemExit(f"Pin each model to an immutable SHA using model-id@sha: {model_spec}")
        model_id, requested_revision = model_spec.rsplit("@", 1)
        commit = api.model_info(model_id, revision=requested_revision).sha
        tokenizer = AutoTokenizer.from_pretrained(
            model_id, revision=commit, token=hf_token, use_fast=True
        )
        if not tokenizer.is_fast:
            raise SystemExit(f"Tokenizer does not provide offsets required for span metrics: {model_id}")
        for row in rows:
            result = measure_prompt(
                tokenizer, row, tokenizer_revision=commit, normalization=args.normalization,
                system_prompt=args.system_prompt,
            )
            measurements.append(result)
        del tokenizer
    baselines = {
        (row["model_id"], row["item_id"]): row
        for row in measurements
        if row["condition"] == "A"
    }
    for row in measurements:
        baseline = baselines.get((row["model_id"], row["item_id"]))
        baseline_chat = baseline.get("chat_input_token_count") if baseline else None
        baseline_plain = baseline.get("plain_prompt_token_count") if baseline else None
        chat_count = row.get("chat_input_token_count")
        plain_count = row.get("plain_prompt_token_count")
        row["matched_A_chat_input_token_count"] = baseline_chat
        row["chat_input_token_inflation_vs_A"] = (
            chat_count - baseline_chat
            if chat_count is not None and baseline_chat is not None else None
        )
        row["chat_input_token_ratio_vs_A"] = (
            chat_count / baseline_chat
            if chat_count is not None and baseline_chat else None
        )
        row["plain_prompt_token_inflation_vs_A"] = (
            plain_count - baseline_plain
            if plain_count is not None and baseline_plain is not None else None
        )
    write_records(args.output, measurements)
    print(f"Wrote {len(measurements)} tokenizer measurements to {args.output}")


if __name__ == "__main__":
    main()

