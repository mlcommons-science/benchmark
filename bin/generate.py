import argparse
import bibtexparser
import os
import sys
import yaml
import re
from typing import List
import textwrap


COLUMN_TITLES = [
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

FULL_CITE_TITLE = ("full_cite", "1cm", "Full BibTeX")


def get_column_triples(selected: list[str]) -> list[tuple[str, str, str]]:
    selected_lower = [s.lower() for s in selected]
    return [triple for triple in COLUMN_TITLES if triple[0] in selected_lower]

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

    # merged_records = []
    # for record in records:
    #     merged_record = {col[0]: record.get(col[0], None) for col in COLUMN_TITLES}
    #     merged_records.append(merged_record)

    # return merged_records
    return records



def get_bibtex(cell_val: str, author_limit: int) -> str:
    """
    Returns a substring of `cell_val` containing a BibTeX string with `author_limit` displayed authors.
    If there is no BibTex string, returns the string "No citation found".

    If there are multiple BibTeX entries, the first entry is returned.

    Parameters:
        cell_val: string possibly containing a BibTeX entry
        author_limit: maximum number of author names to include before truncating with "et al." If not None, must be a positive integer
    Returns:
        BibTeX entry in `cell_val` or "None"
    """
    assert type(cell_val)==str, "cell value must be a string"
    assert author_limit==None or (type(author_limit)==int and author_limit>0), "author limit must be a positive integer"

    match = re.search(r'@(?:\w+)\s*\{', cell_val)
    if not match:
        return "No citation found"

    start = match.start()
    brace_count = 0
    end = start
    in_entry = False

    while end < len(cell_val):
        if cell_val[end] == '{':
            brace_count += 1
            in_entry = True
        elif cell_val[end] == '}':
            brace_count -= 1
            if brace_count == 0 and in_entry:
                end += 1
                break
        end += 1

    bibtex_entry = cell_val[start:end] if in_entry and brace_count == 0 else "Format Error"
    if bibtex_entry == "none":
        return "none"


    # Find the 'author' field
    author_match = re.search(r'author\s*=\s*\{([^}]*)\}', bibtex_entry, re.IGNORECASE)
    if not author_match:
        return bibtex_entry  # No author field found

    authors = author_match.group(1)

    # Split by 'and'
    authors_list = authors.split(' and ')

    # Recombine authors
    new_authors = authors_list[0]
    for a in range(1, min(len(authors_list), author_limit)):
        new_authors += (" and " + authors_list[a])
    
    #Append 'et al.' if needed
    if len(authors_list) > author_limit:
        new_authors += " et al."

    #Add authors to citation
    modified_bibtex = (bibtex_entry[:author_match.start(1)] +
                       new_authors +
                       bibtex_entry[author_match.end(1):])

    #Remove newlines
    modified_bibtex = modified_bibtex.replace("\n", " ")

    return modified_bibtex


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


def write_md(input_filepaths: list[str], output_dir: str, columns: list[tuple], author_limit:int=10) -> None:
    """
    Combines the YAML tables at `input_filepaths` and exports the combined table 
    to a Markdown file called "benchmarks.md" in `output_dir`.
    Headers for each column are called `columns`.

    If the output directory does not exist, the function creates a new directory
    with the given name.

    Parameters:
        input_filepaths: list of filepaths
        output_dir: directory to export results
        columns: column names for the exported table
        author_limit: maximum number of authors that appear in citations before being truncated with 'et al.'
    """

    contents = merge_yaml_files(input_filepaths)
    os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join(output_dir, "benchmarks.md"), 'w', encoding='utf-8') as md_file:
        headers = [col[2] for col in columns]
        md_file.write('| ' + ' | '.join(headers) + ' |\n')
        md_file.write('| ' + ' | '.join(['---'] * len(columns)) + ' |\n')

        for row in contents:
            current_article_name = None

            row_cells = []
            for col_name, _, _ in columns:
                cell_value = row.get(col_name, '')

                #save the article's name
                if col_name == "name":
                    current_article_name = cell_value

                # replace characters that would break the MD table
                cell_value = str(cell_value).replace("\n", " ").replace("['", "").replace("']", "")
                cell_value = cell_value.replace("', '", ", ").replace("','", ", ").replace("[]", "")
                cell_value = cell_value.replace("[", " ").replace("]", " ").replace("(", " ").replace(")", " ")

                # if adding the citation, put in [<title>][<URL>] format
                if col_name == "cite":

                    #find the first instance of the string "http" in the value
                    link_start_location = cell_value.find("http")
                    link_end_location = cell_value.find("}", link_start_location)
                    link = cell_value[link_start_location:link_end_location].strip()

                    #put the link in the citation
                    cell_value = f"[{current_article_name}]({link})"

                # if adding citations, add the citation row with author limit
                elif col_name == "full_cite":
                    cell_value = get_bibtex(row.get("cite", '')[0], author_limit)

                row_cells.append(cell_value)
                
            md_file.write('| ' + ' | '.join(row_cells) + ' |\n')


