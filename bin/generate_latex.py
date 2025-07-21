#
# please do not modify this file
# it is maintained bt gregor
#
import os
import re
import sys
import textwrap
from typing import List, Dict, Union, Any

from pybtex.database import parse_string
from pybtex.plugin import find_plugin
from pylatexenc.latexencode import unicode_to_latex
from cloudmesh.common.console import Console
import bibtexparser
import numpy as np
import matplotlib.pyplot as plt



VERBOSE = True

# --- Constants ---

LATEX_PREFIX = textwrap.dedent(
    r"""
    \documentclass{article}
    \usepackage{fullpage}
    \usepackage{enumitem}
    \usepackage{hyperref}
    \usepackage{amsmath}
    \usepackage{pdflscape}
    \usepackage{wasysym}
    \usepackage{longtable}
    \usepackage[style=ieee, url=true]{biblatex}
    \addbibresource{benchmarks.bib} 
    \usepackage{caption}
    \usepackage[numbers]{natbib}
    \usepackage{url}
    \usepackage{graphicx}
    \graphicspath{{images/}}
    
    \begin{document}
"""
)

LATEX_POSTFIX = textwrap.dedent(
    r"""
    \printbibliography
    \end{document}
"""
)

TABLEFONT = r"\footnotesize"
# TABLEFONT = r"\tiny"

DESCRIPTION_STYLE = "[labelwidth=5em, labelsep=1em, leftmargin=*, align=left, itemsep=0.3em, parsep=0em]"

# Define all columns with their properties for clarity and consistency
ALL_COLUMNS: Dict[str, Dict[str, Union[str, float]]] = {
    "date": {"width": 1.5, "label": "Date"},
    "expired": {"width": 1, "label": "Expired"},
    "valid": {"width": 0.7, "label": "Valid"},
    "name": {"width": 2.5, "label": "Name"},
    "url": {"width": 0.7, "label": "URL"},
    "domain": {"width": 2, "label": "Domain"},
    "focus": {"width": 2, "label": "Focus"},
    "keywords": {"width": 2.5, "label": "Keywords"},
    "description": {"width": 4, "label": "Description"},
    "task_types": {"width": 3, "label": "Task Types"},
    "ai_capability_measured": {"width": "3", "label": "AI Capability"},
    "metrics": {"width": 2, "label": "Metrics"},
    "models": {"width": 2, "label": "Models"},
    "notes": {"width": 3, "label": "Notes"},
    "cite": {"width": 1, "label": "Citation"},
    "ratings": {"width": 3, "label": "Ratings"},
    "ratings.specification.rating": {"width": 1, "label": "Specification Rating"},
    "ratings.specification.reason": {"width": 3, "label": "Specification Reason"},
    "ratings.dataset.rating": {"width": 1, "label": "Dataset Rating"},
    "ratings.dataset.reason": {"width": 3, "label": "Dataset Reason"},
    "ratings.metrics.rating": {"width": 1, "label": "Metrics Rating"},
    "ratings.metrics.reason": {"width": 3, "label": "Metrics Reason"},
    "ratings.reference_solution.rating": {
        "width": "1",
        "label": "Reference Solution Rating",
    },
    "ratings.reference_solution.reason": {
        "width": "3",
        "label": "Reference Solution Reason",
    },
    "ratings.documentation.rating": {"width": "1", "label": "Documentation Rating"},
    "ratings.documentation.reason": {"width": "3", "label": "Documentation Reason"},
}

DEFAULT_COLUMNS = [
    "ratings",
    "date",
    # "expired",
    # "valid",
    "name",
    # "url",
    "domain",
    "focus",
    "keywords",
    # "description",
    "task_types",
    "ai_capability_measured",
    "metrics",
    "models",
    "notes",
    "cite",
]

