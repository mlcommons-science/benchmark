import yaml
import os
import sys  # Import sys to handle command-line arguments
from cloudmesh.common.util import banner


def green(text: str) -> str:
    """
    Returns the input text formatted in green color for terminal output.
    """
    return f"\033[92m{text}\033[0m"


def red(text: str) -> str:
    """
    Returns the input text formatted in red color for terminal output.
    """
    return f"\033[91m{text}\033[0m"


def purple(text: str) -> str:
    """
    Returns the input text formatted in purple color for terminal output.
    """
    return f"\033[95m{text}\033[0m"


WARNING = purple("WARNING")
OK = green("OK")
RED = red("ERROR")

TODO = [
    "None",
    "none",
    "TODO",
    "unkown",
    "UNKOWN",
    "N/A",
    "na",
    "n/a",
    "null",
    "NULL",
    "None",
]


def fill_string(s: str, target_length: int) -> str:
    """
    Fills a string to a specified target length.
    If the string is shorter, it's padded with spaces on the right.
    If the string is longer, it's truncated to the target length.

    Args:
        s (str): The input string.
        target_length (int): The desired final length of the string.

    Returns:
        str: The string filled or cut to the target length.
    """
    if target_length < 0:
        raise ValueError("Target length cannot be negative.")

    if len(s) > target_length:
        return s[:target_length]  # Truncate if longer than target_length
    else:
        return s.ljust(target_length)  # Pad with spaces on the right if shorter


