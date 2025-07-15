import argparse
import os
import sys
import yaml
import re
import textwrap
import bibtexparser

ALL_COLUMNS = [
    ("date", "1.5cm", "Date"),
    ("expiration", "1.5cm", "Expiration"),
    ("valid", "1.5cm", "Valid"),
    ("name", "2.5cm", "Name"),
    ("url", "2.5cm", "URL"),
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
    ("ratings", "1cm", "Ratings"),
]

FULL_CITE_COLUMN = ("full_cite", "1cm", "Full BibTeX")

RATINGS_COLUMNS = [
    ("problem_spec_rating", "1cm", "Problem Specification Rating"),
    ("problem_spec_reason", "3cm", "Problem Specification Reason"),
    ("dataset_rating", "1cm", "Dataset Rating"),
    ("dataset_reason", "3cm", "Dataset Reason"),
    ("metrics_rating", "1cm", "Metrics Rating"),
    ("metrics_reason", "3cm", "Metrics Reason"),
    ("reference_solution_rating", "1cm", "Reference Solution Rating"),
    ("reference_solution_reason", "3cm", "Reference Solution Reason"),
    ("documentation_rating", "1cm", "Documentation Rating"),
    ("documentation_reason", "3cm", "Documentation Reason")
]

#THESE ARE SUGGESTIONS AND DO NOT NEED TO BE RIGOUOURSLY FOLLOWED

# class Ratings(object):
#     """
#     Reads and verifies YAML file contents
#     """

#     def __init__(self):
#         self.topics = self.read_format()

#     def read_format(self, filename: str='benchmarks-gregor-format.yaml'):
#         """
#         Reads which topics topics from the formatting YAML
#         """
#         pass

#     def check(self, content: list[dict]):
#         """
#         For each entry in `content`, 
#         """
#         for entry in content:
#             for topic in self.topics:
#                 if "rating" in entry[topic]:
#                     print("yay")
#                 else:
#                     print("boo")
                
#                 if "reason" in entry[topic]:
#                     print("yay")
#                 else:
#                     print("boo")

# class Citation(object):
#     """
#     Contains a single BibTeX citation
#     """

#     def kind(self):
#         pass

#     def label(self):
#         pass 

#     def url(self):
#         pass

#     def attributes(self):
#         """
#         Everything but `kind` and `label`
#         """
#         pass

#     def __str__(self):
#         raise Exception("NOT YET IMPLEMENTED")

#     def check(self):
#         """
#         "Is the kind valid, label properly formatted..."
#         """
#         pass

   

# class Citations(object):
#     """
#     Contains the citations of one YAML entry
#     """
#     pass 



# class AllCitations(object):
#     """
#     Holds a list of Citations objects
#     """
#     pass


# RATINGS_TOPICS = [
#     #Insert ratings topics from gregor yaml format
# ]

CHECKED_RATINGS_COLUMNS = RATINGS_COLUMNS[:]

MAX_AUTHOR_LIMIT = 9999

def get_column_triples(selected: list[str]) -> list[tuple[str, str, str]]:
    selected_lower = [s.lower() for s in selected]
    return [triple for triple in ALL_COLUMNS if triple[0] in selected_lower]


