import os

class MarkdownWriter:
    """Class to write formatted YAML contents to a Markdown file"""

    def __init__(self, entries: list[dict]):
        """
        Creates a new writer responsible for writing `entries` to a Markdown file

        Parameters:
            entries (list[dict]): list of benchmark entries, where each entry is a list of {key: value} dictionaries
        """
        self.entries = entries


    def _escape_md(self, text) -> str:
        """
        Returns `text`, where all Markdown special characters are replaced with escape sequences.

        Parameters:
            text (str): text to convert to MD
        Returns:
            MD-friendly version of `text`
        """
        if not isinstance(text, str):
            text = str(text)
        return text.replace("|", "\\|").replace("\n", " ")



    def write_table(self, output_path: str, column_names: list[str]) -> None:
        """
        Writes all entries stored by this writer into one Markdown document at `output_path`/md/benchmarks.md

        Parameters:
            output_path (str): filepath to write to
            columns (list[str]): subset of columns in the table to include- any columns not in `selected_columns` will not appear in the table
        """
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


        os.makedirs(os.path.join(output_path, "md"), exist_ok=True)
        with open(os.path.join(output_path, "md", "benchmarks.md"), "w", encoding='utf-8') as f:
            f.write(header + divider + current_contents)


    def write_individual_entries(self, output_dir: str, column_names: list[str]) -> None:
        """
        Writes the entries stored by this writer into separate Markdown documents. All are in the directory `output_path`/md_pages

        Parameters:
            output_path (str): filepath to write to
            columns (list[str]): subset of columns in the table to include- any columns not in `selected_columns` will not appear in the table
        """
        os.makedirs(os.path.join(output_dir, "md_pages"), exist_ok=True)

        for i, entry in enumerate(self.entries):
            filename = os.path.join(os.path.join(output_dir, "md_pages"), f"entry_{i+1}.md")
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
    pass