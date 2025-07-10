# Scientific AI Benchmark Collection

This repository holds a list of scientific AI benchmarks. 

It is maintained through a yaml file to which anyone can add through a
pull request. The file is located at:

* https://github.com/mlcommons-science/benchmark/blob/main/source/benchmarks.yaml

To edit simply follow our
[edit][https://github.com/mlcommons-science/benchmark/edit/main/source/benchmarks.yaml]
link and create the pull request when done.

Make sure that the entries are in the format specified and that
indentation is used with 2 spaces, do not use tabs. The explanation of
the attributes is given at the end of this README.

Form this yaml file several documents are generated. An index file that
points to individual markdown files for each benchmark 

* https://github.com/mlcommons-science/benchmark/blob/main/content/md/index.md

A pdf file that generates a table of selected attributes and its tex
source and bibtex file

* https://github.com/mlcommons-science/benchmark/blob/main/content/tex/benchmarks.pdf
* https://github.com/mlcommons-science/benchmark/tree/main/content/tex


## Generating the PDF, TeX, and md files

The content should not be directly modified, but instead only the YAML
file. The content can be generated with a simple make file under the
assumption you have latex, biber, and latexmk installed

To generate the pdf and TeX files use

```make pdf```

To generate the markdown files use

```make md```

In case you need to start from a clean content dir, you can use

```make clean```



## Attributes

This is the list of current attriutes

* date: date first found

* expired: date when we first noted it is no longer valid

* valid: yes if still valid

* name: The name of the benchmark

* url: The main url for the benchmark

* domain: The scientific domain(s) of this benchmark

* focus: short keyword of wht the main focus of the benchmark is

* keyword: keywords related to this benchmark

* description: A short paragraph describing the benchamrk (abstract)

* task_types (from either task_types or tasks): Gregor forgot what
  this is, figure out

* ai_capability_measured (from either ai_capability_measured or
  metrics): A more detailed description of what AI task is measured,
  could be keywords

* metrics: The main metrics defined by this benchmark

* models: The main models used in this benchmark

* notes: additinal notes to this benchmark

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