def verify_checked_columns(file_contents: list[dict], printing_warnings: bool = True) -> bool:
    """
    Returns True if all entries in `file_contents` have a "name", "cite", and "ratings" entry,
    where each "ratings" entry contains the keys listed in `RATINGS_COLUMNS`.

    Parameters:
        file_contents: YAML entries to check
        printing_warnings: whether to print error messages to the console for each missing rating. Default is True
    Returns:
        whether the inputted file contents have the proper fields
    """
    check_passed = True

    for entry in file_contents:

        #Check name and cite first
        name = entry.get("name")
        if not name:
            print(f"\033[91mWARNING: Missing name in entry \033[33m{entry}\033[00m")
            check_passed = False
            continue
        citation = entry.get("cite")
        if not citation:
            print(f'\033[91mWARNING: Missing citation in entry "{name}"\033[00m')
            check_passed = False
            continue
        
        #Check if ratings exist
        ratings_dicts = entry.get("ratings")
        if not ratings_dicts:
            if printing_warnings:
                print(f'\033[91mWARNING: Ratings not present in entry "{name}"\033[00m')
                check_passed = False
                continue

        #Check number of ratings
        if not len(ratings_dicts)==len(CHECKED_RATINGS_COLUMNS): #ignore the warning
            if printing_warnings:
                print(f'\033[91mWARNING: There must be {len(CHECKED_RATINGS_COLUMNS)} rating categories (found {len(ratings_dicts)} categories) in entry "{name}"\033[00m')
                check_passed = False
                continue

        #Check if each entry in RATINGS_COLUMNS exist
        for i in range(len(CHECKED_RATINGS_COLUMNS)):
            # print(ratings_dicts[i].get(RATINGS_COLUMNS[i][0]))
            if ratings_dicts[i].get(CHECKED_RATINGS_COLUMNS[i][0])==None:
                print(f'\033[91mWARNING: Category "{CHECKED_RATINGS_COLUMNS[i][0]}" missing from entry "{name}"\033[00m')
                check_passed = False

    return check_passed


def load_yaml_file(file_path: str) -> list[dict]:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"\033[91mYAML SYNTAX ERROR in {file_path}:\033[00m\n{e}")
        return []  # Skip this file or entry instead of crashing

    if isinstance(content, dict):
        return [content]
    elif isinstance(content, list):
        return content
    else:
        print(f"\033[93mWARNING: Unsupported YAML format in {file_path}\033[00m")
        return []


def sanitize_filename(name: str) -> str:
    output = ""
    for ch in name:
        if 32<=ord(ch)<=126:
            output += ch

    output = re.sub(r' {2,}', ' ', output) #Replace 2+ spaces with single space
    output = output.strip().replace("(", "").replace(")", "").replace(" ", "_")

    return output


def merge_yaml_files(file_paths: list[str], disable_error_messages: bool = False) -> list[dict]:
    """
    Combines the contents of the files at `file_paths` into a single dictionary.
    Each key in the dictionary is a fields in the YAML files (i.e. name, expired, cite).

    If any duplicate "name" fields are found, the function prints an error message and
    does not add the duplicate to the output.

    Parameters:
        file_paths: file paths of the YAMLs to merge
        disable_error_messages: True if not printing error messages
    Returns:
        list of dictionaries representing combines YAML file entries
    """
    records = []
    seen_names = set()
    for path in file_paths:

        for record in load_yaml_file(path):
            name = record.get("name")
            if name:

                if name in seen_names and not disable_error_messages:
                        print(f"\033[91mERROR: \"{name}\" is a duplicate. Duplicated names are not allowed\033[00m")
                else:
                    seen_names.add(name)
                    records.append(record)

    return records

# #####################################################################################
# Latex Formatting
# #####################################################################################

def escape_latex(text):
    if not isinstance(text, str):
        text = str(text)
    return (
        text.replace("\\", "\\textbackslash{}").replace("&", "\\&").replace("%", " percent")
            .replace("_", "\\_").replace("#", "\\#").replace("{", "\\{").replace("}", "\\}")
            .replace("^", "\\^{}").replace("~", "\\~{}").replace("$", "\\$")
    )

def extract_cite_label(cite_entry: str) -> str:
    match = re.match(r'@\w+\{([^,]+),', cite_entry.strip())
    return match.group(1) if match else ""

# -------------------------------------------------------------------------------------
# Subsection
# -------------------------------------------------------------------------------------

def extract_cite_url(cite_entry: str) -> str:
    match = re.search(r'url\s*=\s*[{"]([^}"]+)[}"]', cite_entry)
    return match.group(1) if match else ""


# #####################################################################################
# Checking
# #####################################################################################


def unique_in_list(arr: list):
    seen = set()
    for item in arr:
        if item in seen:
            return True  # Duplicate found
        seen.add(item)
    return False  # No duplicates found

def check_unique_names(yaml_data: list[dict]) -> None:
    found = set()
    for entry in yaml_data:
        value = entry.get('name')
        if value in found:
            print(f"\033[91mERROR: {value} is a duplicate name\033[00m")
        found.add(value)

