import argparse
import os
import sys
import yaml
import re
from typing import List
import textwrap

ALL_COLUMNS = [
    ("date", "1.5cm", "Date"),
    ("expiration", "1.5cm", "Expiration"),
    ("valid", "1.5cm", "Valid"),
    ("name", "2.5cm", "Name"),
    ("url", "2.5cm", "URL"),
    ("domain", "2cm", "Domain"),
    ("focus", "2cm", "Focus"),
    ("keyword", "2.5cm", "Keyword"),
    ("description", "4cm", "Description"),
    ("task_types", "3cm", "Task Types"),
    ("ai_capability_measured", "3cm", "AI Capability"),
    ("metrics", "2cm", "Metrics"),
    ("models", "2cm", "Models"),
    ("notes", "3cm", "Notes"),
    ("cite", "1cm", "Citation")
]

# Gregor:
#    this seems like a bug as it should not be forced to be lower case ?
#    capitalization in the yaml file is defined in the yaml file

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

    merged_records = []
    for record in records:
        merged_record = {col[0]: record.get(col[0], None) for col in ALL_COLUMNS}
        merged_records.append(merged_record)

    return merged_records


def write_md(input_filepaths: list[str], output_dir: str, columns: List[tuple]) -> None:
    """
    Combines the YAML tables at `input_filepaths`
    """

    contents = merge_yaml_files(input_filepaths)
    os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join(output_dir, "benchmarks.md"), 'w', encoding='utf-8') as md_file:
        headers = [col[2] for col in columns]
        md_file.write('| ' + ' | '.join(headers) + ' |\n')
        md_file.write('| ' + ' | '.join(['---'] * len(columns)) + ' |\n')

        for row in contents:
            current_article_name = None
            current_url = None

            row_cells = []
            for col_name, _, _ in columns:
                val = row.get(col_name, '')

                #save the article's name
                if col_name == "name":
                    current_article_name = val
                #save the article's URL
                if col_name == "url":
                    current_url = val

                # replace characters that would break the MD table
                val = str(val).replace("\n", " ").replace("['", "").replace("']", "")
                val = val.replace("', '", ", ").replace("','", ", ").replace("[]", "")
                val = val.replace("[", " ").replace("]", " ").replace("(", " ").replace(")", " ")

                # if adding the citation, put in [<title>][<URL>] format
                if col_name == "cite":
                    #Handle case where there are multiple URLs
                    if isinstance(current_url, list):
                        val = current_article_name.replace("(", " ").replace(")", " ") + " "
                        for i in range(len(current_url)):
                            val += f"[(Link {i+1})]({current_url[i]}) "
                    #Case where there is only one URL
                    else:
                        val = f"[{current_article_name}]({current_url})"

                row_cells.append(val)
            
            md_file.write('| ' + ' | '.join(row_cells) + ' |\n')



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

def extract_cite_url(cite_entry: str) -> str:
    match = re.search(r'url\s*=\s*[{"]([^}"]+)[}"]', cite_entry)
    if match:
        return match.group(1)
    return ""

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

def write_latex(input_filepaths: List[str], output_filepath: str, columns: List[tuple], standalone: bool = False) -> None:
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
                preamble = textwrap.dedent(
                    r"""
                    \documentclass{article}
                    \usepackage{hyperref}
                    \usepackage[margin=1in]{geometry}
                    \usepackage{pdflscape}
                    \usepackage{wasysym}
                    \usepackage{longtable}
                    \usepackage[style=ieee, url=true]{biblatex}
                    \addbibresource{benchmarks.bib}
                    \begin{document}
                    """)
                f.write(preamble)

            f.write("\\begin{landscape}\n")

            column_specs = "|".join([f"p{{{col[1]}}}" for col in columns])
            headers = [col[2] for col in columns]

            bf_headers = [f"{{\\bf {col[2]}}}" for col in columns]
            #print (bf_headers)
            #sys.exit(1)
            
            f.write("{\\footnotesize\n")
            f.write(f"\\begin{{longtable}}{{|{column_specs}|}}\n")
            f.write("\\hline\n")
            # Header for first page
            f.write(" & ".join(bf_headers) + " \\\\ \\hline\n")
            f.write("\\endfirsthead\n")

            # Header for subsequent pages
            f.write("\\hline\n")
            f.write(" & ".join(bf_headers) + " \\\\ \\hline\n")
            f.write("\\endhead\n")

            # Footer for all pages except last
            f.write("\\hline\n")
            f.write("\\multicolumn{" + str(len(columns)) + "}{r}{Continued on next page} \\\\\n")
            f.write("\\endfoot\n")

            # Footer for last page
            f.write("\\hline\n")
            f.write("\\endlastfoot\n")

            for record in records:
                row = []
                cite_keys = [extract_cite_label(c) for c in record.get("cite", []) if c]
                cite_urls = [extract_cite_url(c) for c in record.get("cite", []) if c]
                primary_url = cite_urls[0] if cite_urls else record.get("url", "")

                for col_name, _, _ in columns:
                    val = record.get(col_name, '')

                    if col_name == "cite":
                        cite_part = f"\\cite{{{', '.join(cite_keys)}}}" if cite_keys else ""
                        url_part = f" \\href{{{primary_url}}}{{$\\Rightarrow$ }}" if primary_url else ""
                        val = cite_part + url_part
                    elif col_name == "url":
                        val = ""  # already shown in cite
                    elif isinstance(val, list):
                        if args.authorlimit is not None and col_name in "authors":
                            displayed = val[:args.authorlimit]
                            suffix = ", et al." if len(val) > args.authorlimit else ""
                            val = "[" + ", ".join(escape_latex(str(v)) for v in displayed) + suffix + "]"
                            val = " " + ", ".join(escape_latex(str(v)) for v in displayed) + suffix + " "                            
                        else:
                            #val = "[" + ", ".join(escape_latex(str(v)) for v in val) + "]"
                            val = " " + ", ".join(escape_latex(str(v)) for v in val) + " "

                    else:
                        val = escape_latex(val)

                    row.append(val)

                f.write(" & ".join(row) + " \\\\ \\hline\n")

            f.write("\\end{longtable}\n")
            f.write("}\n")
            f.write("\\end{landscape}\n")

            if standalone:
                
                f.write("\\printbibliography\n")
                f.write("\\end{document}\n")
            

        # Also write BibTeX
        generate_bibtex(input_filepaths, output_filepath)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process YAML benchmark files to MD or LaTeX.")

    parser.add_argument('--files', '-i', type=str, nargs='+', required=True,
                        help='YAML file paths to process.')
    parser.add_argument('--format', '-f', type=str, choices=['md', 'tex'],
                        help="Output file format: 'md' or 'tex'")
    parser.add_argument('--standalone', '-s', action='store_true',
                        help="Include full LaTeX document preamble.")
    parser.add_argument('--out-dir', '-o', type=str, default='../content/',
                        help="Output directory")
    parser.add_argument('--columns', type=lambda s: s.split(','),
                        help="Subset of columns to include (comma-separated, e.g. name,url,description)")
    parser.add_argument('--readme', action='store_true',
                        help="Show README.md content")
    # Limiting the number of authors
    parser.add_argument('--authorlimit', type=int, default=None,
                    help="Limit number of authors (e.g., --authorlimit 10 adds 'et al.' if exceeded)")

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

    if args.format == 'md':
        write_md(args.files, os.path.join(args.out_dir, "md"), columns)
    elif args.format == 'tex':
        write_latex(args.files, os.path.join(args.out_dir, "tex"), columns, standalone=args.standalone)
