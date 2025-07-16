import yaml
from yaml.representer import SafeRepresenter

# --- YAML literal string formatting ---
class LiteralString(str):
    pass

def literal_representer(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')

yaml.add_representer(LiteralString, literal_representer)
yaml.add_representer(type(None), SafeRepresenter.represent_none)

# --- Clean and annotate all strings ---
def clean_string(value):
    if not isinstance(value, str):
        return value

    cleaned = value.replace('\\n', '')  # Remove the string literal "\n"

    if '\n' in cleaned or len(cleaned) > 80:
        return LiteralString(cleaned.strip())

    return cleaned.strip()

def clean_all_strings(data):
    if isinstance(data, dict):
        return {k: clean_all_strings(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_all_strings(i) for i in data]
    elif isinstance(data, str):
        return clean_string(data)
    else:
        return data

# --- Dataset parsing ---
def split_datasets(dataset_str):
    datasets = []
    for item in dataset_str.split(', '):
        if '(' in item:
            name, url = item.split('(', 1)
            datasets.append({
                'name': name.strip(),
                'url': url.strip(')')
            })
    return datasets

# --- Rating transformation ---
def format_ratings(rating_list):
    rating_map = {
        'problem_spec_rating': 'specification',
        'problem_spec_reason': 'specification',
        'dataset_rating': 'dataset',
        'dataset_reason': 'dataset',
        'metrics_rating': 'metrics',
        'metrics_reason': 'metrics',
        'reference_solution_rating': 'reference_solution',
        'reference_solution_reason': 'reference_solution',
        'documentation_rating': 'documentation',
        'documentation_reason': 'documentation'
    }

    ratings = {
        'software': {
            'rating': 0,
            'reason': LiteralString('Not yet evaluated')
        }
    }

    for item in rating_list:
        for key, value in item.items():
            section = rating_map.get(key)
            if not section:
                continue
            if section not in ratings:
                ratings[section] = {}
            if 'rating' in key:
                ratings[section]['rating'] = value
            elif 'reason' in key:
                ratings[section]['reason'] = LiteralString(value.replace('\\n', '').strip())

    return ratings

# --- Transform each benchmark entry ---
def transform_entry(entry):
    entry = clean_all_strings(entry)

    return {
        'date': entry.get('date'),
        'last_updated': entry.get('Last Updated') or entry.get('date'),
        'expired': entry.get('expired'),
        'valid': entry.get('valid'),
        'name': entry.get('name'),
        'url': entry.get('url'),
        'domain': entry.get('domain'),
        'focus': entry.get('focus'),
        'keywords': entry.get('keywords'),
        'description': LiteralString(entry.get('description', '')),
        'task_types': entry.get('task_types', []),
        'ai_capability_measured': [
            cap.strip() for cap in entry.get('ai_capability_measured', '').split(',')
            if cap.strip()
        ],
        'metrics': entry.get('metrics', []),
        'models': entry.get('models', []),
        'ml_motif': [entry.get('ML Motif')] if entry.get('ML Motif') else [],
        'type': entry.get('Type'),
        'ml_task': entry.get('ML task'),
        'notes': LiteralString(entry.get('notes', '')) if 'notes' in entry else None,
        'contact': {
            'name': entry.get('Support Contact Person'),
            'email': None
        },
        'cite': [LiteralString(c.replace('\\n', '').strip()) for c in entry.get('cite', [])],
        'dataset': split_datasets(entry.get('Dataset', '')),
        'results': [
            {
                'name': 'Gemini LLM Deep Research',
                'url': entry.get('Results from Gemini LLM Deep Research')
            },
            {
                'name': 'ChatGPT LLM',
                'url': entry.get('Results from ChatGPT LLM')
            }
        ],
        'fair': {
            'reproducible': entry.get('Software', False),
            'benchmark_ready': entry.get('Benchmark-Ready', False)
        },
        'ratings': format_ratings(entry.get('ratings', []))
    }

# --- Main execution ---
def main():
    input_file = 'source/benchmarks-addon.yaml'
    output_file = 'benchmarks_transformed.yaml'

    with open(input_file, 'r') as f:
        old_entries = yaml.safe_load(f)

    new_entries = [transform_entry(entry) for entry in old_entries]

    with open(output_file, 'w') as f:
        yaml.dump(new_entries, f, sort_keys=False, allow_unicode=True, width=100)

    print(f"✅ Transformed entries written to {output_file}")

if __name__ == '__main__':
    main()
