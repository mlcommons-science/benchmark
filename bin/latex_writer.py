import os
import re
import textwrap
from pybtex.database import parse_string
from pybtex.plugin import find_plugin


_RED = "\033[91m"
"""ANSI escape code. Changes to printing in red"""

_DEFAULT_COLOR = "\033[00m"
"""ANSI escape code. Changes to printing in the default color"""



LATEX_PREFIX = textwrap.dedent(rf"""
    \documentclass{{article}}

    \usepackage[margin=1in]{{geometry}}
    \usepackage{{hyperref}}
    \usepackage{{pdflscape}}
    \usepackage{{wasysym}}
    \usepackage{{longtable}}
    \usepackage[style=ieee, url=true]{{biblatex}}
    \addbibresource{{benchmarks.bib}}

    \begin{{document}}

    """)
'''Header and preamble for LaTeX documents'''

LATEX_POSTFIX = textwrap.dedent(rf"""
    \end{{document}}
    """)
'''Footer for LaTeX documents'''






class BibtexWriter:
    def __init__(self, entries: list[dict]):
        self.entries = entries

    def _extract_cite_label(self, bib_entry: str) -> str:
        match = re.match(r"@\w+\{([^,]+),", bib_entry.strip())
        return match.group(1) if match else "<unknown>"

    def write(self, output_dir: str, filename: str = "benchmarks.bib") -> None:
        os.makedirs(output_dir, exist_ok=True)
        bib_entries = []
        found_labels = set()
        found_entries = set()
        found_names = set()

        for record in self.entries:
            record_cite_entries = record.get("cite", [])
            name = record.get("name", "UNKNOWN")

            if isinstance(record_cite_entries, str):
                record_cite_entries = [record_cite_entries]
            elif not isinstance(record_cite_entries, list):
                continue

            for cite_entry in record_cite_entries:
                if not isinstance(cite_entry, str) or not cite_entry.strip().startswith("@"):
                    continue

                label = self._extract_cite_label(cite_entry.lower())

                if label in found_labels:
                    print(f"{_RED}ERROR: Duplicate citation label \"{label}\" found in entry \"{name}\".{_DEFAULT_COLOR}")
                elif cite_entry in found_entries and name in found_names:
                    continue
                else:
                    found_labels.add(label)
                    found_entries.add(cite_entry)
                    found_names.add(name)
                    bib_entries.append(cite_entry.strip())

        bib_path = os.path.join(output_dir, filename)
        with open(bib_path, "w", encoding="utf-8") as f:
            f.write("\n\n".join(bib_entries))