def check_unique_citations(yaml_data: list[dict]) -> None:
    found = set()
    for entry in yaml_data:
        value = str(entry.get('cite'))

        #Fix missing citations
        if value=="None":
            print(f"\033[91mERROR: The entry \033[33m{entry}\033[91m has a missing citation\033[00m")
            continue

        if value in found:
            print(f"\033[91mERROR: \033[33m{value}\033[91m is a duplicate citation\033[00m")
        found.add(value)

def check_unique_citation_labels(yaml_data: list[dict]) -> None:
    #Read label, not the entire citation
    found = set()
    for entry in yaml_data:
        value = entry.get('cite')

        #Handle nonexistent citations
        if value:
            if type(value)==list:
                label = extract_cite_label(value[0])
            else:
                label = extract_cite_label(str(value))
        else:
            continue

        if label in found:
            print(f"\033[91mERROR: {label} is a duplicate citation label\033[00m")
        found.add(label)

def validate_required_fields(yaml_data: list, required_fields: list[str] | None) -> None:
    if not required_fields:
        return  # No validation needed

    for i, entry in enumerate(yaml_data):
        if not isinstance(entry, dict):
            print(f"\033[93mWARNING: Entry #{i} is not a dictionary. Skipping.\033[00m")
            continue  # skip bad entry

        missing = []
        for field in required_fields:
            if field not in entry or entry[field] in [None, '', [], {}]:
                missing.append(field)

        if missing:
            name = entry.get("name", f"<entry #{i}>")
            print(f"\033[91mERROR: Entry '{name}' is missing required fields: {', '.join(missing)}\033[00m")


def check_yaml(file_paths: list[str], required_fields: list[str] | None = None) -> None:
    #Check if YAML files are syntactically correct
    for path in file_paths:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = yaml.safe_load(f)

        except Exception as e:
            print(e)
            sys.exit(1)
    #Check of required fields are there
    if required_fields:
        validate_required_fields(content, required_fields)
        # print(required_fields)

    #Check if all names of entries are unique
    contents = merge_yaml_files(file_paths)
    check_unique_names(contents)

    #Check if all citations are (string-wise) unique
    check_unique_citations(contents)

    #Check if all citation labels are unique
    check_unique_citation_labels(contents)


# #####################################################################################
# Get Bibtex
# #####################################################################################


def get_bibtex(cell_val: str, author_limit: int) -> str:
    """
    Returns a substring of `cell_val` containing a BibTeX string with `author_limit` displayed authors.
    If there is no BibTex string, returns the string "No citation found".

    If there are multiple BibTeX entries, the first entry is returned.

    Parameters:
        cell_val: string possibly containing a BibTeX entry
        author_limit: maximum number of author names to include before truncating with "et al." If not None, must be a positive integer
    Returns:
        BibTeX entry in `cell_val` or "None"
    """
    assert type(cell_val)==str, "cell value must be a string"
    assert type(author_limit)==int and author_limit>0, "author limit must be a positive integer"

    match = re.search(r'@(?:\w+)\s*\{', cell_val)
    if not match:
        return "No citation found"

    start = match.start()
    brace_count = 0
    end = start
    in_entry = False

    while end < len(cell_val):
        if cell_val[end] == '{':
            brace_count += 1
            in_entry = True
        elif cell_val[end] == '}':
            brace_count -= 1
            if brace_count == 0 and in_entry:
                end += 1
                break
        end += 1

    bibtex_entry = cell_val[start:end] if in_entry and brace_count == 0 else "Format Error"
    if bibtex_entry == "none":
        return "none"


    # Find the 'author' field
    author_match = re.search(r'author\s*=\s*\{([^}]*)\}', bibtex_entry, re.IGNORECASE)
    if not author_match:
        return bibtex_entry  # No author field found

    authors = author_match.group(1)

    # Split by 'and'
    authors_list = authors.split(' and ')

    # Recombine authors
    new_authors = authors_list[0]
    for a in range(1, min(len(authors_list), author_limit)):
        new_authors += (" and " + authors_list[a])
    
    #Append 'et al.' if needed
    if len(authors_list) > author_limit:
        new_authors += " et al."

    #Add authors to citation
    modified_bibtex = (bibtex_entry[:author_match.start(1)] +
                       new_authors +
                       bibtex_entry[author_match.end(1):])

    #Remove newlines
    modified_bibtex = modified_bibtex.replace("\n", " ")

    return modified_bibtex


