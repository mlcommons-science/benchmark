import os
import re
import textwrap


def escape_latex(text):
    if not isinstance(text, str):
        text = str(text)
    return (
        text.replace("\\", "\\textbackslash{}").replace("&", "\\&").replace("%", " percent")
            .replace("_", "\\_").replace("#", "\\#").replace("{", "\\{").replace("}", "\\}")
            .replace("^", "\\^{}").replace("~", "\\~{}").replace("$", "\\$")
    )


def extract_cite_label(cite_entry: str) -> str:
    match = re.match(r'@\w+\{([^,]+),', cite_entry.strip())
    return match.group(1) if match else ""


def extract_cite_url(cite_entry: str) -> str:
    match = re.search(r'url\s*=\s*[{"]([^}"]+)[}"]', cite_entry)
    return match.group(1) if match else ""


def sanitize_filename(name: str) -> str:
    output = "".join(ch for ch in name if 32 <= ord(ch) <= 126)
    output = re.sub(r' {2,}', ' ', output)
    output = output.strip().replace("(", "").replace(")", "").replace(" ", "_")
    return output


def write_latex_for_entry(entry: dict, output_dir: str, columns: list[tuple], author_limit: int = 10):
    os.makedirs(output_dir, exist_ok=True)
    entry_name = entry.get("name", "entry")
    filename = sanitize_filename(entry_name) + ".tex"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("\\begin{table}[h!]\n\\centering\n")
        f.write("\\begin{tabular}{|l|p{10cm}|}\n\\hline\n")

        for col_name, _, col_display in columns:
            val = entry.get(col_name, '')
            if col_name == "cite":
                cite_keys = [extract_cite_label(c) for c in val] if isinstance(val, list) else []
                url = extract_cite_url(val[0]) if isinstance(val, list) and val else ""
                val = (f"\\cite{{{', '.join(cite_keys)}}}" if cite_keys else "") + (
                      f" \\href{{{url}}}{{$\\Rightarrow$ }}" if url else "")
            elif isinstance(val, list):
                val = escape_latex(", ".join(map(str, val)))
            else:
                val = escape_latex(val)

            f.write(f"\\textbf{{{escape_latex(col_display)}}} & {val} \\\\ \\hline\n")

        f.write("\\end{tabular}\n\\end{table}\n")


def write_latex_for_all(entries: list[dict], output_path: str, columns: list[tuple], standalone: bool = True, author_limit: int = 10):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
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

        for entry in entries:
            row = []
            cite_keys = [extract_cite_label(c) for c in entry.get("cite", []) if c]
            cite_urls = [extract_cite_url(c) for c in entry.get("cite", []) if c]
            primary_url = cite_urls[0] if cite_urls else entry.get("url", "")

            for col_name, _, _ in columns:
                val = entry.get(col_name, '')
                if col_name == "cite":
                    val = (f"\\cite{{{', '.join(cite_keys)}}}" if cite_keys else "") + (
                          f" \\href{{{primary_url}}}{{$\\Rightarrow$ }}" if primary_url else "")
                elif col_name == "url":
                    val = ""
                elif isinstance(val, list):
                    val = ", ".join(escape_latex(str(v)) for v in val)
                else:
                    val = escape_latex(str(val))
                row.append(val)

            f.write(" & ".join(row) + " \\\\ \\hline\n")

        f.write("\\end{longtable}\n}\n\\end{landscape}\n")
        if standalone:
            f.write("\\printbibliography\n\\end{document}\n")
