from pprint import pprint
from yaml_manager import YamlManager

manager = YamlManager("source/benchmarks-addon-new.yaml")
content = manager.get_table_formatted_dicts()
pprint(content)