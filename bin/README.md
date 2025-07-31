# Runnables
This directory contains all programs used to check YAML files and convert YAML files into tables.

## Scripts

The main script is `generate.py`. Its input is one or more YAML files. The output is TeX or YAML files in the `content` directory.

This directory contains additional scripts for checking YAML files and the outputs produced with them:
- `check_log.py`: Contains functions to filter content in TeX logs
- `check_structure.py`: Standalone script that checks YAML files against a template YAML file. The output is whether the given YAML matches the format given in the template.
- `getbib.py`: Standalone script. Prints the BibTeX citation given a DOI, Arxiv ID, or other official identifier.
- `url_checker.py`: Contains functions to check whether a given URL exists and can generate a BibTeX citation. Can also convert a HTML page into a Markdown document.

### `generate.py` Documentation
Usage:

    generate.py --files=file1,file2 --check_structure [--structure=<file>]
    generate.py --files=file1,file2 --check
    generate.py --files=file1,file2 --check_url [--url=<URL>]
    generate.py --files=file1,file2 --format=<fmt> --outdir=<dir> [--authortruncation=N] [--columns=col1,col2] [--check] [--noratings] [--required] [--standalone] [--withcitation] [--urlcheck]
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
    --check_url                 Check if URLs exist.
    --check_log                 Check the latex log file by removing unneded content
    --url=<URL>                 URL to check for validity (used with --urlcheck).
    --structure=<file>          Path to a structure file for validation [default: None].
    --check_structure           Check if YAML entries conform to a reference structure. If no structure file
                                is provided the first element of the first file is used.

Notes:
  - --standalone is only valid with --format=tex
  - --withcitation is only valid with --format=md
  - Author truncation must be a positive integer

Examples:

  `python bin/generate.py --files=source/benchmarks.yaml --check_structure`  
    Checks the structure of the yaml files against the first entry of the first file.

  `python bin/generate.py --files=source/benchmarks.yaml --check_structure --structure=source/benchmarks-addon.yaml`  
    Checks the structure of the yaml files against the first element in ths structure file.