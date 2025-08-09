import re
import sys
import os

def remove_overfull_errors(log_content: str) -> str:
    """
    Removes all "Overfull \hbox" and "Overfull \vbox" error messages
    from a LaTeX log file content string.

    Args:
        log_content: The full content of the LaTeX log file as a string.

    Returns:
        A new string with all "Overfull" error messages removed.
    """
    # Regex pattern to match "Overfull \hbox" or "Overfull \vbox"
    # followed by anything until a new log entry marker or end of string.
    # LaTeX log entries typically start on a new line.
    # We'll use re.DOTALL to allow '.' to match newlines for multi-line messages
    # and re.MULTILINE to allow '^' to match the start of lines.

    # Pattern for Overfull \hbox:
    # Matches "Overfull \hbox" and then non-greedily matches any characters
    # until it hits a newline followed by an optional space/tab and a '[' (for page numbers),
    # or a newline followed by 'l.' (for line numbers),
    # or a newline followed by 'LaTeX Warning:', '!' (another error), 'Underfull',
    # or the end of the string.
    overfull_hbox_pattern = re.compile(
        r'Overfull \\hbox\b.*?(?=\n\s*\[\d+\]|\n\s*l\.\d+|\nLaTeX Warning:|\n!|\nUnderfull|.)',
        re.DOTALL | re.MULTILINE
    )

    # Pattern for Overfull \vbox (less common, but good to include)
    overfull_vbox_pattern = re.compile(
        r'Overfull \\vbox\b.*?(?=\n\s*\[\d+\]|\n\s*l\.\d+|\nLaTeX Warning:|\n!|\nUnderfull|.)',
        re.DOTALL | re.MULTILINE
    )

    # First, remove Overfull \hbox messages
    cleaned_content = overfull_hbox_pattern.sub('', log_content)

    # Then, remove Overfull \vbox messages from the already partially cleaned content
    cleaned_content = overfull_vbox_pattern.sub('', cleaned_content)

    # You might end up with empty lines or multiple newlines after removal.
    # It's good practice to clean these up for better readability.
    # Replace multiple consecutive newlines with a single newline.
    cleaned_content = re.sub(r'\n{2,}', '\n', cleaned_content)
    # Remove any leading/trailing whitespace from lines
    cleaned_content = '\n'.join([line.strip() for line in cleaned_content.splitlines() if line.strip()])

    return cleaned_content



def remove_bad_box_details(log_content: str) -> str:
    """
    Removes specific detailed "bad box" messages like
    "(12.71114pt too wide) in paragraph at lines 53--53" or
    "(zero depth) too high in paragraph at lines 100--101"
    from a LaTeX log file content string.

    Args:
        log_content: The full content of the LaTeX log file as a string.

    Returns:
        A new string with the specified bad box detail messages removed.
    """
    # Regex pattern to match the specific bad box detail message format.
    # This pattern is very specific to avoid unintended removals.
    # It accounts for:
    # - Start of line with optional leading whitespace: `^\s*` (due to re.MULTILINE)
    # - Opening parenthesis `\(`
    # - Measurement: `\d+\.\d+pt` (e.g., "12.71114pt") OR "zero depth" OR "zero height"
    # - " too wide" or " too high": ` too (wide|high)`
    # - Closing parenthesis `\)`
    # - " in paragraph at lines" or " in alignment at lines": ` in (paragraph|alignment) at lines `
    # - Line range: `\d+--\d+`
    # - Optional trailing whitespace and end of line: `\s*$`
    bad_box_detail_pattern = re.compile(
        r'^\s*\((\d+\.\d+pt|zero depth|zero height) too (wide|high)\) in (paragraph|alignment) at lines \d+--\d+\s*$',
        re.MULTILINE
    )

    cleaned_content = bad_box_detail_pattern.sub('', log_content)

    # Clean up multiple newlines and empty lines that might result from removal.
    cleaned_content = re.sub(r'\n{2,}', '\n', cleaned_content)
    cleaned_content = '\n'.join([line.strip() for line in cleaned_content.splitlines() if line.strip()])

    return cleaned_content

import re

def remove_enumitem_negative_labelwidth_warning(log_content: str) -> str:
    """
    Removes the specific multi-line warning from Package enumitem regarding
    'Negative labelwidth' from a LaTeX log file content string.

    Example warning:
    Package enumitem Warning: Negative labelwidth. This does not make much
    (enumitem)                sense, on input line 3.

    Args:
        log_content: The full content of the LaTeX log file as a string.

    Returns:
        A new string with the specified warning messages removed.
    """
    enumitem_warning_pattern = re.compile(
        r'Package enumitem Warning: Negative labelwidth\. This does not make much\n'
        r'\(enumitem\)\s+sense, on input line \d+\.',
        re.MULTILINE
    )

    cleaned_content = enumitem_warning_pattern.sub('', log_content)

    cleaned_content = re.sub(r'\n{2,}', '\n', cleaned_content)
    cleaned_content = '\n'.join([line.strip() for line in cleaned_content.splitlines() if line.strip()])

    return cleaned_content


