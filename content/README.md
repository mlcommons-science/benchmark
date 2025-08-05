## Markdown Output Files

All Markdown files are located in the folder: `benchmark/content/md`. This folder contains the following:

| File/Folder              | Description                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| `benchmarks.md`          | Combined Markdown file containing all benchmarks in a single table format. |
| `benchmarks/`            | Folder containing individual Markdown files for each benchmark entry.       |

### `benchmarks/` — Individual Benchmark Files

Each file in this folder represents a single benchmark and follows a consistent format. For example:

```markdown
# AIME (American Invitational Mathematics Examination)

**Date**: 2025-03-13  
**Name**: AIME — American Invitational Mathematics Examination  
**Domain**: Mathematics  
**Focus**: Problem-solving skills for top math students in the U.S.  
**Metrics**: Score percentile, accuracy  
**Models**: GPT-4, Claude 3, PaLM 2  
**Summary**:  
The AIME is a highly selective mathematics exam used in the United States to identify students for the USA Mathematical Olympiad. Benchmarks that evaluate performance on AIME problems test advanced reasoning and symbolic math abilities.  
...
```



## LaTeX Output Files

All LaTeX files are located in the folder: `benchmark/content/tex`. This folder contains the following files:

| File                         | Description                                                                 |
|------------------------------|-----------------------------------------------------------------------------|
| `benchmarks.tex`             | Main LaTeX source file that defines the benchmark table layout and content. |
| `benchmarks.pdf`             | Compiled PDF output of the benchmark table for sharing and review.          |
| `benchmarks.log`             | Log file containing compilation details, warnings, and error messages.      |
| `benchmarks.bib`             | Bibliography file containing BibTeX entries for cited benchmark sources.    |
| `benchmarks.aux`             | Auxiliary file used for references, table of contents, and citations.       |
| `benchmarks.out`             | Stores external references (e.g. for cross-referencing sections or labels). |
| `benchmarks.bcf`             | BibLaTeX control file used by `biber` for processing citations.             |
| `benchmarks.fdb_latexmk`     | Dependency file used by `latexmk` to track what needs recompiling.          |
| `benchmarks.fls`             | File listing all input/output files accessed during LaTeX compilation.      |
| `benchmarks.run.xml`         | XML file used by `biber` to parse and resolve bibliography data.            |
| `table.tex`                  | LaTeX subfile that contains the benchmark table only (used in `benchmarks.tex`). |
| `radar_grid.tex`             | LaTeX subfile that contains the radar chart grid (if used for visualization). |
| `section/`                   | Directory containing additional LaTeX sections or modular content.          |
| `images/`                    | Directory containing images included in the LaTeX document.                 |



