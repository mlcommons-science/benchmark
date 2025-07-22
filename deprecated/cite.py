from pybtex.database import parse_string
from pybtex.plugin import find_plugin

from yaml_manager import YamlManager
from latex_writer import LatexWriter

# # Example BibTeX entry
# bibtex_examples = ["""
# @article{sample2025,
#   author = {John Doe and Jane Smith},
#   title = {Understanding AI in Modern Applications},
#   journal = {Journal of AI Research},
#   year = {2025},
#   volume = {50},
#   pages = {123-145},
#   doi = {10.1234/ai.2025.56789}
# }
# """,
# """ 
# @article{sample0000,
#   author = {John Cena and Jane Smith},
#   title = {Understanding AI in Modern Applications},
#   journal = {Journal of AI Research},
#   year = {2025},
#   volume = {50},
#   pages = {123-145},
#   doi = {10.1234/ai.2025.56789}
# }
# """]

YAML_FILE = "source/benchmarks-addon-new.yaml"
DEBUG = False
def bibtex_to_label(entry: str):
    try:
        label = LatexWriter._extract_cite_label(entry)
        if DEBUG:
            print(label)
        # Parse the BibTeX entry with the 'bibtex' format
        bib_data = parse_string(entry, bib_format='bibtex')
    

        # Use the default citation style (plain)
        style = find_plugin('pybtex.style.formatting', 'plain')
        formatter = style()

        # Format the citation and extract the first item from the generator
        formatted_citation = next(formatter.format_entries(bib_data.entries.values()))

        # Replace LaTeX commands with ASCII characters
        citation_text = str(formatted_citation.text)
        citation_text = citation_text.replace('<newblock>', ' ').replace('<ndash>', '-')
    except Exception as e:
        positions = find_string_occurrences_in_file(label, YAML_FILE)
        if DEBUG:
            print(str(e))
            print("Error in label: " + label + " for the entry " + entry)
        for pos in positions:
            print(f"{YAML_FILE}: line {pos[0]}, column {pos[1]} -- {str(e)}")
        
        return ""

    return citation_text

def find_string_occurrences_in_file(search_string, file_path):
    """
    Find all line numbers and column numbers where the search_string occurs in the file.

    :param search_string: The string to search for
    :param file_path: The path to the file
    :return: A list of tuples, each containing the line number and column number
    """
    occurrences = []
    
    try:
        with open(file_path, 'r') as file:
            # Iterate through the file line by line
            for line_num, line in enumerate(file, start=1):
                start_idx = 0
                while True:
                    # Find the next occurrence of the search_string in the current line
                    start_idx = line.find(search_string, start_idx)
                    if start_idx == -1:
                        break
                    # Calculate the column number (start_idx + 1 for 1-based index)
                    occurrences.append((line_num, start_idx + 1))
                    start_idx += 1  # Move to the next character to continue searching
    except FileNotFoundError:
        print(f"The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return occurrences



m = YamlManager(YAML_FILE)
dicts = m.get_table_formatted_dicts()

for yaml_dict in dicts:
    for citation in yaml_dict.get("cite", []):
        print(bibtex_to_label(citation))

for yaml_dict in dicts:
    for citation in yaml_dict.get("cite", []):
        print(bibtex_to_label(citation))