class LatexWriter:
    """Class to write formatted YAML contents to a LaTeX file"""

    def __init__(self, entries: list[dict]):
        """
        Creates a new converter that writes `entries` to LaTeX files.

        Parameters:
            entries (list[dict]): list of benchmark entries, where each entry is a list of {key: value} dictionaries
        """
        self._entries = entries
        self._bib_writer = BibtexWriter(entries)


    def _sanitize_filename(self, name: str) -> str:
        """
        Returns a lowercased version of `name` without whitespace and leading/trailing spaces.

        Parameters:
            name (str): filename to sanitize
        Returns:
            sanitized filename
        """
        output = ""
        for ch in name:
            if 32<=ord(ch)<=126:
                output += ch

        output = re.sub(r' {2,}', ' ', output) #Replace 2+ spaces with single space
        output = output.strip().replace("(", "").replace(")", "").replace(" ", "_")

        return output.lower()



    def _escape_latex(self, text: str) -> str:
        """
        Returns `text`, where all TeX special characters are replaced with escape sequences.

        Parameters:
            text (str): text to convert to LaTeX
        Returns:
            TeX-friendly version of `text`
        """
        if not isinstance(text, str):
            text = str(text)
        return (
            text.replace("\\", "\\textbackslash{}")
                .replace("&", "\\&")
                .replace("%", "\\%")
                .replace("$", "\\$")
                .replace("#", "\\#")
                .replace("_", "\\_")
                .replace("{", "\\{")
                .replace("}", "\\}")
                .replace("~", "\\textasciitilde{}")
                .replace("^", "\\textasciicircum{}")
        )
    
    
 
    def _extract_cite_label(self, bib_entry: str) -> str:
        """
        Extracts the citation label from a BibTeX entry like '@article{label,...}'
        """
        match = re.match(r"@\w+\{([^,]+),", bib_entry.strip())
        return match.group(1) if match else "<unknown>"


    def _extract_cite_url(self, cite_entry: str) -> str:
        match = re.search(r'url\s*=\s*[{"]([^}"]+)[}"]', cite_entry)
        return match.group(1) if match else ""

    
    def _entry_to_row(self, row_dict: dict, columns: list[str]) -> str:
        """
        Returns a string containing `row_dict` converted to one row of the TeX table.

        This function handles one row at a time.

        Each entry in the row is separated by ' & '. The row ends with "\\\\ \\hline". There is no newline!

        Parameters:
            row_dict (dict): dictionary representing the row contents, whose keys are column names and associated values are contents of the column
            columns (list[str]): list of column names to include
        Returns:
            row of TeX table
        """

        row_contents = ""

        #loop through row
        for key, value in row_dict.items():
            #don't add "description" or "condition", or anything not in the selected columns
            if key in ("description", "condition") or (not key in columns):
                continue
            
            #format the field value
            field_value = (
                self._escape_latex(value)
                if not isinstance(value, list)
                else ", ".join(map(self._escape_latex, value))
            )

            #handle citations
            if key == "cite":   
                cite_keys = [self._extract_cite_label(c) for c in row_dict.get("cite", []) if c]
                cite_urls = [self._extract_cite_url(c) for c in row_dict.get("cite", []) if c]
                primary_url = cite_urls[0] if cite_urls else row_dict.get("url", "")
                field_value = (f"\\cite{{{', '.join(cite_keys)}}}" if cite_keys else "") + (f" \\href{{{primary_url}}}{{$\\Rightarrow$ }}" if primary_url else "")


            #add field to the row
            row_contents += f"{field_value} & "
        
        #Remove the last '& ' and add line end
        row_contents = row_contents[:-2]
        row_contents += "\\\\ \\hline"
        
        return row_contents



    def _generate_latex_doc(self, rows: list[str], selected_columns: list[str], 
                            column_names: list[str], column_widths: list[float | int] | None = None) -> str:
        """
        Returns a string representing a TeX table generated from `rows` and containing only `selected_columns`.

        Uses 2cm column widths for all columns if `column_widths` is None.

        Parameters:
            rows (list[str]): rows of table. Each index must be a valid row in a TeX table
            selected_columns (list[str]): columns in raw dict to include- any columns not in `selected_columns` will not appear in the table
            column_names (list[str]): names of columns to include. Must have the same length as `selected_columns`
            column_widths (list[float] or None): widths of each column in centimeters. If not None, length must be the same length as `selected_columns` and all indices must be positive
        Returns:
            TeX table string to be written to a file
        """
        #enforce type preconditions
        assert isinstance(rows, list), "rows must be a list of strings"
        assert isinstance(selected_columns, list), "selected columns must be a list of strings"
        #enforce length preconditions
        assert len(column_names)==len(selected_columns), f"length of selected columns ({len(selected_columns)}) must equal length of selected columns ({len(selected_columns)})"
        if column_widths != None:
            assert len(selected_columns)==len(column_widths), f"length of column widths ({len(column_widths)}) must equal length of selected columns ({len(selected_columns)})"
        
        #Column length header
        column_width_str = "{"

        if column_widths==None:
            #append 2cm column widths
            column_width_str += ("|p{2cm}" * len(selected_columns))
        else:
            #individually append all the column widths to the header
            for w in column_widths:
                assert w>0, "all column widths must be positive"
                column_width_str += "|p{" + str(round(w, 5)) + "cm}"

        column_width_str += "|}"


        #Column names
        column_names_header = ""
        col_number = 0
        for key, _ in self._entries[0].items():
            if (not key in selected_columns):
                continue
            column_names_header += "{\\bf " + self._escape_latex(column_names[col_number]) + "} & "
            col_number += 1

        column_names_header = column_names_header[:-2]
        column_names_header += "\\\\\\\\ \\hline"


        # Create a mapping: label -> formatted citation
        label_to_citation = {}
        style = find_plugin('pybtex.style.formatting', 'plain')()
        for record in self._bib_writer.entries:
            cites = record.get("cite", [])
            if isinstance(cites, str):
                cites = [cites]
            for entry in cites:
                if not entry.strip().startswith("@"):
                    continue
                try:
                    bib_data = parse_string(entry, "bibtex")
                    for e in bib_data.entries.values():
                        formatted = style.format_entries([e])
                        label_to_citation[list(bib_data.entries.keys())[0]] = next(formatted).text
                except Exception as e:
                    print(f"Warning: Failed to format citation for BibTeX: {e}")

        contents = ""
        footnotes = []
        footnote_refs = {}

        #Put each entry in the contents
        for entry in self._entries:

            #convert citations to list
            cites = entry.get("cite", [])
            if isinstance(cites, str):
                cites = [cites]

            for col in selected_columns:
                value = entry.get(col, '')

                #handle citations
                if col == "cite":
                    refs = []
                    for cite in cites:
                        label_match = self._bib_writer._extract_cite_label(cite)
                        if label_match not in footnote_refs:
                            footnote_refs[label_match] = len(footnotes) + 1
                            footnotes.append(label_to_citation.get(label_match, f"(Unparseable citation: {label_match})"))
                        refs.append(f"[^{footnote_refs[label_match]}]")
                    joined_refs = self._escape_latex(", ".join(refs))
                    contents += joined_refs

                elif isinstance(value, list):
                    contents += ", ".join(self._escape_latex(v) for v in value)
                else:
                    contents += self._escape_latex(str(value))

                contents += " & "

            contents = contents[:-2]
            contents += "\n"

        
        table = textwrap.dedent(rf"""
            \begin{{landscape}}
            {{\footnotesize
            \begin{{longtable}}{column_width_str}
            \hline
            {column_names_header}
            \endfirsthead
            \hline
            {column_names_header}
            \endhead
            \hline
            \multicolumn{{9}}{{r}}{{Continued on next page}} \\
            \endfoot
            \hline
            \endlastfoot
            """) + "\n".join(rows) + textwrap.dedent(r"""
            \end{longtable}
            }
            \end{landscape}
            \printbibliography
        """)

    
        content = LATEX_PREFIX + table + LATEX_POSTFIX

        return content



    def write_table(self, output_path: str, selected_columns: list[str], 
                    column_names: list[str] | None = None, column_widths: list[float | int] | None = None) -> None:
        """
        Writes all entries stored by this writer into one Markdown document at `output_path`/tex/benchmarks.tex,
        with BibTeX citations rendered as formatted footnotes.

        Parameters:
            output_path (str): filepath to write to
            selected_columns (list[str]): list of raw column names to include
            column_names (list[str] or None, default=None): names of columns to include. If not None, must have the same length as `selected_columns`
            column_widths (list[float | int] or None, default=None): widths of each column in centimeters (if None, columns are 2cm).  If not None, must have the same length as `selected_columns` and all indices must be positive
        """
        #enforce preconditions
        if column_names != None:
            assert len(column_names)==len(selected_columns), f"length of selected columns ({len(selected_columns)}) must equal length of selected columns ({len(selected_columns)})"
        if column_widths != None:
            assert len(selected_columns)==len(column_widths), f"length of column widths ({len(column_widths)}) must equal length of selected columns ({len(selected_columns)})"
            for c in column_widths:
                assert (type(c)==int or type(c)==float) and c>0, "all indices in column widths must be positive numbers"

        #Create rows of the table
        all_rows = []
        for entry in self._entries:
            all_rows.append(self._entry_to_row(entry, selected_columns).replace('\n', ' '))

        #Create column names, if not provided
        if not column_names:
            column_names_written = [col.strip().replace("_", " ").title() for col in selected_columns]
        else:
            column_names_written = column_names

        #Make string containing the document
        contents = self._generate_latex_doc(all_rows, selected_columns, column_names_written, column_widths=column_widths)

        #Write it
        os.makedirs(os.path.join(output_path, "tex"), exist_ok=True)
        filepath = os.path.join(output_path, "tex", "benchmarks.tex")
        with open(filepath, "x", encoding="utf-8") as f:
            f.write(contents)
        
        #Make bibtex
        self._write_bibtex(output_path)



    def write_individual_entries(self, output_path: str, selected_columns: list[str],
                                 column_names: list[str] | None = None, column_widths: list[float | int] | None = None) -> None: 
        """
        Writes the entries stored by this writer into separate LaTeX documents. All are in the directory `output_path`/tex_pages

        Parameters:
            output_path (str): filepath to write to
            selected_columns (list[str]): subset of columns in the table to include- any columns not in `selected_columns` will not appear in the table
            column_names (list[str] or None, default=None): names of columns to include. If not None, must have the same length as `selected_columns`
            column_widths (list[float] or list[int] or None, default=None): 
                widths of each column in centimeters (2cm columns if None). If not None, length must be the same length as `selected_columns` and all indices must be positive
        """
        #enforce preconditions
        if column_widths != None:
            assert len(selected_columns)==len(column_widths), "number of columns must equal the number of indices in the column widths"
        if not column_widths==None:
            assert len(selected_columns)==len(column_widths), f"length of column widths ({len(column_widths)}) must equal length of selected columns ({len(selected_columns)})"
            for c in column_widths:
                assert isinstance(c, float) or isinstance(c, int), "all indices in column widths must be floats or ints"
                assert c>0, "all indices in column widths must be positive"


        #Create rows of the table
        all_rows = []
        for entry in self._entries:
            all_rows.append(self._entry_to_row(entry, selected_columns).replace('\n', ' '))

        #Create column names if not given
        if column_names:
            written_col_names = column_names
        else:
            written_col_names = selected_columns

        #Write each row to a file
        os.makedirs(os.path.join(output_path, "tex_pages"), exist_ok=True)
        for i in range(len(all_rows)):

            with open(os.path.join(output_path, "tex_pages", f"entry_{i+1}.tex"), "w") as f:
                    
                latex = self._generate_latex_doc([all_rows[i]], selected_columns, written_col_names, column_widths=column_widths)
                f.write(latex)



    def _write_bibtex(self, output_dir: str):
        """
        Uses BibtexWriter to write a BibTeX bibliography to `output_dir`/tex/benchmarks.bib
        based on 'cite' fields in the LatexWriter's entries.
        """
        self._bib_writer.write(os.path.join(output_dir, "tex"))

