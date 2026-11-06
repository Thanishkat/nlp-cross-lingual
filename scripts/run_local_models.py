"""Run zero-shot local open-weight models on the condition-level prompt CSV."""

from __future__ import annotations

import argparse
import os
from datetime import datetime, timezone

from huggingface_hub import HfApi
from transformers import AutoTokenizer

from crosslingual.io import read_stimuli, write_records
from crosslingual.local_inference import load_local_model, run_one


DEFAULT_SYSTEM = "Answer the task directly. For multiple choice, return only the answer label."


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Local CSV/TSV of condition-level prompts")
    parser.add_argument("--output", required=True, help="Private CSV path for model responses")
    parser.add_argument(
        "--model", action="append", required=True,
        help="Hugging Face model id and immutable SHA, formatted model-id@sha; repeat per model",
    )
    parser.add_argument("--max-new-tokens", type=int, default=64)
    parser.add_argument("--system-prompt", default=DEFAULT_SYSTEM)
    args = parser.parse_args()

    rows = read_stimuli(args.input)
    hf_token = os.getenv("HF_TOKEN") or None
    api = HfApi(token=hf_token)
    records = []
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for model_spec in args.model:
        if "@" not in model_spec:
            raise SystemExit(f"Pin each model to an immutable SHA using model-id@sha: {model_spec}")
        model_id, requested_revision = model_spec.rsplit("@", 1)
        commit = api.model_info(model_id, revision=requested_revision).sha
        tokenizer, model = load_local_model(model_id, commit, hf_token)
        for row in rows:
            records.append(run_one(
                row, model_id, commit, tokenizer, model,
                system_prompt=args.system_prompt, max_new_tokens=args.max_new_tokens,
                run_id=run_id,
            ))
        del model, tokenizer
        if __import__("torch").cuda.is_available():
            __import__("torch").cuda.empty_cache()
    write_records(args.output, records)
    print(f"Wrote {len(records)} model responses to {args.output}")


if __name__ == "__main__":
    main()