def escape_latex(text) -> str:
    """
    Returns a copy of `text` where LaTeX special characters are replaced with valid escape sequences.

    If `text` is not a string, `text` is automatically converted to a string.

    Parameters:
        text: text to transform
    Returns:
        LaTeX friendly version of `text`
    """
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


def write_latex(input_filepaths: List[str], output_filepath: str, columns: List[tuple], standalone: bool = False, author_limit: int|None = 10) -> None:
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
                        if author_limit is not None and col_name in "authors":
                            displayed = val[:author_limit]
                            suffix = ", et al." if len(val) > author_limit else ""
                            val = "[" + ", ".join(escape_latex(str(v)) for v in displayed) + suffix + "]"

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
    parser.add_argument('--standalone', '-s', action='store_true', help="Include full LaTeX document preamble. Works only with LaTeX format")
    parser.add_argument('--out-dir', '-o', type=str, default='../content/', help="Output directory")
    parser.add_argument('--columns', '-c', type=lambda s: s.split(','), help="Subset of columns to include")
    parser.add_argument('--readme', action='store_true', help="Show README.md content")
    parser.add_argument('--index', '-I', action='store_true', help="Generate individual pages for each entry and an index.md. Works only with MD format")
    parser.add_argument('--authorlimit', type=int, default=9999999, help="Limit number of authors for LaTeX")
    parser.add_argument('--authortruncation', type=int, default=None, help="Truncate authors for index pages")
    parser.add_argument('--withcitation', action='store_true', help="Include a row for BibTeX citations. Works only with Markdown format")


    args = parser.parse_args()

    if args.readme:
        with open('README.md', 'r') as file:
            print(file.read())
            sys.exit(0)

    #enforce flag policies
    if args.standalone and args.format != 'tex':
        parser.error("--standalone is only valid with --format tex")
    if args.index and args.format != 'md':
        parser.error("--index is only valid with --format md")
    if args.withcitation and args.format != 'md':
        parser.error("--withcitation is only valid with --format md")


    for file in args.files:
        if not os.path.exists(file):
            parser.error(f"The file {file} does not exist")

    os.makedirs(args.out_dir, exist_ok=True)

    columns = get_column_triples(args.columns) if args.columns else COLUMN_TITLES


    if args.withcitation:
        columns.append(FULL_CITE_TITLE)


    if args.index:
        write_individual_md_pages(args.files, os.path.join(args.out_dir, "md_pages"), columns, author_trunc=args.authortruncation)
    elif args.format == 'md':
        write_md(args.files, os.path.join(args.out_dir, "md"), columns, args.authorlimit)
    elif args.format == 'tex':
        write_latex(args.files, os.path.join(args.out_dir, "tex"), columns, standalone=args.standalone, author_limit=args.authorlimit)