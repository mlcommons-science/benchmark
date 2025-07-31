# Scientific AI Benchmark Collection

This repository holds a list of scientific AI benchmarks. 

It is maintained through a [yaml file](source/benchmarks.yaml) to which anyone can add through a pull request.

To edit, go to our
[edit link](https://github.com/mlcommons-science/benchmark/edit/main/source/benchmarks.yaml) and create the pull request when done.

All benchmark entries should follow the format of `source/benchmarks-format.yaml`. The file has placeholder attributes, which should be substituted for the benchmark's content. Attribute explanations are at the end of this README.

Make sure that yaml indentation is **2 spaces**. *Do not use tabs.* 

To rate benchmarks, use the system defined [here](ratings.md).

The yaml file is used to generate documents, such as:

* An index Markdown file, which points to individual Markdown files: https://github.com/mlcommons-science/benchmark/blob/main/content/md/index.md

* A pdf file with a table of selected attributes: https://github.com/mlcommons-science/benchmark/blob/main/content/tex/benchmarks.pdf

* A TeX source and its BibTeX bibliography: https://github.com/mlcommons-science/benchmark/tree/main/content/tex


## Generating the PDF, TeX, and md files

The content should be modified only through the YAML
file (never directly). The content can be generated with a Makefile given that you have latex, biber, and latexmk installed.

To generate the pdf and TeX files use

```make pdf```

To generate the markdown files use

```make md```

In case you need to start from a clean content dir, you can use

```make clean```



## Attributes

This is the list of attributes that currently appear in the script outputs:

* date: date first found

* expired: date when we first noted it is no longer valid

* valid: yes if still valid

* name: The name of the benchmark

* url: The main url for the benchmark

* domain: The scientific domain(s) of this benchmark

* focus: short keyword of wht the main focus of the benchmark is

* keyword: keywords related to this benchmark

* description: A short paragraph describing the benchmark (abstract)

* task_types (from either task_types or tasks): Gregor forgot what
  this is, figure out

* ai_capability_measured (from either ai_capability_measured or
  metrics): A more detailed description of what AI task is measured,
  could be keywords

* metrics: The main metrics defined by this benchmark

* models: The main models used in this benchmark

* notes: additinal notes to this benchmark

* cite: citations as enumerated list in bibtex format

For more information on the rating system, see the [ratings explanations](ratings.md).


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
