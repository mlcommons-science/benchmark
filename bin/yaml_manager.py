"""
Contains a class for YAML file loading and formatting.

Example program from:

from pprint import pprint
from yaml_manager import YamlManager

manager = YamlManager("source/benchmarks-addon-new.yaml")

pprint(manager.data) # returns the raw list of dicts
pprint(manager.flat) # returns the flattened dicts as a list such that keys are . separated instead of hirarchical

This is some function that Reece and Anjay implemented I do not fully understand, but is used to create flat dicts.
I am not sure what this has to do with a table and what is internally done.

I think this should be separated from flatten

flat = manager.get_flat_dicts())


"""

import yaml
import json
import re
import sys
import requests
from cloudmesh.common.console import Console
from pprint import pprint
from requests.exceptions import (
    RequestException,
    Timeout,
    ConnectionError,
    HTTPError,
    MissingSchema,
    InvalidSchema,
    InvalidURL,
    TooManyRedirects,
    SSLError,
)
from collections import OrderedDict
import codecs

from field_format_manager import FieldFormatManager
from cloudmesh.common.util import banner


def find_unicode_chars(filename=None):
    """
    Checks a file for specific non-ASCII Unicode characters, prints their
    location, and suggests ASCII alternatives.
    """
    # Define a dictionary mapping Unicode characters to their suggested ASCII alternatives
    # You can expand this dictionary with more mappings as needed.
    UNICODE_TO_ASCII_MAP = {
        "ä": "ae",
        "ö": "oe",
        "ü": "ue",  # German umlauts
        "é": "e",
        "è": "e",
        "ê": "e",
        "ë": "e",  # French accents
        "ç": "c",  # French/Portuguese cedilla
        "ñ": "n",  # Spanish enye
        "á": "a",
        "à": "a",
        "â": "a",
        "ã": "a",  # Portuguese/Spanish/French accents
        "í": "i",
        "ì": "i",
        "î": "i",  # Various accents
        "ó": "o",
        "ò": "o",
        "ô": "o",
        "õ": "o",  # Various accents
        "ú": "u",
        "ù": "u",
        "û": "u",  # Various accents
        "æ": "ae",
        "ø": "oe",
        "å": "aa",  # Nordic characters
        "ß": "ss",  # German sharp s
        "©": "(c)",  # Copyright symbol
        "®": "(R)",  # Registered symbol
        "™": "(TM)",  # Trademark symbol
        "–": "-",  # En dash
        "—": "-",  # Em dash
        "…": "...",  # Ellipsis
        "„": '"',  # German/East European double low quotation mark
        "”": '"',  # Right double quotation mark
        "“": '"',  # Left double quotation mark
        "’": "'",  # Right single quotation mark (apostrophe)
        "‘": "'",  # Left single quotation mark
        # Add more mappings as needed
        # Example for Cyrillic (note: not all Cyrillic have simple 1-to-1 ASCII transliterations)
        "П": "P",
        "р": "r",
        "и": "i",
        "в": "v",
        "е": "e",
        "т": "t",  # Partial for "Привет"
        "!": "!",  # Example: if you wanted to specifically suggest for common punctuation
    }
    found = set()
    try:
        with codecs.open(filename, "r", encoding="utf-8", errors="strict") as f:
            for line_num, line in enumerate(f, 1):
                line_content_printed = False
                for col_num, char in enumerate(line, 1):
                    # Check if the character is a specific Unicode character we want to handle
                    if char in UNICODE_TO_ASCII_MAP:
                        found.add(char)
                        if not line_content_printed:
                            print(79 * "-")
                            Console.error(
                                f"Specific Unicode character(s) found on line {line_num}:"
                            )
                            Console.info(f"  Content: '{line.strip()}'")
                            line_content_printed = True

                        suggested_alternative = UNICODE_TO_ASCII_MAP[char]
                        Console.info(
                            f"    - Found '{char}' (U+{ord(char):04X}) at column {col_num}. Suggest alternative: '{suggested_alternative}'"
                        )
                    else:
                        # Optionally, you can also check for *any* non-ASCII character here
                        # if you want to report characters not in your specific map.
                        try:
                            char.encode("ascii")
                        except UnicodeEncodeError:
                            found.add(char)
                            if not line_content_printed:
                                Console.info(
                                    f"\nNon-ASCII Unicode character(s) found on line {line_num}:"
                                )
                                Console.info(f"  Content: '{line.strip()}'")
                                line_content_printed = True
                            Console.info(
                                f"    - Found '{char}' (U+{ord(char):04X}) at column {col_num}. No specific alternative suggested."
                            )

    except FileNotFoundError:
        Console.error(f"Error: File '{filename}' not found.")
    except Exception as e:
        Console.error(f"An unexpected error occurred: {e}")

    print("#" * 79)
    print("# Summary of found characters:")
    print("#" * 79)
    for c in found:
        if c not in UNICODE_TO_ASCII_MAP:
            Console.warning(
                f"Found character '{c}' (U+{ord(c):04X}) not in the mapping. No alternative suggested."
            )
        else:
            Console.info(
                f"Found character '{c}' (U+{ord(c):04X}) with suggested alternative '{UNICODE_TO_ASCII_MAP[c]}'."
            )


