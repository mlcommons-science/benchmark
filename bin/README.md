# Benchmark Runnables

Run `generate.py` to convert YAML files to a Markdown or LaTeX table.
A valid Python installation is required to run the script.   

`generate.py` takes a path to a YAML file representing a table as its input, as well as an output directory. The output appears as a table within an automatically generated subdirectory. The table is in a user-defined format.  

All input options are specified using command-line flags. Note that flags can be declared in any order.

### `generate.py` instructions
For Python 3.12+

##### Required modules
bibtexparser, pyyaml

##### Preinstalled Python modules used
argparse, os, re, sys, typing, textwrap

#### Usage
generate.py [-h]  
--files FILES [FILES ...]  
--format {md, tex} 
[--out-dir OUT_DIR]  
[--authortruncation AUTHORTRUNCATION]  
[--columns COLUMNS]  
[--index]  
[--standalone]  
[--withcitation]

##### Option Details

`--files FILES [FILES ...]`  
One or more input YAML files, or paths to YAML files relative to the user's current directory.  
Required argument.  

`--format {md, tex, indv-md, indv-tex} `  
Output file format. Must be one of `md` or `tex`.  
md -> Markdown. Result appears in {output directory}/md  
tex -> LaTeX. Result appears  in {output directory}/tex  
Required argument.

`[--out-dir OUT_DIR]`  
Specifies the output directory. Creates the directory if the chosen directory does not exist. Default: ../content/, placed in the directory above the script's location

`[--authortruncation AUTHORTRUNCATION]`  
Replaces any author names appearing after the `AUTHORTRUNCATION`-th name in BibTeX citations with "et al." If not set, includes all author names.  
Note that if the `--withcitation` flag is not used, this option does nothing.  
`AUTHORTRUNCATION` must be a positive integer.  

`[--columns COLUMNS]`  
Subset of columns to include, joined by commas, as a single string. Example: date,name,domain,focus,keyword,task_types  

`[--index]`  
Creates each entry as its own file, as well as creating the full table. Individual files appear in (output directory)/(file format)_pages.  
If format is set to `md`, also creates a files called index.md  

`[--standalone]`  
Puts the LaTeX table in a document with a preamble and header.  
Valid only with `format --tex`.  

`[--withcitation]`  
The produced Markdown table will have an additional column containing the BibTeX citations of each entry.  
Valid only with `--format md`