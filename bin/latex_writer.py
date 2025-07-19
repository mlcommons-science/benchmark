import os
import re
import sys
import textwrap
from typing import List, Dict, Union, Any

from pybtex.database import parse_string
from pybtex.plugin import find_plugin
from pylatexenc.latexencode import unicode_to_latex
from cloudmesh.common.console import Console

# --- Constants ---

LATEX_PREFIX = textwrap.dedent(r"""
    \documentclass{article}
    \usepackage[margin=1in]{geometry}
    \usepackage{hyperref}
    \usepackage{amsmath}
    \usepackage{pdflscape}
    \usepackage{wasysym}
    \usepackage{longtable}
    \usepackage[style=ieee, url=true]{biblatex}
    \addbibresource{benchmarks.bib}
    \begin{document}
""")

LATEX_POSTFIX = textwrap.dedent(r"""
    \printbibliography
    \end{document}
""")

# Define all columns with their properties for clarity and consistency
ALL_COLUMNS: Dict[str, Dict[str, Union[str, float]]] = {
    "date": {"width": "1.5cm", "label": "Date"},
    "expired": {"width": "1cm", "label": "Expired"},
    "valid": {"width": "0.7cm", "label": "Valid"},
    "name": {"width": "2.5cm", "label": "Name"},
    "url": {"width": "0.7cm", "label": "URL"},
    "domain": {"width": "2cm", "label": "Domain"},
    "focus": {"width": "2cm", "label": "Focus"},
    "keywords": {"width": "2.5cm", "label": "Keywords"},
    "description": {"width": "4cm", "label": "Description"},
    "task_types": {"width": "3cm", "label": "Task Types"},
    "ai_capability_measured": {"width": "3cm", "label": "AI Capability"},
    "metrics": {"width": "2cm", "label": "Metrics"},
    "models": {"width": "2cm", "label": "Models"},
    "notes": {"width": "3cm", "label": "Notes"},
    "cite": {"width": "1cm", "label": "Citation"},
    "ratings.specification.rating": {"width": "1cm", "label": "Specification Rating"},
    "ratings.specification.reason": {"width": "3cm", "label": "Specification Reason"},
    "ratings.dataset.rating": {"width": "1cm", "label": "Dataset Rating"},
    "ratings.dataset.reason": {"width": "3cm", "label": "Dataset Reason"},
    "ratings.metrics.rating": {"width": "1cm", "label": "Metrics Rating"},
    "ratings.metrics.reason": {"width": "3cm", "label": "Metrics Reason"},
    "ratings.reference_solution.rating": {"width": "1cm", "label": "Reference Solution Rating"},
    "ratings.reference_solution.reason": {"width": "3cm", "label": "Reference Solution Reason"},
    "ratings.documentation.rating": {"width": "1cm", "label": "Documentation Rating"},
    "ratings.documentation.reason": {"width": "3cm", "label": "Documentation Reason"},
}

# --- Utility Functions ---

def has_capital_letter(text_to_check: str) -> bool:
    """
    Checks if the given text contains at least one capital letter.

    Args:
        text_to_check (str): The input text.

    Returns:
        bool: True if the text contains a capital letter, False otherwise.
    """
    return any(char.isupper() for char in text_to_check)

def escape_latex(text: Any) -> str:
    """
    Returns `text` converted to LaTeX-safe representation using pylatexenc.

    Parameters:
        text (Any): Text to convert to LaTeX. Can be non-string.
    Returns:
        TeX-friendly version of `text`.
    """
    if not isinstance(text, str):
        text = str(text)
    return unicode_to_latex(text, non_ascii_only=False)

def sanitize_filename(name: str) -> str:
    """
    Returns a lowercased version of `name` suitable for a filename,
    replacing spaces with hyphens and removing invalid characters.

    Parameters:
        name (str): filename to sanitize.
    Returns:
        Sanitized filename.
    """
    # Remove characters not typically allowed in filenames
    output = re.sub(r'[^\w\s.-]', '', name)
    # Replace sequences of spaces with a single hyphen
    output = re.sub(r'\s+', '-', output)
    # Remove leading/trailing hyphens and convert to lowercase
    output = output.strip('-').lower()
    return output

# --- BibtexWriter Class ---

