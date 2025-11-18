#!/usr/bin/env python3
"""
Select columns from a LaTeX table.

Usage:
  select_columns.py --in=<input> --out=<output> --columns=<cols>
  select_columns.py (-h | --help)

Options:
  --in=<input>        Input LaTeX file containing a tabular environment.
  --out=<output>      Output LaTeX file to write filtered table.
  --columns=<cols>    Comma-separated list of columns to keep (match header text).
  -h --help           Show this screen.
"""

from docopt import docopt
import re

def parse_row(line):
    """Split a LaTeX row into columns, ignoring & inside braces."""
    parts = []
    cur = ""
    depth = 0
    for char in line:
        if char == '{':
            depth += 1
        elif char == '}':
            depth -= 1

        if char == '&' and depth == 0:
            parts.append(cur.strip())
            cur = ""
        else:
            cur += char

    return [p.strip() for p in parts]

def rebuild_row(cols):
    return " & ".join(cols) + " \\\\"

def main():
    args = docopt(__doc__)
    infile = args["--in"]
    outfile = args["--out"]
    keep_cols = [c.strip() for c in args["--columns"].split(",")]

    with open(infile, "r") as f:
        lines = f.readlines()

    # Find header line (first row before \hline)
    header_idx = None
    for i, line in enumerate(lines):
        if "&" in line and "\\\\" in line:
            header_idx = i
            break

    if header_idx is None:
        raise RuntimeError("No table header found.")

    header_cols = parse_row(lines[header_idx])

    # Map header name → index
    col_indices = []
    for col in keep_cols:
        try:
            idx = header_cols.index(col)
            col_indices.append(idx)
        except ValueError:
            raise RuntimeError(f"Column '{col}' not found in header: {header_cols}")

    # Build new table lines
    new_lines = []

    for line in lines:
        if "&" in line and "\\\\" in line:
            cols = parse_row(line)
            selected = [cols[i] for i in col_indices if i < len(cols)]
            new_lines.append(rebuild_row(selected) + "\n")
        else:
            new_lines.append(line)

    with open(outfile, "w") as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    main()
