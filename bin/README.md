Scripts for converting YAML files into other formats.

fmtconvert.py combines all inputted YAML files into a single table, then outputs them in a format chosen by the user.


Syntax for fmtconvert.py:
fmtconvert.py {file1.yaml file2.yaml ...} --{option} {output filename}

Options:
--md: converts input files to Markdown format
--tex: converts to Latex format
--indv-tex: converts each benchmark listing to an indvidual latex file
--print: prints input files to the standard output
Reece Shiraishi