class BibtexWriter:
    """
    Class to write BibTeX citations to a file.
    """

    def __init__(self, entries: List[Dict]):
        """
        Creates a BibtexWriter with entries from a table.

        Args:
            entries (List[Dict]): A list of dictionaries, each representing a benchmark entry.
        """
        self.entries = entries

    @staticmethod
    def _get_citation_label(bib_entry: str) -> str:
        """
        Extracts the citation label from a BibTeX entry string.

        Args:
            bib_entry (str): BibTeX citation string (e.g., "@article{label, ...}").

        Returns:
            str: The extracted citation label, or "<unknown>" if not found.
        """
        match = re.match(r"@\w+\{([^,]+),", bib_entry.strip())
        return match.group(1) if match else "<unknown>"

    @staticmethod
    def _extract_cite_url(cite_entry: str) -> str:
        """
        Extracts the URL from the given BibTeX citation entry.
        
        Parameters:
            cite_entry (str): BibTeX entry to extract URL from.
        Returns:
            str: Citation's URL, or an empty string if not found.
        """
        match = re.search(r'url\s*=\s*[{"]([^}"]+)[}"]', cite_entry)
        return match.group(1) if match else ""

    def write(self, output_dir: str, filename: str = "benchmarks.bib") -> None:
        """
        Writes the writer's stored contents to `output_dir`/`filename`.
        Validates BibTeX entries before writing.

        Parameters:
            output_dir (str): Output directory to write to.
            filename (str): Filename to write to, placed inside of `output_dir`.
        """
        os.makedirs(output_dir, exist_ok=True)
        bib_entries_to_write = []
        found_labels = set()
        fatal_errors = False

        for record in self.entries:
            record_cite_entries = record.get("cite", [])
            name = record.get("name", record.get("id", "UNKNOWN_ENTRY"))

            if isinstance(record_cite_entries, str):
                record_cite_entries = [record_cite_entries]
            elif not isinstance(record_cite_entries, list):
                continue # Skip if 'cite' field is not a string or list

            for cite_entry_raw in record_cite_entries:


                
                if not isinstance(cite_entry_raw, str) or not cite_entry_raw.strip().startswith("@"):
                    Console.warning(f"Skipping malformed citation entry in '{name}': '{cite_entry_raw}'")
                    continue

                cite_entry = cite_entry_raw.strip()
                label = self._get_citation_label(cite_entry)

                match = re.search(r'author\s*=\s*{(.+?)}', cite_entry_raw, re.DOTALL)
                if match:
                    authors_raw = match.group(1)
                    authors = [a.strip() for a in authors_raw.split(" and ")]
                    
                    if "others" in authors:
                        Console.error(f"Entry '{name}' contains a citation '{label}' that includes others'. Please use full author names.")   
        

                if has_capital_letter(label):
                    Console.error(f"Citation label \"{label}\" in entry \"{name}\" is capitalized. Labels should be lowercase.")
                    fatal_errors = True
                if re.search(r'[\s\n\t]', label):
                    Console.error(f"Citation label \"{label}\" in entry \"{name}\" contains whitespace. Labels should not contain spaces, newlines, or tabs.")
                    fatal_errors = True
                
                if label in found_labels:
                    Console.error(f"Duplicate citation label \"{label}\" found. All labels must be unique.")
                    fatal_errors = True
                else:
                    found_labels.add(label)
                    bib_entries_to_write.append(cite_entry)

        if fatal_errors:
            print()
            Console.error("BibTeX entries contain errors. Please fix them to proceed.")
            print()
            sys.exit(1)

        bib_path = os.path.join(output_dir, filename)
        try:
            with open(bib_path, "w", encoding="utf-8") as f:
                f.write("\n\n".join(bib_entries_to_write))
            Console.ok(f"Successfully wrote BibTeX file to: {bib_path}")
        except IOError as e:
            Console.error(f"Error writing BibTeX file to {bib_path}: {e}")
            sys.exit(1)


# --- LatexWriter Class ---

