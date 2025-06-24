import argparse
import os
import sys
import yaml
import re
from typing import List


# Predefined list of all possible column names
ALL_COLUMNS = [ 
    "date", "expiration", "valid", 
    "name", "url", "domain", "focus",
    "keyword", "description", "task_types", "ai_capability_measured",
    "metrics", "models", "notes", 
    "cite"
]


def load_yaml_file(file_path:str) -> (list[dict] | list):
    """
    Returns the contents of a YAML file at `file_path` as a dictionary or a list.

    Parameters:
        file_path: file path to load from
    Returns:
        most appropriate format for YAML file contents
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = yaml.safe_load(f)
        if isinstance(content, dict):
            return [content]
        elif isinstance(content, list):
            return content
        else:
            raise ValueError(f"Unsupported YAML format in {file_path}")
    

def merge_yaml_files(file_paths:list[str]) -> list[dict]:
    """
    Returns a list containing the merged contents of the filepaths in `file_paths`.

    Each array in the output is a list representing a row in the table.
    The row is represented as a dictionary.

    Any row not present in any of the tables in `file_paths` is automatically created in the output.

    Parameters:
        file_paths: the paths to each file to load from
    Returns:
        list of dictionaries containing merged file contents
    """
    records = []
    for path in file_paths:
        records.extend(load_yaml_file(path))

    # Ensure all records have all columns, filling missing columns with None
    merged_records = []
    for record in records:
        merged_record = {col: record.get(col, None) for col in ALL_COLUMNS}
        merged_records.append(merged_record)
    
    return merged_records



def write_md(input_filepaths:list[str]=['../source/benchmarks.yaml'], output_dir:str='../content') -> None:
    """
    Converts the YAML table at `input_filepaths` to a Markdown table at `output_filepath`.

    Results are placed into `md` inside the output directory. `md` must exist prior to the method call.

    Parameters:
        input_filepaths: paths to input YAML files. Must be a list of strings. All files must exist.
        output_dir: path to output directory. Must be a string. The directory at the path must exist and contain a directory called "md".
    """

    contents = merge_yaml_files(input_filepaths)

    with open(output_dir + "/benchmarks.md", 'w', encoding='utf-8') as md_file:
        # Write the table header
        header_row = '| ' + ' | '.join(ALL_COLUMNS) + ' |'
        md_file.write(header_row + '\n')
        
        # Write a separator row
        separator_row = '| ' + ' | '.join(['---'] * len(ALL_COLUMNS)) + ' |'
        md_file.write(separator_row + '\n')
        
        # Write each data row
        for row in contents:
            cleaned_row = '| ' + ' | '.join(str(row.get(cell, '')) for cell in row) + ' |'

            cleaned_row = cleaned_row.replace("\n", " ") #BUGFIX: Newlines mess up the Markdown format
            #Formatting fixes
            cleaned_row = cleaned_row.replace("['", "")
            cleaned_row = cleaned_row.replace("']", "")
            cleaned_row = cleaned_row.replace("', '", ", ")
            cleaned_row = cleaned_row.replace("','", ", ")
            cleaned_row = cleaned_row.replace("[]", "")

            md_file.write(cleaned_row + '\n')




def escape_latex(text):
    """Escape special LaTeX characters."""
    if not isinstance(text, str):
        text = str(text)
    return (
        text.replace("\\", "\\textbackslash{}")
            .replace("&", "\\&")
            .replace("%", " percent")
            .replace("_", "\\_")
            .replace("#", "\\#")
            .replace("{", "\\{")
            .replace("}", "\\}")
            .replace("^", "\\^{}")
            .replace("~", "\\~{}")
            .replace("$", "\\$")
    )

def extract_cite_keys(cite_entries):
    """Extract citation keys from BibTeX entries."""
    keys = []
    for entry in cite_entries:
        match = re.search(r"@\w+\{([^,]+),", entry)
        if match:
            keys.append(match.group(1))
    return keys

def wrap_url_with_cite(url: str, cite_keys: List[str]) -> str:
    """Wrap URL with \\href{}{} and add \\cite{} if keys present."""
    if cite_keys:
        return f"\\href{{{url}}}{{{url}}} \\cite{{{', '.join(cite_keys)}}}"
    return f"\\href{{{url}}}{{{url}}}"

def write_latex(input_filepaths: List[str] = ['../source/benchmarks.yaml'],
               output_filepath: str = '../content/',
               standalone: bool = False) -> None:
    os.makedirs(output_filepath, exist_ok=True)

    for filepath in input_filepaths:
        with open(filepath, 'r', encoding='utf-8') as f:
            records = yaml.safe_load(f)

        if not isinstance(records, list):
            raise ValueError(f"{filepath} must contain a list of benchmark records")

        base_name = os.path.splitext(os.path.basename(filepath))[0]
        output_tex_path = os.path.join(output_filepath, f"{base_name}.tex")

        with open(output_tex_path, 'w', encoding='utf-8') as f:
            if standalone:
                f.write("\\documentclass{article}\n")
                f.write("\\usepackage{hyperref}\n")
                f.write("\\usepackage[margin=1in]{geometry}\n")
                f.write("\\begin{document}\n")

            f.write("\\begin{table}[h!]\n\\centering\n")
            f.write("\\begin{tabular}{|" + " | ".join(["l"] * len(ALL_COLUMNS)) + "|}\n")
            f.write("\\hline\n")
            f.write(" & ".join(ALL_COLUMNS) + " \\\\ \\hline\n")

            for record in records:
                cite_keys = extract_cite_keys(record.get("cite", []))
                row = []
                for col in ALL_COLUMNS:
                    val = record.get(col, '')
                    if col == "url" and val:
                        val = wrap_url_with_cite(val, cite_keys)
                    elif isinstance(val, list):
                        val = "[" + ", ".join(escape_latex(str(v)) for v in val) + "]"
                    else:
                        val = escape_latex(val)
                    row.append(val)
                f.write(" & ".join(row) + " \\\\ \\hline\n")

            f.write("\\end{tabular}\n\\end{table}\n")

            if standalone:
                f.write("\\end{document}\n")



if __name__ == "__main__":

    # Create the parser
    parser = argparse.ArgumentParser(
        description="A script to process files with specified format and output directory."
    )

    # Add --files argument
    parser.add_argument(
        '--files', '-i',
        type=str,
        nargs='+',  # Allows one or more arguments
        required=True,
        help='One or more file paths to process. Required argument.'
    )

    # Add --format argument
    parser.add_argument(
        '--format', '-f',
        type=str,
        choices=['md', 'tex'], # Restricts input to 'md' or 'tex'
        help="Output file format. Must be 'md' (Markdown) or 'tex' (LaTeX)"
    )

    # Add --standalone argument
    parser.add_argument(
        '--standalone', '-s',
        action='store_true', # Stores True if the flag is present, False otherwise
        help="If set, generates the table with a LaTeX preamble. If not set, generates only the table. This flag may be used only when --format is 'tex'"
    )

    # Add --out argument
    parser.add_argument(
        '--out-dir', '-o',
        type=str,
        default='../content/', # Default output directory
        help="Output directory for processed files. Default: '../content/'"
    )

    # Add --readme argument
    parser.add_argument(
        '--readme',
        action="store_true",
        help="Prints the contents of the README help document"
    )

    # Parse the arguments from the command line
    args = parser.parse_args()


    
    #check if the readme flag is used. if so, print the README
    if args.readme:
        with open('README.md', 'r') as file:
            print(file.read())
            sys.exit(0)


    #Check standalone flag
    if args.standalone and args.format != 'tex':
        parser.error("--standalone flag may be used only when --format option is 'tex'")


    # Print the parsed arguments (for demonstration purposes)
    # print(f"Parsed Arguments:")
    # print(f"  Files: {args.files}")
    # print(f"  Format: {args.format}")
    # print(f"  Standalone: {args.standalone}")
    # print(f"  Output Directory: {args.out_dir}")


    #check if input files exist
    for file in args.files:
        if not os.path.exists(file):
            parser.error("The file " + file + " does not exist")

    #create directories in the output directory if they don't exist
    if not os.path.isdir(args.out_dir):
        os.makedirs(args.out_dir, exist_ok=True)
    if args.format=='md' and not os.path.isdir(args.out_dir + "/md"):
        os.makedirs(args.out_dir + "/md", exist_ok=True)
    if args.format=='tex' and not os.path.isdir(args.out_dir + "/tex"):
        os.makedirs(args.out_dir + "/tex", exist_ok=True)
    

    #convert the yaml(s) into specified format
    if args.format == 'md':
        write_md(args.files, args.out_dir + "/md")
    elif args.format == 'tex':
        write_latex(args.files, args.out_dir + "/tex")
    