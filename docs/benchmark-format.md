# Benchmark YAML Format

This guide describes how benchmark definitions are stored in YAML and which rules contributors must follow when proposing changes. All authoritative benchmark data lives under `source/`.

- `source/benchmarks.yaml` and `source/benchmarks-addon.yaml` currently hold the published catalogue.
- `source/benchmarks-format.yaml` is the schema. It lists every field and the expected data type.
- `source/benchmarks-sample.yaml` provides an example entry that mirrors the schema with realistic values.

New YAML files can be added to the catalogue when needed—ensure they follow the same schema conventions.

For validation commands and Makefile shortcuts, see `docs/tooling.md`.

## Formatting Rules

- **Indentation**: Use exactly two spaces. Tabs are not allowed.
- **Required fields**: Every field described in `benchmarks-format.yaml` must be present. Do not remove keys.
- **Unknown values**: Use the literal string `"unknown"` if information is missing. Never leave values empty or set them to `null`.
- **Strings**: Wrap string values in double quotes (especially URLs or entries containing punctuation).
- **Lists**: Preserve the list format shown in the schema. Every list element should be indented two spaces relative to the key.
- **Booleans**: Use lowercase YAML booleans (`true` / `false`) unless the schema explicitly requires quoted strings.
- **Multiline text**: Use the pipe (`|`) block style for prose. Do not wrap multiline fields in quotes.
- **URLs**: Provide official benchmark resources (GitHub repository, website, or paper).
- `url` field cannot be `"unknown"`.

## Multiline Examples

Multiline strings should follow this pattern:

```yaml
summary: |
  This is a multiline description of the benchmark.
  It renders as a single paragraph in the generated reports.
```

Lists are indented relative to their keys:

```yaml
keywords:
  - "multitask"
  - "multiple-choice"
```

The rating `reason` fields are often multiline blocks:

```yaml
ratings:
  software:
    rating: 5
    reason: |
      Installation scripts are provided and container images are available.
  documentation:
    rating: 4
    reason: |
      Background and motivation are clear, but deployment details are missing.
```

## Suggested Workflow

1. Copy the skeleton entry from `source/benchmarks-sample.yaml` and paste it into the appropriate YAML file.
2. Fill in each field with benchmark-specific details. Quote strings and follow the indentation conventions.
3. Run the validation commands described in `docs/tooling.md` to ensure the entry matches the schema and that referenced URLs are reachable.
4. Review the diff to ensure only the intended YAML changes are present before opening a pull request.

Following these rules keeps the benchmark catalogue consistent and makes PR reviews straightforward.
