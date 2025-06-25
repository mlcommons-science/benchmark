import argparse
import os
import sys
import yaml
import re
from typing import List

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

def sanitize_filename(name: str) -> str:
    return re.sub(r'[^\w\-_\. ]', '_', name).replace(' ', '_').lower()

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

def write_individual_md_pages(input_filepaths: List[str], output_dir: str, columns: List[tuple]) -> None:
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
                            lines = bibtex.strip().splitlines()

                            # Parse entry type and id from first line
                            if lines:
                                first_line = lines[0].strip()
                                m = re.match(r'@(\w+)\s*\{\s*([^,]+),', first_line)
                                if m:
                                    entry_type = m.group(1)
                                    entry_id = m.group(2)
                                    f.write(f"  - type: {entry_type}\n")
                                    f.write(f"  - id: {entry_id}\n")

                            # Parse all key = value lines (attributes)
                            for line in lines[1:]:
                                line = line.strip()
                                if line == "}" or line == "":
                                    continue
                                m = re.match(r'(\w+)\s*=\s*[{"]?(.*?)[}"]?,?$', line)
                                if m:
                                    key = m.group(1).strip()
                                    value = m.group(2).strip()
                                    if value.endswith(','):
                                        value = value[:-1].strip()
                                    f.write(f"  - {key}: {value}\n")

                            # Print the full original bibtex block last
                            f.write("  - bibtex: |\n")
                            for bib_line in lines:
                                f.write(f"      {bib_line}\n")
                        f.write("\n")
                    else:
                        val_str = str(val).replace("\n", " ").replace("['", "").replace("']", "")
                        val_str = val_str.replace("', '", ", ").replace("','", ", ").replace("[]", "")
                        val_str = val_str.replace("[", " ").replace("]", " ").replace("(", " ").replace(")", " ")
                        f.write(f"**{col_display}**: {val_str}\n\n")
            index_file.write(f"- [{entry_name}]({filename})\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process YAML benchmark files to Markdown or LaTeX.")

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
    parser.add_argument('--authorlimit', type=int, default=None,
                        help="Limit number of authors (e.g., --authorlimit 10 adds 'et al.' if exceeded)")
    parser.add_argument('--index', action='store_true',
                        help="Generate individual pages for each entry and an index.md file")

    args = parser.parse_args()

    if args.readme:
        with open('README.md', 'r') as file:
            print(file.read())
            sys.exit(0)

    for file in args.files:
        if not os.path.exists(file):
            parser.error(f"The file {file} does not exist")

    os.makedirs(args.out_dir, exist_ok=True)
    columns = get_column_triples(args.columns) if args.columns else ALL_COLUMNS

    if args.index:
        index_output_dir = os.path.join(args.out_dir, "md")
        write_individual_md_pages(args.files, index_output_dir, columns)
    else:
        print("Use --index to generate individual Markdown pages and index.md.")
