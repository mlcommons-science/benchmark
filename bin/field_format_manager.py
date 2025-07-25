import yaml
# from pprint import pprint

class FieldFormatManager:
    """
    Used for storing and processing YAML formatting files
    """

    def __init__(self, format_file: str = 'source/benchmarks-format.yaml'):
        """
        Creates a new FieldFormatManager with `format_file` as the formatting file.

        The file at `format_file` must meet the following preconditions:
        - Be in valid YAML format
        - Use 2 spaces (no tabs) as indentation.
        - Have at least 2 commented lines below each entry, one which starts with "description:" and another starting with "condition:"
        The "description" line may have multiple commented lines below it, in case its text takes multiple lines.
        The "condition:" line must consist of exactly one line.
        "description" lines must come before "condition" lines.
        - All commented lines have 4 spaces of indentation.
        - A field called 'ratings' exists and appears last. 
        Its subfield names are indented by 4 spaces. Its commented lines have 6 spaces of indentation.

        Parameters:
            format_file (str): path to the formatting file
        """
        initial_contents = []
        with open(format_file, 'r') as file:
            for line in file:
                if line.strip() != '' and line.strip() != '\n':
                    initial_contents.append(line)

        self.contents = self._process_yaml_lines(initial_contents, format_file)

        self.contents = {**self.contents, **self._process_ratings(initial_contents, format_file)} 

        # pprint(self.contents)


    def _process_yaml_lines(self, yaml_file_list: list[str], format_filename: str) -> dict:
        """
        Returns a dictionary created from the lines in `yaml_file_list`.
        
        The keys are `format_filename`'s fields, followed by ".description" or ".condition".

        The values are the commented lines below each field. If the line, excluding whitespace, begins with "description:",
        any commented line afterwards is treated as part of the "*.description" field. If the line starts with "condition:",
        the line is part of the ".condition" field.

        Precondition: The file at `format_filename` is a YAML file meeting the preconditions of '__init__'. 

        Parameters:
            yaml_file_list (list): list containing lines from a YAML file
            format_filename (str): filename to read from
        Returns:
            YAML file contents as a dictionary
        """
        output = {}
        
        with open(format_filename, 'r') as f:
            file_contents = yaml.safe_load(f)
        file_contents = file_contents[0]    

        file_categories = list(file_contents.keys())

        # print(file_categories)

        file_cat_index = 0
        description = ""
        condition = ""

        for line in yaml_file_list:
            #Check commented lines
            if line.strip().startswith('#'):
                
                #Check for a "description" header
                if line.replace("|", "").replace("#", "").strip().startswith("description:"):
                    # print(">>>> BEGIN DESCRIPTION")
                    description += line.replace("|", "").replace("#", "").strip() [12:] + " "
                    continue
                
                #Check for a "condition" header. If found, move on
                elif line.replace("|", "").replace("#", "").strip().startswith("condition:"):
                    condition = line.replace("|", "").replace("#", "").strip() [11:]
                    output[ file_categories[file_cat_index] + ".description"] = description
                    output[ file_categories[file_cat_index] + ".condition"] = condition
                    # print(">>>> CONDITION: " + line.replace("|", "").replace("#", "").strip() [10:])
                    # pprint(output)
                    # print()

                    condition = ""
                    description = ""
                    continue

                # print(f"{line.strip().replace('|', "").replace("#", "").replace(":", "")} (for {file_categories[file_cat_index]})")
                description += line.replace("|", "").replace("#", "").strip() + " "

            elif line.startswith("  ") and line[2]!=' ':
                
                if line.strip().startswith("ratings:"):
                    # print(">>>>>>>>>>BEGIN RATINGS")
                    break

                file_cat_index += 1

        return output
    

    # -----------------------------------------------------------------------------------------------------------------
    # Helpers to constructor
    # -----------------------------------------------------------------------------------------------------------------


    def _process_ratings(self, yaml_file_list: list, format_filename: str) -> dict:
        """
        Returns a dictionary from the 'ratings' field created from the lines in `yaml_file_list`.
        
        The keys are "ratings", followed by a subfield from the 'ratings' field in `format_filename`, followed by ".description" or ".condition".

        The values are the commented lines below each 'ratings' subfield. If the line, excluding whitespace, begins with "description:",
        any commented line afterwards is treated as part of the "*.description" field. If the line starts with "condition:",
        the line is part of the ".condition" field.

        Precondition: The file at `format_filename` is a YAML file. If unindented by two spaces, the 'ratings' field meets the preconditions of '__init__'. 

        Parameters:
            yaml_file_list (list): list containing lines from a YAML file
            format_filename (str): filename to read from
        Returns:
            YAML file contents (ratings only) as a dictionary
        """

        output = {}

        with open(format_filename, 'r') as f:
            file_contents = yaml.safe_load(f)
        file_contents = file_contents[0]
        file_contents = file_contents.get("ratings")  

        file_categories = list(file_contents.keys())
        file_cat_index = -1

        ratings_lines = yaml_file_list[yaml_file_list.index("  ratings:\n") : ]

        description = ""
        condition = ""

        for line in ratings_lines:
            if line.strip()=="ratings:" or line.startswith('    #'):
                continue


            #Check commented lines
            if line.startswith('      #'):
                
                #Check for a "description" header
                if line.replace("|", "").replace("#", "").strip().startswith("description:"):

                    # print(">>>> BEGIN DESCRIPTION")
                    description += line.replace("|", "").replace("#", "").strip() [12:] + " "
                    continue
                
                #Check for a "condition" header. If found, move on
                elif line.replace("|", "").replace("#", "").strip().startswith("condition:"):
                    condition = line.replace("|", "").replace("#", "").strip() [11:]

                    output[ "ratings." + file_categories[file_cat_index] + ".description"] = description
                    output[ "ratings." + file_categories[file_cat_index] + ".condition"] = condition
                    # print(">>>> CONDITION: " + line.replace("|", "").replace("#", "").strip() [10:])
                    # pprint(output)
                    # print()

                    condition = ""
                    description = ""
                    continue

                # print(f"{line.strip().replace('|', "").replace("#", "").replace(":", "")} (for {file_categories[file_cat_index]})")
                description += line.replace("|", "").replace("#", "").strip() + " "


            #update file category
            elif not line.startswith("      ") and not line.strip().startswith("#"):
                file_cat_index += 1

        return output



    # -----------------------------------------------------------------------------------------------------------------
    # Methods
    # -----------------------------------------------------------------------------------------------------------------



    def load(self, filename = 'source/benchmarks.yaml'):
        """
        Specification unknown. Does nothing.
        """
        pass


    def get_field(self, field_name) -> tuple[str, str, str]:
        """
        Returns the field name, description, and condition of `field_name` as a tuple.

        To get a subfield inside `ratings`, use `ratings`.{subfield name}. Example: 'ratings.specification'.

        If `field_name`'s description or condition is not found, raises a ValueError.

        Parameters:
            field_name: name of desired field (dot-separated)
        Returns:
            (given field name, description of field, condition of field)
        """
        #Get description and check it
        description = self.contents.get(field_name + ".description")
        if not description:
            raise ValueError(f"The description for '{field_name}' was not found")
        
        #Get condition and check it
        condition = self.contents.get(field_name + ".condition")
        if not condition:
            raise ValueError(f"The condition for '{field_name}' was not found")

        return (field_name, description.strip(), condition.strip())


    def get_all_fields(self) -> list[tuple[str, str, str]]:
        """
        Returns a list of tuples. Each tuple contains the name, description, and condition of the fields in the checking file.

        Returns:
            list containing, for each field name, (field name, description of field, condition of field)
        """
        output = []
        description = None
        condition = None

        field_names = self.contents.keys()
        for name in field_names:

            value = self.contents.get(name)
            if value == None:
                raise AssertionError(f"INTERNAL ERROR: '{name}' is not a valid field name")
            
            if name.endswith("description"):
                description = value 
            elif name.endswith("condition"):
                condition = value 
            else:
                raise AssertionError(f"INTERNAL ERROR: '{name}' does not end in 'description' or 'condition'")
            

            if description != None and condition != None:
                output.append((name[:-10], description.strip(), condition.strip()))
                description = None 
                condition = None
        
        return output


    def create_manual(self):
        """
        Specification unknown. Does nothing.
        """
        pass

