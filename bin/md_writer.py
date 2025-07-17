import os
import re
from pybtex.database import parse_string
from pybtex.plugin import find_plugin


def bibtex_to_text(entry: list):

    # Parse the BibTeX entry with the 'bibtex' format
    bib_data = parse_string(entry[0], bib_format='bibtex')

    # Use the default citation style (plain)
    style = find_plugin('pybtex.style.formatting', 'plain')
    formatter = style()

    # Format the citation
    print(formatter)
    print(bib_data.entries.values())
    formatted_citation = formatter.format_entries(bib_data.entries.values())[0]
    return formatted_citation.text


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
            text: text to convert to MD
        Returns:
            MD-friendly version of `text`
        """
        if not isinstance(text, str):
            text = str(text)
        return text.replace("|", "\\|").replace("\n", " ")


    def _sanitize_filename(self, name: str) -> str:
        """
        Returns a lowercased version of `name` without whitespace and leading/trailing spaces.

        Parameters:
            name (str): filename to sanitize
        Returns:
            sanitized filename
        """
        output = ""
        for ch in name:
            if 32<=ord(ch)<=126:
                output += ch

        output = re.sub(r' {2,}', ' ', output) #Replace 2+ spaces with single space
        output = output.strip().replace("(", "").replace(")", "").replace(" ", "_")

        return output.lower()


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
        citations = []
        for entry in self.entries:
            
            for col in column_names:
                #Get current column name from the entries
                col_data = entry.get(col, '')

                if col=="cite":
                    #do footnotes
                    if isinstance(col_data, list):
                        #list: append all indices to the citations
                        for col_index in col_data:
                            citations.append(self._escape_md(col_index))
                            current_contents += f'[^{len(citations)}]'
                    else:
                        #not a list: append to citations
                        citations.append(self._escape_md(col_index))
                        current_contents += f'[^{len(citations)}]'
                        

                #If list, append each entry in the list
                elif isinstance(col_data, list):
                    current_contents += ", ".join(map(self._escape_md, col_data))
                #If not list, add to the list
                else:
                    current_contents += self._escape_md(str(col_data))
                
                current_contents += " | "

            current_contents += '\n'

        #Add all the citations
        current_contents += '\n'
        for i, citation in enumerate(citations):
            current_contents += f"[^{i+1}]: {citation}\n"

        #write to the file
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
            filename = os.path.join(os.path.join(output_dir, "md_pages"), self._sanitize_filename(entry.get("name", f"unknown_name_{i}"))) + ".md"
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