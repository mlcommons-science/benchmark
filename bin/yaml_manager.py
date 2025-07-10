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


    def _verify_dict(self, yaml_dict: dict, checking_dict: dict, current_section: str = "<whole document>", printing_warnings: bool = True) -> bool:
        """
        Returns whether `yaml_dict` contains all mandatory fields as stated in `checking_dict`.

        `yaml_dict` is deemed valid if it has all fields and subfields that `checking_dict` contains, and
        all fields marked as "mandatory" in `checking_dict` are non-null and present.

        Parameters:
            yaml_dict (dict): dictionary to test
            checking_dict (dict): dictionary containing mandatory and optional fields
            current_section (str, optional): sub-dictionary checked
            printing_warnings (bool, optional): whether to print warning messages upon finding errors
        Returns:
            whether `yaml_dict` has the structure and mandatory fields of `checking_dict`
        """

        valid = True
        # print("NEW CALL")
        # print(checking_dict)
        # print(yaml_dict)

        for field in checking_dict:

            checking_dict_value = checking_dict[field]
            
            print(field)
            print(checking_dict_value)

            yaml_dict_value = None
            #Attempt to load the YAML dictionary value
            try:
                yaml_dict_value = yaml_dict[field]
            except KeyError:
                print(f"\033[91mWARNING: Field '{field}' in section '{current_section}' is missing. If optional and not present, set the subfields to null\033[00m")
                valid = False
                continue
            
            print(yaml_dict_value)
            

            if isinstance(checking_dict_value, dict):
                #First, verify that the corresponding YAML entry is a dictionary
                if not isinstance(yaml_dict_value, dict):
                    print(f"\033[91mWARNING: Section '{field}' must contain subfields\033[00m")
                    valid = False
                    continue 
                else:
                    print("ok")

                #Use the same dictionary-checking procedure on the values
                if not self._verify_dict(yaml_dict_value, checking_dict_value, current_section=field):
                    valid = False
                    continue
            
            elif isinstance(checking_dict_value, str):
                #"mandatory" check: see if the YAML dict value is present
                if checking_dict_value.startswith("required"):
                    if yaml_dict_value==None:
                        print(f"\033[91mWARNING: Required field '{field}' in section '{current_section}' is not present in the file\033[00m")
                        valid = False
                        continue
                    else:
                        print("ok")
            
                #">=n" check: see if the value is a list, and if the correct number of elements are present
                elif checking_dict_value.startswith(">="):
                    required_length = -1
                    try:
                        required_length = int(checking_dict_value[2:].strip())
                    except:
                        print("FATAL: Required length is not a number")
                        sys.exit(1)

                    #list check
                    if not isinstance(yaml_dict_value, list):
                        print(f"\033[91mWARNING: Field {field} must be a list\033[00m")
                        valid = False
                        continue
                    #length check
                    elif not len(yaml_dict_value)>=required_length:
                        print(f"\033[91mWARNING: Field {field} must be a list of length {required_length}\033[00m")
                        valid = False
                        continue
                    else:
                        print("ok")
            
            print()

        return valid


    def verify_fields(self, printing_warnings: bool = True) -> bool:
        """
        Returns True if all entries in the manager's YAML files have the fields marked as "mandatory" in the checking dictionary.
        Returns False otherwise.

        :param printing_warnings: whether to print error messages to the console for each missing rating. Default is True
        :return whether the inputted file contents have the proper fields
        """
        valid = True

        # Iterate over the list of dictionaries
        for yaml_dict in self._yaml_dicts:
            self._verify_dict(yaml_dict, self._checking_dict, printing_warnings=printing_warnings) #type: ignore

        return valid
    

    def get_dict(self) -> list[dict]:
        """
        :return: the manager's list of YAML content dictionaries
        """
        return self._yaml_dicts


if __name__ == "__main__":
    m = YamlManager()
    m.load_yamls("source/benchmarks-gregor.yaml")
    m.load_checking_dict("source/benchmarks-gregor-format.yaml")

    print(m._verify_dict(m._yaml_dicts[0], m._checking_dict)) # type: ignore


