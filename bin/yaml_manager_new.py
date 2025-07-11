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
        Each dictionary is a field in the YAML files (i.e. name, expired, cite).

        Parameters:
            file_paths: file paths of the YAMLs to merge
            enable_error_messages: True if printing error messages
        Returns:
            list of dictionaries representing combines YAML file entries
        """
        records = []
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



    def _verify_dict(self, yaml_contents, printing_warnings: bool = True, dict_required: bool = False, parent_dict_name: str = "",) -> bool:
        """
        Returns whether all fields marked as "required" in the given yaml contents are present.

        Parameters:
            yaml_contents: contents of the current YAML file
            printing_warnings (bool): whether to print warnings to the console
            dict_required (bool): (for recursive calls) whether all subfields inside the input are required
            parent_dict_name (str): (for recursive calls) the name of the parent field
        """

        #Get the field name
        field_names = [key for key in yaml_contents if key not in ["description", "condition"]]
        primary_field_name = field_names[0]


        #Check if a condition field exists in the first place. If not, check the field
        if not isinstance(yaml_contents, dict) or not yaml_contents.get("condition", None):
            valid_ = True
            for name in field_names:
                #Check individual subfields, if mandated
                if dict_required and not yaml_contents.get(name):
                    if printing_warnings:
                        print(f"\033[91mERROR: Required subfield '{name}' in dictionary-like field '{parent_dict_name}' not present\033[00m")
                    valid_ = False
                
            return valid_
        
        # print(yaml_dict)
        # print(field_names)
        # print()

        #Check if a required field is present
        if ((yaml_contents.get("condition")=="required" or yaml_contents.get("condition", "").startswith(">="))
            and not yaml_contents.get(primary_field_name, None)):

            if printing_warnings:
                print(f"\033[91mERROR: Required field in '{primary_field_name}' not present\033[00m")
            return False
        
        #Check >=n presence
        if yaml_contents.get("condition", "").startswith(">="):
            required_value_count = -1
            try:
                required_value_count = int(yaml_contents.get("condition", "")[2:])
            except ValueError:
                if printing_warnings:
                    print(f'\033[91mERROR: Condition on field "{primary_field_name}" is not a number- instead received "{yaml_contents.get("condition", "")[2:]}"\033[00m')
                return False

            if not isinstance(yaml_contents.get(primary_field_name), list):
                if printing_warnings:
                    print(f"\033[91mERROR: Field '{primary_field_name}' must contain a list\033[00m")
                return False

            if len(yaml_contents.get(primary_field_name, [])) < required_value_count:
                if printing_warnings:
                    print(f"\033[91mERROR: Field '{primary_field_name}' must have at least {required_value_count} list elements\033[00m")
                return False
            

        #check subfields
        valid = True
        for name in field_names:
            current_value = yaml_contents.get(name, None)

            #If subfield is itself a dictionary, check the dictionary
            if isinstance(current_value, dict):
                if not self._verify_dict(yaml_contents.get(name, None), dict_required = yaml_contents.get("condition")=="required", parent_dict_name=primary_field_name):
                    valid = False
            
            #Handle lists of dictionaries
            if isinstance(current_value, list):
                for i in current_value:
                    if isinstance(i, dict):
                         if not self._verify_dict(i, dict_required = i.get("condition","")=="required", parent_dict_name=primary_field_name):
                            valid = False


            #Check all the other values
            if yaml_contents.get("condition", "")=="required" and not yaml_contents.get(name):
                if printing_warnings:
                    print(f"\033[91mERROR: Required subfield '{name}' in '{primary_field_name}' not present\033[00m")
                valid = False

        return valid



    def verify_fields(self, printing_warnings: bool = True) -> bool:
        """
        Returns True if all entries in the manager's YAML files have the fields marked as "mandatory" in the checking dictionary.
        Returns False otherwise.

        :param printing_warnings: whether to print error messages to the console for each missing rating. Default is True
        :return: whether the inputted file contents have the proper fields
        """
        valid = True

        # Iterate over the list of dictionaries
        for current_dict in self._yaml_dicts:
            # print(current_dict)
            if not self._verify_dict(current_dict, dict_required=False, printing_warnings=printing_warnings):
                # print("Error here")
                valid = False
            # print()

        return valid


    
    def get_dicts(self) -> list[dict]:
        """
        :return: the manager's list of YAML content dictionaries
        """
        return self._yaml_dicts
    

    def _get_single_dict_pretty(self, entry) -> list:
        """
        Returns:
            the contents of the given dictionary in a writable format

            Every entry should be in one dictionary
        """
        if not isinstance(entry, dict):
            return []

        output = []

        #Get all fields except for "description" and "condition"
        field_names = [key for key in entry if key not in ["description", "condition"]]

        #Get all the values, sending each through this procedure
        for field_name in field_names:
            output_dict = dict()
            output_dict[field_name] = entry.get(field_name)
            output.append(output_dict)

        return output


    def get_dicts_pretty(self):
        """
        Returns:
            the manager's list of YAML conent dictionaries in a writable format

            Every entry should be in one dictionary
        """
        output = []
        for current_dict in self._yaml_dicts:
            name = [key for key in current_dict if key not in ["description", "condition"]][0]

            output += self._get_single_dict_pretty(current_dict)
            print(self._get_single_dict_pretty(current_dict))
            print()

        
        return output
            
            


if __name__ == "__main__":
    m = YamlManager()
    m.load_yamls("source/benchmark-entry-comment-gregor.yaml")

    print(m._yaml_dicts)
    print()
    print(m.get_dicts_pretty())