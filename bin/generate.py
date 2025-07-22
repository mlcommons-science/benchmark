"""
Usage:
  generate.py --files=file1,file2 --check
  generate.py --files=file1,file2 --format=<fmt> --outdir=<dir> [--authortruncation=N] [--columns=col1,col2] [--check] [--noratings] [--required] [--standalone] [--withcitation] [--withurlcheck]
  generate.py --check_log


Options:
  --files=<file>...           YAML file paths to process (one or more) [default: source/benchmark-addon.yaml].
  --format=<fmt>              Output file format [default: tex].
  --outdir=<dir>              Output directory [default: ./content/].
  --authortruncation=N        Truncate authors for index pages [default: 9999].
  --columns=<cols>            Subset of columns to include, comma-separated.
  --check                     Conduct formatting checks only.
  --noratings                 Removes rating columns from output.
  --required                  Requires all specified columns to exist.
  --standalone                Include full LaTeX document preamble (tex only).
  --withcitation              Add a citation row (md only).
  --withurlcheck              Check if URLs exist.
  --check_log                     Check the latex log file by removing unneded content

Notes:
  - --standalone is only valid with --format=tex
  - --withcitation is only valid with --format=md
  - Author truncation must be a positive integer
"""

import os
import sys
from docopt import docopt
from typing import Union, Dict
from yaml_manager import YamlManager
from md_writer import MarkdownWriter
from generate_latex import GenerateLatex, ALL_COLUMNS
from cloudmesh.common.console import Console
from check_log import print_latex_log
from cloudmesh.common.console  import Console
from yaml_manager import find_unicode_chars

VERBOSE = True
if VERBOSE:
    Console.ok("Starting the generation process...")

if __name__ == "__main__":
    args = docopt(__doc__)

    check_log = args["--check_log"]
    if check_log:
        print_latex_log(filename="content/tex/benchmarks.log")
        sys.exit(0)

    format_type = args["--format"] or "tex"
    output_dir = args["--outdir"] or "./content/"
     
    author_trunc = int(args["--authortruncation"])
    
    files = args["--files"]
    if files is None:
        files = ["source/benchmark-addon.yaml"]
    else:
        files = files.split(",") 

    columns = args["--columns"] 
    if columns is None:
        columns = ALL_COLUMNS.keys() 
    else:
        columns = columns.split(",")     
    
    if args["--standalone"] and format_type != "tex":
        print("Error: --standalone is only valid with --format=tex")
        sys.exit(1)

    if args["--withcitation"] and format_type != "md":
        print("Error: --withcitation is only valid with --format=md")
        sys.exit(1)

    if author_trunc <= 0:
        print("Error: --authortruncation must be a positive integer")
        sys.exit(1)

    for file in files:
        if not os.path.exists(file):
            print(f"Error: file not found: {file}")
            sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    manager = YamlManager(files)
    entries = manager.get_flat_dicts()

    if args["--check"]:

        print ("HHHH")
        for file in files:
            if not os.path.exists(file):
                print(f"Error: file not found: {file}")
                sys.exit(1)
            Console.info("Checking YAML files for formatting issues...")
            find_unicode_chars(filename=file)
        manager.check_required_fields()
        sys.exit(0)

    if args["--required"]:
        if not manager.check_required_fields():
            sys.exit(1)

    if args["--withurlcheck"]:
        manager.check_urls()

    if format_type == "md":

        converter = MarkdownWriter(entries, raw_entries=manager.data)
        converter.write_table(columns=columns)
        converter.write_individual_entries(columns=columns)

    elif format_type == "tex":
        converter = GenerateLatex(entries)

        converter.generate_radar_chart_grid()

        Console.info("generate radar charts..")
        converter.generate_radar_charts(fmt="pdf")
        converter.generate_radar_charts(fmt="png")

        Console.info("Generating LaTeX table...")
        converter.generate_table()
        Console.info("Generating LaTeX BibTeX...")
        converter.generate_bibtex()
        Console.info("Generating section document...")
        converter.generate_section()
        Console.info("Generating document...")
        converter.generate_document()
