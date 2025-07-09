import os
import re


def sanitize_filename(name: str) -> str:
    output = "".join(ch for ch in name if 32 <= ord(ch) <= 126)
    output = re.sub(r' {2,}', ' ', output)
    output = output.strip().replace("(", "").replace(")", "").replace(" ", "_")
    return output


def clean_md_text(val):
    if isinstance(val, list):
        return ", ".join(map(str, val))
    if val is None:
        return ""
    return (
        str(val)
        .replace("\n", " ")
        .replace("['", "")
        .replace("']", "")
        .replace("', '", ", ")
        .replace("','", ", ")
        .replace("[", "")
        .replace("]", "")
        .replace("(", "")
        .replace(")", "")
    )


def write_md_for_entry(entry: dict, output_dir: str, columns: list[tuple]):
    os.makedirs(output_dir, exist_ok=True)
    entry_name = entry.get("name", "entry")
    filename = sanitize_filename(entry_name) + ".md"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"# {entry_name}\n\n")

        for col_name, _, col_display in columns:
            val = entry.get(col_name, '')
            if col_name == "cite" and isinstance(val, list):
                f.write(f"**{col_display}**:\n\n")
                for cite_entry in val:
                    f.write(f"```bibtex\n{cite_entry.strip()}\n```\n\n")
            else:
                val_str = clean_md_text(val)
                f.write(f"**{col_display}**: {val_str}\n\n")


def write_md_for_all(entries: list[dict], output_path: str, columns: list[tuple]):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        headers = [col[2] for col in columns]
        f.write("| " + " | ".join(headers) + " |\n")
        f.write("| " + " | ".join(["---"] * len(headers)) + " |\n")

        for entry in entries:
            row = []
            for col_name, _, _ in columns:
                val = entry.get(col_name, "")
                if col_name == "cite" and isinstance(val, list):
                    label_match = re.match(r'@\w+\{([^,]+),', val[0])
                    label = label_match.group(1) if label_match else ""
                    row.append(f"`{label}`")
                else:
                    row.append(clean_md_text(val))
            f.write("| " + " | ".join(row) + " |\n")
