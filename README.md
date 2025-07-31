# Scientific AI Benchmark Collection

This repository holds a list of scientific AI benchmarks. 

It is maintained through a [yaml file](source/benchmarks.yaml) to which anyone can add through a pull request.

To edit, go to our
[edit link](https://github.com/mlcommons-science/benchmark/edit/main/source/benchmarks.yaml) and create the pull request when done.

All benchmark entries should follow the format of `source/benchmarks-format.yaml`. The file has placeholder attributes, which should be substituted for the benchmark's content. Attribute explanations are at the end of this README.

Make sure that yaml indentation is **2 spaces**. *Do not use tabs.* 

To rate benchmarks, use the system defined [here](ratings_explanations.md).

The yaml file is used to generate documents, such as:

* An index Markdown file, which points to individual Markdown files: https://github.com/mlcommons-science/benchmark/blob/main/content/md/index.md

* A pdf file with a table of selected attributes: https://github.com/mlcommons-science/benchmark/blob/main/content/tex/benchmarks.pdf

* A TeX source and its BibTeX bibliography: https://github.com/mlcommons-science/benchmark/tree/main/content/tex


## Generating the PDF, TeX, and md files

The content should be modified only through the YAML
file (never directly). The content can be generated with the [Makefile](Makefile) given that you have latex, biber, and latexmk installed.  
A list of required Python packages is in the [requirements document](requirements.txt).

To generate the pdf and TeX files use

```make pdf```

To generate the markdown files use

```make md```

In case you need to start from a clean content dir, you can use

```make clean```


## Attributes

This is the list of attributes that currently appear in the script outputs:

* date: date when the benchmark was first found. In YYYY-MM-DD format.

* name: The benchmark's title as listed in the paper or project GitHub

* domain: The scientific domain(s) of this benchmark, i.e. physics, biology, math

* focus: short sentence on the main topics of the benchmark. Likely to be deprecated.

* keywords: keywords related to this benchmark, which may appear in a paper abstract

* task_types: what models evaluated by the benchmark should do

* metrics: The main ways of measuring performance on the benchmark, i.e. number of questions correct

* models: List of notable models that were evaluated with the benchmark

* cite: List of BibTeX citations

* ratings (each category listed separately): See the [ratings explanations](ratings_explanations.md).