def validate_yaml_entries(data_filepath=None, structure_filepath=None) -> bool:
    """
    Validates entries in a YAML data file against the structure and data types
    defined by an arbitrary example from a separate YAML structure file.

    Assumptions for the STRUCTURE FILE:
    1. It must contain a single YAML object at its top-level.
    2. This object must either be:
       a. A dictionary (which will directly serve as the template).
       b. A list, whose first item MUST be a dictionary (this dictionary
          will serve as the template).

    Assumptions for the DATA FILE:
    1. Its top-level structure must be a list of entries.
    2. Each entry in this list is expected to be a dictionary.

    Args:
        structure_filepath (str): The path to the YAML file defining the structure.
        data_filepath (str): The path to the YAML file containing the data to validate.

    Returns:
        bool: True if all entries in the data file conform to the structure
              defined in the structure file, False otherwise.
    """
    if structure_filepath is None:
        structure_filepath = data_filepath

    # --- Load and process the STRUCTURE FILE ---
    arbitrary_example = None
    try:
        with open(structure_filepath, "r", encoding="utf-8") as f:
            structure_data = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Structure file '{structure_filepath}' not found.")
        return False
    except yaml.YAMLError as e:
        print(f"Error parsing structure file '{structure_filepath}': {e}")
        return False
    except Exception as e:
        print(
            f"An unexpected error occurred while reading structure file '{structure_filepath}': {e}"
        )
        return False

    if isinstance(structure_data, dict):
        arbitrary_example = structure_data
    elif isinstance(structure_data, list):
        if not structure_data:
            print(
                f"Error: Structure file '{structure_filepath}' contains an empty list. Cannot define a template."
            )
            return False
        if not isinstance(structure_data[0], dict):
            print(
                f"Error: The first item in the list of structure file '{structure_filepath}' is not a dictionary. Cannot define a template."
            )
            return False
        arbitrary_example = structure_data[0]
    else:
        print(
            f"Error: Structure file '{structure_filepath}' must define a top-level dictionary or a list starting with a dictionary to serve as a template."
        )
        return False

    print(f"\n--- Structure loaded from '{structure_filepath}' ---")
    print(f"**Reference structure (from arbitrary example):**")
    for k, v in arbitrary_example.items():
        print(f"  - '{k}': Type = {type(v).__name__}")
    print("-" * 70)

    # --- Load and process the DATA FILE ---
    try:
        with open(data_filepath, "r", encoding="utf-8") as f:
            data_to_validate = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Data file '{data_filepath}' not found.")
        return False
    except yaml.YAMLError as e:
        print(f"Error parsing data file '{data_filepath}': {e}")
        return False
    except Exception as e:
        print(
            f"An unexpected error occurred while reading data file '{data_filepath}': {e}"
        )
        return False

    if not isinstance(data_to_validate, list):
        print(
            f"Validation Error: The top-level YAML structure of '{data_filepath}' must be a list of entries."
        )
        print("Example: - item1_key: value1")
        print("         - item2_key: value2")
        return False

    if not data_to_validate:  # Check if the list is empty
        print(
            f"Note: The data file '{data_filepath}' contains an empty list. No entries to validate."
        )
        return True  # Considered valid as there's nothing to fail

    print(f"\n--- Verifying entries in data file '{data_filepath}' ---")
    all_entries_valid = True

    # Iterate through all entries in the data file
    for i, entry in enumerate(data_to_validate):
        i = i + 1  # Start counting from 1 for user-friendly output
        no = f"{i:4d}"
        name = entry.get(
            "name", f"Entry {no}"
        )  # Use 'name' key if available, else default to "Entry i"
        name = fill_string(name, 30)
        print(f"Checking {no}: {name}", end="...  ")
        entry_is_current_valid = True
        issues_found = []

        if not isinstance(entry, dict):
            issues_found.append(
                f"Expected a dictionary, but found type '{type(entry).__name__}'."
            )
            entry_is_current_valid = False
            print(f"  Status: INVALID. Reason: {issues_found[0]}")
            all_entries_valid = False
            continue

        # 1. Check for missing keys (keys in example but not in current entry)
        for key in arbitrary_example:
            if key not in entry:
                issues_found.append(
                    f"{RED} Missing key: '{key}' (expected based on reference)."
                )
                entry_is_current_valid = False
            else:
                # 2. Check for type mismatch
                expected_type = type(arbitrary_example[key])
                actual_value = entry[key]
                actual_type = type(actual_value)

                if actual_value in TODO:
                    issues_found.append(
                        f"{WARNING} Key '{key}': Value is marked as TODO or N/A, which may need to be changed."
                    )
                    entry_is_current_valid = False
                

                if expected_type != actual_type:
                    issues_found.append(
                        f"{RED} Key '{key}': Expected type '{expected_type.__name__}', but found '{actual_type.__name__}' for value '{actual_value}'."
                    )
                    entry_is_current_valid = False

        # 3. Check for extra keys (keys in current entry but not in example)
        for key in entry:
            if key not in arbitrary_example:
                issues_found.append(
                    f"Extra key: '{key}' found (not present in reference example)."
                )
                # Uncomment the next line if extra keys should make the entry invalid:
                # entry_is_current_valid = False

        if entry_is_current_valid:
            print(f"  {OK}:  Conforms to the reference structure and types.")
        else:
            print("  Status: INVALID. Issues found:")
            for issue in issues_found:
                print(14 * " ", f"- {issue}")
            all_entries_valid = False

    print("\n" + "=" * 70)
    if all_entries_valid:
        print(
            "Validation Summary: All data entries successfully conform to the reference structure."
        )
    else:
        print(
            "Validation Summary: Some data entries failed to conform to the reference structure. Please review the issues above."
        )
    print("=" * 70)

    return all_entries_valid


# --- Main execution block ---
if __name__ == "__main__":
    benchmark_addon = "source/benchmarks-addon.yaml"
    benchmarks = "source/benchmarks.yaml"

    banner(f"Running validation using '{benchmarks}")

    is_valid = validate_yaml_entries(benchmarks)

    print(f"\nFinal Validation Result for '{benchmarks}': {is_valid}")

    banner(
        f"# Running validation using '{benchmarks} with '{benchmark_addon}' as structure"
    )

    is_valid = validate_yaml_entries(benchmarks, benchmark_addon)
    print(f"\nFinal Validation Result for '{benchmarks}': {is_valid}")
