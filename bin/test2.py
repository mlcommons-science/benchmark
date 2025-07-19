from pprint import pprint
from yaml_manager import YamlManager

manager = YamlManager("source/benchmarks-addon-new.yaml")

# get entries as flattent list of dicts

#content = manager.get_dicts()
content = manager.entries()

# get dicts



pprint(content)