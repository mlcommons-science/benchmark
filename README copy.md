# benchmark


## Attribute

This is the list of current attriutes

* date: date first found (so far, "date" looks like the date the benchmark was published)

* expired: date when we first noted it is no longer valid

* valid: yes if still valid, no otherwise

* name: The name of the benchmark

* url: Link to where the benchmark is defined or where additional information can be found

* domain: The scientific domain(s) of this benchmark

* focus: short keyword of what the main focus of the benchmark is

* keyword: keywords related to this benchmark

* description: A short paragraph describing the benchamrk (abstract)

* task_types (from either task_types or tasks): formats of questions that can be asked to the AI

* ai_capability_measured (from either ai_capability_measured or
  metrics): A more detailed description of what AI task is measured,
  could be keywords

* metrics: How the benchmark measures AI performance

* models: The main models used in this benchmark

* notes: additional notes about this benchmark

* cite: citations as enumerated list in bibtex format


## Proposed Markdown


```
# Science Benchmarks

## Name of the benchmark

| Attribute | Description |
| ----------- | ----------- |
| name | abc |
| date | xyz |
...


```