# #####################################################################################
# File Writing
# #####################################################################################


def write_individual_md_pages(input_filepaths: list[str], output_dir: str, columns: list[tuple], 
                              author_trunc: int = MAX_AUTHOR_LIMIT, writing_ratings: bool = True) -> None:
    """
    Writes the contents of the YAML file(s) at `input_filepaths` to `output_dir`/md_pages.
    Each entry in the YAML files appears as a separate file.

    The files are indexed by `output_dir`/md_pages/index.md

    Parameters:
        input_filepaths: list of filepaths to the input YAML files
        output_dir: directory for output
        columns: which entries to include in the output MD files
        author_trunc: number of authors to include in the file's bibtex citation
        writing_ratings: whether to write the benchmark's ratings to the output files
    """
    assert type(author_trunc)==int and author_trunc>0, "author truncation amount must be positive"

    contents = merge_yaml_files(input_filepaths)
    os.makedirs(output_dir, exist_ok=True)
    index_path = os.path.join(output_dir, "index.md")

    with open(index_path, 'w', encoding='utf-8') as index_file:
        index_file.write("# Index of Benchmarks\n\n")
        for i, entry in enumerate(contents):
            entry_name = entry.get("name", f"entry_{i}")
            filename = sanitize_filename(entry_name) + ".md"
            filepath = os.path.join(output_dir, filename)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# {entry_name}\n\n")

                for col_name, _, col_display in columns:
                    val = entry.get(col_name, '')

                    if col_name == "cite" and isinstance(val, list):
                        f.write(f"**{col_display}**:\n\n")
                        for bibtex in val:
                            f.write("-\n")
                            try:
                                parser = bibtexparser.bparser.BibTexParser(common_strings=True)
                                db = bibtexparser.loads(bibtex, parser=parser)
                                if db.entries:
                                    bib = db.entries[0]
                                    f.write(f"  - type: {bib.get('ENTRYTYPE', '')}\n")
                                    f.write(f"  - id: {bib.get('ID', '')}\n")
                                    for key, value in bib.items():
                                        if key in ('ENTRYTYPE', 'ID'):
                                            continue
                                        if key == 'author' and author_trunc:
                                            authors = [a.strip() for a in value.replace('\n', ' ').split(' and ')]
                                            if len(authors) > author_trunc:
                                                authors = authors[:author_trunc] + ['et al.']
                                            value = ', '.join(authors)
                                        f.write(f"  - {key}: {value}\n")
                            except Exception as e:
                                f.write(f"  - parsing_error: {str(e)}\n")
                            f.write("  - bibtex: |\n")
                            for raw_line in bibtex.strip().splitlines():
                                f.write(f"      {raw_line}\n")
                        f.write("\n")


                    #Handle special case for ratings
                    elif col_name == "ratings":
                        if writing_ratings:
                            #`val` should be a list of dictionaries of the same length as RATINGS_COLUMNS
                            for i in range(len(val)):
                                ratings_col_display = RATINGS_COLUMNS[i][2]
                                ratings_val_str = str(val[i].get(RATINGS_COLUMNS[i][0], ""))

                                ratings_val_str = ratings_val_str.replace("\n", " ").replace("['", "").replace("']", "")
                                ratings_val_str = ratings_val_str.replace("', '", ", ").replace("','", ", ").replace("[]", "")
                                ratings_val_str = ratings_val_str.replace("[", " ").replace("]", " ").replace("(", " ").replace(")", " ")

                                f.write(f"**{ratings_col_display}**: {ratings_val_str}\n\n")
                    
                    #Proceed normally if not writing ratings
                    else:
                        val_str = str(val).replace("\n", " ").replace("['", "").replace("']", "")
                        val_str = val_str.replace("', '", ", ").replace("','", ", ").replace("[]", "")
                        val_str = val_str.replace("[", " ").replace("]", " ").replace("(", " ").replace(")", " ")
                        f.write(f"**{col_display}**: {val_str}\n\n")


            index_file.write(f"- [{entry_name}]({filename})\n")



