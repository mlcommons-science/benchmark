import argparse
import os
import sys
import yaml
import re
from typing import List
import textwrap

ALL_COLUMNS = [ 
    "date", "expiration", "valid", 
    "name", "url", "domain", "focus",
    "keyword", "description", "task_types", "ai_capability_measured",
    "metrics", "models", "notes", 
    "cite"
]

def load_yaml_file(file_path: str) -> list[dict]:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = yaml.safe_load(f)
        if isinstance(content, dict):
            return [content]
        elif isinstance(content, list):
            return content
        else:
            raise ValueError(f"Unsupported YAML format in {file_path}")

def merge_yaml_files(file_paths: list[str]) -> list[dict]:
    records = []
    for path in file_paths:
        records.extend(load_yaml_file(path))

    merged_records = []
    for record in records:
        merged_record = {col: record.get(col, None) for col in ALL_COLUMNS}
        merged_records.append(merged_record)

    return merged_records

def write_md(input_filepaths: list[str] = ['../source/benchmarks.yaml'], output_dir: str = '../content') -> None:
    contents = merge_yaml_files(input_filepaths)
    os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join(output_dir, "benchmarks.md"), 'w', encoding='utf-8') as md_file:
        header_row = '| ' + ' | '.join(ALL_COLUMNS) + ' |'
        md_file.write(header_row + '\n')
        separator_row = '| ' + ' | '.join(['---'] * len(ALL_COLUMNS)) + ' |'
        md_file.write(separator_row + '\n')

        for row in contents:
            cleaned_row = '| ' + ' | '.join(str(row.get(cell, '')) for cell in row) + ' |'
            cleaned_row = cleaned_row.replace("\n", " ").replace("['", "").replace("']", "")
            cleaned_row = cleaned_row.replace("', '", ", ").replace("','", ", ").replace("[]", "")
            md_file.write(cleaned_row + '\n')

def escape_latex(text):
    if not isinstance(text, str):
        text = str(text)
    return (
        text.replace("\\", "\\textbackslash{}")
            .replace("&", "\\&")
            .replace("%", " percent")
            .replace("_", "\\_")
            .replace("#", "\\#")
            .replace("{", "\\{")
            .replace("}", "\\}")
            .replace("^", "\\^{}")
            .replace("~", "\\~{}")
            .replace("$", "\\$")
    )

def extract_cite_label(cite_entry: str) -> str:
    match = re.match(r'@\w+\{([^,]+),', cite_entry.strip())
    if match:
        return match.group(1)
    return ""

def write_latex(input_filepaths: List[str] = ['../source/benchmarks.yaml'],
                output_filepath: str = '../content/',
                standalone: bool = False) -> None:
    os.makedirs(output_filepath, exist_ok=True)

    for filepath in input_filepaths:
        with open(filepath, 'r', encoding='utf-8') as f:
            records = yaml.safe_load(f)

        if not isinstance(records, list):
            raise ValueError(f"{filepath} must contain a list of benchmark records")

        base_name = os.path.splitext(os.path.basename(filepath))[0]
        output_tex_path = os.path.join(output_filepath, f"{base_name}.tex")

        with open(output_tex_path, 'w', encoding='utf-8') as f:
            if standalone:
                f.write("\\documentclass{article}\n")
                f.write("\\usepackage{hyperref}\n")
                f.write("\\usepackage[margin=1in]{geometry}\n")
                f.write("\\usepackage{pdflscape}\n")
                f.write("\\begin{document}\n")

            f.write("\\begin{landscape}\n")
            f.write("\\begin{table}[h!]\n")


            # f.write("\\begin{tabular}{|" + " | ".join(["l"] * len(ALL_COLUMNS)) + "|}\n")

            # date & expiration & valid & name & url & domain & focus & keyword
            # & description & task_types & ai_capability_measured & metrics &
            # models & notes & cite
            
            width = """
               |
               p{1cm}|
               p{1cm}|
               p{1cm}|
               p{1cm}|
               p{1cm}|
               p{1cm}|
               p{1cm}|
               p{1cm}|
               p{1cm}|
               p{1cm}|
               p{1cm}|
               p{1cm}|
               p{1cm}|
               p{1cm}|
               p{1cm}|
            """
            columns = textwrap.dedent(width).strip()
            f.write("\\begin{tabular}{" + columns+ "}\n")

            f.write("\\hline\n")
            f.write(" & ".join(ALL_COLUMNS) + " \\\\ \\hline\n")

            for record in records:
                row = []
                cite_keys = [extract_cite_label(c) for c in record.get("cite", []) if c]

                for col in ALL_COLUMNS:
                    val = record.get(col, '')

                    if col == "cite":
                        cite_part = f"\\cite{{{', '.join(cite_keys)}}}" if cite_keys else ""
                        url = record.get("url", "")
                        url_part = f" \\href{{url}}{{{escape_latex(url)}}}" if url else ""
                        val = cite_part + url_part

                    elif col == "url":
                        val = ""  # already handled in cite

                    elif isinstance(val, list):
                        val = "[" + ", ".join(escape_latex(str(v)) for v in val) + "]"

                    else:
                        val = escape_latex(val)

                    row.append(val)

                f.write(" & ".join(row) + " \\\\ \\hline\n")

            f.write("\\end{tabular}\n\\end{table}\n")

            f.write("\\end{landscape}\n")

            if standalone:
                f.write("\\end{document}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A script to process files with specified format and output directory.")

    parser.add_argument('--files', '-i', type=str, nargs='+', required=True,
                        help='One or more file paths to process. Required argument.')

    parser.add_argument('--format', '-f', type=str, choices=['md', 'tex'],
                        help="Output file format. Must be 'md' (Markdown) or 'tex' (LaTeX)")

    parser.add_argument('--standalone', '-s', action='store_true',
                        help="If set, generates the table with a LaTeX preamble. Only valid when format is 'tex'")

    parser.add_argument('--out-dir', '-o', type=str, default='../content/',
                        help="Output directory for processed files. Default: '../content/'")

    parser.add_argument('--readme', action='store_true',
                        help="Prints the contents of the README help document")

    args = parser.parse_args()

    if args.readme:
        with open('README.md', 'r') as file:
            print(file.read())
            sys.exit(0)

    if args.standalone and args.format != 'tex':
        parser.error("--standalone flag may be used only when --format option is 'tex'")

    for file in args.files:
        if not os.path.exists(file):
            parser.error("The file " + file + " does not exist")

    if not os.path.isdir(args.out_dir):
        os.makedirs(args.out_dir, exist_ok=True)

    if args.format == 'md' and not os.path.isdir(os.path.join(args.out_dir, "md")):
        os.makedirs(os.path.join(args.out_dir, "md"), exist_ok=True)

    if args.format == 'tex' and not os.path.isdir(os.path.join(args.out_dir, "tex")):
        os.makedirs(os.path.join(args.out_dir, "tex"), exist_ok=True)

    if args.format == 'md':
        write_md(args.files, os.path.join(args.out_dir, "md"))
    elif args.format == 'tex':
        write_latex(args.files, os.path.join(args.out_dir, "tex"), standalone=args.standalone)
