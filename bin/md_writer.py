import os
import re
from random import randint
from typing import Any

class MarkdownWriter:
    """
    A class to generate Markdown documentation from data structured as a (list of) dictionaries
    """

    def __init__(self):
        """
        Initializes the MarkdownWriter instance
        """
        pass

    def _sanitize_filename(self, name: str) -> str:
        """
        Returns a copy of `name` without non-printing characters, spaces, or non-ASCII characters.

        Parameters:
            name (str): The name to sanitize.

        Returns:
            str: The sanitized filename.
        """
        output = "".join(ch for ch in name if 32 <= ord(ch) <= 126)
        output = re.sub(r' {2,}', ' ', output)
        output = output.strip().replace("(", "").replace(")", "").replace(" ", "_")
        return output

    def _clean_md_text(self, val: Any) -> str:
        """
        Returns a copy of `val` as a string of comma-separated values. Unwanted characters are removed.

        If `val` is a list, returns a comma-separated list. Each element in the list is converted to a string.  
        If `val` is None, returns the empty string.  
        If `val` is not a list or None, returns a cleaned string version of the input.

        Parameters:
            val (str, list, or None): The value to clean and format.

        Returns:
            str: The cleaned text ready for use in Markdown.
        """
        if isinstance(val, list):
            val_list = [str(val)
                .replace("\n", " ")
                .replace("['", "")
                .replace("']", "")
                .replace("', '", ", ")
                .replace("','", ", ")
                .replace("[", "")
                .replace("]", "")
                .replace("(", "")
                .replace(")", "")
                for v in val
            ]
            return ", ".join(map(str, val_list))
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


    def write_md_for_entry(self, entry: dict, output_dir: str, columns: list[tuple]):
        """
        Writes the contents of `entry` to `output_dir` as a table, using `columns` as the column names.

        If the `entry` dictionary doesn't have a "name" field, the method prints an error message. The title becomes
        "entry" plus a randomly generated number.

        Parameters:
            entry (dict): A dictionary representing a single entry's data.
            output_dir (str): The directory where the Markdown file should be saved.
            columns (list): A list of tuples representing the columns (name, width, display name).
        """
        os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists

        #Check entry name
        entry_name = entry.get("name", None)
        if not entry_name:
            print(f"\033[91mWARNING: The given entry \033[33m'{entry}'\033[91m has no name. File written to '{entry_name}'.\033[00m")
            entry_name = "entry_" + str(randint(0, 99999999))
            
        filename = self._sanitize_filename(entry_name) + ".md"  # Sanitize the entry name to create a valid filename
        filepath = os.path.join(output_dir, filename)

        # Open the file for writing the Markdown content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {entry_name}\n\n")  # Write the title as the entry name

            # Loop over columns and write the corresponding values
            for col_name, _, col_display in columns:
                val = entry.get(col_name, '')  # Get the column value from the entry
                if col_name == "cite" and isinstance(val, list):  # Handle citations
                    f.write(f"**{col_display}**:\n\n")
                    for cite_entry in val:
                        f.write(f"```bibtex\n{cite_entry.strip()}\n```\n\n")
                else:  # Handle normal text
                    val_str = self._clean_md_text(val)  # Clean and format the value
                    f.write(f"**{col_display}**: {val_str}\n\n")


    def write_md_for_all(self, entries: list[dict], output_path: str, columns: list[tuple]):
        """
        Writes the contents of `entries` to `output_path` as a single table, using `columns` as the column names.

        `output_path` must include the output filename.

        Parameters:
            entries (list): A list of dictionaries, each representing an entry.
            output_path (str): The path where the Markdown file should be saved.
            columns (list): A list of tuples representing the columns (name, width, display name).
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)  # Ensure the output directory exists

        # Open the file for writing the Markdown content
        with open(output_path, 'w', encoding='utf-8') as f:
            headers = [col[2] for col in columns]  # Extract column headers
            f.write("| " + " | ".join(headers) + " |\n")  # Write the table headers
            f.write("| " + " | ".join(["---"] * len(headers)) + " |\n")  # Write the separator line

            # Loop over entries and write each as a row in the table
            for entry in entries:
                row = []
                for col_name, _, _ in columns:
                    val = entry.get(col_name, "")  # Get the value for the column
                    if col_name == "cite" and isinstance(val, list):  # Handle citations
                        label_match = re.match(r'@\w+\{([^,]+),', val[0])
                        label = label_match.group(1) if label_match else ""
                        row.append(f"`{label}`")  # Add citation label to the row
                    else:
                        row.append(self._clean_md_text(val))  # Clean and add value to the row
                f.write("| " + " | ".join(row) + " |\n")  # Write the row to the table
