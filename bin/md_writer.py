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


        with open(os.path.join(output_path, "benchmarks.md"), "w", encoding='utf-8') as f:
            f.write(header + divider + current_contents)
    

if __name__ == "__main__":
    from yaml_manager import YamlManager
    m = YamlManager()
    m.load_yamls("source/benchmark-entry-comment-gregor.yaml")
    
    c = YamlToMarkdownConverter(m.get_table_formatted_dicts())

    c._generate_md_doc("content", ['date','name','domain','focus','keyword','task_types','metrics','models','cite'])