# --- Example Usage ---
if __name__ == "__main__":
    # Create a dummy file with various unicode characters
    with open("example_with_alternatives.txt", "w", encoding="utf-8") as f:
        f.write("This line has umlauts: äöü.\n")
        f.write("And French accents: éàç.\n")
        f.write("A Spanish ñ and Nordic øåæ.\n")
        f.write("Copyright © and trademark ™ symbols.\n")
        f.write("Dashes: – and — and ellipsis …\n")
        f.write("Quotes: “Hello world!” and single ‘quote’.\n")
        f.write("Russian: Привет!\n")  # Some Cyrillic
        f.write("Line with a character not in map: ♪ (music note)\n")
        f.write("Final line.\n")

    print("Checking 'example_with_alternatives.txt' for specific Unicode alternatives:")
    unicode_alternatives("example_with_alternatives.txt")
    print("\n" + "=" * 50 + "\n")

    # Test with a file that has no problematic unicodes
    with open("example_ascii_only.txt", "w", encoding="utf-8") as f:
        f.write("This is an ASCII only file.\n")
        f.write("No special characters here.\n")

    print("Checking 'example_ascii_only.txt':")
    unicode_alternatives("example_ascii_only.txt")


def clean_string(s):
    # Replace spaces with underscores
    s = s.replace(" ", "_")
    # Remove all characters except a-z, A-Z, -, and _
    s = re.sub(r"[^a-zA-Z\-_]", "", s)
    return str(s)


