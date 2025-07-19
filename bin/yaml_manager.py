"""
Contains a class for YAML file loading and formatting.

Example program from:

from pprint import pprint
from yaml_manager import YamlManager

manager = YamlManager("source/benchmarks-addon-new.yaml")

pprint(manager.data) # returens the raw list of dicts
pprint(manager.flat) # returns the flattened dicts as a list such taht keys are . seperated instead of hirarchical

This is some function that Reece and Anjay implemented i do not fully undesratnd, but is used to create flatt dicts. 
I am not sure what this has to do with a table and what is internally done.

I think this should be separated from flatten

flat = manager.get_table_formatted_dicts()) 


"""

import yaml
import re
import sys
import requests
from cloudmesh.common.console import Console

class YamlManager(object):
    """
    Loads, stores, and formats the contents of YAML files.

    Inputs are loaded via filepaths.
    The class can give the raw output of `yaml.safe_load` (as a list of dictionaries)
    or as a list of dictionaries for table output.
    """

    def __init__(self, yamls: str | list[str], 
                 overwriting_contents: bool = True, 
                 printing_syntax_errors: bool = True):
        """
        Creates a new YamlManager in charge of the contents of `yamls`.

        Parameters:
            yamls (str or list[str]): one or more YAML filepaths to load from
            overwriting_contents (bool, default=True): True if overwriting existing contents, False if appending to existing contents
            printing_syntax_errors (bool, default=True): whether to print warnings to the console if a YAML syntax error is found
        """
        self.data = self.load(yamls, 
                              overwrite=overwriting_contents, 
                              verbose=printing_syntax_errors)
        self.flat = self.get_table_formatted_dicts()

    # ---------------------------------------------------------------------------------------------------------
    # File Loading
    # ---------------------------------------------------------------------------------------------------------


    def load_single_yaml_file(self, file_path: str, enable_error_messages: bool = True) -> list[dict]:
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
            with open(file_path, 'r', encoding='utf-8') as f:
                content = yaml.safe_load(f)

            if isinstance(content, dict):
                Console.warning(f'YAML file "{file_path}" is not a list. Converting to list of dicts.')
                sys.exit(1)
                return [content]

            elif isinstance(content, list):
                return content

            else:
                raise ValueError("Unsupported YAML format. Expected a dict or list of dicts.")
        except FileNotFoundError:
            if enable_error_messages:
                Console.error(f"File not found: '{file_path}'")
                sys.exit(1)
                
        except yaml.YAMLError as e:
            if enable_error_messages:
                Console.error(f'YAML syntax error in "{file_path}": \n{e}')
            return []

    def load(self, 
             file_paths: str | list[str], 
             overwrite: bool = True, 
             verbose: bool = True) -> list[dict]:
        """
        Loads the contents of `file_paths` into this YamlManager.

        If `overwrite_existing` is True, any previous contents are overwritten upon load.
        If a YAML file contains syntax errors, that file is skipped.
        Raises a FileNotFoundError if any specified file does not exist.

        Parameters:
            file_paths (str or list[str]): File path(s) to load from.
            overwrite_existing (bool, default=True): Whether to overwrite the manager's existing contents.
            print_syntax_errors (bool, default=True): Whether to print error messages for YAML syntax issues.

        Returns:
            list[dict]: The updated list of YAML dictionaries stored in the manager.
        """
        # Normalize file_paths to always be a list
        paths_to_load = [file_paths] if isinstance(file_paths, str) else file_paths

        newly_loaded_records = []
        for path in paths_to_load:
            # Each file's content (which is guaranteed to be a list) is extended
            newly_loaded_records.extend(self.load_single_yaml_file(path, verbose))

        if overwrite:
            self._yaml_dicts = newly_loaded_records
        else:
            self._yaml_dicts.extend(newly_loaded_records)

        self.data = self._yaml_dicts  # Update the data attribute

        # BUG: We should not use self._yaml_dicts, but self.data instead.
        #      make self._yaml_dicts a local variable e.g. yaml_dicts
        #      replace everywhere self._yaml_dicts with self.data
        
        return self._yaml_dicts



    # def load_multiple_yaml_files(self, file_paths: list[str], enable_error_messages: bool = True) -> list[dict]:
    #     """
    #     Returns a list of dictionaries representing the contents of a YAML file.

    #     Parameters:
    #         file_paths (list[str]): list of file paths to load from
    #         enable_error_messages (bool): whether to print error messages to the console. Default True
    #     Returns:
    #         contents of given YAML files
    #     """
    #     records = []
    #     for path in file_paths:
    #         records += self.load_single_yaml_file(path, enable_error_messages)
    #     return records


    # def load_yamls(self, file_paths: str | list[str], overwriting_contents: bool = True, print_syntax_errors: bool = True) -> None:
    #     """
    #     Loads the contents of `file_paths` into this YamlManager.

    #     If `overwriting_prev` is True, any previous contents are overwritten upon load.

    #     Raises a FileNotFoundError if an invalid filepath is given.
    #     If a YAML file contains syntax errors, the file is **not loaded**.

    #     Parameters:
    #         file_paths (str or list[str]): filepath(s) to load from
    #         overwriting_contents (bool, default=True): whether to overwrite the manager's existing contents.
    #         print_syntax_errors (bool, default=True): whether to print error messages upon finding YAML syntax errors.
    #     """
    #     if isinstance(file_paths, str):
    #         if overwriting_contents:
    #             self._yaml_dicts =  self.load_multiple_yaml_files([file_paths], print_syntax_errors)
    #         else:
    #             self._yaml_dicts += self.load_multiple_yaml_files([file_paths], print_syntax_errors)

    #     else:
    #         if overwriting_contents:
    #             self._yaml_dicts =  self.load_multiple_yaml_files(file_paths, print_syntax_errors)
    #         else:
    #             self._yaml_dicts += self.load_multiple_yaml_files(file_paths, print_syntax_errors)
    #     return self._yaml_dicts


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
        # return self._yaml_dicts
        return self.data
    

    def _flatten_dict(self, entry, parent_key='') -> list[dict]:
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
            if key in ['description', 'condition']:
                continue
            new_key = f"{parent_key}.{key}" if parent_key else key

            #dict: use same procedure
            if isinstance(value, dict):
                result.extend(self._flatten_dict(value, parent_key=new_key))

            #list: use procedure on each index, if it's a dict. Otherwise, add key/value pair
            elif isinstance(value, list):
                for v in value:
                    if isinstance(v, dict):
                        result.extend(self._flatten_dict(v, parent_key=new_key))
                    else:
                        result.append({new_key: value})
            
            #anything else: append key/value pair as is
            else:
                result.append({new_key: value})
        return result


    def get_table_formatted_dicts(self) -> list[dict]:
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
        # for y in self._yaml_dicts:
        #     print(y, end='\n\n')

        output = []
        for yaml in self._yaml_dicts:

            current_row = []
            for item in yaml:
                current_row += self._flatten_dict(item)
            
            current_row_dict = {}
            for cell in current_row:
                for k, v in cell.items():
                    current_row_dict[k] = v

            output.append(current_row_dict)

        return output


    # ---------------------------------------------------------------------------------------------------------
    #  Error Checking
    # ---------------------------------------------------------------------------------------------------------
    

    def _verify_entry(self, entry, parent_required: bool = False, parent_name: str = '<top level>', printing_errors: bool = True) -> bool:
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
            return True #Ignore non-dicts


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
            if (condition=="required" or parent_required) and value is None:
                if printing_errors:
                    printed_parent_name = parent_name if parent_name=='<top level>' else f'"{parent_name}"'
                    Console.error(f'Required field "{key}" in {printed_parent_name} not present')
                valid_dict =  False
            
            #Do >=
            elif condition != None and condition.startswith(">="):
                try:
                    required_length = int(condition[2:])
                except ValueError:
                    if printing_errors:
                        Console.errror('Condition "{condition[2:]}" is not a number')
                    valid_dict = False
                
                if not isinstance(value, list) or len(value) < required_length:
                    if printing_errors:
                        Console.errror('Field "{key}" must be a list of length {required_length} or more')
                    valid_dict =  False

            #Recurse on the dict
            if isinstance(value, dict):
                if not self._verify_entry(value, parent_required=(condition=='required'), parent_name=key):
                    valid_dict =  False

            #Recurse on any dictionaries in the list  
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):

                        if not self._verify_entry(item, parent_required=(condition=='required'), parent_name=key):
                            valid_dict =  False
                        
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
            return False

        valid = True
        for i in range(len(self._yaml_dicts)):
            #Check each column (type: dict) in each YAML dictionary stored
            for column in self._yaml_dicts[i]:
                if not self._verify_entry(column, printing_errors=printing_errors):
                    Console.errror('in YAML entry {i+1}')
                    print()
                    valid = False

        return valid


    def check_urls(self, printing_status: bool = True) -> bool:
        """
        Returns whether all the URLs in the manager's YAML files are valid.

        Any field without subfields that ends with "url" is checked. 
        The "cite" field's URL is also checked.

        Parameters:
            printing_status (bool): whether to print statuses
        Returns:
            bool: True if all URLs are valid, False otherwise
        """
        urls = []
        
        for entry in self.get_table_formatted_dicts():
            for key, value in entry.items():
                # Handle flat keys with 'url'
                if key.lower().endswith('url'):
                    if isinstance(value, str):
                        urls.append(value)
                # Handle BibTeX citation strings
                elif key == 'cite':
                    if isinstance(value, list):
                        for bib in value:
                            urls.extend(re.findall(r'url\s*=\s*\{(.*?)\}', bib))

        # Remove duplicates
        unique_urls = list(set(urls))

        # Check each URL
        all_urls_valid = True
        for url in unique_urls:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    if printing_status:
                        Console.ok(f"[OK] {url}")
                else:
                    if printing_status:
                        Console.error(f"{response.status_code}: {url}")
                    all_urls_valid = False
            except requests.RequestException as e:
                if printing_status:
                    Console.error(f"{url} - {e}")
                all_urls_valid = False

        return all_urls_valid
    


    def check_filenames(self, printing_errors: bool = True) -> bool:
        """
        Returns whether a properly formatted "name" field exists in each loaded YAML file.

        Parameters:
            printing_errors (bool, default=True): whether to print error messages to the console
        Returns:
            bool: True if all managed YAML files have properly formatted names, False otherwise
        """
        filenames_ok = True

        formatted_entries = self.get_table_formatted_dicts()
        for i, entry in enumerate(formatted_entries):

            name = entry.get("name", None)
            if not name:
                if printing_errors:
                    Console.error(" Entry {i + 1} is missing a 'name' field")
                filenames_ok = False
                continue
            if not isinstance(name, str):
                if printing_errors:
                    Console.error(" Entry {i + 1} has a non-string 'name': {name}")
                filenames_ok = False
                continue

            # Validate name
            for ch in name:
                if not (32 <= ord(ch) <= 126):
                    if printing_errors:
                        Console.error(" Non-ASCII character in name: {repr(ch)} in '{name}'")
                    filenames_ok = False

            if re.search(r' {2,}', name):
                if printing_errors:
                    Console.error(" Entry {i + 1} name has multiple consecutive spaces: '{name}'")
                filenames_ok = False

            if name.strip() != name:
                if printing_errors:
                    Console.error(" Entry {i + 1} name has leading/trailing spaces: '{name}'")
                filenames_ok = False

            if re.search(r'[()]', name):
                if printing_errors:
                    Console.error(" Entry {i + 1} name contains parentheses: '{name}'")
                filenames_ok = False

            if not re.fullmatch(r'[\w\-. ]+', name):
                if printing_errors:
                    Console.error(" Entry {i + 1} name contains disallowed characters: '{name}'")
                filenames_ok = False

        return filenames_ok


if __name__ == '__main__':
    pass