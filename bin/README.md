# Benchmark Runnables

Run `generate.py` to convert the YAML table in the source/ folder to a Markdown or LaTeX table.
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
--format {md, tex, indv-md, indv-tex} 
[--out-dir OUT_DIR]  
[--authortruncation AUTHORTRUNCATION]  
[--columns COLUMNS]  
[--readme]  
[--standalone]  
[--withcitation]

##### Option Details

`--files FILES [FILES ...]`  
One or more input YAML files, or paths to YAML files relative to the user's current directory.  
Mandatory argument.  

`--format {md, tex, indv-md, indv-tex} `  
Output file format. Must be one of `md`, `tex`, or `indv-tex`.  
md -> Markdown. Result appears in {output directory}/md  
tex -> LaTeX. Result appears  in {output directory}/tex  
indv-md -> Markdown, with all entries exported as their own table. Result appears  in {output directory}/md_pages.    
indv-tex -> LaTeX, with all entries exported as their own table. Result appears  in {output directory}/tex.  
Mandatory argument.

`[--out-dir OUT_DIR]`  
Specifies the output directory. Creates the directory if the chosen directory does not exist. Default: ./content  

`[--authortruncation AUTHORTRUNCATION]`  
Replaces any author names appearing after the `AUTHORTRUNCATION`-th name in BibTeX citations with "et al." If not set, includes all author names.  
Note that if the `--withcitation` flag is not used, this option does nothing.
`AUTHORTRUNCATION` must be a positive integer. Valid only with `--format md`

`[--columns COLUMNS]`  
Subset of columns to include, joined by commas, as a single string. Example: date,name,domain,focus,keyword,task_types  

`[--readme]`  
Prints the contents of this README file. If this flag is set, the script will not convert its input file.  

`[--standalone]`  
Creates a LaTeX file with a preamble and header, allowing it to function as its own LaTeX file.  
Valid only with `--format tex`  

`[--withcitation]`  
Creates a Markdown table with an additional column containing the BibTeX citations of each entry.  
Valid only with `--format md`    
  

##### Example
Current directory is `benchmark`, with the generate script in `benchmark/bin/generate.py`. Input files are `source/file1.yaml` and `source/file2.yaml`, output directory is `content`. To produce a Markdown table with an additional row for BibTeX citations, each containing at most 10 author names:  
`python bin/generate.py --files source/file1.yaml source/file2.yaml --out-dir content --format md --withcitation --authortruncation 10`  
Note that flags can be declared in any order.