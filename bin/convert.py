import yaml
import os
from typing import List, Dict, Any

# Custom Dumper to handle multiline strings and specifically BibTeX
class MultilineDumper(yaml.Dumper):
    def represent_scalar(self, tag, value, style=None):
        # Explicitly handle BibTeX literal block style tagged with LiteralString
        if isinstance(value, LiteralString):
            return super().represent_scalar('tag:yaml.org,2002:str', str(value), style='|')

        # Original logic for other long strings not explicitly marked as literal
        if isinstance(value, str) and len(value) > 70 and '\n' not in value:
            return super().represent_scalar(tag, value, style='|')
        else:
            return super().represent_scalar(tag, value, style)

# Define a custom class to tag strings that should always be literal blocks
class LiteralString(str):
    pass

# Register a representer for our custom LiteralString class
def represent_literal_string(dumper, data):
    # Force the literal block style ('|') for LiteralString instances
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')

MultilineDumper.add_representer(LiteralString, represent_literal_string)


def transform_entry_ratings(entry: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transforms the 'ratings' list in a benchmark entry into a nested dictionary
    format, grouping rating and reason by category (e.g., 'problem_spec' becomes 'specification').
    Also ensures BibTeX citations are properly formatted as multiline strings.

    Args:
        entry (Dict[str, Any]): A single benchmark entry dictionary.

    Returns:
        Dict[str, Any]: The transformed benchmark entry with ratings in the new format.
    """
    # --- Handle 'ratings' transformation ---
    if 'ratings' in entry and isinstance(entry['ratings'], list):
        transformed_ratings: Dict[str, Dict[str, Any]] = {}
        CATEGORY_MAPPING = {
            "problem_spec": "specification",
            "dataset": "dataset",
            "metrics": "metrics",
            "reference_solution": "reference_solution",
            "documentation": "documentation",
            "software": "software",
        }
        for item in entry['ratings']:
            if not isinstance(item, dict):
                continue
            for key, value in item.items():
                if key.endswith('_rating'):
                    flat_category_key = key.replace('_rating', '')
                    category_name = CATEGORY_MAPPING.get(flat_category_key, flat_category_key)
                    if category_name not in transformed_ratings:
                        transformed_ratings[category_name] = {}
                    transformed_ratings[category_name]['rating'] = value
                elif key.endswith('_reason'):
                    flat_category_key = key.replace('_reason', '')
                    category_name = CATEGORY_MAPPING.get(flat_category_key, flat_category_key)
                    if category_name not in transformed_ratings:
                        transformed_ratings[category_name] = {}
                    # Strip any leading/trailing whitespace and then strip explicit \n
                    transformed_ratings[category_name]['reason'] = value.strip().replace('\\n', '\n')

        entry['ratings'] = transformed_ratings

    # --- Handle 'cite' field for multiline BibTeX ---
    if 'cite' in entry and isinstance(entry['cite'], list):
        processed_citations = []
        for citation_str in entry['cite']:
            if isinstance(citation_str, str):
                # Critical step: Convert YAML-escaped newlines and then strip.
                # Also remove any literal backslashes used for line continuation like `\ `
                clean_citation = citation_str.replace('\\n', '\n').replace('\\ ', ' ').strip()
                
                # If the string starts with "@" and contains "{" it's likely BibTeX.
                if clean_citation.startswith('@') and '{' in clean_citation:
                    # Wrap it in LiteralString to force '|' style representation
                    processed_citations.append(LiteralString(clean_citation))
                else:
                    processed_citations.append(clean_citation)
            else:
                processed_citations.append(citation_str) # Keep non-string items as is
        entry['cite'] = processed_citations

    return entry

def transform_yaml_file(input_filepath: str, output_filepath: str) -> None:
    """
    Reads a YAML file, transforms the 'ratings' section of each entry,
    and writes the updated content to a new YAML file.
    Uses a custom Dumper to print multiline strings for long text.

    Args:
        input_filepath (str): Path to the input YAML file.
        output_filepath (str): Path to the output YAML file.
    """
    if not os.path.exists(input_filepath):
        print(f"Error: Input file not found at {input_filepath}")
        return

    with open(input_filepath, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    if not isinstance(data, list):
        print(f"Warning: Input YAML is not a list of entries. Skipping transformation and writing original data.")
        os.makedirs(os.path.dirname(output_filepath) or '.', exist_ok=True)
        with open(output_filepath, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, indent=2, sort_keys=False, Dumper=MultilineDumper, default_flow_style=False, allow_unicode=True)
        return

    transformed_data = [transform_entry_ratings(entry) for entry in data]

    os.makedirs(os.path.dirname(output_filepath) or '.', exist_ok=True)

    with open(output_filepath, 'w', encoding='utf-8') as f:
        yaml.dump(transformed_data, f, indent=2, sort_keys=False, Dumper=MultilineDumper, default_flow_style=False, allow_unicode=True)
    print(f"Transformed data written to {output_filepath}")

# --- Main execution ---
if __name__ == "__main__":
    input_file_path = "source/benchmarks.yaml"
    output_file_path = "source/abc.yaml" # Output path also changed to source/abc.yaml

    print(f"Attempting to transform ratings and citations from '{input_file_path}' to '{output_file_path}'...")
    transform_yaml_file(input_file_path, output_file_path)

    if os.path.exists(output_file_path):
        with open(output_file_path, 'r', encoding='utf-8') as f:
            print(f"\n--- Transformed Output (content of {output_file_path}) ---")
            print(f.read())
    else:
        print(f"Output file '{output_file_path}' was not created (likely due to input file error).")