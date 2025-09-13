#!/usr/bin/env python
import re
import sys
from docopt import docopt

"""
Check BibTeX Non-Space Characters: Lint BibTeX files for common syntax issues.

Usage:
  check-bibtex-non-space <file>...
  check-bibtex-non-space (-h | --help)

Arguments:
  <file>        One or more BibTeX files to lint.

Options:
  -h --help     Show this help message.

Description:
  This tool scans BibTeX files and warns about:
    - Invisible or non-printable characters
    - Missing commas between fields
    - Unclosed or mismatched braces
    - Entries starting while a previous entry is not closed

Examples:
  # Lint a single file
  check-bibtex-non-space references.bib

  # Lint multiple files at once
  check-bibtex-non-space file1.bib file2.bib file3.bib
"""


def lint_bibtex_file(file_path):
    """
    Scans a BibTeX file to find common syntax errors that lead to
    parsing warnings like "1 non-space characters ignored".

    Args:
        file_path (str): The path to the BibTeX file.
    """
    print(f"Scanning file: {file_path}\n")

    try:
        # We try to open with UTF-8, which is the standard
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: The file at '{file_path}' was not found.")
        return
    except UnicodeDecodeError:
        # If it fails, we know it's a character encoding problem.
        print(f"Error: The file at '{file_path}' could not be decoded as UTF-8.")
        print(
            "This is a common cause of BibTeX errors. Try resaving the file with UTF-8 encoding."
        )
        return
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")
        return

    issues_found = False

    # Regex to find a field entry without a comma after the closing brace/parenthesis.
    # It looks for a pattern like `key = {value}` followed by text without a comma.
    # This is a common cause of the "non-space characters ignored" error.
    missing_comma_pattern = re.compile(r"=\s*(\s*\{[^}]*\}|\([^\)]*\))\s*(\w)")

    # Regex to find a misplaced '@' symbol or entry type.
    misplaced_entry_pattern = re.compile(r"^[^@]*@")

    # Keep track of open braces to check for unclosed entries
    open_braces = 0
    in_entry = False

    for i, line in enumerate(lines, 1):
        # Check for invisible or non-printable characters.
        # This is the most likely cause of the "1 non-space characters ignored" error
        # for a seemingly correct entry.
        for char_index, char in enumerate(line):
            # We are checking for characters that are not printable (like non-breaking spaces)
            # and are not standard space characters.
            if not char.isprintable() and not char.isspace():
                print(
                    f"Warning on line {i}, position {char_index}: Found an invisible or non-printable character '{repr(char)}'."
                )
                print(
                    f"  This is a very common cause of parsing errors. Please retype this character."
                )
                print(f"  Line content: {line.strip()}")
                issues_found = True
                break  # Exit inner loop, move to next line.

        # Strip leading/trailing whitespace for easier analysis
        stripped_line = line.strip()

        # Check for unclosed entries. A new @ entry starts while inside another.
        if stripped_line.startswith("@"):
            if in_entry and open_braces > 0:
                print(
                    f"Warning on line {i}: Likely unclosed entry. A new '@' entry started."
                )
                print(f"  Line content: {line.strip()}")
                issues_found = True
            in_entry = True

        # Check for missing commas between fields
        match_comma = missing_comma_pattern.search(line)
        if match_comma:
            # Check if the text after the closing brace is a new field name.
            # We are assuming it's a new field if it's alphanumeric.
            if stripped_line.endswith("}"):
                # This is a specific case of the above pattern.
                pass
            else:
                # The regex found something suspicious.
                # Example: `title={Some Title} author={...}`
                print(
                    f"Warning on line {i}: Possible missing comma. Found text '{match_comma.group(2)}' right after a value."
                )
                print(f"  Check if a comma is needed after the preceding field.")
                print(f"  Line content: {line.strip()}")
                issues_found = True

        # Simple check for unclosed brackets within a line
        if line.count("{") > line.count("}"):
            open_braces += 1
        elif line.count("}") > line.count("{"):
            if open_braces > 0:
                open_braces -= 1
            else:
                print(f"Warning on line {i}: Mismatched closing brace '}}'.")
                print(f"  Line content: {line.strip()}")
                issues_found = True

    if not issues_found:
        print(
            "\nNo common BibTeX syntax issues found. The file syntax seems to be correct."
        )
        print(
            "The warning may be due to other reasons, such as character encoding issues."
        )
    else:
        print("\nScanning complete. Please review the warnings above.")


def main():
    args = docopt(__doc__)
    file_to_check = args["<file>"]
    lint_bibtex_file(file_to_check)


if __name__ == "__main__":
    main()
