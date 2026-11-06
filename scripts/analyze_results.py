"""Summarize model accuracy and paired condition deltas from a local run CSV."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def _numeric_correct(value: object) -> float:
    if isinstance(value, bool):
        return float(value)
    text = str(value).strip().casefold()
    if text == "true":
        return 1.0
    if text == "false":
        return 0.0
    try:
        return float(text)
    except ValueError:
        return float("nan")


def summarize(
    path: str | Path, *, bootstrap_reps: int = 10_000, seed: int = 42
) -> tuple[pd.DataFrame, pd.DataFrame]:
    frame = pd.read_csv(path)
    required = {"item_id", "condition", "model_id", "correct"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"Run file is missing required columns: {sorted(missing)}")
    frame["correct"] = frame["correct"].map(_numeric_correct)
    summary = (
        frame.groupby(["model_id", "condition"], dropna=False)
        .agg(n_items=("item_id", "nunique"), n_scored=("correct", "count"), accuracy=("correct", "mean"))
        .reset_index()
    )
    item_wide = frame.pivot_table(
        index=["model_id", "item_id"], columns="condition", values="correct", aggfunc="mean"
    )
    contrast_specs = [
        ("A", "B", "B_minus_A"),
        ("B", "C", "C_minus_B"),
        ("A", "C", "C_minus_A"),
    ]
    delta_rows = []
    rng = np.random.default_rng(seed)
    for model_id, model_items in item_wide.groupby(level="model_id"):
        row: dict[str, object] = {"model_id": model_id}
        for baseline, condition, label in contrast_specs:
            if baseline in model_items.columns and condition in model_items.columns:
                paired = model_items[[baseline, condition]].dropna()
                differences = (paired[condition] - paired[baseline]).to_numpy(dtype=float)
                row[label] = float(differences.mean()) if len(differences) else None
                row[f"n_{label}"] = len(paired)
                if len(differences):
                    boot_means = rng.choice(
                        differences, size=(bootstrap_reps, len(differences)), replace=True
                    ).mean(axis=1)
                    lower, upper = np.quantile(boot_means, [0.025, 0.975])
                    row[f"{label}_ci95_low"] = float(lower)
                    row[f"{label}_ci95_high"] = float(upper)
                else:
                    row[f"{label}_ci95_low"] = None
                    row[f"{label}_ci95_high"] = None
            else:
                row[label] = None
                row[f"n_{label}"] = 0
                row[f"{label}_ci95_low"] = None
                row[f"{label}_ci95_high"] = None
        delta_rows.append(row)
    return summary, pd.DataFrame(delta_rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Private results CSV")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--bootstrap-reps", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    summary, deltas = summarize(args.input, bootstrap_reps=args.bootstrap_reps, seed=args.seed)
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    summary.to_csv(out / "accuracy_by_model_condition.csv", index=False)
    deltas.to_csv(out / "paired_accuracy_deltas.csv", index=False)
    print(f"Wrote summaries to {out}")


if __name__ == "__main__":
    main()

