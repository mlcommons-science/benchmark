import os
import textwrap
from typing import List

class YamlToLatexConverter:
    def __init__(self, entries: List[dict]):
        self.entries = entries

    def escape_latex(self, text: str) -> str:
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

    def entry_to_rows(self, entry: dict) -> List[str]:
        rows = []
        for key, value in entry.items():
            if key in ("description", "condition"):
                continue
            field_name = self.escape_latex(key)
            field_value = (
                self.escape_latex(value)
                if not isinstance(value, list)
                else ", ".join(map(self.escape_latex, value))
            )
            description = self.escape_latex(entry.get("description", ""))
            condition = self.escape_latex(entry.get("condition", ""))
            rows.append(
                f"{field_name} & {field_value} & {description} & {condition} \\\\ \\hline"
            )
        return rows

    def generate_latex_doc(self, title: str, rows: List[str]) -> str:
        return textwrap.dedent(rf"""
        \documentclass{{article}}
        \usepackage[margin=1in]{{geometry}}
        \usepackage{{longtable}}
        \begin{{document}}
        \section*{{{title}}}
        \begin{{longtable}}{{|p{{3cm}}|p{{3cm}}|p{{7cm}}|p{{2cm}}|}}
        \hline
        \textbf{{Field}} & \textbf{{Value}} & \textbf{{Description}} & \textbf{{Condition}} \\
        \hline
        \endfirsthead
        \hline
        \textbf{{Field}} & \textbf{{Value}} & \textbf{{Description}} & \textbf{{Condition}} \\
        \hline
        \endhead
        \hline
        \endfoot
        \hline
        \endlastfoot
        """) + "\n".join(rows) + textwrap.dedent(r"""
        \end{longtable}
        \end{document}
        """)

    def convert_to_single_file(self, output_path: str):
        all_rows = []
        for entry in self.entries:
            all_rows.extend(self.entry_to_rows(entry))
        latex = self.generate_latex_doc("Benchmark Field Specification", all_rows)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(latex)

    def write_individual_entries(self, output_dir: str):
        os.makedirs(output_dir, exist_ok=True)

        for i, entry in enumerate(self.entries):
            rows = self.entry_to_rows(entry)
            latex = self.generate_latex_doc(f"Benchmark Entry {i+1}", rows)

            output_file = os.path.join(output_dir, f"entry_{i+1}.tex")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(latex)
