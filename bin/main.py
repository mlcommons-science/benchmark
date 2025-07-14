import argparse
import os
import sys
from yaml_manager import YamlManager
from md_writer import YamlToMarkdownConverter
from latex_writer import YamlToLatexConverter

# Optional: define MAX_AUTHOR_LIMIT and FULL_CITE_COLUMN if not imported
MAX_AUTHOR_LIMIT = 3
FULL_CITE_COLUMN = ("full_cite", "1cm", "Full BibTeX")

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
    ("cite", "1cm", "Citation"),
    ("ratings", "1cm", "Ratings"),
]



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process YAML benchmark files to Markdown or LaTeX.")
    parser.add_argument('--files', '-i', type=str, nargs='+', required=True, help='YAML file paths to process.')
    parser.add_argument('--format', '-f', type=str, choices=['md', 'tex'], required=True, help="Output file format: 'md' or 'tex'")
    parser.add_argument('--outdir', '-o', type=str, default='../content/', required=True, help="Output directory")
    parser.add_argument('--authortruncation', type=int, default=MAX_AUTHOR_LIMIT, help="Truncate authors for index pages")
    parser.add_argument('--columns', type=lambda s: s.split(','), help="Subset of columns to include")
    parser.add_argument('--check', action='store_true', help="Conduct formatting checks on inputted YAML files. Does not produce an output file.")
    parser.add_argument('--index', action='store_true', help="Generate individual pages for each entry for the given format. If format is MD, generates an index.md file")
    parser.add_argument('--noratings', action='store_true', help="Removes rating columns from the output file")
    parser.add_argument('--required', action='store_true', help="Makes all the columns required that are listed in the --columns command")
    parser.add_argument('--standalone', '-s', action='store_true', help="Include full LaTeX document preamble.")
    parser.add_argument('--withcitation', action='store_true', help="Include a row for BibTeX citations. Works only with Markdown format")

    args = parser.parse_args()

    if args.standalone and args.format != 'tex':
        parser.error("--standalone is only valid with --format tex")
    if args.withcitation and args.format != "md":
        parser.error("--withcitation is only valid with --format md")
    if args.authortruncation <= 0:
        parser.error("author truncation amount must be a positive integer")

    for file in args.files:
        if not os.path.exists(file):
            parser.error(f"The file {file} does not exist")

    os.makedirs(args.outdir, exist_ok=True)
    columns = get_column_triples(args.columns) if args.columns else []  # Fallback if ALL_COLUMNS not in scope

    manager = YamlManager()
    manager.load_yamls(args.files)
    entries = manager.get_dicts()

    if args.required:
        manager.verify_fields(entries)

    if args.check:
        manager.verify_fields(entries)
        sys.exit(0)

    if args.withcitation:
        columns.append(FULL_CITE_COLUMN)

    if args.format == 'md':
        converter = YamlToMarkdownConverter(entries)
        if args.index:
            converter.write_individual_entries(os.path.join(args.outdir, "md_pages"))
        converter.convert_to_single_file(os.path.join(args.outdir, "benchmarks.md"))

    elif args.format == 'tex':
        converter = YamlToLatexConverter(entries)
        if args.index:
            converter.write_individual_entries(os.path.join(args.outdir, "tex_pages"))
        converter.convert_to_single_file(os.path.join(args.outdir, "benchmarks.tex"))
