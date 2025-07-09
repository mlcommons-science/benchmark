import os
import re
import textwrap

class LatexWriter:
    """
    A class to generate LaTeX tables from structured data (e.g., dictionaries).
    This class can handle citation and URL formatting, LaTeX escape characters, 
    and multiple LaTeX files.
    """

    def __init__(self):
        """
        Initializes a LatexWriter instance
        """
        pass


    # -------------------------------------------------------------------------------------------
    # PRIVATE HELPERS
    # -------------------------------------------------------------------------------------------

    def _escape_latex(self, text):
        """
        Returns a LaTeX-safe copy of `text`. Special characters are replaced with the proper LaTeX escape sequences.

        Parameters:
            text (str): input text to replace

        Returns:
            str: LaTeX-safe version of the input text
        """
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
    
    def _extract_cite_label(self, cite_entry: str) -> str:
        """
        Extracts the citation label from a BibTeX citation entry string

        Parameters:
            cite_entry (str): The citation entry in BibTeX format

        Returns:
            str: The citation label extracted from the entry, or an empty string if not found.
        """
        match = re.match(r'@\w+\{([^,]+),', cite_entry.strip())
        return match.group(1) if match else ""
    
    def _extract_cite_url(self, cite_entry: str) -> str:
        """
        Extracts the URL from a BibTeX citation entry string, if present.

        Parameters:
            cite_entry (str): The citation entry in BibTeX format.

        Returns:
            str: The URL extracted from the entry, or an empty string if not found.
        """
        match = re.search(r'url\s*=\s*[{"]([^}"]+)[}"]', cite_entry)
        return match.group(1) if match else ""
    
    def _sanitize_filename(self, name: str) -> str:
        """
        Returns a copy of `name` without non-printing characters, spaces, or non-ASCII characters.

        Parameters:
            name (str): The original name to sanitize

        Returns:
            str: sanitized filename
        """
        output = "".join(ch for ch in name if 32 <= ord(ch) <= 126)
        output = re.sub(r' {2,}', ' ', output)
        output = output.strip().replace("(", "").replace(")", "").replace(" ", "_")
        return output
    

    # -------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # -------------------------------------------------------------------------------------------

    def write_latex_for_entry(self, entry: dict, output_dir: str, columns: list[tuple], author_limit: int = 999):
        """
        Generates a LaTeX table for `entry` at `output_dir`/tex/benchmarks.tex.

        Parameters:
            entry (dict): A dictionary containing the entry data.
            output_dir (str): The directory where the LaTeX file should be saved.
            columns (list): A list of tuples representing columns (name, width, display name).
            author_limit (int, optional): The maximum number of authors to display (default is 999).
        """
        os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists
        entry_name = entry.get("name", "entry")  # Default to 'entry' if no name is provided
        filename = self._sanitize_filename(entry_name) + ".tex"  # Sanitize and create filename
        filepath = os.path.join(output_dir, filename)

        # Open the file for writing LaTeX content
        with open(filepath, 'w', encoding='utf-8') as f:
            # Begin the table structure
            f.write("\\begin{table}[h!]\n\\centering\n")
            f.write("\\begin{tabular}{|l|p{10cm}|}\n\\hline\n")

            # Loop over the columns and write each column's content
            for col_name, _, col_display in columns:
                val = entry.get(col_name, '')  # Get the value for the column from the entry
                if col_name == "cite":  # Handle citations and URLs
                    cite_keys = [self._extract_cite_label(c) for c in val] if isinstance(val, list) else []
                    url = self._extract_cite_url(val[0]) if isinstance(val, list) and val else ""
                    val = (f"\\cite{{{', '.join(cite_keys)}}}" if cite_keys else "") + (
                        f" \\href{{{url}}}{{$\\Rightarrow$ }}" if url else "")
                elif isinstance(val, list):  # Handle list values (e.g., multiple authors)
                    val = self._escape_latex(", ".join(map(str, val)))
                else:
                    val = self._escape_latex(val)  # Escape non-list values

                f.write(f"\\textbf{{{self._escape_latex(col_display)}}} & {val} \\\\ \\hline\n")

            f.write("\\end{tabular}\n\\end{table}\n")


    def write_latex_for_all(self, entries: list[dict], output_path: str, columns: list[tuple], standalone: bool = True, author_limit: int = 999):
        """
        Writes a LaTeX table containing `entries` at `output_path`/tex/benchmarks.tex.

        Parameters:
            entries (list): A list of dictionaries, each representing an entry.
            output_path (str): The path where the LaTeX file should be saved.
            columns (list): A list of tuples representing columns (name, width, display name).
            standalone (bool, optional): Whether to generate a full document (default is True).
            author_limit (int, optional): The maximum number of authors to display (default is 999).
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)  # Ensure the output directory exists

        # Open the file for writing LaTeX content
        with open(output_path, 'w', encoding='utf-8') as f:
            # If standalone, add the document preamble
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

            # Write each entry as a row in the LaTeX table
            for entry in entries:
                row = []
                cite_keys = [self._extract_cite_label(c) for c in entry.get("cite", []) if c]
                cite_urls = [self._extract_cite_url(c) for c in entry.get("cite", []) if c]
                primary_url = cite_urls[0] if cite_urls else entry.get("url", "")

                for col_name, _, _ in columns:
                    val = entry.get(col_name, '')  # Get the column value from the entry
                    if col_name == "cite":
                        val = (f"\\cite{{{', '.join(cite_keys)}}}" if cite_keys else "") + (
                            f" \\href{{{primary_url}}}{{$\\Rightarrow$ }}" if primary_url else "")
                    elif col_name == "url":
                        val = ""
                    elif isinstance(val, list):
                        val = ", ".join(self._escape_latex(str(v)) for v in val)
                    else:
                        val = self._escape_latex(str(val))
                    row.append(val)

                f.write(" & ".join(row) + " \\\\ \\hline\n")

            f.write("\\end{longtable}\n}\n\\end{landscape}\n")
            if standalone:
                f.write("\\printbibliography\n\\end{document}\n")
