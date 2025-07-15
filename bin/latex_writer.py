import os
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
            # description = self._escape_latex(entry.get("description", ""))
            # condition = self._escape_latex(entry.get("condition", ""))
            rows.append(
                # f"{field_name} & {field_value} & {description} & {condition} \\\\ \\hline"
                f"{field_name} & {field_value} \\\\ \\hline"
            )
        return rows


    def _generate_latex_doc(self, title: str, rows: list[str]) -> str:
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


    # def write_single_file_old(self, output_path: str):
    #     """Writes a single TeX entry to `output_path`"""
    #     all_rows = []
    #     for entry in self.entries:
    #         for col in entry:
    #             all_rows.extend(self._entry_to_rows(col))
    #     latex = self._generate_latex_doc("Benchmark Field Specification", all_rows)

    #     os.makedirs(os.path.dirname(output_path), exist_ok=True)
    #     with open(output_path, "w", encoding="utf-8") as f:
    #         f.write(latex)

    
    def write_single_file(self, output_path: str, columns: tuple):
        """Writes a single TeX entry to `output_path`"""

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:

            all_rows = []
            for entry in self.entries:
                print(entry)
                line = []
                for col in columns:
                    line.append(entry[col])
                    # # line.append(self._entry_to_rows(col))
                    # all_rows.extend(self._entry_to_rows(col))
                line_str = ' & '.join(map(str, line)) + '\\'
                f.write(line_str)


    def write_individual_entries(self, output_dir: str):
        """Writes single TeX entries, each containing one of the class's stored entries, to `output_path`"""
        os.makedirs(output_dir, exist_ok=True)

        for yaml in self.entries:
            for i, entry in enumerate(yaml):
                rows = self._entry_to_rows(entry)
                latex = self._generate_latex_doc(f"Benchmark Entry {i+1}", rows)

                output_file = os.path.join(output_dir, f"entry_{i+1}.tex")
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(latex)
