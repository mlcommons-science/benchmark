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
        self._yaml_dicts = []

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
                return self._group_field_blocks_by_first_key(content)

            else:
                raise ValueError("Unsupported YAML format. Expected a dict or list of dicts.")

        except yaml.YAMLError as e:
            if enable_error_messages:
                print(f"\033[91mYAML SYNTAX ERROR in {file_path}: \n{e}\033[00m")
            return []

    def _group_field_blocks_by_first_key(self, content: list[dict]) -> list[dict]:
        """
        Groups a flat list of field dictionaries into logical entries by using the key of the first real field block
        (e.g., 'date') as a boundary trigger — but only when that key appears *alone*, not as part of a multi-field entry.
        """
        if not content or not isinstance(content, list):
            return []

        # Determine the trigger key (e.g., 'date', 'name', etc.)
        for item in content:
            if isinstance(item, dict):
                trigger_keys = [k for k in item if k not in ("description", "condition")]
                if len(trigger_keys) == 1:
                    trigger_key = trigger_keys[0]
                    break
        else:
            raise ValueError("Could not determine a suitable trigger key from the YAML")

        grouped_entries = []
        current_entry = {}

        for field in content:
            if not isinstance(field, dict):
                continue

            # New entry only starts when field contains only one non-metadata key (e.g., just 'date')
            field_keys = [k for k in field if k not in ("description", "condition")]
            is_new_entry = trigger_key in field_keys and len(field_keys) == 1

            if is_new_entry and current_entry:
                grouped_entries.append(current_entry)
                current_entry = {}

            current_entry.update({k: v for k, v in field.items() if k not in ("description", "condition")})

        if current_entry:
            grouped_entries.append(current_entry)

        return grouped_entries


    def _load_multiple_yaml_files(self, file_paths: list[str], enable_error_messages: bool = True) -> list[dict]:
        """
        Returns a list of dictionaries representing the contents of a YAML file.

        Parameters:
            file_paths (list[str]): list of file paths to load from
            enable_error_messages: 
        """
        records = []
        for path in file_paths:
            records += self._load_single_yaml_file(path, enable_error_messages)
        return records

    def load_yamls(self, file_paths: str | list[str], enable_error_messages: bool = True):
        if isinstance(file_paths, str):
            self._yaml_dicts = self._load_multiple_yaml_files([file_paths], enable_error_messages)
        else:
            self._yaml_dicts = self._load_multiple_yaml_files(file_paths, enable_error_messages)

    def get_dicts(self) -> list[dict]:
        return self._yaml_dicts


    def _flatten_dict(self, entry, parent_key=''):
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


    def get_table_formatted_dicts(self):

        output = []
        for item in self._yaml_dicts:
            output.extend(self._flatten_dict(item))
        return output


            
if __name__ == '__main__':
    m = YamlManager()
    m.load_yamls("source/benchmark-entry-comment-gregor.yaml")

    fields = m.get_table_formatted_dicts()
    for f in fields:
        print(f, end="\n")
