"""
Usage:
  summary.py [--file=<path>] [--reason] [--graph=<fmt>] [--output=<dir>]
  summary.py (-h | --help)

Options:
  --file=<path>     Path to the YAML file to evaluate [default: source/benchmarks-addon-new.yaml].
  --reason          Print rating reasons along with scores.
  --graph=<fmt>     Output radar charts in one of: pdf, jpeg, png, gif.
  --output=<dir>    Directory to save radar charts and LaTeX [default: content/summary].
  -h --help         Show this help message.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import textwrap
from docopt import docopt
from yaml_manager import YamlManager


class Evaluate:
    def __init__(self, yaml_path=None):
        self.yaml_path = yaml_path
        self.entries = []

    def read(self):
        """
        Loads entries using YamlManager.
        """
        if not self.yaml_path:
            print("YAML path not provided.")
            return

        try:
            manager = YamlManager(self.yaml_path)
            self.entries = manager.get_table_formatted_dicts()
            if not isinstance(self.entries, list):
                raise ValueError("YamlManager did not return a list of entries.")
        except Exception as e:
            print(f"Error reading YAML via YamlManager: {e}")
            self.entries = []

    def print_ratings(self, show_reasons=False):
        """
        Prints ratings (and optionally reasons) for each entry.
        """
        if not self.entries:
            print("No entries loaded. Did you call read()?") 
            return

        for i, entry in enumerate(self.entries):
            print(f"\nEntry {i + 1}: {entry.get('name', 'Unnamed')}")
            print("-" * 40)

            ratings = {}
            for key, value in entry.items():
                if key.startswith("ratings.") and (".rating" in key or ".reason" in key):
                    parts = key.split('.')
                    if len(parts) != 3:
                        continue
                    rating_type = parts[1]
                    subkey = parts[2]
                    if rating_type not in ratings:
                        ratings[rating_type] = {}
                    ratings[rating_type][subkey] = value

            for category, data in ratings.items():
                rating = data.get("rating", "N/A")
                print(f"{category.capitalize()} Rating: {rating}")
                if show_reasons:
                    reason = data.get("reason", "N/A")
                    print(f"Reason: {reason}\n")

    def plot_radar_charts(self, fmt, output_dir):
        """
        Generates and saves radar charts for each entry's ratings.
        """
        if not self.entries:
            print("No entries loaded. Did you call read()?") 
            return

        valid_formats = {"pdf", "jpeg", "png", "gif"}
        fmt = fmt.lower()
        if fmt not in valid_formats:
            print(f"Unsupported format '{fmt}'. Supported formats: {', '.join(valid_formats)}")
            return

        os.makedirs(output_dir, exist_ok=True)

        for i, entry in enumerate(self.entries):
            name = entry.get('name', f'Entry_{i+1}')
            ratings = {}

            for key, value in entry.items():
                if key.startswith("ratings.") and key.endswith(".rating"):
                    parts = key.split('.')
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
            ax.plot(angles, values, color='tab:blue', linewidth=2)
            ax.fill(angles, values, color='tab:blue', alpha=0.25)
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(labels)
            ax.set_yticklabels([])
            ax.set_title(f"Ratings for {name}", y=1.08)

            safe_name = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in name).strip()
            filename = os.path.join(output_dir, f"{safe_name}_radar.{fmt}")
            plt.savefig(filename, bbox_inches='tight')
            plt.close(fig)

            print(f"Saved radar chart for '{name}' as '{filename}'.")

    def generate_latex_summary(self, output_dir, show_reasons=False):
        """
        Generates a LaTeX file summarizing all radar chart PDFs with figure captions.
        """
        tex_path = os.path.join(output_dir, "summary.tex")
        figures = []

        for i, entry in enumerate(self.entries):
            name = entry.get("name", f"Entry_{i+1}")
            safe_name = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in name).strip()
            pdf_path = f"{safe_name}_radar.pdf"
            caption = name

            if show_reasons:
                reasons = []
                for key, value in entry.items():
                    if key.startswith("ratings.") and key.endswith(".reason"):
                        try:
                            parts = key.split('.')
                            rating_type = parts[1]
                            reason = value.strip()
                            reasons.append(f"{rating_type.capitalize()}: {reason}")
                        except Exception:
                            continue
                if reasons:
                    caption += " — " + "; ".join(reasons)

            figure_block = textwrap.dedent(f"""
                \\begin{{figure}}[h!]
                  \\centering
                  \\includegraphics[width=0.7\\textwidth]{{{pdf_path}}}
                  \\caption{{{caption}}}
                \\end{{figure}}
            """)
            figures.append(figure_block)

        header = textwrap.dedent(r"""
            \documentclass{article}
            \usepackage{graphicx}
            \usepackage[margin=1in]{geometry}
            \usepackage{caption}
            \title{Radar Chart Summary}
            \date{}
            \begin{document}
            \maketitle
        """)

        footer = r"\end{document}"

        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(header)
            f.writelines(figures)
            f.write("\n" + footer)

        print(f"LaTeX summary written to '{tex_path}'")


if __name__ == "__main__":
    args = docopt(__doc__)
    yaml_file = args["--file"]
    show_reasons = args["--reason"]
    graph_fmt = args["--graph"]
    output_dir = args["--output"] or "content/summary"

    evaluator = Evaluate(yaml_file)
    evaluator.read()
    evaluator.print_ratings(show_reasons=show_reasons)

    if graph_fmt:
        evaluator.plot_radar_charts(graph_fmt, output_dir)
        if graph_fmt == "pdf":
            evaluator.generate_latex_summary(output_dir, show_reasons=show_reasons)
