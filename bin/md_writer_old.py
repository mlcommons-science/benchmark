import os

class YamlToMarkdownConverter:
    def __init__(self, entries: list[dict]):
        """
        entries: list of benchmark entries, where each entry is a list of {key: value} dictionaries
        """
        self.entries = entries

    def _escape_md(self, text) -> str:
        if not isinstance(text, str):
            text = str(text)
        return text.replace("|", "\\|").replace("\n", " ")

    def _escape_md_value(self, value) -> str:
        """
        Escapes Markdown characters and safely formats values.
        Handles lists, dicts, and None.
        """
        if isinstance(value, list):
            return ", ".join(self._escape_md(str(v)) for v in value)
        elif isinstance(value, dict):
            return self._escape_md(str(value))
        elif value is None:
            return ""
        else:
            return self._escape_md(str(value))

    def _flatten_entry(self, entry: list[dict]) -> dict:
        """
        Converts a list of single-key dicts into one flat dictionary.
        """
        flat = {}
        for field in entry:
            flat.update(field)
        return flat

    def _get_all_fields(self) -> list[str]:
        """
        Returns a sorted list of all unique field names across all entries.
        """
        fields = set()
        for entry in self.entries:
            flat = self._flatten_entry(entry)
            fields.update(flat.keys())
        return sorted(fields)

    def _generate_markdown_doc(self, title: str) -> str:
        """
        Combines all field blocks across entries into a single flat dictionary,
        then renders a Markdown table with one header and one row of values.
        """
        header = f"# {title}\n\n"

        if not self.entries:
            return header + "_No entries found._\n"

        # 👇 STEP 1: Flatten all field dicts from all sublists
        all_combined_fields = []
        for entry in self.entries:
            combined_fields = {}
            for field_dict in entry:
                combined_fields.update(field_dict)

            all_combined_fields.append(combined_fields)

        # 👇 STEP 2: Collect all keys (unique key functionality is deprecated)
        all_fields = all_combined_fields[0].keys()

        # 👇 STEP 3: Create table rows
        table_header = "| " + " | ".join(self._escape_md(k).replace("_", " ") for k in all_fields) + " |"
        table_divider = "| " + " | ".join(["---"] * len(all_fields)) + " |"
        

        value_rows = ""
        for field in all_combined_fields:
            single_value_row = "| " + " | ".join(self._escape_md_value(field.get(k, "")) for k in all_fields) + " |"
            value_rows += single_value_row + "\n"

        return header + table_header + "\n" + table_divider + "\n" + value_rows + "\n"


    def write_single_file(self, output_path: str):
        """
        Writes the first entry in Markdown format to a single file.
        """
        markdown = self._generate_markdown_doc("Benchmark Field Specification")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown)

    def write_individual_entries(self, output_dir: str):
        """
        Writes one Markdown file per entry in the output directory.
        """
        os.makedirs(output_dir, exist_ok=True)
        all_fields = self._get_all_fields()

        for i, entry in enumerate(self.entries):
            flat_entry = self._flatten_entry(entry)
            field_values = [flat_entry.get(field, "") for field in all_fields]

            table_header = "| " + " | ".join(self._escape_md(k) for k in all_fields) + " |"
            table_divider = "| " + " | ".join(["---"] * len(all_fields)) + " |"
            value_row = "| " + " | ".join(self._escape_md_value(v) for v in field_values) + " |"

            markdown = f"# Benchmark Entry {i+1}\n\n" + table_header + "\n" + table_divider + "\n" + value_row + "\n"
            output_file = os.path.join(output_dir, f"entry_{i+1}.md")

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(markdown)
