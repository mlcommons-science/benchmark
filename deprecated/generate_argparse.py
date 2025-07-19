import argparse
import os
import sys
from yaml_manager import YamlManager
from md_writer import MarkdownWriter
from latex_writer import LatexWriter


ALL_COLUMNS = [
    ("date", "1.5cm", "Date"),
    ("expired", "1cm", "Expired"),
    ("valid", "0.7cm", "Valid"),
    ("name", "2.5cm", "Name"),
    ("url", "0.7cm", "URL"),
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
    ("ratings.specification.rating", "1cm", "Specification Rating"),
    ("ratings.specification.reason", "3cm", "Specification Reason"),
    ("ratings.dataset.rating", "1cm", "Dataset Rating"),
    ("ratings.dataset.reason", "3cm", "Dataset Reason"),
    ("ratings.metrics.rating", "1cm", "Metrics Rating"),
    ("ratings.metrics.reason", "3cm", "Metrics Reason"),
    ("ratings.reference_solution.rating", "1cm", "Reference Solution Rating"),
    ("ratings.reference_solution.reason", "3cm", "Reference Solution Reason"),
    ("ratings.documentation.rating", "1cm", "Documentation Rating"),
    ("ratings.documentation.reason", "3cm", "Documentation Reason"),
]

# BUG: THESE ARE BUGGY DATA STRUCTURES NOT RECOMMENDED TO BE USED. ALL_COLUMNS SHOULD BE USED INSTEAD
# ALSO TE REMOVAL OF cm is questionable


COLUMN_NAMES = []
COLUMN_WIDTHS = []
COLUMN_TITLES = []
for name, width, title in ALL_COLUMNS:
    COLUMN_NAMES.append(name)
    COLUMN_WIDTHS.append(float(width.strip().replace("cm", "")))
    COLUMN_TITLES.append(title)


if __name__ == "__main__":

    script_help = """Process YAML benchmark files to a Markdown or LaTeX table.
    The user specifies one or more input files, the output table format, and the output directory.
    All files in the output directory are under the output."""

    parser = argparse.ArgumentParser(description=script_help)
    parser.add_argument('--files', '-i', type=str, nargs='+', required=True, help='YAML file paths to process.')
    parser.add_argument('--format', '-f', type=str, choices=['md', 'tex'], required=True, help="Output file format: 'md' or 'tex'")
    parser.add_argument('--outdir', '-o', type=str, default='../content/', required=True, help="Output directory")
    parser.add_argument('--authortruncation', type=int, default=9999, help="Truncate authors for index pages")
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

    #Eliminate column names if precondition is broken
    if len(COLUMN_TITLES) != len(columns):
        COLUMN_TITLES = None

    manager = YamlManager(args.files)
    entries = manager.get_table_formatted_dicts()

    # this is a bug. an id is used to convert the name to a unique id and that is checked with the yaml reader
    # #check filenames
    # if not manager.check_filenames():
    #    sys.exit(1)
    

    if args.check:
        check_passed = manager.check_required_fields()
        sys.exit(0)

    if args.required:
        if not manager.check_required_fields():
            sys.exit(1)
    
        
    if args.withurlcheck:
        manager.check_urls() # URL check

    if args.format == 'md':
        converter = MarkdownWriter(entries)

        if args.index:
            converter.write_individual_entries(args.outdir, args.columns, COLUMN_TITLES)
        converter.write_table(args.outdir, args.columns, COLUMN_TITLES)

    elif args.format == 'tex':
        converter = LatexWriter(entries)
        if args.index:
            converter.write_individual_entries(args.outdir, args.columns)
        converter.write_table(args.outdir, 
                              args.columns)
#                              columns=ALL_COLUMNS)