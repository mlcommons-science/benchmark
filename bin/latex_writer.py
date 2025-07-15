import os
import re
import textwrap

class YamlToLatexConverter:
    def __init__(self, entries: list[dict]):
        self.entries = entries

    def _escape_latex(self, text: str) -> str:
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

    def _entry_to_rows(self, entry: dict) -> list[str]:
        rows = []
        for key, value in entry.items():
            if key in ("description", "condition"):
                continue
            field_name = self._escape_latex(key)
            field_value = (
                self._escape_latex(value)
                if not isinstance(value, list)
                else ", ".join(map(self._escape_latex, value))
            )
            rows.append(f"{field_name} & {field_value} \\\\ \\hline")
        return rows

    def _generate_latex_doc(self, title: str, rows: list[str]) -> str:
        return textwrap.dedent(rf"""
        \documentclass{{article}}
        \usepackage[margin=1in]{{geometry}}
        \usepackage{{longtable}}
        \begin{{document}}
        \section*{{{self._escape_latex(title)}}}
        \begin{{longtable}}{{|p{{5cm}}|p{{10cm}}|}}
        \hline
        \textbf{{Field}} & \textbf{{Value}} \\\\ \hline
        \endfirsthead
        \hline
        \textbf{{Field}} & \textbf{{Value}} \\\\ \hline
        \endhead
        \hline
        \endfoot
        \hline
        \endlastfoot
        """) + "\n".join(rows) + textwrap.dedent(r"""
        \end{longtable}
        \end{document}
        """)

    def write_single_file(self, output_path: str):
        """Writes all entries into one LaTeX document."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        all_rows = []
        for entry in self.entries:
            all_rows.extend(self._entry_to_rows(entry))

        latex = self._generate_latex_doc("Benchmark Field Specification", all_rows)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(latex)

        self._write_bibtex(os.path.dirname(output_path))

    def write_individual_entries(self, output_dir: str):
        """Writes one LaTeX file per entry."""
        os.makedirs(output_dir, exist_ok=True)

        for i, entry in enumerate(self.entries):
            rows = self._entry_to_rows(entry)
            latex = self._generate_latex_doc(f"Benchmark Entry {i+1}", rows)
            output_path = os.path.join(output_dir, f"entry_{i+1}.tex")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(latex)

        self._write_bibtex(output_dir)

    def _extract_cite_label(self, bib_entry: str) -> str:
        """
        Extracts the citation label from a BibTeX entry like '@article{label,...}'
        """
        match = re.match(r"@\w+\{([^,]+),", bib_entry.strip())
        return match.group(1) if match else "<unknown>"

    def _write_bibtex(self, output_dir: str):
        """
        Writes a BibTeX bibliography to output_dir/benchmarks.bib from 'cite' fields in entries.
        """
        os.makedirs(output_dir, exist_ok=True)
        bib_entries = []
        found_labels = set()
        found_entries = set()
        found_names = set()

        for record in self.entries:
            record_cite_entries = record.get("cite", [])
            name = record.get("name", "<no name>")

            if isinstance(record_cite_entries, str):
                record_cite_entries = [record_cite_entries]
            elif not isinstance(record_cite_entries, list):
                continue

            for cite_entry in record_cite_entries:
                if not isinstance(cite_entry, str) or not cite_entry.strip().startswith("@"):
                    continue

                label = self._extract_cite_label(cite_entry.lower())

                if label in found_labels:
                    print(f"\033[91mERROR: Duplicate citation label \"{label}\" found in entry \"{name}\".\033[00m")
                elif cite_entry in found_entries and name in found_names:
                    pass  # Same citation reused
                else:
                    found_labels.add(label)
                    found_entries.add(cite_entry)
                    found_names.add(name)
                    bib_entries.append(cite_entry.strip())

        bib_path = os.path.join(output_dir, "benchmarks.bib")
        with open(bib_path, 'w', encoding='utf-8') as bib_file:
            for entry in bib_entries:
                bib_file.write(entry + "\n\n")
