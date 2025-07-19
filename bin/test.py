from pprint import pprint
from yaml_manager import YamlManager

manager = YamlManager("source/benchmarks-addon-new.yaml")

#pprint(manager.data)
#pprint(manager.flat)

pprint(manager.get_citations())