class YamlManager(object):
    """
    Loads, stores, and formats the contents of YAML files.

    Inputs are loaded via filepaths.
    The class can give the raw output of `yaml.safe_load` (as a list of dictionaries)
    or as a list of dictionaries for table output.
    """

    def __init__(
        self,
        yamls: (
            str | list[str] | None
        ) = None,  # Made yamls optional for direct instantiation
        overwriting_contents: bool = True,
        printing_syntax_errors: bool = True,
    ):
        """
        Creates a new YamlManager in charge of the contents of `yamls`.

        Parameters:
            yamls (str or list[str] or None): one or more YAML filepaths to load from. If None, initializes empty.
            overwriting_contents (bool, default=True): True if overwriting existing contents, False if appending to existing contents
            printing_syntax_errors (bool, default=True): whether to print warnings to the console if a YAML syntax error is found
        """
        self._yaml_dicts: list[dict] = []  # Initialize internal storage directly
        if yamls:  # Only load if yamls are provided at init
            self.load(
                yamls, overwrite=overwriting_contents, verbose=printing_syntax_errors
            )

    # Add this __iter__ method
    def __iter__(self):
        """
        Makes the YamlManager instance iterable, allowing direct iteration over its loaded data.
        Example: for entry in manager: ...
        """
        return iter(self._yaml_dicts)

    # Add this __len__ method for convenience (optional, but good practice for collections)
    def __len__(self):
        """
        Returns the number of entries in the loaded YAML data.
        Example: len(manager)
        """
        return len(self._yaml_dicts)

    # Add this __getitem__ method for indexing (optional, but good practice for collections)
    def __getitem__(self, index):
        """
        Allows indexing into the loaded YAML data.
        Example: manager[0]
        """
        return self._yaml_dicts[index]

    @property
    def data(self) -> list[dict]:
        """
        Returns the raw list of dictionaries loaded by the manager.
        """
        return self._yaml_dicts

    @property
    def flat(self) -> list[dict]:
        """
        Returns the flattened dictionaries as a list such that keys are dot-separated instead of hierarchical.
        """
        return self.get_flat_dicts()

    # ---------------------------------------------------------------------------------------------------------
    # File Loading
    # ---------------------------------------------------------------------------------------------------------

    def load_single_yaml_file(
        self, file_path: str, enable_error_messages: bool = True
    ) -> list[dict]:  # type: ignore
        """
        Loads a YAML file containing a flat list of field-level entries,
        and groups them into full benchmark entries using 'name' as the reset key.

        Parameters:
            file_path (str): filepath to load from
            enable_error_messages (bool): whether to print syntax errors to the console. Default True
        Returns:
            list of benchmark entries for the YAML file
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = yaml.safe_load(f)

            if content is None:  # Handle empty YAML files
                return []
            elif isinstance(content, dict):
                Console.warning(
                    f'YAML file "{file_path}" is a dictionary. Treating it as a list containing one dictionary.'
                )
                # The sys.exit(1) here is problematic for library usage.
                # It's better to raise an error or just return, letting the caller decide to exit.
                # For now, keeping it as per your original, but flagging for review.
                # If this is truly a critical error, consider raising a custom exception.
                sys.exit(1)
                # return [content] # This line is unreachable due to sys.exit(1)

            elif isinstance(content, list):
                return content

            else:
                raise ValueError(
                    "Unsupported YAML format. Expected a dict or list of dicts."
                )
        except FileNotFoundError:
            if enable_error_messages:
                Console.error(f"File not found: '{file_path}'")
                sys.exit(1)  # Same note as above regarding sys.exit(1)

        except yaml.YAMLError as e:
            if enable_error_messages:
                Console.error(f'YAML syntax error in "{file_path}": \n{e}')
            return []

    def load(
        self, file_paths: str | list[str], overwrite: bool = True, verbose: bool = True
    ) -> list[dict]:
        """
        Loads the contents of `file_paths` into this YamlManager.

        If `overwrite_existing` is True, any previous contents are overwritten upon load.
        If a YAML file contains syntax errors, that file is skipped.
        Raises a FileNotFoundError if any specified file does not exist.

        Parameters:
            file_paths (str or list[str]): File path(s) to load from.
            overwrite (bool, default=True): Whether to overwrite the manager's existing contents.
            verbose (bool, default=True): Whether to print error messages for YAML syntax issues.

        Returns:
            list[dict]: The updated list of YAML dictionaries stored in the manager.
        """
        # Normalize file_paths to always be a list
        paths_to_load = [file_paths] if isinstance(file_paths, str) else file_paths

        newly_loaded_records = []
        for path in paths_to_load:
            # Each file's content (which is guaranteed to be a list) is extended
            # Catching specific errors from _load_single_yaml_file
            try:
                newly_loaded_records.extend(self.load_single_yaml_file(path, verbose))
            except (FileNotFoundError, ValueError) as e:
                # If sys.exit(1) is called in load_single_yaml_file, these exceptions
                # might not be reached. But if sys.exit(1) were removed, this catch
                # would be important for graceful handling.
                if verbose:
                    Console.error(f"Error loading '{path}': {e}")
                # Depending on desired behavior, you might re-raise or just skip.
                # Given current sys.exit(1) in load_single_yaml_file, this might be redundant
                # if the program exits immediately. If sys.exit(1) is removed, then this
                # 'continue' ensures the loop proceeds to next file after an error.
                continue

        if overwrite:
            self._yaml_dicts = newly_loaded_records
        else:
            self._yaml_dicts.extend(newly_loaded_records)

        # BUG Fix: self.data is now a property, no need to assign to it.
        # The internal storage is _yaml_dicts.
        # self.data = self._yaml_dicts # This line is removed.

        found = []
        for entry in self._yaml_dicts:
            key = clean_string(entry.get("name", "unknown")).lower()
            if key in found:
                Console.error(
                    f"Duplicate entry name found: {key}. Please ensure all entries have unique names."
                )
            found.append(key)
            entry["id"] = key

        return self._yaml_dicts  # Or return self.data

    # ---------------------------------------------------------------------------------------------------------
    # Contents Presentation
    # ---------------------------------------------------------------------------------------------------------

    def get_dicts(self) -> list[dict]:
        """
        BUG: This function is deprecated and should be replaced with manager.data.

        Returns a list of the raw internal dictionaries read to by the manager. Not intended for writing to tables.

        DO NOT MODIFY THE OUTPUT OF THIS FUNCTION!
        The values returned are shallow copies. Any modification will affect the YAML manager's contents.

        Returns:
            list[dict]: manager's current file contents, as dictionaries
        """
        return self.data

    def _flatten_dict(self, entry, parent_key="") -> list[dict]:
        """
        Turns `entry` into a list of dictionaries easily convertable into a table.

        Values associated with "description" and "condition" are ignored.

        The output varies by `entry`'s datatype:
        - anything but a `dict` or a `list`: string value of entry is appended to the output as a dictionary.
        - `dict`: this procedure is applied to all sub-dictionaries. The parent dictionary's key is appended to all sub-dictionary keys.
        - `list`: this procedure is applied to all elements of the list

        Parameters:
            entry (Any): current entry to add to the output
            parent_key (str): name of parent dictionary's key, used in recursive calls
        Returns:
            dictionary version of `entry`
        """

        result = []
        for key, value in entry.items():
            if key in ["description", "condition"]:
                continue
            new_key = f"{parent_key}.{key}" if parent_key else key

            # dict: use same procedure
            if isinstance(value, dict):
                result.extend(self._flatten_dict(value, parent_key=new_key))

            # list: use procedure on each index, if it's a dict. Otherwise, add key/value pair
            elif isinstance(value, list):
                for v in value:
                    if isinstance(v, dict):
                        result.extend(self._flatten_dict(v, parent_key=new_key))
                    else:
                        # If a list item is not a dict, represent it as new_key: [original_list_values]
                        # This might be different from what was intended. The original code
                        # `result.append({new_key: value})` would add the whole list 'value' under 'new_key'
                        # for *each* non-dict item. It seems more logical to add it once.
                        # Assuming 'value' here is the full list.
                        result.append({new_key: value})
                        break  # Add the whole list once and break for this key, assuming all non-dict list items are treated same.
                        # If each non-dict item needs its own entry, this logic needs refinement.

            # anything else: append key/value pair as is
            else:
                result.append({new_key: value})
        return result

    def get_flat_dicts(self) -> list[dict]:
        """
        Returns a list of entries for table conversion.

        The entries in the output list are dictionaries.
        In each dictionary, the key is the field name, and the value is the contents under the field name.
        Each index in the output can be converted to a row in a Markdown or TeX table.

        Any sub-dictionaries have their parent dictionary's key appended to it, separated by a dot.
        Example: if the parent dictionary's name is 'key' and a subdictionary's key is 'subkey',
        the output dictionary will have an entry whose key is 'key.subkey'.

        The 'description' and 'condition' fields are not added.

        Returns:
            list[dict]: well-formatted entries for table conversion
        """
        output = []
        for (
            yaml_doc
        ) in (
            self._yaml_dicts
        ):  # Iterate over each top-level YAML document (which is a dict or a list)

            # The current structure implies self._yaml_dicts is a list of dicts.
            # If yaml_doc itself is a list of items (e.g., from a single YAML file like valid_list.yaml),
            # then you need to iterate over its items.
            # If each yaml_doc in self._yaml_dicts is meant to be one "row" that's processed,
            # then the inner loop needs to change.

            # Assuming self._yaml_dicts is a list of benchmark entries, where each entry is a dict:
            current_row_dict = {}
            # The structure `for item in yaml:` suggests `yaml` is a list of dicts here.
            # But if `self._yaml_dicts` is already the list of top-level benchmark entries,
            # then `yaml` in `for yaml in self._yaml_dicts:` is an individual benchmark entry.
            # Let's adjust this based on the common structure: a list of benchmark entries,
            # each being a dictionary that needs flattening.

            # Revised logic for get_flat_dicts
            # If self._yaml_dicts contains elements like:
            # [{'name': 'item1', 'details': {'sub1': 'value'}}, {'name': 'item2', ...}]
            # Each 'yaml_doc' from self._yaml_dicts is one dictionary representing one entry.
            # This entry needs to be flattened.
            flattened_entry_parts = self._flatten_dict(
                yaml_doc
            )  # Flatten the single dictionary

            # Now, combine the flattened parts into a single dictionary for the row
            current_row_dict = {}
            for part in flattened_entry_parts:
                current_row_dict.update(part)  # Merge dictionaries

            output.append(current_row_dict)

        return output

    # ---------------------------------------------------------------------------------------------------------
    #  Error Checking
    # ---------------------------------------------------------------------------------------------------------

    def _verify_entry(
        self,
        entry,
        parent_required: bool = False,
        parent_name: str = "<top level>",
        printing_errors: bool = True,
    ) -> bool:
        """
        Returns True if `entry` is not a dict, or `entry` contains all required fields.

        If `entry`'s "condition" field equals "required" and there are no fields other than "condition" or "description",
        returns False.

        if `entry`'s non-"condition"/"description" field is a list, all non-dicts in the list are checked using this procedure.

        Parameters:
            entry (Any): the value to check
            parent_required (bool): (for recursive calls) whether the parent dictionary's "condition" field is "required"
            parent_name (str): (for recursive calls) name of the field of the parent dictionary
            printing_errors (bool): whether to print error messages to the console
        Returns:
            whether the given entry is a valid dictionary (or not a dictionary)
        """

        if not isinstance(entry, dict):
            return True  # Ignore non-dicts

        valid_dict = True

        # Get condition
        condition = entry.get("condition")

        for key, value in entry.items():
            if key in ("description", "condition"):
                continue

            # print(key)
            # print(condition)
            # print(parent_required)
            # print()

            # If condition is "required" or the parent dict is checked, field must be present
            if (condition == "required" or parent_required) and value is None:
                if printing_errors:
                    printed_parent_name = (
                        parent_name
                        if parent_name == "<top level>"
                        else f'"{parent_name}"'
                    )
                    Console.error(
                        f'Required field "{key}" in {printed_parent_name} not present'
                    )
                valid_dict = False

            # Do >=
            elif condition != None and condition.startswith(">="):
                try:
                    required_length = int(condition[2:])
                except ValueError:
                    if printing_errors:
                        Console.error(
                            f'Condition "{condition[2:]}" is not a number'
                        )  # Fix typo: Console.errror -> Console.error
                    valid_dict = False

                if not isinstance(value, list) or len(value) < required_length:
                    if printing_errors:
                        Console.error(
                            f'Field "{key}" must be a list of length {required_length} or more'
                        )  # Fix typo: Console.errror -> Console.error
                    valid_dict = False

            # Recurse on the dict
            if isinstance(value, dict):
                if not self._verify_entry(
                    value,
                    parent_required=(condition == "required"),
                    parent_name=key,
                    printing_errors=printing_errors,
                ):
                    valid_dict = False

            # Recurse on any dictionaries in the list
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        if not self._verify_entry(
                            item,
                            parent_required=(condition == "required"),
                            parent_name=key,
                            printing_errors=printing_errors,
                        ):
                            valid_dict = False

        return valid_dict

    def check_required_fields(self, printing_errors: bool = True) -> bool:
        """
        Returns True if all YAML entries in the manager contains all fields marked as "required".

        Parameters:
            printing_errors (bool, default=True): whether to print error messages to the console
        Returns:
            bool: whether all required entries in the YAMLs are present
        """

        # Top-level must be a list of dict entries
        if not isinstance(self._yaml_dicts, list):
            # This case might be hit if the YAML file was a single dict that
            # was not converted to a list of dicts in load_single_yaml_file
            # due to sys.exit(1). If sys.exit(1) is removed, this check is more crucial.
            if printing_errors:
                Console.error(
                    "Internal data is not a list of dictionaries. Cannot check required fields."
                )
            return False

        valid = True
        for i in range(len(self._yaml_dicts)):
            # Check each top-level entry in self._yaml_dicts
            # _yaml_dicts is already a list of benchmark entries (dictionaries)
            if not self._verify_entry(
                self._yaml_dicts[i], printing_errors=printing_errors
            ):
                if printing_errors:
                    Console.error(f"Required field check failed in YAML entry {i+1}")
                valid = False

        return valid

    def check_required_fields_comment(
        self, checking_file: str = "source/benchmarks-format.yaml"
    ) -> bool:
        """
        Returns True if all YAML entries in the manager contains all fields marked as "required".

        This method uses the new YAML template. Required fields are listed as YAML comments.

        Parameters:
            printing_errors (bool, default=True): whether to print error messages to the console
        Returns:
            bool: whether all required entries in the YAMLs are present
        """
        valid = True

        fmt_manager = FieldFormatManager(format_file=checking_file)

        field_information = fmt_manager.get_all_fields()

        # Check all the flattened benchmarks
        for i, benchmark in enumerate(self.flat):

            # Get name and condition from the field format manager
            for name, _, condition in field_information:

                name_value = benchmark.get(name)

                # Check presence if required
                if not name_value and (
                    condition == "required" or condition.startswith('">=')
                ):
                    valid = False
                    Console.error(
                        f"ERROR: {name_value} is required in benchmark entry {i}"
                    )
                    continue

                # Check >= condition
                if condition.startswith('">='):
                    if not isinstance(name_value, list):
                        valid = False
                        Console.error(
                            f"ERROR: {name_value} must be a YAML list in benchmark entry {i}"
                        )
                        continue

                    # get numerical length and check it
                    try:
                        min_length = int(condition[2:-1])
                    except ValueError:
                        valid = False
                        Console.warning(
                            f"WARNING: Minimum length specified ({condition[2:-1]}) is not a number"
                        )
                        continue

                    if len(name_value) < min_length:
                        valid = False
                        Console.error(
                            f"ERROR: {name_value} (length: {len(name_value)}) must have a length of at least {min_length} in benchmark {i}"
                        )
                        continue

        return valid

    

    #############################################################################################
    # FILENAME Checking
    #############################################################################################

    def check_filenames(self, printing_errors: bool = True) -> bool:
        """
        Returns whether a properly formatted "name" field exists in each loaded YAML file.

        Parameters:
            printing_errors (bool, default=True): whether to print error messages to the console
        Returns:
            bool: True if all managed YAML files have properly formatted names, False otherwise
        """
        filenames_ok = True

        # Use the `data` property to get the original (non-flattened) entries
        # As 'name' is expected at the top level of each benchmark entry.
        # If 'name' can also be nested and accessed via flat, then use self.flat.
        # Assuming 'name' refers to the top-level 'name' field of each benchmark entry.
        for i, entry in enumerate(self.data):  # Use self.data (raw loaded dicts)

            name = entry.get("name", None)
            if not name:
                if printing_errors:
                    Console.error(f"Entry {i + 1} is missing a 'name' field")
                filenames_ok = False
                continue
            if not isinstance(name, str):
                if printing_errors:
                    Console.error(f"Entry {i + 1} has a non-string 'name': {name}")
                filenames_ok = False
                continue

            # Validate name
            for ch in name:
                # Check for non-ASCII characters that are not allowed
                if not (32 <= ord(ch) <= 126):  # ASCII printable characters
                    if printing_errors:
                        Console.error(
                            f"Non-ASCII character in name: {repr(ch)} in '{name}' in Entry {i + 1}"
                        )
                    filenames_ok = False

            if re.search(r" {2,}", name):
                if printing_errors:
                    Console.error(
                        f"Entry {i + 1} name has multiple consecutive spaces: '{name}'"
                    )
                filenames_ok = False

            if name.strip() != name:
                if printing_errors:
                    Console.error(
                        f"Entry {i + 1} name has leading/trailing spaces: '{name}'"
                    )
                filenames_ok = False

            if re.search(r"[()]", name):
                if printing_errors:
                    Console.error(f"Entry {i + 1} name contains parentheses: '{name}'")
                filenames_ok = False

            # This regex `[\w\-. ]+` matches word characters (alphanumeric + underscore), hyphen, dot, and space.
            # If `name` can contain other characters (e.g., specific symbols allowed in filenames), adjust this regex.
            if not re.fullmatch(r"[\w\-. ]+", name):
                if printing_errors:
                    Console.error(
                        f"Entry {i + 1} name contains disallowed characters: '{name}'"
                    )
                filenames_ok = False

        return filenames_ok

    def get_entries(self, attribute, value) -> list[dict]:
        """
        Returns a list of entries where the attribute equals the value.

        Parameters:
            attribute (str): name of the attribute to filter by
            value (Any): value to match for the attribute
        Returns:
            list[dict]: list of entries with the given attribute-value pair
        """
        if not isinstance(self.data, list):
            # This means self._yaml_dicts is not a list.
            # This should ideally not happen if load_single_yaml_file ensures list return.
            Console.error(
                "Internal data is not a list of dictionaries. Cannot filter entries."
            )
            return []  # Return empty list if data is not in expected format

        entries = []
        for entry in self.data:
            if entry.get(attribute) == value:
                entries.append(entry)
        return entries  # Return the list of found entries

    def get_by_name(
        self, name: str
    ) -> dict | None:  # Changed return type to allow None
        """
        Returns the first benchmark entry with the given name.

        Parameters:
            name (str): name of the entry to return, listed in the "name" field
        Returns:
            dict or None: first entry with the given name, or None if not found
        """
        for entry in self.data:
            if entry.get("name") == name:
                return entry
        return None

    def get_citations(self) -> list[str]:  # Changed return type to list[str]
        """
        Returns a list of all citations in the manager's YAML files.

        Returns:
            list[str]: all citations in the manager's YAML files
        """
        citations = []
        for entry in self.data:
            cite = entry.get("cite")
            name = entry.get(
                "name", "Unnamed Entry"
            )  # Provide a default for name if missing for error message
            if cite:
                if isinstance(cite, list):
                    citations.extend(cite)
                else:
                    citations.append(cite)
                    Console.error(
                        f"Entry '{name}' has a single citation, but it must be formulated as a list (use a - in front of the multiline string)."
                    )
        return citations
    
    def to_json_file(
        self, path: str, *, indent: int | None = 2, ensure_ascii: bool = False
    ) -> str:
        """Write the raw data as JSON to `path` and return the path."""
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self._yaml_dicts, f, indent=indent, ensure_ascii=ensure_ascii)
        return path
