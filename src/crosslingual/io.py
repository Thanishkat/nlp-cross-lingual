"""Read local pilot stimuli and write run records without changing source text."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


def read_stimuli(path: str | Path) -> list[dict[str, str]]:
    """Read a UTF-8 CSV/TSV export with one condition-level prompt per row."""
    source = Path(path)
    delimiter = "\t" if source.suffix.lower() == ".tsv" else ","
    with source.open("r", encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter=delimiter))
    required = {"prompt_id", "item_id", "condition", "prompt_text", "gold_answer"}
    missing = required - (set(rows[0]) if rows else set())
    if missing:
        raise ValueError(f"Stimulus file is missing required columns: {sorted(missing)}")
    seen: set[str] = set()
    for row in rows:
        prompt_id = row["prompt_id"].strip()
        if not prompt_id or prompt_id in seen:
            raise ValueError(f"Blank or duplicate prompt_id: {prompt_id!r}")
        if not row["prompt_text"].strip():
            raise ValueError(f"Empty prompt text for {prompt_id}")
        seen.add(prompt_id)
    return rows


def write_records(path: str | Path, rows: list[dict[str, Any]]) -> None:
    """Write homogeneous records as UTF-8 CSV; create the parent directory."""
    if not rows:
        raise ValueError("Refusing to write an empty result file")
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    fields = list(dict.fromkeys(key for row in rows for key in row))
    with target.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

