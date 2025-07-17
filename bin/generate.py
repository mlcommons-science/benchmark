import argparse
import os
import sys
from yaml_manager import YamlManager
from md_writer import MarkdownWriter
from latex_writer import LatexWriter
from bib_writer import BibtexWriter

# Optional: define MAX_AUTHOR_LIMIT and FULL_CITE_COLUMN if not imported
MAX_AUTHOR_LIMIT = 9999
FULL_CITE_COLUMN = ("full_cite", "1cm", "Full BibTeX")

# ALL_COLUMNS = [
#     ("date", "1.5cm", "Date"),
#     ("expiration", "1.5cm", "Expiration"),
#     ("valid", "1.5cm", "Valid"),
#     ("name", "2.5cm", "Name"),
#     ("url", "2.5cm", "URL"),
#     ("domain", "2cm", "Domain"),
#     ("focus", "2cm", "Focus"),
#     ("keywords", "2.5cm", "Keywords"),
#     ("description", "4cm", "Description"),
#     ("task_types", "3cm", "Task Types"),
#     ("ai_capability_measured", "3cm", "AI Capability"),
#     ("metrics", "2cm", "Metrics"),
#     ("models", "2cm", "Models"),
#     ("notes", "3cm", "Notes"),
#     ("cite", "1cm", "Citation"),
#     ("ratings", "1cm", "Ratings"),
# ]

COLUMN_TUPLES = [
    ("date", 1.5, "Date"),
    ("name", 2.5, "Name"),
    ("domain", 2, "Domain"),
    ("focus", 2, "Focus"),
    ("keywords", 2.5, "Keywords"),
    ("task_types", 3, "Task Types"),
    ("metrics", 2, "Metrics"),
    ("models", 2, "Models"),
    ("cite", 1, "Citation"),
]
COLUMN_NAMES = []
COLUMN_WIDTHS = []
COLUMN_TITLES = []
for name, width, title in COLUMN_TUPLES:
    COLUMN_NAMES.append(name)
    COLUMN_WIDTHS.append(width)
    COLUMN_TITLES.append(title)


# def get_column_triples(selected: list[str]) -> list[tuple[str, str, str]]:
#     selected_lower = [s.lower() for s in selected]
#     return [triple for triple in ALL_COLUMNS if triple[0] in selected_lower]


if __name__ == "__main__":

    script_help = """Process YAML benchmark files to a Markdown or LaTeX table.
    The user specifies one or more input files, the output table format, and the output directory.
    All files in the output directory are under the output."""

    parser = argparse.ArgumentParser(description=script_help)
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
    parser.add_argument('--withurlcheck', action='store_true', help="Checks if url exists or not")

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
    columns = args.columns if args.columns else COLUMN_NAMES # Fallback if args.columns not in scope

    manager = YamlManager(args.files)
    entries = manager.get_table_formatted_dicts()

    #check filenames
    if not manager.check_filenames():
        sys.exit(1)
    

    if args.check:
        check_passed = manager.check_required_fields()
        sys.exit(0)

    if args.required:
        if not manager.check_required_fields():
            sys.exit(1)


    # if args.withcitation:
    #     columns.append(['cite'])
    
        
    if args.withurlcheck:
        manager.check_urls() # URL check

    if args.format == 'md':
        bib_writer = BibtexWriter(entries)
        converter = MarkdownWriter(entries)

        if args.index:
            converter.write_individual_entries(args.outdir, args.columns, COLUMN_TITLES)
        converter.write_table(args.outdir, args.columns, COLUMN_TITLES)

    elif args.format == 'tex':
        converter = LatexWriter(entries)
        if args.index:
            converter.write_individual_entries(args.outdir, args.columns)
        converter.write_table(args.outdir, columns=args.columns)
