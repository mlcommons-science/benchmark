#!/usr/bin/env python

import argparse
import yaml
import sys
from pathlib import Path

def print_entry(entry, out_stream):
    """Print a formatted benchmark entry."""
    print("=" * 40, file=out_stream)
    for key, value in entry.items():
        print(f"{key}: {value}", file=out_stream)
    print("=" * 40, file=out_stream)

def load_yaml_entries(file_path):
    """Load YAML entries from a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return list(data.values())  # in case the entries are stored under keys
        else:
            return []

def main():
    parser = argparse.ArgumentParser(description="Process benchmark YAML files.")
    parser.add_argument("files", nargs="+", help="YAML file(s) containing benchmark entries.")
    parser.add_argument("--out", type=str, help="Output file path. Defaults to stdout.", default=None)
    parser.add_argument("--all", action="store_true", help="Include all entries, not just valid ones.")

    args = parser.parse_args()

    out_stream = open(args.out, 'w', encoding='utf-8') if args.out else sys.stdout

    all_entries = []
    for file_path in args.files:
        entries = load_yaml_entries(file_path)
        all_entries.extend(entries)

    for entry in all_entries:
        if args.all or str(entry.get("valid", "")).strip().lower() == "yes":
            print_entry(entry, out_stream)

    if args.out:
        out_stream.close()

if __name__ == "__main__":
    main()
