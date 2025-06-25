import argparse
import os
import sys
import yaml
import re
import textwrap
from typing import List
import bibtexparser

ALL_COLUMNS = [
    ("date", "1.5cm", "Date"),
    ("expiration", "1.5cm", "Expiration"),
    ("valid", "1.5cm", "Valid"),
    ("name", "2.5cm", "Name"),
    ("url", "2.5cm", "URL"),
    ("domain", "2cm", "Domain"),
    ("focus", "2cm", "Focus"),
    ("keywords", "2.5cm", "Keywords"),
    ("description", "4cm", "Description"),
    ("task_types", "3cm", "Task Types"),
    ("ai_capability_measured", "3cm", "AI Capability"),
    ("metrics", "2cm", "Metrics"),
    ("models", "2cm", "Models"),
    ("notes", "3cm", "Notes"),
    ("cite", "1cm", "Citation")
]

def get_column_triples(selected: list[str]) -> list[tuple[str, str, str]]:
    selected_lower = [s.lower() for s in selected]
    return [triple for triple in ALL_COLUMNS if triple[0] in selected_lower]

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
    return records

def sanitize_filename(name: str) -> str:
    return re.sub(r'[^\w\-_\. ]', '_', name).replace(' ', '_').lower()

def write_individual_md_pages(input_filepaths: List[str], output_dir: str, columns: List[tuple], author_trunc: int = None) -> None:
    contents = merge_yaml_files(input_filepaths)
    os.makedirs(output_dir, exist_ok=True)
    index_path = os.path.join(output_dir, "index.md")
    with open(index_path, 'w', encoding='utf-8') as index_file:
        index_file.write("# Index of Benchmarks\n\n")
        for i, entry in enumerate(contents):
            entry_name = entry.get("name", f"entry_{i}")
            filename = sanitize_filename(entry_name) + ".md"
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# {entry_name}\n\n")
                for col_name, _, col_display in columns:
                    val = entry.get(col_name, '')
                    if col_name == "cite" and isinstance(val, list):
                        f.write(f"**{col_display}**:\n\n")
                        for bibtex in val:
                            f.write("-\n")
                            try:
                                parser = bibtexparser.bparser.BibTexParser(common_strings=True)
                                db = bibtexparser.loads(bibtex, parser=parser)
                                if db.entries:
                                    bib = db.entries[0]
                                    f.write(f"  - type: {bib.get('ENTRYTYPE', '')}\n")
                                    f.write(f"  - id: {bib.get('ID', '')}\n")
                                    for key, value in bib.items():
                                        if key in ('ENTRYTYPE', 'ID'):
                                            continue
                                        if key == 'author' and author_trunc:
                                            authors = [a.strip() for a in value.replace('\n', ' ').split(' and ')]
                                            if len(authors) > author_trunc:
                                                authors = authors[:author_trunc] + ['et al.']
                                            value = ', '.join(authors)
                                        f.write(f"  - {key}: {value}\n")
                            except Exception as e:
                                f.write(f"  - parsing_error: {str(e)}\n")
                            f.write("  - bibtex: |\n")
                            for raw_line in bibtex.strip().splitlines():
                                f.write(f"      {raw_line}\n")
                        f.write("\n")
                    else:
                        val_str = str(val).replace("\n", " ").replace("['", "").replace("']", "")
                        val_str = val_str.replace("', '", ", ").replace("','", ", ").replace("[]", "")
                        val_str = val_str.replace("[", " ").replace("]", " ").replace("(", " ").replace(")", " ")
                        f.write(f"**{col_display}**: {val_str}\n\n")
            index_file.write(f"- [{entry_name}]({filename})\n")

def write_md(input_filepaths: list[str], output_dir: str, columns: List[tuple]) -> None:
    contents = merge_yaml_files(input_filepaths)
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "benchmarks.md"), 'w', encoding='utf-8') as md_file:
        headers = [col[2] for col in columns]
        md_file.write('| ' + ' | '.join(headers) + ' |\n')
        md_file.write('| ' + ' | '.join(['---'] * len(columns)) + ' |\n')
        for row in contents:
            current_article_name = row.get("name", "")
            current_url = row.get("url", "")
            row_cells = []
            for col_name, _, _ in columns:
                val = row.get(col_name, '')
                if col_name == "cite":
                    if isinstance(current_url, list):
                        val = current_article_name + " " + " ".join(f"[(Link {i+1})]({url})" for i, url in enumerate(current_url))
                    else:
                        val = f"[{current_article_name}]({current_url})"
                else:
                    val = str(val).replace("\n", " ").replace("['", "").replace("']", "")
                    val = val.replace("', '", ", ").replace("','", ", ").replace("[]", "")
                    val = val.replace("[", " ").replace("]", " ").replace("(", " ").replace(")", " ")
                row_cells.append(val)
            md_file.write('| ' + ' | '.join(row_cells) + ' |\n')

def escape_latex(text):
    if not isinstance(text, str):
        text = str(text)
    return (
        text.replace("\\", "\\textbackslash{}").replace("&", "\\&").replace("%", " percent")
            .replace("_", "\\_").replace("#", "\\#").replace("{", "\\{").replace("}", "\\}")
            .replace("^", "\\^{}").replace("~", "\\~{}").replace("$", "\\$")
    )