class LatexWriter:
    """Class to write formatted YAML contents to a LaTeX file."""

    def __init__(self, entries: List[Dict]):
        """
        Creates a new converter that writes `entries` to LaTeX files.

        Parameters:
            entries (List[Dict]): List of benchmark entries, where each entry is a dictionary.
        """
        self._entries = entries
        self._bib_writer = BibtexWriter(entries)
        self._latex_filename_map: Dict[str, str] = {}
        self._create_latex_filenames()

    def _create_latex_filenames(self) -> None:
        """
        Generates a LaTeX filename for each entry and stores it internally.
        """
        for entry in self._entries:
            name = entry.get("id", entry.get("name", "unknown"))
            entry["_tex_filename"] = sanitize_filename(name) + ".tex"
            self._latex_filename_map[entry.get("id", name)] = entry["_tex_filename"]


    def _entry_to_row(self, row_dict: Dict, selected_columns: List[str]) -> str:
        """
        Returns a string containing `row_dict` converted to one row of the TeX table.
        This function handles one row at a time.

        Each entry in the row is separated by ' & '. The row ends with "\\\\ \\hline".
        There is no newline at the very end of the string.

        Parameters:
            row_dict (Dict): Dictionary representing the row contents, whose keys are column names
                             and associated values are contents of the column.
            selected_columns (List[str]): List of column names to include in this row.
        Returns:
            str: A single row of the TeX table.
        """
        row_contents_list = []

        for col_name in selected_columns:
            value = row_dict.get(col_name)

            field_value = ""
            if value is None:
                field_value = "" # Empty string for None values
            elif col_name == "cite":
                cite_entries = value if isinstance(value, list) else [value] if isinstance(value, str) else []
                cite_keys = [BibtexWriter._get_citation_label(c) for c in cite_entries if c and c.strip().startswith("@")]
                primary_url = row_dict.get("url", "")
                
                # Try to get URL from the first citation entry if available
                if not primary_url and cite_entries:
                    first_cite_url = BibtexWriter._extract_cite_url(cite_entries[0])
                    if first_cite_url:
                        primary_url = first_cite_url


                cite_text = f"\\cite{{{','.join(cite_keys)}}}" if cite_keys else ""

                print("ZZZ", cite_text)

                url_text = f"\\href{{{escape_latex(primary_url)}}}{{$\\Rightarrow$}}" if primary_url else ""
                field_value = f"{cite_text}{url_text}"
            elif col_name == "url":
                field_value = f"\\href{{{escape_latex(value)}}}{{link}}" if value else ""
            elif isinstance(value, list):
                field_value = ", ".join(escape_latex(item) for item in value)
            else:
                field_value = escape_latex(value)
            
            row_contents_list.append(field_value)
        
        return " & ".join(row_contents_list) + r" \\ \hline"


    def _generate_latex_table_content(self, rows: List[str], 
                                      selected_columns: List[str], 
                                      column_titles: List[str], 
                                      column_widths: List[Union[float, int]] | None = None) -> str:
        """
        Generates the core LaTeX table environment content (excluding document preamble/postfix).

        Parameters:
            rows (List[str]): Formatted table rows, each ending with `\\ \\hline`.
            selected_columns (List[str]): List of column names (keys in `ALL_COLUMNS`) to include.
            column_titles (List[str]): Display titles for the selected columns.
            column_widths (List[Union[float, int]] | None): Widths for each column in cm.
                                                             If None, defaults to 2cm per column.
        Returns:
            str: LaTeX code for the table environment.
        """
        # Column width string for LaTeX longtable environment
        column_width_str = "{|"
        if column_widths is None:
            column_width_str += "|".join([f"p{{2cm}}" for _ in selected_columns])
        else:
            for w in column_widths:
                if not isinstance(w, (int, float)) or w <= 0:
                    Console.error(f"Invalid column width: {w}. Widths must be positive numbers.")
                    sys.exit(1)
                column_width_str += f"|p{{{round(w, 5)}cm}}"
        column_width_str += "|}"

        # Column names header for LaTeX table
        column_names_header_parts = []
        for title in column_titles:
            column_names_header_parts.append(f"\\textbf{{{escape_latex(title)}}}")
        column_names_header = " & ".join(column_names_header_parts) + r" \\ \hline"

        # Constructing the table content
        table_content = textwrap.dedent(rf"""
            \begin{{longtable}}{column_width_str}
            \hline
            {column_names_header}
            \endfirsthead
            \hline
            {column_names_header}
            \endhead
            \hline
            \multicolumn{{{len(selected_columns)}}}{{r}}{{Continued on next page}} \\
            \endfoot
            \hline
            \endlastfoot
        """) + "\n".join(rows) + textwrap.dedent(r"""
            \end{longtable}
        """)
        return table_content

    def write_table(self, 
                    output_path: str, 
                    selected_columns_keys: List[str], 
                    column_titles: List[str] | None = None, 
                    column_widths: List[Union[float, int]] | None = None) -> None:
        """
        Writes all entries stored by this writer into one LaTeX document at
        `output_path`/tex/benchmarks.tex. Also generates the BibTeX file.

        Parameters:
            output_path (str): Base directory for output.
            selected_columns_keys (List[str]): List of column keys (from ALL_COLUMNS) to include.
            column_titles (List[str] | None): Optional display titles for the columns.
                                              If None, titles are derived from `ALL_COLUMNS`.
            column_widths (List[Union[float, int]] | None): Optional widths for each column in cm.
                                                             If None, defaults to 2cm per column.
        """
        if not selected_columns_keys:
            Console.warning("No columns selected for the table. Skipping table generation.")
            return

        # Validate and prepare column information
        if column_titles:
            if len(column_titles) != len(selected_columns_keys):
                Console.error(f"Mismatch: {len(selected_columns_keys)} columns selected, but {len(column_titles)} titles provided.")
                sys.exit(1)
        else:
            column_titles = [ALL_COLUMNS.get(key, {"label": key.replace('_', ' ').title()})["label"] for key in selected_columns_keys]

        if column_widths:
            if len(column_widths) != len(selected_columns_keys):
                Console.error(f"Mismatch: {len(selected_columns_keys)} columns selected, but {len(column_widths)} widths provided.")
                sys.exit(1)

        # Generate rows
        all_rows = [self._entry_to_row(entry, selected_columns_keys) for entry in self._entries]

        # Generate the main LaTeX table content
        table_latex = self._generate_latex_table_content(
            all_rows, selected_columns_keys, column_titles, column_widths
        )
        
        # Assemble the full LaTeX document
        full_latex_doc = LATEX_PREFIX + r"\begin{landscape}" + r"\footnotesize" + table_latex + r"\end{landscape}" + LATEX_POSTFIX

        # Ensure output directory exists and write the file
        tex_output_dir = os.path.join(output_path, "tex")
        os.makedirs(tex_output_dir, exist_ok=True)
        filepath = os.path.join(tex_output_dir, "benchmarks.tex")
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(full_latex_doc)
            Console.ok(f"Successfully wrote main LaTeX table to: {filepath}")
        except IOError as e:
            Console.error(f"Error writing main LaTeX table to {filepath}: {e}")
            sys.exit(1)
        
        # Write BibTeX file
        self._bib_writer.write(tex_output_dir)

    def write_individual_entries(self, 
                                 output_path: str, 
                                 selected_columns_keys: List[str],
                                 column_titles: List[str] | None = None, 
                                 column_widths: List[Union[float, int]] | None = None) -> None: 
        """
        Writes each entry stored by this writer into a separate LaTeX document.
        All individual documents are placed in `output_path`/tex_pages.

        Parameters:
            output_path (str): Base directory for output.
            selected_columns_keys (List[str]): List of column keys (from ALL_COLUMNS) to include.
            column_titles (List[str] | None): Optional display titles for the columns.
                                              If None, titles are derived from `ALL_COLUMNS`.
            column_widths (List[Union[float, int]] | None): Optional widths for each column in cm.
                                                             If None, defaults to 2cm per column.
        """
        if not selected_columns_keys:
            Console.warning("No columns selected for individual entries. Skipping generation.")
            return

        # Validate and prepare column information
        if column_titles:
            if len(column_titles) != len(selected_columns_keys):
                Console.error(f"Mismatch: {len(selected_columns_keys)} columns selected, but {len(column_titles)} titles provided for individual entries.")
                sys.exit(1)
        else:
            column_titles = [ALL_COLUMNS.get(key, {"label": key.replace('_', ' ').title()})["label"] for key in selected_columns_keys]

        if column_widths:
            if len(column_widths) != len(selected_columns_keys):
                Console.error(f"Mismatch: {len(selected_columns_keys)} columns selected, but {len(column_widths)} widths provided for individual entries.")
                sys.exit(1)

        # Ensure output directory exists
        tex_pages_output_dir = os.path.join(output_path, "tex_pages")
        os.makedirs(tex_pages_output_dir, exist_ok=True)
        
        # Write BibTeX file for individual pages too, as they might reference it
        self._bib_writer.write(os.path.join(output_path, "tex")) # Use the same bib dir as main table

        for i, entry in enumerate(self._entries):
            # Generate row for the current entry
            single_row = self._entry_to_row(entry, selected_columns_keys)

            # Generate LaTeX content for this single-row table
            table_latex = self._generate_latex_table_content(
                [single_row], selected_columns_keys, column_titles, column_widths
            )
            
            # Assemble the full LaTeX document for this entry
            full_latex_doc = LATEX_PREFIX + table_latex + LATEX_POSTFIX

            # Determine filename
            entry_name = entry.get("name", entry.get("id", f"entry_{i+1}"))
            filename = sanitize_filename(entry_name) + ".tex"
            filepath = os.path.join(tex_pages_output_dir, filename)

            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(f"% LaTeX table for \"{entry_name}\"\n")
                    f.write(full_latex_doc)
                Console.ok(f"Successfully wrote individual LaTeX page for '{entry_name}' to: {filepath}")
            except IOError as e:
                Console.error(f"Error writing individual LaTeX page for '{entry_name}' to {filepath}: {e}")
                # Continue processing other entries, but log the error