def write_md_table(input_filepaths: list[str], output_dir: str, columns: list[tuple], 
                   author_limit: int = MAX_AUTHOR_LIMIT, writing_ratings: bool = True) -> None:
    """
    Writes the contents of the YAML file(s) at `input_filepaths` to `output_dir`/md_pages.
    All entries in the YAML files appear in a single merged table.

    Parameters:
        input_filepaths: list of filepaths to the input YAML files
        output_dir: directory for output
        columns: which entries to include in the output MD files
        author_trunc: number of authors to include in the file's bibtex citation
        writing_ratings: whether to write the benchmark's ratings to the output files
    """

    contents = merge_yaml_files(input_filepaths)
    verify_checked_columns(contents)

    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "benchmarks.md"), 'w', encoding='utf-8') as md_file:
        headers = [col[2] for col in columns]
        #The "ratings" header is a dummy header

        headers.remove(ALL_COLUMNS[-1][2]) #This is the header for "ratings"

        #If writing the ratings, replace the "ratings" column with the 5 criteria and their accompanying descriptions
        if writing_ratings:
            for rc in RATINGS_COLUMNS:
                headers.append(rc[2])

        md_file.write('| ' + ' | '.join(headers) + ' |\n')
        md_file.write('| ' + ' | '.join(['---'] * len(headers)) + ' |\n')
        for row in contents:

            current_article_name = row.get("name", "")
            current_url = row.get("url", "")
            row_cells = []
            for col_name, _, _ in columns:
                val = row.get(col_name, '')
                if col_name == "cite":
                    if isinstance(current_url, list):
                        val = current_article_name + " " + " ".join(f"[(Link {i+1})]({url})" for i, url in enumerate(current_url))
                    else:
                        val = f"[{current_article_name}]({current_url})"
                elif col_name == "full_cite":
                    if isinstance(row.get("cite", ''), list):
                        val = get_bibtex(row.get("cite", '')[0], author_limit)
                    else:
                        val = get_bibtex(row.get("cite", ''), author_limit)

                else:
                    val = str(val).replace("\n", " ").replace("['", "").replace("']", "")
                    val = val.replace("', '", ", ").replace("','", ", ").replace("[]", "")
                    val = val.replace("[", " ").replace("]", " ").replace("(", " ").replace(")", " ")

                if not col_name=="ratings":
                    row_cells.append(val)

            if row.get("ratings") and writing_ratings:
                ratings_list = row.get("ratings", [])
                ratings_dict = {list(item.keys())[0]: list(item.values())[0] for item in ratings_list if isinstance(item, dict)}
                
                if isinstance(ratings_dict, dict):
                    for rating_col, _, _ in RATINGS_COLUMNS:
                        val = ratings_dict.get(rating_col, "")
                        if val != "":
                            row_cells.append(str(val))
                            
            md_file.write('| ' + ' | '.join(row_cells) + ' |\n')


def generate_bibtex(input_filepaths: list[str], output_dir: str) -> None:
    """
    Combines the entries in `input_filepaths` and writes a BibTeX bibliography to `output_dir`/benchmarks.bib.
    Prints any error messages to the standard output.
    """
  
    os.makedirs(output_dir, exist_ok=True)
    entries = []
    found_labels = set()
    found_entries = set()
    found_names = set()

    records = merge_yaml_files(input_filepaths, disable_error_messages=True)
    for record in records:

        #Extract citations
        record_cite_entries = record.get("cite", [])
        name = record.get("name", [])

        if name and record_cite_entries:
            current_cite_entry = record_cite_entries[0]

            #Check for error: When citation label in the citation is the same as another with another entry
            if extract_cite_label(current_cite_entry.lower()) in found_labels:
                print(f"\033[91mERROR: Entry with name \"{name}\" has the duplicate citation label \"{extract_cite_label(current_cite_entry)}\" (case-insensitive) \033[00m")

            #Check for error: Cite in different entry is the same, but recorded under a different name in the YAML file
            elif (str(current_cite_entry) in found_entries) and (name in found_names):
                pass
                #This error condition was checked in `merge_yaml_files`

            #All checks passed- OK to write
            else:
                found_entries.add(str(current_cite_entry))
                found_labels.add(extract_cite_label(current_cite_entry.lower()))
                found_names.add(name)

                entries.extend(record_cite_entries)

    with open(os.path.join(output_dir, "benchmarks.bib"), 'w', encoding='utf-8') as bib_file:
        for entry in entries:
            bib_file.write(entry.strip() + "\n\n")


