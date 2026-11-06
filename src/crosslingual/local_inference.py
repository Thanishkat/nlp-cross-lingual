"""Deterministic local Hugging Face evaluation for the controlled pilot."""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from .scoring import score_output
from .tokenization import normalize_text


def load_local_model(model_id: str, revision: str, hf_token: str | None = None) -> tuple[Any, Any]:
    if not revision or revision == "main":
        raise ValueError("Pin an immutable Hugging Face commit SHA in the run configuration")
    token = hf_token or os.getenv("HF_TOKEN") or None
    tokenizer = AutoTokenizer.from_pretrained(
        model_id, revision=revision, token=token, use_fast=True
    )
    if not tokenizer.is_fast:
        raise ValueError(f"A fast tokenizer is required for span offsets: {model_id}")
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        revision=revision,
        token=token,
        torch_dtype="auto",
        device_map="auto" if torch.cuda.is_available() else None,
    )
    if not torch.cuda.is_available():
        model.to("cpu")
    model.eval()
    return tokenizer, model


def run_one(
    row: dict[str, str],
    model_id: str,
    model_revision: str,
    tokenizer: Any,
    model: Any,
    *,
    system_prompt: str,
    max_new_tokens: int = 64,
    run_id: str | None = None,
    normalization: str = "NFC",
) -> dict[str, Any]:
    prompt_text = normalize_text(row["prompt_text"], normalization)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt_text},
    ]
    input_ids = tokenizer.apply_chat_template(
        messages, tokenize=True, add_generation_prompt=True, return_tensors="pt"
    )
    input_ids = input_ids.to(model.device)
    with torch.inference_mode():
        generated = model.generate(
            input_ids,
            do_sample=False,
            max_new_tokens=max_new_tokens,
            pad_token_id=(
                tokenizer.pad_token_id
                if tokenizer.pad_token_id is not None
                else tokenizer.eos_token_id
            ),
        )
    new_ids = generated[0, input_ids.shape[-1] :]
    output = tokenizer.decode(new_ids, skip_special_tokens=True).strip()
    prediction, correct = score_output(output, row["gold_answer"])
    return {
        "run_id": run_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "run_time_utc": datetime.now(timezone.utc).isoformat(),
        "prompt_id": row["prompt_id"],
        "item_id": row["item_id"],
        "dataset": row.get("dataset", ""),
        "condition": row["condition"],
        "model_id": model_id,
        "model_revision": model_revision,
        "provider": "huggingface",
        "prompt_template": "tokenizer.apply_chat_template",
        "normalization": normalization,
        "system_prompt": system_prompt,
        "temperature": 0,
        "max_new_tokens": max_new_tokens,
        "input_token_count": int(input_ids.shape[-1]),
        "output_token_count": int(new_ids.shape[-1]),
        "raw_output": output,
        "normalized_answer": prediction,
        "gold_answer": row["gold_answer"],
        "correct": correct,
        "status": "complete",
    }

