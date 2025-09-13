#!/usr/bin/env python"""
Check and fix suspicious characters in BibTeX files.

Usage:
  check_bibtex [--file=<filename>...]
  check_bibtex (-h | --help)

Options:
  -h --help           Show this help message.
  --file=<filename>    Path(s) to one or more BibTeX files to check and optionally fix.
                       [default: content/tex/benchmarks.bib]

Description:
  This tool scans BibTeX files for suspicious non-ASCII, zero-width, or UTF-8 characters
  that can cause LaTeX compilation warnings. It can also replace these characters
  with LaTeX-safe equivalents and save a corrected version of the file.

Examples:
  # Check a single BibTeX file (default file)
  check_bibtex

  # Check a specific BibTeX file
  check_bibtex --file=references.bib

  # Check multiple BibTeX files
  check_bibtex --file=file1.bib --file=file2.bib
"""

import sys
import os
from docopt import docopt


def check_file(filename):
    """
    Checks the specified file for suspicious characters.
    Returns True if suspicious characters are found, False otherwise.
    """
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        return False

    print(f"Checking '{filename}' for suspicious characters...")

    suspicious_chars_found = False
    suspicious_chars_to_check = {
        "\u200b": "Zero-Width Space",
        # Add other suspicious Unicode characters here as needed
    }

    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                # Check for characters that are not standard ASCII
                if not all(ord(c) < 128 for c in line):
                    print(f"Warning: Non-ASCII character found on line {line_num}:")
                    print(line.strip())
                    suspicious_chars_found = True

                # Check for specific known problematic characters
                for char, name in suspicious_chars_to_check.items():
                    if char in line:
                        print(f"Warning: Found a {name} ('{char}') on line {line_num}:")
                        print(line.strip())
                        suspicious_chars_found = True

    except UnicodeDecodeError:
        print(f"Error: Could not read '{filename}' as a UTF-8 encoded file.")
        print("This may be an indication of an encoding issue.")
        return True

    if not suspicious_chars_found:
        print("\nSuccess: No suspicious characters found.")
    else:
        print("\nFinished checking. Please review the warnings above.")

    return suspicious_chars_found


def replace_chars(filename):
    """
    Replaces common non-ASCII characters with their LaTeX equivalents.
    """
    replacements = {
        "á": "\\'{a}",
        "é": "\\'{e}",
        "í": "\\'{i}",
        "ó": "\\'{o}",
        "ú": "\\'{u}",
        "ý": "\\'{y}",
        "Á": "\\'{A}",
        "É": "\\'{E}",
        "Í": "\\'{I}",
        "Ó": "\\'{O}",
        "Ú": "\\'{U}",
        "Ý": "\\'{Y}",
        "à": "\\`{a}",
        "è": "\\`{e}",
        "ì": "\\`{i}",
        "ò": "\\`{o}",
        "ù": "\\`{u}",
        "À": "\\`{A}",
        "È": "\\`{E}",
        "Ì": "\\`{I}",
        "Ò": "\\`{O}",
        "Ù": "\\`{U}",
        "â": "\\^{a}",
        "ê": "\\^{e}",
        "î": "\\^{i}",
        "ô": "\\^{o}",
        "û": "\\^{u}",
        "Â": "\\^{A}",
        "Ê": "\\^{E}",
        "Î": "\\^{I}",
        "Ô": "\\^{O}",
        "Û": "\\^{U}",
        "ä": '\\"{a}',
        "ë": '\\"{e}',
        "ï": '\\"{i}',
        "ö": '\\"{o}',
        "ü": '\\"{u}',
        "Ä": '\\"{A}',
        "Ë": '\\"{E}',
        "Ï": '\\"{I}',
        "Ö": '\\"{O}',
        "Ü": '\\"{U}',
        "ã": "\\~{a}",
        "õ": "\\~{o}",
        "ñ": "\\~{n}",
        "Ã": "\\~{A}",
        "Õ": "\\~{O}",
        "Ñ": "\\~{N}",
        "ç": "\\c{c}",
        "Ç": "\\c{C}",
        "ş": "\\c{s}",
        "Ş": "\\c{S}",
        "ć": "\\'{c}",
        "Ć": "\\'{C}",
        "đ": "\\dj",
        "Đ": "\\DJ",
        "ğ": "\\u{g}",
        "Ğ": "\\u{G}",
        "ı": "i",
        "İ": "I",
        "ł": "\\l",
        "Ł": "\\L",
        "ń": "\\'{n}",
        "Ń": "\\'{N}",
        "ň": "\\v{n}",
        "Ň": "\\v{N}",
        "ř": "\\v{r}",
        "Ř": "\\v{R}",
        "ś": "\\'{s}",
        "Ś": "\\'{S}",
        "š": "\\v{s}",
        "Š": "\\v{S}",
        "ž": "\\v{z}",
        "Ž": "\\v{Z}",
        "ź": "\\'{z}",
        "Ź": "\\'{Z}",
        "ż": "\\.{z}",
        "Ż": "\\.{Z}",
        "ą": "\\k{a}",
        "Ą": "\\k{A}",
        "ę": "\\k{e}",
        "Ę": "\\k{E}",
        "ó": "\\'{o}",
        "Ó": "\\'{O}",
        "ú": "\\'{u}",
        "Ú": "\\'{U}",
        "ø": "\\o",
        "Ø": "\\O",
        "’": "'",
        "‘": "'",
        "”": "''",
        "“": "``",
        "—": "---",
        "–": "--",
        "\u200b": "",
        "ă": "\\u{a}",
        "Ă": "\\u{A}",
    }

    output_filename = filename.replace(".bib", ".fixed.bib")

    try:
        with open(filename, "r", encoding="utf-8") as infile:
            content = infile.read()
            for char, repl in replacements.items():
                content = content.replace(char, repl)

        with open(output_filename, "w", encoding="utf-8") as outfile:
            outfile.write(content)

        print(
            f"\nSuccessfully replaced characters. The corrected file is saved as '{output_filename}'."
        )
    except Exception as e:
        print(f"\nError occurred while trying to fix the file: {e}")


def main():
    """
    Main function to run the script.
    """
    arguments = docopt(__doc__)
    filename = arguments["--file"]

    if check_file(filename):
        response = input(
            "Do you want to fix the characters and save a new file? (yes/no): "
        )
        if response.lower().strip() == "yes":
            replace_chars(filename)


if __name__ == "__main__":
    main()
