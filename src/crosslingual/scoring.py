"""Conservative answer extraction for multiple-choice and XNLI-style items."""

from __future__ import annotations

import re


def normalize_answer(output: str, expected: str) -> str | None:
    """Extract a leading answer label without guessing from free-form reasoning."""
    text = output.strip()
    if not text:
        return None
    gold = expected.strip().lower()
    if gold in {"entailment", "neutral", "contradiction"}:
        match = re.match(
            r"^(?:answer\s*[:=-]?\s*)?(entailment|neutral|contradiction|[012])\b",
            text,
            flags=re.IGNORECASE,
        )
        if not match:
            match = re.match(
                r"^(?:the\s+)?(?:answer\s+is|label\s+is)\s+(entailment|neutral|contradiction|[012])\b",
                text,
                flags=re.IGNORECASE,
            )
        if not match:
            return None
        value = match.group(1).lower()
        return {"0": "entailment", "1": "neutral", "2": "contradiction"}.get(value, value)

    if gold in {"a", "b", "c", "d"}:
        match = re.match(r"^(?:answer\s*[:=-]?\s*)?\(?([A-D])\)?[.)\s]*$", text.splitlines()[0], re.I)
        if not match:
            match = re.match(r"^(?:the\s+)?(?:answer|option)\s*(?:is|:|=)\s*\(?([A-D])\)?\b", text, re.I)
        return match.group(1).lower() if match else None
    return text.splitlines()[0].strip().lower()


def score_output(output: str, expected: str) -> tuple[str | None, bool | None]:
    """Return normalized answer and correctness; unparseable responses stay missing."""
    normalized = normalize_answer(output, expected)
    if normalized is None:
        return None, None
    return normalized, normalized.casefold() == expected.strip().casefold()

