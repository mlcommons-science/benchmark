# Tooling Guide

The repository ships with helper scripts in `bin/` and a `Makefile` that automates common tasks. Contributors typically only need the validation commands, while maintainers run the publishing steps.

## Prerequisites

- Python 3.9 or newer (the `requirements.txt` file defines the exact dependencies).
- Optional for maintainers: a LaTeX distribution (`texlive-full`, `latexmk`, and `biber`) to produce the PDF report (installable via `make install_latex` on Debian-based systems).

Install the Python dependencies into a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
make install
```

### Docker workflow

The repository’s Dockerfile bundles Python, LaTeX, and all tooling. To build and enter the container:

```bash
docker build -t benchmark .
docker run --rm -it -v "$PWD":/workspace -e SERVE_HOST=0.0.0.0 -p 8000:8000 benchmark
```

All Make targets and scripts are available from inside the container.

## Make Targets

The most frequently used targets are:

- `make check` – runs `python bin/generate.py --check` to verify required fields and highlight non-ASCII characters.
- `make check_url` – wraps `python bin/generate.py --check_url` to confirm that referenced URLs resolve.
- `make structure` – executes `--check_structure` against the schema for deeper structural validation.
- `make md` – produces Markdown summaries in `content/md/` using `--format=md`.
- `make tex` – generates LaTeX assets (tables, bib, radar charts) into `content/tex/`.
- `make pdf` – calls `latexmk` inside `content/tex/` to build `benchmarks.pdf`.
- `make mkdocs` – renders MkDocs-friendly content and copies assets into `www/science-ai-benchmarks/`.
- `make serve` – serves the MkDocs site locally (`mkdocs serve -a $(SERVE_HOST):8000`).
- `make publish` – commits generated site updates and runs `mkdocs gh-deploy` (maintainer use only).
- `make clean` – removes generated folders under `content/`.


## Core Scripts (`bin/`)

- `generate.py` – central file for validating YAML and producing Markdown/TeX/MkDocs artifacts. The Makefile wraps most common calls.
- `check_structure.py` – standalone validator that compares YAML files against a template (typically `source/benchmarks-format.yaml`) and reports structural mismatches.
- `check_log.py` – contains helper functions to filter LaTeX logs so warnings and errors surface quickly.
- `getbib.py` – standalone utility that prints a BibTeX citation given a DOI, arXiv ID, or other supported identifier.

`generate.py` includes a built-in usage guide at the top of the file (see the docstring beginning with `Usage:`). Refer to it for the complete list of command-line switches and examples. You can pass a comma-separated list of files to the `--files` option when testing new YAML documents.

## Generated Content

Most commands write intermediate files into the `content/` directory. These assets (Markdown pages, TeX sources, MkDocs metadata, images) should be treated as generated output—avoid manual edits. When you run `make mkdocs` or `make publish`, MkDocs writes the deployable static site to `www/science-ai-benchmarks/`. The entire `www/` folder is ignored by Git and serves as the staging area for GitHub Pages.

## Troubleshooting

- If LaTeX builds fail, run `make pdf` twice and inspect `content/tex/benchmarks.log`.
- URL checks occasionally fail due to transient outages. Re-run `make check_url`; if a link is consistently down, replace it with an archived source or note the outage in your PR.
- When adding new dependencies, update `requirements.txt` and mention the change in your PR description.
