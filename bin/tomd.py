#!/usr/bin/env python

import argparse
import yaml
import sys
from pathlib import Path

def print_entry(entry, out_stream):
    """Print a benchmark entry as a Markdown table."""
    fields = [
        "date", "expiration", "valid", "name", "url", "domain", "focus",
        "keyword", "description", "task_types", "ai_capability_measured",
        "metrics", "models", "notes", "cite"
    ]

    print("| Field | Value |", file=out_stream)
    print("|-------|-------|", file=out_stream)

    for field in fields:
        value = entry.get(field) or entry.get("tasks") if field == "task_types" else entry.get("metrics") if field == "ai_capability_measured" else None
        if value is None:
            value = entry.get(field, "—")
        elif isinstance(value, list):
            value = ", ".join(str(v) for v in value)
        elif isinstance(value, dict):
            value = str(value)
        print(f"| {field} | {value} |", file=out_stream)

    print("\n", file=out_stream)

def load_yaml_entries(file_path):
    """Load YAML entries from a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return list(data.values())
        else:
            return []

def main():
    parser = argparse.ArgumentParser(description="Print benchmark entries from YAML in Markdown table format.")
    parser.add_argument("files", nargs="+", help="YAML file(s) to read.")
    parser.add_argument("--out", type=str, help="Output file (Markdown). Defaults to stdout.", default=None)
    parser.add_argument("--all", action="store_true", help="Include all entries, not just valid ones.")

    args = parser.parse_args()

    out_stream = open(args.out, "w", encoding="utf-8") if args.out else sys.stdout

    all_entries = []
    for file_path in args.files:
        entries = load_yaml_entries(file_path)
        all_entries.extend(entries)

    for entry in all_entries:
        is_valid = str(entry.get("valid", "")).strip().lower() == "yes"
        if args.all or is_valid:
            print_entry(entry, out_stream)

    if args.out:
        out_stream.close()

if __name__ == "__main__":
    main()
