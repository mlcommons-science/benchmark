"""
Contains a class for YAML file loading and formatting
"""

import yaml

class YamlManager(object):
    """
    Loads, stores, and formats the contents of YAML files.

    Inputs are loaded via filepaths.
    The class can give the raw output of `yaml.safe_load` (as a list of dictionaries)
    or as a list of dictionaries for table output.
    """

    def __init__(self):
        """
        Creates a new YamlManager. It initially has no contents loaded.
        """
        self._yaml_dicts = []


    # ---------------------------------------------------------------------------------------------------------
    # File Loading
    # ---------------------------------------------------------------------------------------------------------


    def _load_single_yaml_file(self, file_path: str, enable_error_messages: bool = True) -> list[dict]:
        """
        Loads a YAML file containing a flat list of field-level entries,
        and groups them into full benchmark entries using 'name' as the reset key.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = yaml.safe_load(f)

            if isinstance(content, dict):
                return [content]

            elif isinstance(content, list):
                return content

            else:
                raise ValueError("Unsupported YAML format. Expected a dict or list of dicts.")

        except yaml.YAMLError as e:
            if enable_error_messages:
                print(f"\033[91mYAML SYNTAX ERROR in {file_path}: \n{e}\033[00m")
            return []


    def _load_multiple_yaml_files(self, file_paths: list[str], enable_error_messages: bool = True) -> list[dict]:
        """
        Returns a list of dictionaries representing the contents of a YAML file.

        Parameters:
            file_paths (list[str]): list of file paths to load from
            enable_error_messages (bool): whether to print error messages to the console
        Returns:
            contents of given YAML files
        """
        records = []
        for path in file_paths:
            records += self._load_single_yaml_file(path, enable_error_messages)
        return records


    def load_yamls(self, file_paths: str | list[str], overwriting_prev: bool = True, enable_error_messages: bool = True) -> None:
        """
        Loads the contents of `file_paths` into this YamlManager.

        If `overwriting_prev` is True, any previous contents are overwritten upon load.

        Parameters:
            file_paths (str or list[str]): filepath(s) to load from
            overwriting_prev (bool): whether to overwrite the manager's existing contents. Default True
            enable_error_messages (bool): whether to print error messages on an unsuccessful load. Default True
        """
        if isinstance(file_paths, str):
            if overwriting_prev:
                self._yaml_dicts =  self._load_multiple_yaml_files([file_paths], enable_error_messages)
            else:
                self._yaml_dicts += self._load_multiple_yaml_files([file_paths], enable_error_messages)

        else:
            if overwriting_prev:
                self._yaml_dicts =  self._load_multiple_yaml_files(file_paths, enable_error_messages)
            else:
                self._yaml_dicts += self._load_multiple_yaml_files(file_paths, enable_error_messages)


    # ---------------------------------------------------------------------------------------------------------
    # Contents Presentation
    # ---------------------------------------------------------------------------------------------------------


    def get_dicts(self) -> list[dict]:
        """
        Returns a list of the raw internal dictionaries read to by the manager.

        DO NOT MODIFY THE OUTPUT! The values returned are shallow copies. Any modification will affect the YAML manager's contents.

        Returns:
            manager's current file contents, as dictionaries
        """
        return self._yaml_dicts


    def _flatten_dict(self, entry, parent_key='') -> list[dict]:
        """
        Turns `entry` into a list of dictionaries easily convertable into a table.

        The output varies by `entry`'s datatype:  
        - anything but a `dict` or a `list`: string value of entry is appended to the output.
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
            new_key = f"{parent_key} - {key}" if parent_key else key

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
                result.append({new_key: str(value)})
        return result


    def get_table_formatted_dicts(self) -> list[list[dict]]:
        """
        Returns a list of entries for table conversion.

        The entries in the output list are lists of dictionaries.
        In each dictionary, the key is the field name, and the value is the contents under the field name.  
        Each index in the output can be converted to a row in a Markdown or TeX table.

        Any sub-dictionaries have their parent dictionary's key appended to it, separated by a dash.  
        Example: if the parent dictionary's name is 'key' and a subdictionary's key is 'subkey', 
        the output dictionary will have an entry whose key is 'key - subkey'.

        Returns:
            well-formatted entries for table conversion
        """

        output = []
        for item in self._yaml_dicts:
            output.append(self._flatten_dict(item))
        return output
    

# if __name__ == "__main__":
#     m = YamlManager()
#     m.load_yamls("source/benchmark-entry-comment-gregor.yaml")
#     print(m.get_table_formatted_dicts())