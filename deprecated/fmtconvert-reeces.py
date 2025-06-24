#!/usr/bin/env python

"""
Module to convert YAML tables into other formats

If in the bin/ directory, to convert a table in source/table.yaml to Markdown:
python fmtconvert.py ../source/table.yaml --md ../content/table.md
"""

import argparse
import os
import yaml


# Predefined list of all possible column names
ALL_COLUMNS = [ 
    "date", "expiration", "valid", 
    "name", "url", "domain", "focus",
    "keyword", "description", "task_types", "ai_capability_measured",
    "metrics", "models", "notes", 
    "cite"
]

DEFAULT_OUTPUT_DIR = os.path.join("..", "source")


def load_yaml_file(file_path:str) -> (list[dict] | list):
    """
    Returns the contents of a YAML file at `file_path` as a dictionary or a list.

    Parameters:
        file_path: file path to load from
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = yaml.safe_load(f)
        if isinstance(content, dict):
            return [content]
        elif isinstance(content, list):
            return content
        else:
            raise ValueError(f"Unsupported YAML format in {file_path}")


def merge_yaml_files(file_paths) -> list[list]:
    """
    Returns a list containing the merged contents of the filepaths in `file_paths`.

    Any row not present in any of the tables in `file_paths` is automatically created in the output.

    Parameters:
        file_paths: the paths to each file to load from
    """
    records = []
    for path in file_paths:
        records.extend(load_yaml_file(path))

    # Ensure all records have all columns, filling missing columns with None
    merged_records = []
    for record in records:
        merged_record = {col: record.get(col, None) for col in ALL_COLUMNS}
        merged_records.append(merged_record)
    
    return merged_records


def write_markdown(records, output_path):
    """
    Creates a Markdown file at `output_path` containing the contents from `records` (a nested list).

    Each row in `records` becomes one row of the table.

    Parameters:
        records: a list containing the table's contents
        output_path: filepath to the output file
    """

    with open(output_path, 'w', encoding='utf-8') as f:
        # Write header row
        f.write("| " + " | ".join(ALL_COLUMNS) + " |\n")
        f.write("|" + "------|" * len(ALL_COLUMNS) + "\n")
        
        # Write records
        for record in records:
            row = " | ".join([str(record.get(col, '')) for col in ALL_COLUMNS])

            row = row.replace("\n", " ") #BUGFIX: Newlines mess up the Markdown format

            #Formatting fixes
            row = row.replace("['", "")
            row = row.replace("']", "")
            row = row.replace("', '", ", ")
            row = row.replace("','", ", ")
            row = row.replace("[]", "")

            f.write(f"| {row} |\n")


def write_latex(records: list[list], output_path:str) -> None:
    """
    Creates a LaTeX file at `output_path` containing the contents from `records` (a nested list).

    Each row in `records` becomes one row of the table.

    Parameters:
        records: a nested list containing the table's contents
        output_path: filepath to the output file
    """

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\\begin{table}[h!]\n\\centering\n")
        f.write("\\begin{tabular}{|" + " | ".join(["l"] * len(ALL_COLUMNS)) + "|}\n")
        f.write("\\hline\n")
        
        # Write header row
        f.write(" & ".join(ALL_COLUMNS) + " \\\\ \\hline\n")
        
        # Write records
        for record in records:
            row = " & ".join([str(record.get(col, '')) for col in ALL_COLUMNS])
            
            #Bugfix: % is a comment in Latex
            row = row.replace("(%)", "(percent)")
            row = row.replace("%", " percent")

            f.write(row + " \\\\ \\hline\n")
        
        f.write("\\end{tabular}\n\\end{table}\n")


def main():
    """
    Entry point of the script
    """

    parser = argparse.ArgumentParser(description="Merge YAML files into a unified table.")
    parser.add_argument('yaml_files', nargs='+', help='Input YAML files')
    parser.add_argument('--md', metavar='FILENAME', help='Output Markdown file')
    parser.add_argument('--tex', metavar='FILENAME', help='Output LaTeX file')
    parser.add_argument('--print', action='store_true', help='Print table to stdout')

    args = parser.parse_args()

    # Merge YAML files
    records = merge_yaml_files(args.yaml_files)

    # Output directory
    output_dir = os.path.abspath(DEFAULT_OUTPUT_DIR)
    os.makedirs(output_dir, exist_ok=True)

    if args.md:
        md_path = os.path.join(output_dir, args.md)
        write_markdown(records, md_path)
        print(f"[+] Markdown table written to {md_path}")

    if args.tex:
        tex_path = os.path.join(output_dir, args.tex)
        write_latex(records, tex_path)
        print(f"[+] LaTeX table written to {tex_path}")

    if args.print:
        # Print table to stdout
        header = " | ".join(ALL_COLUMNS)
        print(f"| {header} |")
        print("|" + "------|" * len(ALL_COLUMNS))
        
        for record in records:
            row = " | ".join([str(record.get(col, '')) for col in ALL_COLUMNS])
            row = row.replace("\n", " ") #BUGFIX from MD converter: Newlines mess up the Markdown format
            row = row.replace("['", "")
            row = row.replace("']", "")
            row = row.replace("', '", ", ")
            row = row.replace("','", ", ")
            row = row.replace("[]", "")
            print(f"| {row} |")


if __name__ == '__main__':
    main()