REQUIRED_FIELDS_BY_TYPE = {
    "article": ["author", "title", "journal", "year", "doi"],
    "book": ["author", "title", "publisher", "year", "doi"],  # OR editor
    "booklet": ["title"],
    "conference": ["author", "title", "booktitle", "year"],
    "inbook": ["author", "title", "chapter", "publisher", "year"],  # OR pages
    "incollection": ["author", "title", "booktitle", "publisher", "year"],
    "inproceedings": ["author", "title", "booktitle", "year"],
    "manual": ["title"],
    "mastersthesis": ["author", "title", "school", "year"],
    "misc": ["title", "url", "year"],
    "phdthesis": ["author", "title", "school", "year"],
    "proceedings": ["title", "year"],
    "techreport": ["author", "title", "institution", "year"],
    "unpublished": ["author", "title", "note"],
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


def validate_bibtex_entries(bibtex_str):
    try:
        bib_database = bibtexparser.loads(bibtex_str)
        errors = []

        for entry in bib_database.entries:
            entry_type = entry.get("ENTRYTYPE", "").lower()
            entry_id = entry.get("ID", "?")
            required = REQUIRED_FIELDS_BY_TYPE.get(entry_type, [])

            # Special case logic (e.g., book can have author OR editor)
            if entry_type == "book":
                if not ("author" in entry or "editor" in entry):
                    errors.append(
                        f"Entry '{entry_id}' (book) missing 'author' or 'editor'"
                    )
                required = [
                    f for f in required if f not in ("author")
                ]  # skip checking 'author' below

            # Validate required fields
            for field in required:
                if field not in entry:
                    errors.append(
                        f"Entry '{entry_id}' ({entry_type}) missing required field: {field}"
                    )

        return (len(errors) == 0), errors

    except Exception as e:
        return False, [f"Parsing error: {e}"]


def write_to_file(content, filename="content/tex/table.tex"):
    """
    Writes the given content to a file based on the path used in filename.

    Parameters:
        content (str): The LaTeX content to write.
        filename (str): Pathe and name of the  (default is 'content/tex/table.tex').
    """
    try:
        output_dir = os.path.dirname(filename)
        os.makedirs(output_dir, exist_ok=True)

        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

        Console.ok(f"Successfully wrote content to: {filename}")

    except Exception as e:
        Console.error(f"Error writing content to {filename}: {e}")


class GenerateLatex:
    """
    Class to generate LaTeX documents from benchmark entries.
    This class is a placeholder for future functionality.
    """

    def __init__(
        self,
        entries: List[Dict],
        tex_file="content/tex/benchmarks.tex",
        bib_file="content/tex/benchmarks.bib",
        table_file="content/tex/table.tex",
    ):
        """
        Initializes the GenerateLatex with a list of entries.

        Args:
            entries (List[Dict]): List of benchmark entries, where each entry is a dictionary.
        """
        self.entries = entries
        self.files = []
        # mkdir /content/tex/section
        os.makedirs("content/tex/section", exist_ok=True)

        """
        Generates a LaTeX filename for each entry and stores it internally.
        """
        for entry in self.entries:
            name = entry.get("id", entry.get("name", "unknown"))

    # #####################################################
    # MANAGE BIBTEX
    # #####################################################

    @staticmethod
    def get_citation_label(bib_entry: str) -> str:
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
    def extract_cite_url(cite_entry: str) -> str:
        """
        Extracts the URL from the given BibTeX citation entry.

        Parameters:
            cite_entry (str): BibTeX entry to extract URL from.
        Returns:
            str: Citation's URL, or an empty string if not found.
        """
        match = re.search(r'url\s*=\s*[{"]([^}"]+)[}"]', cite_entry)
        return match.group(1) if match else ""

    def generate_bibtex(self, filename: str = "content/tex/benchmarks.bib") -> None:
        """
        Writes the bibtex file into the filename

        Parameters:
            output_dir (str): Output directory to write to.
            filename (str): Filename to write to, placed inside of `output_dir`.
        """
        bib_entries = []
        found_labels = set()
        fatal_errors = False

        for entry in self.entries:
            cite_entries = entry.get("cite", [])
            name = entry.get("name", entry.get("id", "UNKNOWN_ENTRY"))

            if isinstance(cite_entries, str):
                cite_entries = [cite_entries]
            elif not isinstance(cite_entries, list):
                Console.error(
                    f"Skipping entry '{name}' with invalid 'cite' field: {cite_entries}"
                )
                continue

            for cite_entry_raw in cite_entries:

                if not isinstance(
                    cite_entry_raw, str
                ) or not cite_entry_raw.strip().startswith("@"):
                    Console.warning(
                        f"Skipping malformed citation entry in '{name}': '{cite_entry_raw}'"
                    )
                    continue

                cite_entry = cite_entry_raw.strip()
                label = self.get_citation_label(cite_entry)

                valid, errors = validate_bibtex_entries(cite_entry)
                if not valid:
                    Console.error(f"Invalid BibTeX entry in '{name}': {label}")
                    for error in errors:
                        Console.error(f"  - {error}")
                    continue

                match = re.search(r"author\s*=\s*{(.+?)}", cite_entry_raw, re.DOTALL)
                if match:
                    authors_raw = match.group(1)
                    authors = [a.strip() for a in authors_raw.split(" and ")]

                    if "others" in authors:
                        Console.error(
                            f"Entry '{name}' contains a citation '{label}' that includes others'. Please use full author names."
                        )

                if has_capital_letter(label):
                    Console.error(
                        f'Citation label "{label}" in entry "{name}" is capitalized. Labels should be lowercase.'
                    )
                    fatal_errors = True
                if re.search(r"[\s\n\t]", label):
                    Console.error(
                        f'Citation label "{label}" in entry "{name}" contains whitespace. Labels should not contain spaces, newlines, or tabs.'
                    )
                    fatal_errors = True

                if label in found_labels:
                    Console.error(
                        f'Duplicate citation label "{label}" found. All labels must be unique.'
                    )
                    fatal_errors = True
                else:
                    found_labels.add(label)
                    bib_entries.append(cite_entry)

        if fatal_errors:
            print()
            Console.error("BibTeX entries contain errors. Please fix them to proceed.")
            print()
            sys.exit(1)

        content = "\n\n".join(bib_entries)

        if VERBOSE:
            print("\n--- Generated BibTeX Entries ---")
            print(content)
            print("\n--- End of BibTeX Entries ---")

        print(filename)

        write_to_file(content, filename=filename)

    # #####################################################
    # RADAR CHART GENERATION
    # #####################################################

        
    def generate_radar_charts(self, fmt="pdf", output_dir="content/tex/images", font_size=18):

        
        valid_formats = {"pdf", "jpeg", "png", "gif"}
        fmt = fmt.lower()
        if fmt not in valid_formats:
            print(
                f"Unsupported format '{fmt}'. Supported formats: {', '.join(valid_formats)}"
            )
            return

        os.makedirs(output_dir, exist_ok=True)


        for entry in self.entries:

            name = entry.get("name", f"unkown")
            id = entry.get("id", f"unkown")
            ratings = {}

            # Console.info(f"Generating radar chart for '{name}' ({id})...")  

            for key, value in entry.items():
                if key.startswith("ratings.") and key.endswith(".rating"):
                    parts = key.split(".")
                    if len(parts) == 3:
                        rating_type = parts[1]
                        try:
                            ratings[rating_type] = float(value)
                        except (TypeError, ValueError):
                            ratings[rating_type] = 0.0

            if not ratings:
                print(f"No ratings found for '{name}', skipping radar chart.")
                continue

            labels = list(ratings.keys())
            values = list(ratings.values())
            values += values[:1]
            angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
            angles += angles[:1]

            fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
            ax.plot(angles, values, color="tab:blue", linewidth=2)
            ax.fill(angles, values, color="tab:blue", alpha=0.25)

            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(labels, fontsize=font_size)
            ax.set_yticklabels([])
            ax.set_title(f"{name}", y=1.08, fontsize=font_size + 2)

            filename = f"{output_dir}/{id}_radar.{fmt}"
            plt.savefig(filename, bbox_inches="tight")
            plt.close(fig)

            Console.ok(f"Saved radar chart for '{name}' as '{filename}'.")


    def generate_radar_chart_grid(self, output_dir="content/tex", columns=3, rows=5, fmt="pdf"):
        col_count = max(1, columns)
        row_count = max(1, rows)
        charts_per_page = col_count * row_count

        figure_paths = []
        for i, entry in enumerate(self.entries):
            name = entry.get("name", f"Entry_{i+1}")

            filename = self.get_filename(entry, directory="images", fmt=fmt)

            figure_paths.append(filename)

        pages = []
        for i in range(0, len(figure_paths), charts_per_page):
            grid_latex = textwrap.dedent(
                r"""
                \begin{figure}[ht!]
                \centering
            """
            )
            page_paths = figure_paths[i : i + charts_per_page]
            for j, path in enumerate(page_paths):
                # Adjust width to account for spacing between images
                grid_latex += f"\\includegraphics[width={1/col_count-0.01:.4f}\\textwidth]{{{path}}}\n"
                if (j + 1) % col_count == 0:
                    grid_latex += (
                        r"\\[1ex]" + "\n"
                    )  # Add a small vertical space after each row

            grid_latex += (
                f"\\caption{{Radar chart overview (page {i // charts_per_page + 1})}}\n"
            )
            grid_latex += r"\end{figure}" + "\n\n"
            pages.append(grid_latex)

        return "\n\\clearpage\n".join(pages)

    # def generate_radar_chart_summary(self, output_dir="content/tex", show_reasons=False, columns=3, rows=5):
    #     tex_path = os.path.join(output_dir, "summary.tex")
    #     bib_path = os.path.join(output_dir, "summary.bib")
    #     figures = []
    #     bib_entries = []

    #     for i, entry in enumerate(self.entries):
    #         name = caption = entry.get("name", f"Entry_{i+1}")
    #         filename = self.get_filename(entry, directory="images", fmt="pdf")
    #         cite_keys = []

    #         # Include rating reasons in caption if requested
    #         if show_reasons:
    #             reasons = []
    #             for key, value in entry.items():
    #                 if key.startswith("ratings.") and key.endswith(".reason"):
    #                     try:
    #                         parts = key.split(".")
    #                         rating_type = parts[1]
    #                         reason = value.strip()
    #                         reasons.append(f"{rating_type.capitalize()}: {reason}")
    #                     except Exception:
    #                         continue
    #             if reasons:
    #                 caption += " --- " + "; ".join(reasons)

    #         # Extract citations and keys
    #         entry_cites = entry.get("cite", [])
    #         if not isinstance(entry_cites, list):
    #             entry_cites = [entry_cites]

    #         for cite_block in entry_cites:
    #             match = re.search(r"@\w+\{([^,]+),", cite_block)
    #             if match:
    #                 key = match.group(1)
    #             else:
    #                 key = f"entry{i+1}"  # Fallback key
    #             cite_keys.append(key)
    #             bib_entries.append(cite_block.strip())

    #         if cite_keys:
    #             caption += f" \\cite{{{', '.join(cite_keys)}}}"

    #         figure_block = textwrap.dedent(
    #             f"""
    #             \\begin{{figure}}[h!]
    #               \\centering
    #               \\includegraphics[width=0.7\\textwidth]{{{filename}}}
    #               \\caption{{{caption}}}
    #             \\end{{figure}}
    #         """
    #         )
    #         figures.append(figure_block)

    #     header = textwrap.dedent(
    #         r"""
    #         \documentclass{article}
    #         \usepackage{fullpage}
    #         \usepackage{graphicx}
    #         \usepackage{caption}
    #         \usepackage[numbers]{natbib}
    #         \usepackage{url}
    #         \title{Radar Chart Summary}
    #         \date{}
    #         \begin{document}
    #         \maketitle
    #     """
    #     )

    #     grid_pages = self.generate_grid_pages(output_dir, columns=columns, rows=rows)


    #     os.makedirs(output_dir, exist_ok=True)
    #     with open(tex_path, "w", encoding="utf-8") as f:
    #         f.write(header)
    #         f.write(grid_pages)
    #         f.writelines(figures)
    #         f.write(bibliography)
    #         f.write("\n" + footer)

    #     print(f"Write Radar chart summary to '{tex_path}'")

    #     # # Write unique BibTeX entries
    #     # unique_bib_entries = sorted(list(set(bib_entries)))
    #     # with open(bib_path, "w", encoding="utf-8") as bib_file:
    #     #     bib_file.write("\n\n".join(unique_bib_entries) + "\n")
    #     # print(f"BibTeX citations written to '{bib_path}'")

    #     # # Attempt to clean bibliography using bibtool
    #     # try:
    #     #     os.system(f"bibtool -i {bib_path} -o {bib_path}_clean")
    #     #     os.system(
    #     #         f"mv {bib_path}_clean {bib_path}"
    #     #     )  # Use mv for better atomicity than cp and then rm
    #     #     print(f"Cleaned BibTeX file using bibtool.")
    #     # except Exception as e:
    #     #     print(
    #     #         f"Warning: Could not clean BibTeX file with bibtool. Ensure bibtool is installed and in your PATH. Error: {e}"
    #     #     )

    # #####################################################
    # TEX MAIN DOCUMENT WRITER
    # #####################################################

    def generate_document(self, filename="content/tex/benchmarks.tex"):
        """
        Writes the tex file into the filename.

        Args:
            entries (List[Dict]): List of benchmark entries, where each entry is a dictionary.
        """

        content = []
        # add LaTeX preamble to content
        content.append(LATEX_PREFIX)

        content.append("")
        content.append("\\section{Benchmark Overview Table}\n")

        # add table
        content.append("\\input{table.tex}\n")

        # Add sections

        content.append("")
        content.append("\\section{Benchmark Details}\n")

        for entry in self.entries:
            name = entry.get("id", entry.get("name", "unknown"))
            entry_filename = self.get_section_filename(name)
            content.append(f"\\input{{{entry_filename}}}")
        # add Latex Postfix to content
        content.append(LATEX_POSTFIX)

        content = "\n".join(content)

        write_to_file(content, filename=filename)

    # ########################################################
    # SECTION WRITER INTO SEPERATE FILES IN source/tex/section
    # ########################################################

    @staticmethod
    def get_section_filename(name: str, location="section/") -> str:
        return location + name + ".tex"

    def latex_entry_to_string(self, entry):
        def latex_escape(text):
            """Escape LaTeX special characters for LaTeX compatibility."""
            replacements = {
                "&": r"\&",
                "%": r"\%",
                "$": r"\$",
                "#": r"\#",
                "_": r"\_",
                "{": r"\{",
                "}": r"\}",
                "~": r"\textasciitilde{}",
                "^": r"\textasciicircum{}",
                # "\\": r"\textbackslash{}",
            }
            for key, val in replacements.items():
                text = text.replace(key, val)
            return text

        def format_field(key, value, indent=0):
            indent_str = "  " * indent
            key_escaped = latex_escape(str(key))
            if isinstance(value, dict):
                lines = [
                    f"{indent_str}\\item[{key_escaped}] \\begin{{description}}{DESCRIPTION_STYLE}"
                ]
                for sub_key, sub_val in value.items():
                    lines.append(format_field(sub_key, sub_val, indent + 1))
                lines.append(f"{indent_str}\\end{{description}}")
                return "\n".join(lines)
            elif isinstance(value, list):
                lines = [f"{indent_str}\\item[{key_escaped}:]"]
                for item in value:
                    if isinstance(item, (dict, list)):
                        lines.append(format_field("-", item, indent + 1))
                    else:
                        lines.append(f"{indent_str}  - {latex_escape(str(item))}")
                return "\n".join(lines)
            elif value is not None:
                return f"{indent_str}\\item[{key_escaped}:] {latex_escape(str(value))}"
            else:
                return ""

        # Start with section and description paragraph
        lines = [f"\\section{{{latex_escape(entry['name'])}}}"]
        lines.append("{{\\footnotesize")

        if "description" in entry and entry["description"]:
            lines.append(f"\\noindent {latex_escape(entry['description'])}\n")

        # Use description environment for all fields except name/description/cite
        lines.append(f"\\begin{{description}}{DESCRIPTION_STYLE}")

        skip_fields = {"name", "description", "cite"}
        for key, value in entry.items():
            if key not in skip_fields:
                if "url" in key:
                    # Special handling for URL
                    if value:
                        lines.append(
                            f"  \\item[{key}:] "
                            f"\\href{{{latex_escape(value)}}}{{{latex_escape(value)}}}"
                        )
                else:
                    formatted = format_field(key, value, indent=1)
                    if formatted.strip():
                        lines.append(formatted)

        if "cite" in entry and entry["cite"]:
            citations = []
            # lines.append("\\textbf{Citation:}")
            # for cite_entry in entry["cite"]:
            #    lines.append(f"\\begin{{quote}}\\footnotesize {latex_escape(cite_entry)}\\end{{quote}}")

            for cite_entry in entry["cite"]:
                # get label from BibTeX entry
                label = self.get_citation_label(cite_entry)
                # print \cite{label} in LaTeX
                citations.append(f"\\cite{{{label}}}")
            lines.append(f"  \\item[Citations:] {', '.join(citations)}")

            if "ratings" in DEFAULT_COLUMNS:
                lines.append(f"  \\item[Ratings:]")

                id = entry.get("id", "unknown")
                name = entry.get("name", f"unknown_{id}")
                image = f"{id}_radar.pdf"

                # radar_block = textwrap.dedent(
                #     f"""
                #     # \\begin{{figure}}[h!]
                #     #  \\centering
                #     \\includegraphics[width=0.7\\textwidth]{{{image}}}
                #     #  \\caption{{{name}}}
                #     # \end{{figure}}
                #     """

                radar_block = f"\\includegraphics[width=0.2\\textwidth]{{{image}}}"
                lines.append(radar_block)

        # Close the description environmentif

        lines.append("\\end{description}")
        lines.append("}}")

        lines.append("\\clearpage")

        # if a line in lines contains "\_tex\_filename" remove that line
        lines = [line for line in lines if "\\_tex\\_filename" not in line]

        return "\n".join(lines)

    def input_all_sections(self, file="source/tex/sections.tex"):
        """
        Creates LaTeX sections for all entries and writes them to a file.

        Args:
            file (str): Path to the output LaTeX file.
        """
        content = ["\\section{Benchmark Details}\n"]

        names = []
        for entry in self.entries:
            # get id from entry
            filename = entry["id"] + ".tex"
            names.append(filename)

        # create a result so that each name is in a newline embedded in \input{}
        names = [f"\\input{{section/{name}}}" for name in names]
        # join the names with newline
        for name in names:
            content.append(name)

        write_to_file(content="\n".join(content), filename=file)

    def generate_section(self, outdir="content/tex/section"):
        """
        Writes a section of the LaTeX document containing the specified entries.

        Args:
            output_path (str): Base directory for output.
            section_name (str): Name of the section to write.
            selected_columns (List[str]): List of column keys to include in this section.
        """

        for entry in self.entries:
            if not isinstance(entry, dict):
                Console.error(f"Invalid entry format: {entry}. Expected a dictionary.")
                continue

            # Print the LaTeX section for this entry
            section = self.latex_entry_to_string(entry)

            filename = entry["id"] + ".tex"
            output_path = os.path.join(outdir, filename)

            content = section

            write_to_file(content=content, filename=output_path)

    # ########################################################
    # TABLE WRITER
    # ########################################################

    def entry_to_table_row(self, entry, columns=DEFAULT_COLUMNS) -> str:
        row = []

        for column in columns:
            print("CCCCC", "JJJJ", column, columns, entry)

            value = entry.get(column)

            content = ""
            if value is None:
                content = ""  # Empty string for None values

            elif column == "ratings":
                print("CCCCC", entry)
                # id = entry.get("id", "unknown")
                # image = f"{id}_radar.pdf"

                # print("CCCCC", "RRRRR", id, image)

                # content = f"\\includegraphics[width=0.2\\textwidth]{{{image}}}"

                # print ("CCCCC", "RRRRR", id)

                content = "TBD"

            elif column == "cite":
                cite_entries = (
                    value
                    if isinstance(value, list)
                    else [value] if isinstance(value, str) else []
                )
                cite_keys = [
                    self.get_citation_label(c)
                    for c in cite_entries
                    if c and c.strip().startswith("@")
                ]
                primary_url = entry.get("url", "")

                # Try to get URL from the first citation entry if available
                if not primary_url and cite_entries:
                    first_cite_url = self.extract_cite_url(cite_entries[0])
                    if first_cite_url:
                        primary_url = first_cite_url

                cite_text = f"\\cite{{{','.join(cite_keys)}}}" if cite_keys else ""

                url_text = (
                    f"\\href{{{escape_latex(primary_url)}}}{{$\\Rightarrow$}}"
                    if primary_url
                    else ""
                )
                content = f"{cite_text}{url_text}"
            elif column == "url":
                content = f"\\href{{{escape_latex(value)}}}{{link}}" if value else ""
            elif isinstance(value, list):
                content = ", ".join(escape_latex(item) for item in value)
            else:
                content = escape_latex(value)

            print("CCCCC", column, content)
            row.append(content)

        result = " & ".join(row) + r" \\ \hline"

        Console.error(result)

        return result

    def generate_table(
        self, filename="content/tex/table.tex", columns=DEFAULT_COLUMNS
    ) -> str:

        # check if columns are valid
        for col in columns:
            if col not in ALL_COLUMNS:
                Console.error(f"Invalid column name: {col}.")
                sys.exit(1)

        # Generate the table header and column format

        def generate_column_format():

            tex_width = "\textheight"

            width = []
            names = []
            total_width = 0
            for col in columns:
                if col in ALL_COLUMNS:
                    total_width += float(ALL_COLUMNS[col]["width"])
                    width.append(ALL_COLUMNS[col]["width"])
                    names.append(ALL_COLUMNS[col]["label"])
            # normalize the width to fit into the tex_width
            print("TOTAL WIDTH: ", total_width)
            # sys.exit(1)

            for col in range(len(width)):
                w = float(width[col]) / total_width  # with two decimal places
                w = f"{w:.2f}"

                width[col] = f"{w}\\textwidth"

            formated_names = [f"\\textbf{{{escape_latex(name)}}}" for name in names]
            formated_names_str = " & ".join(formated_names) + r" "
            formated_width = "{|" + "|".join([f"p{{{x}}}" for x in width]) + "|}"

            return formated_width, formated_names_str

        column_widths, column_names = generate_column_format()
        if VERBOSE:
            Console.msg("FORMATED WIDTH: " + column_widths)
            Console.msg("FORMATED NAMES: " + column_names)

        # Generate the table rows
        rows = []
        for entry in self.entries:
            row = self.entry_to_table_row(entry, columns)
            if row.strip():
                rows.append(row)
        all_rows = "\n".join(rows)

        # Constructing the table content
        table_content = (
            textwrap.dedent(
                rf"""
                \begin{{landscape}}
                {{{TABLEFONT}
                \begin{{longtable}}{column_widths}
                \hline
                {column_names}
                \hline
                \endfirsthead
                \hline
                {column_names}
                \endhead
                \hline
                \multicolumn{{{len(columns)}}}{{r}}{{Continued on next page}} \\
                \endfoot
                \hline
                \endlastfoot
                """
            )
            + all_rows
            + textwrap.dedent(
                r"""
                }}
                \end{longtable}
                \end{landscape}
                """
            )
        )

        if VERBOSE:
            Console.msg("Generated LaTeX table content:")
            print(table_content)

        write_to_file(content=table_content, filename=filename)

        return table_content