def write_individual_latex_tables(input_filepaths: list[str], output_dir: str, columns: list[tuple], author_limit: int | None = 10) -> None:
    """
    Writes each benchmark entry as its own LaTeX table in separate .tex files.

    THIS FUNCTION DOES NOT PRINT ERRORS WHEN RECEIVING DUPLICATE ENTRIES.
    """

    os.makedirs(output_dir, exist_ok=True)
    entries = merge_yaml_files(input_filepaths, disable_error_messages=True)

    for i, entry in enumerate(entries):
        entry_name = entry.get("name", f"entry_{i}")
        filename = sanitize_filename(entry_name) + ".tex"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("\\begin{table}[h!]\n\\centering\n")
            f.write("\\begin{tabular}{|l|p{10cm}|}\n\\hline\n")

            for col_name, _, col_display in columns:
                val = entry.get(col_name, '')
                if col_name == "cite":
                    cite_keys = [extract_cite_label(c) for c in val] if isinstance(val, list) else []
                    url = extract_cite_url(val[0]) if isinstance(val, list) and val else ""
                    citation_str = (f"\\cite{{{', '.join(cite_keys)}}}" if cite_keys else "") + (
                        f" \\href{{{url}}}{{$\\Rightarrow$ }}" if url else "")
                    val = citation_str
                elif isinstance(val, list):
                    val = escape_latex(", ".join(map(str, val)))
                else:
                    val = escape_latex(val)

                f.write(f"\\textbf{{{escape_latex(col_display)}}} & {val} \\\\ \\hline\n")

            f.write("\\end{tabular}\n\\end{table}\n")


