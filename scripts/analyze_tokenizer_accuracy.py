"""Explore prompt-level associations between tokenizer metrics and correctness.

The output is descriptive. Comparisons across unrelated pretrained models cannot
identify a causal tokenizer effect.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


METRICS = [
    "hindi_token_fertility",
    "hindi_single_token_retention",
    "hindi_chars_per_token",
    "chat_input_token_inflation_vs_A",
    "chat_input_token_ratio_vs_A",
    "plain_prompt_token_inflation_vs_A",
]
KEYS = ["prompt_id", "item_id", "condition", "model_id"]


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


def analyze(tokenizer_path: str | Path, results_path: str | Path) -> pd.DataFrame:
    tokenization = pd.read_csv(tokenizer_path)
    results = pd.read_csv(results_path)
    missing_tokens = set(KEYS + METRICS) - set(tokenization.columns)
    missing_results = set(KEYS + ["dataset", "correct"]) - set(results.columns)
    if missing_tokens:
        raise ValueError(f"Tokenization file is missing columns: {sorted(missing_tokens)}")
    if missing_results:
        raise ValueError(f"Model results file is missing columns: {sorted(missing_results)}")
    if tokenization.duplicated(KEYS).any():
        raise ValueError("Tokenization file has duplicate prompt/model rows; resolve before joining")

    frame = results.merge(
        tokenization[KEYS + METRICS], on=KEYS, how="inner", validate="many_to_one"
    )
    frame["correct"] = frame["correct"].map(_numeric_correct)
    records = []
    for (model_id, condition, dataset), group in frame.groupby(
        ["model_id", "condition", "dataset"], dropna=False
    ):
        for metric in METRICS:
            paired = group[["item_id", "correct", metric]].dropna()
            if len(paired) < 3 or paired["correct"].nunique() < 2 or paired[metric].nunique() < 2:
                association = None
            else:
                association = float(paired["correct"].corr(paired[metric], method="pearson"))
            records.append({
                "model_id": model_id,
                "condition": condition,
                "dataset": dataset,
                "tokenizer_metric": metric,
                "n_prompts": len(paired),
                "n_items": paired["item_id"].nunique(),
                "point_biserial_r": association,
                "interpretation": "Exploratory association only; model differences are confounded.",
            })
    return pd.DataFrame(records)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tokenization", required=True, help="Private tokenizer metrics CSV")
    parser.add_argument("--results", required=True, help="Private model results CSV")
    parser.add_argument("--output", required=True, help="Private output CSV")
    args = parser.parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    analyze(args.tokenization, args.results).to_csv(output, index=False)
    print(f"Wrote exploratory associations to {output}")


if __name__ == "__main__":
    main()
