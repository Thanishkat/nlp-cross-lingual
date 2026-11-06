"""Model-specific tokenizer measurements for complete prompts and Hindi spans."""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Iterable
from typing import Any


def normalize_text(text: str, form: str = "NFC") -> str:
    """Apply the recorded Unicode normalization without changing transliteration."""
    if form not in {"NFC", "NFD", "NFKC", "NFKD"}:
        raise ValueError(f"Unsupported Unicode normalization: {form}")
    return unicodedata.normalize(form, text)


def _spans_from_field(value: str | None) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in value.split("|") if part.strip()]


def find_span_offsets(text: str, spans: Iterable[str]) -> list[tuple[int, int]]:
    """Find span occurrences in order, including repeated words/spans."""
    offsets: list[tuple[int, int]] = []
    cursor = 0
    for span in spans:
        start = text.find(span, cursor)
        if start < 0:
            start = text.find(span)
        if start < 0:
            raise ValueError(f"Declared Hindi span was not found in prompt: {span!r}")
        offsets.append((start, start + len(span)))
        cursor = start + len(span)
    return offsets


def measure_prompt(
    tokenizer: Any,
    row: dict[str, str],
    *,
    tokenizer_revision: str,
    normalization: str = "NFC",
    system_prompt: str = "Answer the task directly. For multiple choice, return only the answer label.",
) -> dict[str, Any]:
    """Measure the original prompt and declared Hindi spans with one tokenizer.

    Offsets are taken from tokenizing the complete normalized prompt. Special tokens
    are excluded from lexical fertility and span counts. ``input_token_count`` records
    the full text plus tokenizer-added special tokens for comparison with actual runs.
    """
    raw_text = row["prompt_text"]
    text = normalize_text(raw_text, normalization)
    spans = [normalize_text(s, normalization) for s in (
        _spans_from_field(row.get("romanized_hindi_spans"))
        + _spans_from_field(row.get("devanagari_hindi_spans"))
    )]
    encoded = tokenizer(
        text,
        add_special_tokens=True,
        return_offsets_mapping=True,
        return_special_tokens_mask=True,
        truncation=False,
    )
    ids = encoded["input_ids"]
    offsets = encoded["offset_mapping"]
    special_mask = encoded.get("special_tokens_mask", [0] * len(ids))
    lexical = [
        (int(start), int(end), int(token_id))
        for (start, end), token_id, special in zip(offsets, ids, special_mask)
        if not special and int(end) > int(start)
    ]

    span_ranges = find_span_offsets(text, spans) if spans else []
    span_tokens = [
        (start, end, token_id)
        for start, end, token_id in lexical
        if any(start < span_end and end > span_start for span_start, span_end in span_ranges)
    ]
    span_word_count = sum(
        len(re.findall(r"[^\W_]+(?:['’][^\W_]+)*", text[start:end], flags=re.UNICODE))
        for start, end in span_ranges
    )
    token_counts_by_word: dict[tuple[int, int], int] = {}
    words = list(re.finditer(r"[^\W_]+(?:['’][^\W_]+)*", text, flags=re.UNICODE))
    for word in words:
        token_counts_by_word[(word.start(), word.end())] = sum(
            1 for start, end, _ in lexical if start < word.end() and end > word.start()
        )
    span_word_ranges = [
        word for word in words
        if any(word.start() < end and word.end() > start for start, end in span_ranges)
    ]
    word_token_counts = [token_counts_by_word[(w.start(), w.end())] for w in span_word_ranges]
    span_chars = sum(end - start for start, end in span_ranges)
    span_token_count = len(span_tokens)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": text},
    ]
    try:
        chat_ids = tokenizer.apply_chat_template(
            messages, tokenize=True, add_generation_prompt=True
        )
        chat_input_token_count = len(chat_ids)
        chat_template_status = "applied"
    except (AttributeError, ValueError, TypeError):
        chat_input_token_count = None
        chat_template_status = "unavailable"

    return {
        "prompt_id": row["prompt_id"],
        "item_id": row["item_id"],
        "condition": row["condition"],
        "model_id": tokenizer.name_or_path,
        "tokenizer_revision": tokenizer_revision,
        "normalization": normalization,
        "plain_prompt_token_count": len(ids),
        "chat_input_token_count": chat_input_token_count,
        "chat_template_status": chat_template_status,
        "chat_template": getattr(tokenizer, "chat_template", None),
        "system_prompt": system_prompt,
        "lexical_token_count": len(lexical),
        "hindi_span_count": len(span_ranges),
        "hindi_span_word_count": span_word_count,
        "hindi_span_token_count": span_token_count,
        "hindi_token_fertility": (
            span_token_count / span_word_count if span_word_count else None
        ),
        "hindi_single_token_retention": (
            sum(count == 1 for count in word_token_counts) / len(word_token_counts)
            if word_token_counts else None
        ),
        "hindi_chars_per_token": (
            span_chars / span_token_count if span_token_count else None
        ),
        "full_prompt_char_count": len(text),
        "hindi_span_char_count": span_chars,
        "tokenizer_status": "complete",
    }