def write_latex(input_filepaths: list[str], output_filepath: str, columns: list[tuple], standalone: bool = False, author_limit: int = None) -> None:
    os.makedirs(output_filepath, exist_ok=True)

    output_tex_path = os.path.join(output_filepath, f"benchmarks.tex")

    with open(output_tex_path, 'w', encoding='utf-8') as f:
        records = merge_yaml_files(input_filepaths, disable_error_messages=True)

        verify_checked_columns(records)

        if standalone:
            f.write(textwrap.dedent(r"""
                \documentclass{article}
                \usepackage{hyperref}
                \usepackage[margin=1in]{geometry}
                \usepackage{pdflscape}
                \usepackage{wasysym}
                \usepackage{longtable}
                \usepackage[style=ieee, url=true]{biblatex}
                \addbibresource{benchmarks.bib}
                \begin{document}
            """))
        f.write("\\begin{landscape}\n{\\footnotesize\n")
        f.write(f"\\begin{{longtable}}{{|{'|'.join([f'p{{{col[1]}}}' for col in columns])}|}}\n\\hline\n")
        f.write(" & ".join([f"{{\\bf {col[2]}}}" for col in columns]) + " \\\\ \\hline\n\\endfirsthead\n")
        f.write("\\hline\n" + " & ".join([f"{{\\bf {col[2]}}}" for col in columns]) + " \\\\ \\hline\n\\endhead\n")
        f.write("\\hline\n\\multicolumn{" + str(len(columns)) + "}{r}{Continued on next page} \\\\\n\\endfoot\n\\hline\n\\endlastfoot\n")
        for record in records:
            cite_keys = [extract_cite_label(c) for c in record.get("cite", []) if c]
            cite_urls = [extract_cite_url(c) for c in record.get("cite", []) if c]
            primary_url = cite_urls[0] if cite_urls else record.get("url", "")
            row = []
            for col_name, _, _ in columns:
                val = record.get(col_name, '')
                if col_name == "cite":
                    val = (f"\\cite{{{', '.join(cite_keys)}}}" if cite_keys else "") + (f" \\href{{{primary_url}}}{{$\\Rightarrow$ }}" if primary_url else "")
                elif col_name == "url":
                    val = ""
                elif isinstance(val, list):
                    if author_limit is not None and col_name == "authors":
                        val = ", ".join(escape_latex(v) for v in val[:author_limit])
                        if len(val) > author_limit:
                            val += ", et al."
                    else:
                        val = ", ".join(escape_latex(v) for v in val)
                else:
                    val = escape_latex(val)
                row.append(val)
            f.write(" & ".join(row) + " \\\\ \\hline\n")
        f.write("\\end{longtable}\n}\n\\end{landscape}\n")
        if standalone:
            f.write("\\printbibliography\n\\end{document}\n")

    generate_bibtex(input_filepaths, output_filepath)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process YAML benchmark files to Markdown or LaTeX.")
    parser.add_argument('--files', '-i', type=str, nargs='+', required=True, help='YAML file paths to process.')
    parser.add_argument('--format', '-f', type=str, choices=['md', 'tex'], required=True, help="Output file format: 'md' or 'tex'")
    parser.add_argument('--outdir', '-o', type=str, default='../content/', required=True, help="Output directory")
    parser.add_argument('--authortruncation', type=int, default=MAX_AUTHOR_LIMIT, help="Truncate authors for index pages")
    parser.add_argument('--columns', type=lambda s: s.split(','), help="Subset of columns to include")
    parser.add_argument('--check', action='store_true', help="Conduct formatting checks on inputted YAML files. Does not produce an output file.")
    parser.add_argument('--index', action='store_true', help="Generate individual pages for each entry for the given format. If format is MD, generates an index.md file")
    parser.add_argument('--noratings', action='store_true', help="Removes rating columns from the output file")
    parser.add_argument('--required', action='store_true',help="Makes all the columns required that are listed in the --columns command")
    parser.add_argument('--standalone', '-s', action='store_true', help="Include full LaTeX document preamble.")
    parser.add_argument('--withcitation', action='store_true', help="Include a row for BibTeX citations. Works only with Markdown format")

    args = parser.parse_args()

    

    if args.standalone and args.format != 'tex':
        parser.error("--standalone is only valid with --format tex")
    if args.withcitation and args.format != "md":
        parser.error("--withcitation is only valid with --format md")
    
    if args.authortruncation<=0:
        parser.error("author truncation amount must be a positive integer")


    for file in args.files:
        if not os.path.exists(file):
            parser.error(f"The file {file} does not exist")

    os.makedirs(args.outdir, exist_ok=True)
    columns = get_column_triples(args.columns) if args.columns else ALL_COLUMNS


    # Required fields in YAML file
    if args.required:
        # --required is explicitly provided, so make all columns required
        required_fields = args.columns
        check_yaml(args.files, required_fields=required_fields )
    else:
        required_fields = None  # No required fields

    if args.check:
        check_yaml(args.files, required_fields=required_fields)
        sys.exit(0)

    if args.withcitation:
        columns.append(FULL_CITE_COLUMN)
    
    if args.format == 'md':
        if args.index:
            write_individual_md_pages(args.files, os.path.join(args.outdir, "md_pages"), columns, 
                                      author_trunc=args.authortruncation, writing_ratings=(not args.noratings))

        write_md_table(args.files, os.path.join(args.outdir, "md_pages"), columns, 
                       author_limit=args.authortruncation, writing_ratings=(not args.noratings))

    elif args.format == 'tex':
        if args.index:
            write_individual_latex_tables(args.files, os.path.join(args.outdir, "tex_pages"), columns, author_limit=args.authortruncation)
        write_latex(args.files, os.path.join(args.outdir, "tex"), columns, standalone=args.standalone, author_limit=args.authortruncation)