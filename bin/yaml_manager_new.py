import yaml
import sys

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
                print(f"\033[91mYAML SYNTAX ERROR in {file_path}: \n{e}\033[00m")
            return []  # Skip this file or entry instead of crashing

        if isinstance(content, dict):
            return [content]
        elif isinstance(content, list):
            return content
        else:
            print(f"\033[91mWARNING: Unsupported YAML format in {file_path}\033[00m")
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
            records += (self._load_single_yaml_file(path, enable_error_messages))

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



    def _verify_dict(self, yaml_dict):

        #Get the field name
        field_names = [key for key in yaml_dict if key not in ["description", "condition"]]
        primary_field_name = field_names[0]

        print(yaml_dict)
        
        
        #Check if a condition field exists in the first place
        if not isinstance(yaml_dict, dict) or not yaml_dict.get("condition", None):
            print("UNCHECKED")
            print()
            return
        
        print()

        #Check if the required field is present
        if yaml_dict["condition"] == "required" and not yaml_dict.get(primary_field_name, None):
            print(f"\033[91mERROR: Required field '{primary_field_name}' not present\033[00m")
            return

        #If field is itself a dictionary, check the dictionary
        for name in field_names:
            if isinstance(yaml_dict.get(name, None), dict):
                self._verify_dict(yaml_dict.get(name, None))


    def verify_fields(self, yaml_dicts, printing_warnings: bool = True) -> bool:
        """
        Returns True if all entries in the manager's YAML files have the fields marked as "mandatory" in the checking dictionary.
        Returns False otherwise.

        :param printing_warnings: whether to print error messages to the console for each missing rating. Default is True
        :return whether the inputted file contents have the proper fields
        """
        valid = True

        # Iterate over the list of dictionaries
        for current_dict in yaml_dicts:
            self._verify_dict(current_dict)
            

        return valid


    

    def get_dicts(self) -> list[dict]:
        """
        :return: the manager's list of YAML content dictionaries
        """
        return self._yaml_dicts


if __name__ == "__main__":
    m = YamlManager()
    m.load_yamls("source/benchmark-entry-comment-gregor.yaml")

    m.verify_fields(m._yaml_dicts)