# Contributing Guide

Thank you for helping expand the MLCommons Science AI Benchmark Collection. This guide focuses on contributions that add or revise benchmark entries. Improvements to tooling and documentation are also welcome—open an issue to discuss substantial changes before you start.

## Workflow Overview

- Fork the repository, clone your fork locally, and keep it in sync with `upstream/main`.
- Create a feature branch for your change (for example, `add-mmlu-updates`).
- Open a pull request targeting `mlcommons-science/benchmark:main` once you have completed the steps below.

## Adding or Updating a Benchmark

1. Create a new file named `benchmark-<your-benchmark-name>.yaml` in the `source/` directory. Each file should contain exactly one benchmark entry.
2. Copy the skeleton from `source/sample/benchmarks-sample.yaml` or use an existing `benchmark-*.yaml` file as a template.
3. Fill out every field described in `source/sample/benchmarks-format.yaml`. Use the literal `"unknown"` when information is unavailable.
4. Keep indentation at two spaces and wrap strings in double quotes to avoid parsing issues.
5. If you introduce new URLs, prefer official project pages, repositories, or publications.

See `docs/benchmark-format.md` for detailed authoring guidance and examples.

## Validation Checklist

Run the following commands from the repository root before committing:

```bash
make check               # verifies required fields and flags non-ASCII characters
make check_url           # optional, verifies external links
```

If you want to preview the full site locally (not required for PRs), run:

```bash
make all           # builds PDF and MkDocs outputs
make serve    # serves the MkDocs site locally for inspection
```

Only YAML files (and any accompanying documentation updates) should be staged for commit. Avoid committing generated artifacts in `content/` or `www/`.

## Pull Request Expectations

- Use a descriptive title such as "Add <benchmark name>" or "Update <benchmark name> ratings".
- Include a short summary of the change and cite primary sources when adjusting ratings.
- Confirm in the PR description that you ran `make check` (and `make check_url` when applicable).
- Limit the scope to benchmark data changes when possible. If a tooling update is required, submit it as a separate PR or call it out explicitly.

Maintainers review every submission for completeness, consistency, and evidence. After approval, they run the publishing pipeline (`make pdf`, `make mkdocs`, etc.) and update the public website. Contributors do not need to include generated files in their PRs.

## Reviews and Turnaround

- Reviewers may ask for clarifications or references supporting scores, metrics, or dataset claims.
- Once merged, updates appear on the public site after the maintainers run their publishing workflow.

## Reporting Issues or Requesting Benchmarks

If you spot a problem in the catalogue or would like to request a new benchmark for consideration, open an issue with relevant context and supporting links.

## Code of Conduct

We expect all contributors to adhere to the MLCommons Code of Conduct, available from the organisation’s “Policies” page (<https://mlcommons.org/policies/>).

Thank you for contributing to the benchmark community!
