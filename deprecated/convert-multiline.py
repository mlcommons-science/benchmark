from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString
from pathlib import Path

input_path = Path("source/abc.yaml")
output_path = Path("source/d.yaml")

def convert_multiline_fields(obj):
    if isinstance(obj, dict):
        return {k: convert_multiline_fields(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_multiline_fields(item) for item in obj]
    elif isinstance(obj, str):
        # Detect either real newlines or escaped \n in string
        if '\n' in obj:
            return LiteralScalarString(obj.strip())
        elif '\\n' in obj:
            decoded = obj.encode().decode('unicode_escape').strip()
            return LiteralScalarString(decoded)
        else:
            return obj
    else:
        return obj

yaml = YAML()
yaml.width = 1000
yaml.preserve_quotes = True

# Load YAML
with input_path.open("r", encoding="utf-8") as f:
    data = yaml.load(f)

# Process all strings recursively
processed = convert_multiline_fields(data)

# Write output YAML
with output_path.open("w", encoding="utf-8") as f:
    yaml.dump(processed, f)
