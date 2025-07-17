import os
import re
import bibtexparser
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


    def write_table(self, output_path: str, column_names: list[str], column_display_names: list[str] | None = None) -> None:
        """
        Writes all entries stored by this writer into one Markdown document at `output_path`/md/benchmarks.md

        Parameters:
            output_path (str): filepath to write to
            column_names (list[str]): subset of columns in the table to include- any columns not in `column_names` will not appear in the table
            column_display_names (list[str] or None, default=None): titles of each column. If not None, must have the same length as `column_names`
        """
        if column_display_names != None:
            assert len(column_names)==len(column_display_names), "length of column names must equal the length of the column display names"

        header = " | " + " | ".join(column_display_names if column_display_names else column_names) + " | " + "\n"
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
            


    def write_individual_entries(self, output_dir: str, column_names: list[str], column_display_names: list[str], author_trunc: int | None = None) -> None:
        """
        Writes the entries stored by this writer into separate Markdown documents. All are in the directory `output_dir`/md_pages

        Parameters:
            output_path (str): filepath to write to
            columns (list[str]): subset of columns in the table to include- any columns not in `selected_columns` will not appear in the table
            column_display_names (list[str]): names of the columns to write. Must be the same length as `columns_names`
            author_trunc (int or None): maximum number of authors to display (None if displaying all authors). Must be positive
        """
        assert len(column_names)==len(column_display_names), "column names and column display names must have the same length"
        if isinstance(author_trunc, int):
            assert author_trunc > 0, "number of authors to truncate must be positive"

        columns = []
        for c in range(len(column_display_names)):
            columns.append((column_names[c], column_display_names[c]))

        os.makedirs(os.path.join(output_dir, "md_pages"), exist_ok=True)
        with open(os.path.join(output_dir, "md_pages", "index.md"), 'w', encoding='utf-8') as index_file:

            index_file.write("# Index of Benchmarks\n\n")
            for i, entry in enumerate(self.entries):
                entry_name = entry.get("name", f"entry_{i}")
                filename = self._sanitize_filename(entry_name) + ".md"
                filepath = os.path.join(output_dir, "md_pages", filename)

                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"# {entry_name}\n\n")

                    for col_name, col_display in columns:
                        val = entry.get(col_name, '')

                        if col_name == "cite" and isinstance(val, list):
                            f.write(f"**{col_display}**:\n\n")
                            for bibtex in val:
                                f.write("-\n")
                                try:
                                    parser = bibtexparser.bparser.BibTexParser(common_strings=True)
                                    db = bibtexparser.loads(bibtex, parser=parser)
                                    if db.entries:
                                        bib = db.entries[0]
                                        f.write(f"  - type: {bib.get('ENTRYTYPE', '')}\n")
                                        f.write(f"  - id: {bib.get('ID', '')}\n")
                                        for key, value in bib.items():
                                            if key in ('ENTRYTYPE', 'ID'):
                                                continue
                                            if key == 'author' and author_trunc:
                                                authors = [a.strip() for a in value.replace('\n', ' ').split(' and ')]
                                                if len(authors) > author_trunc:
                                                    authors = authors[:author_trunc] + ['et al.']
                                                value = ', '.join(authors)
                                            f.write(f"  - {key}: {value}\n")
                                except Exception as e:
                                    f.write(f"  - parsing_error: {str(e)}\n")
                                f.write("  - bibtex: |\n")
                                for raw_line in bibtex.strip().splitlines():
                                    f.write(f"      {raw_line}\n")
                            f.write("\n")
                        
                        #Proceed normally if not writing ratings
                        else:
                            val_str = str(val).replace("\n", " ").replace("['", "").replace("']", "")
                            val_str = val_str.replace("', '", ", ").replace("','", ", ").replace("[]", "")
                            val_str = val_str.replace("[", " ").replace("]", " ").replace("(", " ").replace(")", " ")
                            f.write(f"**{col_display}**: {val_str}\n\n")


                index_file.write(f"- [{entry_name}]({filename})\n")
                

if __name__ == "__main__":
    pass