def remove_specific_overfull_hbox_citation_error(log_content: str) -> str:
    """
    Removes a specific multi-line 'Overfull \hbox' error pattern related to citations
    or similar entries, from a LaTeX log file content string.

    The pattern explicitly matches:
    Line 1: Overfull \hbox (XX.YYYpt too wide/high) in paragraph/alignment at lines N--N
    Line 2: []|SOME_FONT_OR_TEXT_IDENTIFIER| (e.g., []|\OT1/cmr/bx/n/8 Citation|)
    Line 3: [] (potentially with leading whitespace)

    Args:
        log_content: The full content of the LaTeX log file as a string.

    Returns:
        A new string with the specified error messages removed.
    """
    # Define the regex pattern for the specific three-line error.
    # Each part matches a line and is separated by '\n' (newline).
    # '\s*' is used to account for any leading/trailing whitespace on lines.
    # '\(' and '\)' escape literal parentheses.
    # '\[' and '\]' escape literal square brackets.
    # '\|' escapes literal pipe characters.
    # '\d+\.\d+pt' matches floating-point numbers followed by 'pt'.
    # '(?:...)' creates a non-capturing group.
    # '\S+' matches one or more non-whitespace characters (for the text between pipes).
    
    specific_overfull_pattern = re.compile(
        # Line 1: Overfull \hbox (measurement too wide/high) in paragraph/alignment at lines X--Y
        r'Overfull \\hbox \((?:\d+\.\d+pt|zero depth|zero height) too (?:wide|high)\) in (?:paragraph|alignment) at lines \d+--\d+\s*\n'
        # Line 2: []|SOME_TEXT| (e.g., []|\OT1/cmr/bx/n/8 Citation|)
        r'\[\]\|\S+\|\s*\n'
        # Line 3: [] (possibly with leading whitespace)
        r'\s*\[\]',
        re.MULTILINE # Allows `^` and `$` to match start/end of lines (though not explicitly used in this pattern,
                      # it's good for robust line-aware parsing).
    )

    # Perform the substitution, replacing the matched error block with an empty string.
    cleaned_content = specific_overfull_pattern.sub('', log_content)

    # Clean up any residual multiple newlines or completely empty lines that might
    # result from the removal, ensuring a tidy output.
    cleaned_content = re.sub(r'\n{2,}', '\n', cleaned_content)
    # Remove any leading/trailing whitespace from lines and filter out completely empty lines.
    cleaned_content = '\n'.join([line.strip() for line in cleaned_content.splitlines() if line.strip()])

    return cleaned_content

def remove_before_specific_string(content: str, target_string: str) -> str:
    """
    Removes all characters from a string that appear before the first
    occurrence of a specified target string, including the target string itself.

    Args:
        content: The input string (e.g., the LaTeX log file content).
        target_string: The string marker to search for (e.g., 'Package caption Info: End \AtBeginDocument code.').

    Returns:
        A new string containing only the content from (and including)
        the target string onwards. If the target string is not found,
        the original content is returned.
    """
    # Find the starting index of the target string
    index = content.find(target_string)

    # If the target string is found, return the part of the string
    # starting from its index. Otherwise, return the original content.
    
    if index != -1:
        result = content[index:]
    else:
        result = content
    return content
    

def delete_lines_with_substring(log_content: str, substring_to_delete: str) -> str:
    """
    Deletes all lines from a string that contain a specified substring.

    Args:
        log_content: The full content of the LaTeX log file as a string.
        substring_to_delete: The string that, if present in a line, will cause that line to be deleted.

    Returns:
        A new string with all lines containing the specified substring removed.
    """
    cleaned_lines = []
    lines = log_content.splitlines()

    for line in lines:
        if substring_to_delete not in line:
            cleaned_lines.append(line)
    
    joined_content = "\n".join(cleaned_lines)

    # Optional: Clean up multiple newlines or empty lines for tidier output.
    cleaned_content = re.sub(r'\n{2,}', '\n', joined_content)
    cleaned_content = '\n'.join([line.strip() for line in cleaned_content.splitlines() if line.strip()])

    return cleaned_content

def delete_before_last_occurrence(main_string: str, target_string: str) -> str:
    """
    Finds the last occurrence of a given target string within a main string
    and returns everything after it.

    Args:
        main_string: The string to search within.
        target_string: The string to find the last occurrence of.

    Returns:
        A new string containing everything after the last occurrence of the
        target_string. If the target_string is not found, the original
        main_string is returned.
    """
    last_index = main_string.rfind(target_string)

    if last_index != -1:  # If the target_string was found
        return main_string[last_index + len(target_string):]
    else:
        return main_string  # Target string not found, return original string
    
# #####################################################
# LATEX LOG FILE PRINTER
# #####################################################

def print_latex_log(filename="content/tex/benchmarks.log"):
    """
    Prints the content of the LaTeX log file to the console.

    Args:
        filename (str): Path to the LaTeX log file.
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        Console.error(f"Log file '{filename}' not found.")
    except Exception as e:
        Console.error(f"Error reading log file '{filename}': {e}")

    print(content)
    content = remove_overfull_errors(content)
    content = remove_bad_box_details(content)
    content = remove_enumitem_negative_labelwidth_warning(content)
    content = remove_specific_overfull_hbox_citation_error(content)
    content = delete_before_last_occurrence(content, "AtBeginDocument")
    #content = remove_before_specific_string(content, "AtBeginDocument code.")  
    #content = remove_before_specific_string (content, "(./benchmarks.out) (./benchmarks.out")
    content = delete_lines_with_substring(content, "Overfull \hbox") 
    content = delete_lines_with_substring(content, "[]")
    print("\nCleaned Log Content (Overfull Errors Removed):\n")
    print(content)