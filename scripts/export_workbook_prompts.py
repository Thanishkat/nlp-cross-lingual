"""Export the condition-level prompt sheet from the private evaluation workbook."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from openpyxl import load_workbook


def export_prompts(workbook_path: str | Path, output_path: str | Path) -> int:
    workbook = load_workbook(workbook_path, read_only=True, data_only=True)
    if "Prompts" in workbook.sheetnames:  # original source workbook
        sheet = workbook["Prompts"]
        header_row = 3
        source_headers = [str(c or "").strip() for c in next(
            sheet.iter_rows(min_row=header_row, max_row=header_row, values_only=True)
        )]
        rows = sheet.iter_rows(min_row=header_row + 1, values_only=True)
        field_map = {
            "prompt_id": "Prompt ID", "item_id": "Item ID", "dataset": "Dataset",
            "condition": "Condition", "prompt_text": "Prompt text", "gold_answer": "Gold",
            "romanized_hindi_spans": "Romanized Hindi spans",
            "devanagari_hindi_spans": "Devanagari Hindi spans",
        }
        item_sheet = workbook["Items"]
        item_headers = [str(c or "").strip() for c in next(
            item_sheet.iter_rows(min_row=3, max_row=3, values_only=True)
        )]
        inclusion_col = item_headers.index("Inclusion")
        item_rows = [
            row for row in item_sheet.iter_rows(min_row=4, values_only=True) if row[0]
        ]
        item_status = {str(row[0]): str(row[inclusion_col] or "").strip().casefold() for row in item_rows}
    elif "Prompt Tracker" in workbook.sheetnames:  # generated tracker workbook
        sheet = workbook["Prompt Tracker"]
        source_headers = [str(c or "").strip() for c in next(
            sheet.iter_rows(min_row=1, max_row=1, values_only=True)
        )]
        rows = sheet.iter_rows(min_row=2, values_only=True)
        field_map = {
            "prompt_id": "Prompt ID", "item_id": "Item ID", "dataset": "Dataset",
            "condition": "Condition", "prompt_text": "Prompt text", "gold_answer": "Gold answer",
            "romanized_hindi_spans": "Romanized Hindi spans",
            "devanagari_hindi_spans": "Devanagari Hindi spans",
        }
        human_sheet = workbook["Human Review"]
        human_headers = [str(c or "").strip() for c in next(
            human_sheet.iter_rows(min_row=1, max_row=1, values_only=True)
        )]
        item_id_col = human_headers.index("Item ID")
        inclusion_col = human_headers.index("Final inclusion")
        human_items = [row for row in human_sheet.iter_rows(min_row=2, values_only=True) if row[item_id_col]]
        item_status = {
            str(row[item_id_col]): str(row[inclusion_col] or "").strip().casefold()
            for row in human_items
        }
    else:
        raise ValueError("Workbook must contain a Prompts or Prompt Tracker worksheet")

    indices = {name: source_headers.index(source) for name, source in field_map.items() if source in source_headers}
    missing = set(field_map) - set(indices)
    if missing:
        raise ValueError(f"Workbook is missing prompt fields: {sorted(missing)}")
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    unreviewed = []
    with output.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(field_map))
        writer.writeheader()
        for row in rows:
            prompt_id = row[indices["prompt_id"]]
            prompt_text = row[indices["prompt_text"]]
            if not prompt_id or not prompt_text:
                continue
            status = item_status.get(str(row[indices["item_id"]]), "")
            if status not in {"include", "included", "approved", "pass"}:
                if status not in {"exclude", "excluded", "reject", "rejected"}:
                    unreviewed.append(str(prompt_id))
                continue
            record = {
                key: row[indices[key]] if row[indices[key]] is not None else ""
                for key in field_map
            }
            writer.writerow(record)
            count += 1
    if unreviewed:
        output.unlink(missing_ok=True)
        raise ValueError(
            f"Review gate blocked export: {len(unreviewed)} populated prompt rows are not approved. "
            "Complete both independent reviews and adjudication, then mark each item Include or Exclude."
        )
    if count == 0:
        output.unlink(missing_ok=True)
        raise ValueError("No complete prompts found; check the workbook review gate and source sheet")
    return count


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workbook", required=True, help="Private source or tracker workbook")
    parser.add_argument("--output", required=True, help="Private CSV output for local scripts")
    args = parser.parse_args()
    count = export_prompts(args.workbook, args.output)
    print(f"Exported {count} prompts to {args.output}")


if __name__ == "__main__":
    main()
