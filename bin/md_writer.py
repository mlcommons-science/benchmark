import os
import re
import bibtexparser
from pybtex.database import parse_string
from pybtex.plugin import find_plugin


def bibtex_to_text(entry: str) -> str:
    try:
        if not isinstance(entry, str):
            raise TypeError(f"Expected string for BibTeX entry, got {type(entry).__name__}")
        bib_data = parse_string(entry, bib_format='bibtex')
        style = find_plugin('pybtex.style.formatting', 'plain')()
        formatted = next(style.format_entries(bib_data.entries.values()))
        return re.sub(r"<[^>]+>", " ", str(formatted.text)).strip()
    except Exception as e:
        return f"Could not parse citation: {e}"


class MarkdownWriter:
    def __init__(self, entries: list[dict]):
        self.entries = entries

    def _escape_md(self, text) -> str:
        if not isinstance(text, str):
            text = str(text)
        return text.replace("|", "\\|").replace("\n", " ")

    def _sanitize_filename(self, name: str) -> str:
        output = ""
        for ch in name:
            if 32 <= ord(ch) <= 126:
                output += ch
        output = re.sub(r' {2,}', ' ', output)
        output = output.strip().replace("(", "").replace(")", "").replace(" ", "_")
        return output.lower()

    def write_table(self, output_path: str, column_names: list[str]) -> None:
        header = " | " + " | ".join(column_names) + " | " + "\n"
        divider = "| --- " * len(column_names) + "|\n"
        current_contents = ""
        footnotes = []

        for entry in self.entries:
            row = ""
            for col in column_names:
                val = entry.get(col, '')

                if col == "cite":
                    citations = val if isinstance(val, list) else [val]
                    citation_refs = []
                    for c in citations:
                        citation_text = bibtex_to_text(c)
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
            current_contents += f"[^{i + 1}]: {citation}\n"

        os.makedirs(os.path.join(output_path, "md"), exist_ok=True)
        with open(os.path.join(output_path, "md", "benchmarks.md"), "w", encoding="utf-8") as f:
            f.write(header + divider + current_contents)

    def write_individual_entries(self, output_dir: str, column_names: list[str], column_display_names: list[str], author_trunc: int | None = None) -> None:
        assert len(column_names) == len(column_display_names)
        if author_trunc is not None:
            assert author_trunc > 0

        columns = list(zip(column_names, column_display_names))
        os.makedirs(os.path.join(output_dir, "md_pages"), exist_ok=True)

        with open(os.path.join(output_dir, "md_pages", "index.md"), 'w', encoding='utf-8') as index_file:
            index_file.write("# Index of Benchmarks\n\n")

            for i, entry in enumerate(self.entries):
                entry_name = entry.get("name", f"entry_{i}")
                filename = self._sanitize_filename(entry_name) + ".md"
                filepath = os.path.join(output_dir, "md_pages", filename)

                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"# {entry_name}\n\n")

                    for col_name, col_display in columns:
                        val = entry.get(col_name, '')

                        if col_name == "cite":
                            f.write(f"**{col_display}**:\n\n")
                            citations = val if isinstance(val, list) else [val]
                            for bibtex in citations:
                                if not isinstance(bibtex, str):
                                    f.write(f"- Could not parse citation: Expected BibTeX string, got {type(bibtex).__name__}\n")
                                    continue
                                citation_text = bibtex_to_text(bibtex)
                                f.write(f"- {citation_text}\n")

                                # Write raw BibTeX
                                f.write("  - bibtex: |\n")
                                for raw_line in bibtex.strip().splitlines():
                                    f.write(f"      {raw_line}\n")
                            f.write("\n")
                        else:
                            val_str = str(val).replace("\n", " ").replace("['", "").replace("']", "")
                            val_str = val_str.replace("', '", ", ").replace("','", ", ").replace("[]", "")
                            val_str = val_str.replace("[", " ").replace("]", " ").replace("(", " ").replace(")", " ")
                            f.write(f"**{col_display}**: {val_str}\n\n")

                index_file.write(f"- [{entry_name}]({filename})\n")


if __name__ == "__main__":
    pass
