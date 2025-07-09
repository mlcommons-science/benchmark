import yaml


class YamlManager(object):

    _yaml_dicts = []

    _checking_dict = dict()

    def __init__(self):
        pass


    def _load_single_yaml_file(self, file_path: str, enable_error_messages: bool = True) -> list[dict]:
        """
        Returns the contents of the YAML file at `file_path` as a list of dictionaries.

        :param file_path: file path to load from 
        :return: contents of given YAML file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = yaml.safe_load(f)
        except yaml.YAMLError as e:
            if enable_error_messages:
                print(f"\033[91mYAML SYNTAX ERROR in {file_path}:\033[00m\n{e}")
            return []  # Skip this file or entry instead of crashing

        if isinstance(content, dict):
            return [content]
        elif isinstance(content, list):
            return content
        else:
            print(f"\033[93mWARNING: Unsupported YAML format in {file_path}\033[00m")
            return []
        

    def _load_multiple_yaml_files(self, file_paths: list[str], enable_error_messages: bool = True) -> list[dict]:
        """
        Combines the contents of the files at `file_paths`, adding them to the manager as a list of dictionaries.
        Each key in the dictionary is a field in the YAML files (i.e. name, expired, cite).

        If any duplicate "name" fields are found, the function prints an error message and
        does not add the duplicate to the output.

        Parameters:
            file_paths: file paths of the YAMLs to merge
            enable_error_messages: True if printing error messages
        Returns:
            list of dictionaries representing combines YAML file entries
        """
        records = []
        seen_names = set()
        for path in file_paths:

            for record in self._load_single_yaml_file(path, enable_error_messages):
                name = record.get("name")
                if name:

                    if name in seen_names and enable_error_messages:
                            print(f"\033[91mERROR: \"{name}\" is a duplicate. Duplicated names are not allowed\033[00m")
                    else:
                        seen_names.add(name)
                        records.append(record)

        return records
    



    def load_yamls(self, file_paths: str | list[str], enable_error_messages: bool = True):
        """
        Combines the contents of the files at `file_paths`, adding them to the manager as a list of dictionaroes.
        Each key in the dictionary is a field in the YAML files (i.e. name, expired, cite).

        If any duplicate "name" fields are found, the function prints an error message and
        does not add the duplicate to the output.

        Parameters:
            file_paths (str, list[str]): file paths of the YAMLs to merge
            enable_error_messages (bool): True if printing error messages, False otherwise
        """
        if isinstance(file_paths, str):
            self._yaml_dicts = self._load_multiple_yaml_files([file_paths], enable_error_messages)
        else:
            self._yaml_dicts = self._load_multiple_yaml_files(file_paths, enable_error_messages)


    def load_checking_dict(self, path: str, enable_error_messages: bool = True) -> None:
        """
        Loads the dictionary for mandatory argument checking.

        :param path (str): filepath to the checking dictionary
        :param enable_error_messages (bool): True if printing error messages, False otherwise
        """
        self._checking_dict = self._load_multiple_yaml_files([path], enable_error_messages)
        self._checking_dict = self._checking_dict[0]

    

    def verify_fields(self, printing_warnings: bool = True) -> bool:
        """
        Returns True if all entries in the manager's YAML files have a "name", "cite", and "ratings" entry,
        where each "ratings" entry contains the keys listed in the manager's checked columns.

        :param printing_warnings: whether to print error messages to the console for each missing rating. Default is True
        :return whether the inputted file contents have the proper fields
        """
        valid = True

        # Iterate over the list of dictionaries
        for idx, yaml_dict in enumerate(self._yaml_dicts):

            # Iterate through the checking dictionary
            for field, requirement in self._checking_dict.items():
                if requirement == "mandatory":
                    # If the field is mandatory and not present in the yaml_dict
                    if field not in yaml_dict and printing_warnings:
                        print(f"\033[91mWARNING: Field '{field}' is mandatory but missing in dictionary {idx+1}\033[00m")
                        valid = False

        return valid
    

    def get_dict(self) -> list[dict]:
        """
        :return: the manager's list of YAML content dictionaries
        """
        return self._yaml_dicts
