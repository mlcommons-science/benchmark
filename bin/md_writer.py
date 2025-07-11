import os
from typing import List

class YamlToMarkdownConverter:
    def __init__(self, entries: List[dict]):
        self.entries = entries

    def escape_md(self, text: str) -> str:
        if not isinstance(text, str):
            text = str(text)
        # Escape Markdown special characters inside table cells if needed
        return text.replace("|", "\\|").replace("\n", " ")

    def entry_to_rows(self, entry: dict) -> List[str]:
        rows = []
        for key, value in entry.items():
            if key in ("description", "condition"):
                continue
            field_name = self.escape_md(key)
            field_value = (
                self.escape_md(value)
                if not isinstance(value, list)
                else ", ".join(map(self.escape_md, value))
            )
            description = self.escape_md(entry.get("description", ""))
            condition = self.escape_md(entry.get("condition", ""))
            rows.append(f"| {field_name} | {field_value} | {description} | {condition} |")
        return rows

    def generate_markdown_doc(self, title: str, rows: List[str]) -> str:
        header = f"# {title}\n\n"
        table_header = "| Field | Value | Description | Condition |\n"
        table_divider = "|-------|--------|-------------|-----------|\n"
        return header + table_header + table_divider + "\n".join(rows) + "\n"

    def convert_to_single_file(self, output_path: str):
        all_rows = []
        for entry in self.entries:
            all_rows.extend(self.entry_to_rows(entry))
        markdown = self.generate_markdown_doc("Benchmark Field Specification", all_rows)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown)

    def write_individual_entries(self, output_dir: str):
        os.makedirs(output_dir, exist_ok=True)

        for i, entry in enumerate(self.entries):
            rows = self.entry_to_rows(entry)
            markdown = self.generate_markdown_doc(f"Benchmark Entry {i+1}", rows)

            output_file = os.path.join(output_dir, f"entry_{i+1}.md")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(markdown)



