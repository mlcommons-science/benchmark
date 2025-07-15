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



    def _generate_md_doc(self, output_path: str, column_names: list[str]) -> None:
        header = " | " + " | ".join(column_names) + " | " + "\n"
        divider = "| --- "*len(column_names) +  "|\n"

        #Create the contents string
        current_contents = ""
        for entry in self.entries:
            
            for col in column_names:
                #Get current column name from the entries
                col_data = entry.get(col, '')

                #If list, append each entry in the list
                if isinstance(col_data, list):
                    for d in col_data:
                        current_contents += self._escape_md(d) + ","
                    current_contents += "|"
                #If not list, add to the list
                else:
                    current_contents += ' | ' + self._escape_md(col_data)
            current_contents += ' |\n'


        with open(output_path, "w", encoding='utf-8') as f:
            f.write(header + divider + current_contents)
    def write_individual_entries(self, output_dir: str, column_names: list[str]) -> None:
        """
        Writes one Markdown file per benchmark entry in the specified output directory.
        """
        os.makedirs(output_dir, exist_ok=True)

        for i, entry in enumerate(self.entries):
            filename = os.path.join(output_dir, f"entry_{i+1}.md")
            with open(filename, "w", encoding="utf-8") as f:
                header = " | " + " | ".join(column_names) + " |\n"
                divider = "| --- " * len(column_names) + "|\n"
                row = " |"

                for col in column_names:
                    value = entry.get(col, "")
                    if isinstance(value, list):
                        cell = ", ".join(self._escape_md(v) for v in value)
                    else:
                        cell = self._escape_md(value)
                    row += f" {cell} |"
                f.write(header + divider + row + "\n")


if __name__ == "__main__":
    from yaml_manager import YamlManager
    m = YamlManager()
    m.load_yamls("source/benchmark-entry-comment-gregor.yaml")
    
    c = YamlToMarkdownConverter(m.get_table_formatted_dicts())

    c._generate_md_doc("content", ['date','name','domain','focus','keyword','task_types','metrics','models','cite'])