def extract_cite_label(cite_entry: str) -> str:
    match = re.match(r'@\w+\{([^,]+),', cite_entry.strip())
    return match.group(1) if match else ""

def extract_cite_url(cite_entry: str) -> str:
    match = re.search(r'url\s*=\s*[{"]([^}"]+)[}"]', cite_entry)
    return match.group(1) if match else ""

def generate_bibtex(input_filepaths: List[str], output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)
    entries = []
    for filepath in input_filepaths:
        with open(filepath, 'r', encoding='utf-8') as f:
            records = yaml.safe_load(f)
        if not isinstance(records, list):
            continue
        for record in records:
            cite_entries = record.get("cite", [])
            if cite_entries:
                entries.extend(cite_entries)
    with open(os.path.join(output_dir, "benchmarks.bib"), 'w', encoding='utf-8') as bib_file:
        for entry in entries:
            bib_file.write(entry.strip() + "\n\n")

def write_latex(input_filepaths: List[str], output_filepath: str, columns: List[tuple], standalone: bool = False, author_limit: int = None) -> None:
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
                f.write(textwrap.dedent(r"""
                    \documentclass{article}
                    \usepackage{hyperref}
                    \usepackage[margin=1in]{geometry}
                    \usepackage{pdflscape}
                    \usepackage{wasysym}
                    \usepackage{longtable}
                    \usepackage[style=ieee, url=true]{biblatex}
                    \addbibresource{benchmarks.bib}
                    \begin{document}
                """))
            f.write("\\begin{landscape}\n{\\footnotesize\n")
            f.write(f"\\begin{{longtable}}{{|{'|'.join([f'p{{{col[1]}}}' for col in columns])}|}}\n\\hline\n")
            f.write(" & ".join([f"{{\\bf {col[2]}}}" for col in columns]) + " \\\\ \\hline\n\\endfirsthead\n")
            f.write("\\hline\n" + " & ".join([f"{{\\bf {col[2]}}}" for col in columns]) + " \\\\ \\hline\n\\endhead\n")
            f.write("\\hline\n\\multicolumn{" + str(len(columns)) + "}{r}{Continued on next page} \\\\\n\\endfoot\n\\hline\n\\endlastfoot\n")
            for record in records:
                cite_keys = [extract_cite_label(c) for c in record.get("cite", []) if c]
                cite_urls = [extract_cite_url(c) for c in record.get("cite", []) if c]
                primary_url = cite_urls[0] if cite_urls else record.get("url", "")
                row = []
                for col_name, _, _ in columns:
                    val = record.get(col_name, '')
                    if col_name == "cite":
                        val = (f"\\cite{{{', '.join(cite_keys)}}}" if cite_keys else "") + (f" \\href{{{primary_url}}}{{$\\Rightarrow$ }}" if primary_url else "")
                    elif col_name == "url":
                        val = ""
                    elif isinstance(val, list):
                        if author_limit is not None and col_name == "authors":
                            val = ", ".join(escape_latex(v) for v in val[:author_limit])
                            if len(val) > author_limit:
                                val += ", et al."
                        else:
                            val = ", ".join(escape_latex(v) for v in val)
                    else:
                        val = escape_latex(val)
                    row.append(val)
                f.write(" & ".join(row) + " \\\\ \\hline\n")
            f.write("\\end{longtable}\n}\n\\end{landscape}\n")
            if standalone:
                f.write("\\printbibliography\n\\end{document}\n")
    generate_bibtex(input_filepaths, output_filepath)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process YAML benchmark files to MD or LaTeX.")
    parser.add_argument('--files', '-i', type=str, nargs='+', required=True, help='YAML file paths to process.')
    parser.add_argument('--format', '-f', type=str, choices=['md', 'tex'], help="Output file format: 'md' or 'tex'")
    parser.add_argument('--standalone', '-s', action='store_true', help="Include full LaTeX document preamble.")
    parser.add_argument('--out-dir', '-o', type=str, default='../content/', help="Output directory")
    parser.add_argument('--columns', type=lambda s: s.split(','), help="Subset of columns to include")
    parser.add_argument('--readme', action='store_true', help="Show README.md content")
    parser.add_argument('--index', action='store_true', help="Generate individual pages for each entry and an index.md")
    parser.add_argument('--authorlimit', type=int, default=None, help="Limit number of authors for LaTeX")
    parser.add_argument('--authortruncation', type=int, default=None, help="Truncate authors for index pages")

    args = parser.parse_args()

    if args.readme:
        with open('README.md', 'r') as file:
            print(file.read())
            sys.exit(0)

    if args.standalone and args.format != 'tex':
        parser.error("--standalone is only valid with --format tex")

    for file in args.files:
        if not os.path.exists(file):
            parser.error(f"The file {file} does not exist")

    os.makedirs(args.out_dir, exist_ok=True)
    columns = get_column_triples(args.columns) if args.columns else ALL_COLUMNS

    if args.index:
        write_individual_md_pages(args.files, os.path.join(args.out_dir, "md_pages"), columns, author_trunc=args.authortruncation)
    elif args.format == 'md':
        write_md(args.files, os.path.join(args.out_dir, "md"), columns)
    elif args.format == 'tex':
        write_latex(args.files, os.path.join(args.out_dir, "tex"), columns, standalone=args.standalone, author_limit=args.authorlimit)
