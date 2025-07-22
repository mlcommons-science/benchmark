import os
import re
from pybtex.database import parse_string
from pybtex.plugin import find_plugin
from generate_latex import write_to_file
from generate_latex import ALL_COLUMNS, DEFAULT_COLUMNS
from cloudmesh.common.console import Console
import sys


def bibtex_to_text(entry: str) -> str:
    try:
        if not isinstance(entry, str):
            raise TypeError(
                f"Expected string for BibTeX entry, got {type(entry).__name__}"
            )
        bib_data = parse_string(entry, bib_format="bibtex")
        style = find_plugin("pybtex.style.formatting", "plain")()
        formatted = next(style.format_entries(bib_data.entries.values()))
        return re.sub(r"<[^>]+>", " ", str(formatted.text)).strip()

    except Exception as e:
        return f"Could not parse citation: {e}"


def val_to_str(val) -> str:
    val_str = str(val).replace("\n", " ").replace("['", "").replace("']", "")
    val_str = val_str.replace("', '", ", ").replace("','", ", ").replace("[]", "")
    val_str = (
        val_str.replace("[", " ").replace("]", " ").replace("(", " ").replace(")", " ")
    )
    return val_str


class MarkdownWriter:
    """
    Class to write formatted YAML file contents in Markdown format
    """

    def __init__(self, entries: list[dict], raw_entries: list[dict] | None = None):
        self.entries = entries
        self.raw_entries = raw_entries
       
    def _escape_md(self, text) -> str:
        if not isinstance(text, str):
            text = str(text)
        return text.replace("|", "\\|").replace("\n", " ")

    def _sanitize_filename(self, name: str) -> str:
        output = ""
        for ch in name:
            if 32 <= ord(ch) <= 126:
                output += ch
        output = re.sub(r" {2,}", " ", output)
        output = output.strip().replace("(", "").replace(")", "").replace(" ", "_")
        output = output.replace("\n", " ")
        return output.lower()

    def colunm_label(self, col):
        if col not in ALL_COLUMNS:
            Console.error(f"Column '{col}' is not a valid column name.")
            sys.exit(1)
        content = ALL_COLUMNS[col]["label"]
        return content

    def colunm_width(self, col):
        if col not in ALL_COLUMNS:
            Console.error(f"Column '{col}' is not a valid column name.")
            sys.exit(1)
        content = float(ALL_COLUMNS[col]["width"])
        return content

    def column_width_str(self, col):
        if col not in ALL_COLUMNS:
            Console.error(f"Column '{col}' is not a valid column name.")
            sys.exit(1)
        content = "-" * int(self.colunm_width(col) * 10.0)
        return content

    def write_table(
        self, filename="content/md/benchmark.md", columns=DEFAULT_COLUMNS
    ) -> None:

        col_labels = []
        col_widths = []

        for col in columns:
            col_labels.append(self.colunm_label(col))
            col_widths.append(self.column_width_str(col))

        section = "# Benchmarks\n\n"
        header = " | " + " | ".join(col_labels) + " | " + "\n"
        divider = ""
        for e in col_widths:
            divider += "| " + str(e) + " "

        divider += "|\n"

        # Create the contents string
        current_contents = ""
        footnotes = []

        # Write each entry to the table
        for entry in self.entries:
            row = ""

            # Write each cell to the table
            for col in columns:
                val = entry.get(col, "")

                # handle citations
                if col == "cite":
                    citations = val if isinstance(val, list) else [val]
                    citation_refs = []
                    for c in citations:
                        citation_text = bibtex_to_text(c)
                        if citation_text.startswith("Could not parse citation:"):
                            footnotes.append(None)
                        else:
                            footnotes.append(self._escape_md(citation_text))
                            citation_refs.append(f"[^{len(footnotes)}]")
                    row += ", ".join(citation_refs)

                elif isinstance(val, list):
                    row += ", ".join(map(self._escape_md, val))

                else:
                    row += self._escape_md(str(val))

                row += " | "

            current_contents += row + "\n"

        current_contents += "\n"
        for i, citation in enumerate(footnotes):
            current_contents += f"[^{i + 1}]: {citation}\n" if citation else ""

        contents = section + header + divider + current_contents

        write_to_file(content=contents, filename=filename)

    def write_individual_entries(
        self,
        output_dir="content/md/benchmarks",
        columns=DEFAULT_COLUMNS,
        author_trunc: int | None = None,
    ) -> None:
        """
        Writes all entries stored by this writer into individual Markdown documents at `output_dir`/md_tables.

        Each file's name will be the name of the benchmark entry. If no name exists, the name is "entry_" + an arbitrary number.

        An index file, "`output_dir`/md_tables/index.md", will also be written.

        Parameters:
            output_path (str): filepath to write to
            columns (list[str]): subset of columns in the table to include- any columns not in `column_names` will not appear in the table.
            author_trunc (int or None, default=None): maximum number of authors to display (if None, displays all authors). If not None, must be a positive integer
        """

        index = []
        index_filename = f"{output_dir}/index.md"
        index.append("# Index of Benchmarks\n\n")

        for i, entry in enumerate(self.entries):
            lines = []
            id = entry.get("id", f"entry-{i}")
            name = entry.get("name", f"entry-{i}")
            filename = f"{output_dir}/{id}.md"
            link = f"{id}.md"

            ratings_header_written = False
            written_rating_categories = []

            lines.append(f"# {name}\n\n")

            for col in columns:
                val = entry.get(col, "")
                col_label = self.colunm_label(col)

                if col == "cite":

                    lines.append(f"**{col_label}**:\n\n")
                    citations = val if isinstance(val, list) else [val]
                    for bibtex in citations:
                        if not isinstance(bibtex, str):
                            lines.append(
                                f"- Could not parse citation: Expected BibTeX string, got {type(bibtex).__name__}\n"
                            )
                            continue
                        citation_text = bibtex_to_text(bibtex)
                        lines.append(f"- {citation_text}\n")

                        # Write raw BibTeX
                        lines.append("  - bibtex: |\n")
                        for raw_line in bibtex.strip().splitlines():
                            lines.append(f"      {raw_line}\n")
                    lines.append("\n")

                # elif col == "ratings":
                #    print("TODO")

                elif col.startswith("ratings"):
                    if not ratings_header_written:
                        lines.append("**Ratings:**\n\n")
                        ratings_header_written = True

                    # ###########
                    # #Flat writing here
                    # val_str = str(val).replace("\n", " ").replace("['", "").replace("']", "")
                    # val_str = val_str.replace("', '", ", ").replace("','", ", ").replace("[]", "")
                    # val_str = val_str.replace("[", " ").replace("]", " ").replace("(", " ").replace(")", " ")
                    # f.write(f"- **{col_display[9:]}:** {val_str}\n\n")

                    ###########
                    # Hierarchical writing here (will break if the raw rating dictionary is changed)
                    category = col.split(".")[1]

                    if not category in written_rating_categories:
                        lines.append(f"{category.replace("_", " ").title()}:\n\n")
                        written_rating_categories.append(category)

                    val_str = val_to_str(val)

                    lines.append(
                        f"  - **{col.split('.')[2].replace('_', ' ').title()}:** {val_str}\n\n"
                    )
                    ###########

                else:
                    val_str = val_to_str(val)

                    lines.append(f"**{col_label}**: {val_str}\n\n")

            # write the image
            image_location = f"../../tex/images/{id}_radar.png"
            lines.append(
                f"**Radar Plot:**\n ![{id.replace("_", " ").title()} radar plot]({image_location})"
            )

            index.append(f"- [{name}]({link})\n")
            write_to_file(content="\n".join(lines), filename=filename)

        write_to_file(content="\n".join(index), filename=index_filename)
