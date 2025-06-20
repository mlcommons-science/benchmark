import yaml

def load_yaml_file(filename):
    with open(filename, 'r') as f:
        return yaml.safe_load(f)

def normalize_entry(entry):
    """Standardize field names for merging."""
    entry = dict(entry)  # Ensure it's mutable
    if 'description' in entry and 'focus' not in entry:
        entry['focus'] = entry.pop('description')

    if 'tasks' in entry and 'task_types' not in entry:
        entry['task_types'] = entry.pop('tasks')

    if 'metrics' in entry and 'ai_capability_measured' not in entry:
        entry['ai_capability_measured'] = ', '.join(entry.pop('metrics'))

    if 'resources' in entry and 'url' not in entry:
        entry['url'] = entry.pop('resources')

    if 'notes' in entry and 'Notes' not in entry:
        entry['Notes'] = entry.pop('notes')

    return entry

def merge_tables(table1, table2):
    merged = []
    for entry in table1 + table2:
        normalized = normalize_entry(entry)
        merged.append(normalized)
    return merged

def main():
    # Load both YAML files
    table1 = load_yaml_file("source/table1.yaml")
    table2 = load_yaml_file("source/table2.yaml")

    # Merge them
    merged = merge_tables(table1, table2)

    # Write to merged.yaml
    with open("merged.yaml", "w") as f:
        yaml.dump(merged, f, sort_keys=False, allow_unicode=True)

if __name__ == "__main__":
    main()
