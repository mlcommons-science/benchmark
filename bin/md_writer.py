import os
from typing import List

class YamlToMarkdownConverter:
    def __init__(self, entries: List[List[dict]]):
        """
        entries: list of benchmark entries, where each entry is a list of {key: value} dictionaries
        """
        self.entries = entries

    def escape_md(self, text) -> str:
        if not isinstance(text, str):
            text = str(text)
        return text.replace("|", "\\|").replace("\n", " ")

    def escape_md_value(self, value) -> str:
        """
        Escapes Markdown characters and safely formats values.
        Handles lists, dicts, and None.
        """
        if isinstance(value, list):
            return ", ".join(self.escape_md(str(v)) for v in value)
        elif isinstance(value, dict):
            return self.escape_md(str(value))
        elif value is None:
            return ""
        else:
            return self.escape_md(str(value))

    def flatten_entry(self, entry: List[dict]) -> dict:
        """
        Converts a list of single-key dicts into one flat dictionary.
        """
        flat = {}
        for field in entry:
            flat.update(field)
        return flat

    def get_all_fields(self) -> List[str]:
        """
        Returns a sorted list of all unique field names across all entries.
        """
        fields = set()
        for entry in self.entries:
            flat = self.flatten_entry(entry)
            fields.update(flat.keys())
        return sorted(fields)

    def generate_markdown_doc(self, title: str) -> str:
        """
        Combines all field blocks across entries into a single flat dictionary,
        then renders a Markdown table with one header and one row of values.
        """
        header = f"# {title}\n\n"

        if not self.entries:
            return header + "_No entries found._\n"

        # 👇 STEP 1: Flatten all field dicts from all sublists
        combined_fields = {}
        for block in self.entries:
            for field_dict in block:
                combined_fields.update(field_dict)

        # 👇 STEP 2: Collect all unique keys
        all_fields = sorted(combined_fields.keys())

        # 👇 STEP 3: Create table rows
        table_header = "| " + " | ".join(self.escape_md(k) for k in all_fields) + " |"
        table_divider = "| " + " | ".join(["---"] * len(all_fields)) + " |"
        value_row = "| " + " | ".join(self.escape_md_value(combined_fields.get(k, "")) for k in all_fields) + " |"

        return header + table_header + "\n" + table_divider + "\n" + value_row + "\n"


    def convert_to_single_file(self, output_path: str):
        """
        Writes the first entry in Markdown format to a single file.
        """
        markdown = self.generate_markdown_doc("Benchmark Field Specification")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown)

    def write_individual_entries(self, output_dir: str):
        """
        Writes one Markdown file per entry in the output directory.
        """
        os.makedirs(output_dir, exist_ok=True)
        all_fields = self.get_all_fields()

        for i, entry in enumerate(self.entries):
            flat_entry = self.flatten_entry(entry)
            field_values = [flat_entry.get(field, "") for field in all_fields]

            table_header = "| " + " | ".join(self.escape_md(k) for k in all_fields) + " |"
            table_divider = "| " + " | ".join(["---"] * len(all_fields)) + " |"
            value_row = "| " + " | ".join(self.escape_md_value(v) for v in field_values) + " |"

            markdown = f"# Benchmark Entry {i+1}\n\n" + table_header + "\n" + table_divider + "\n" + value_row + "\n"
            output_file = os.path.join(output_dir, f"entry_{i+1}.md")

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(markdown)
