# Scientific AI Benchmark Collection

This repository holds a list of scientific AI benchmarks. 

It is maintained through a [yaml file](source/benchmarks.yaml) to which anyone can add through a pull request.
*Note: Future versions may seperate the inclusion of benchmarks in seperate yaml files.*

To edit, go to our
[edit link](https://github.com/mlcommons-science/benchmark/edit/main/source/benchmarks.yaml) and create a pull request when done.

All benchmark entries must follow the format as defined in `source/benchmarks-format.yaml`.  This file also includes a simple explanation for each field. The file has placeholder attributes, which should be substituted for the benchmark's content. Attribute explanations are at the end of this README.

Make sure that yaml indentation is **2 spaces** and do not use tabs. 

To rate benchmarks, use the [rating system](ratings_explanations.md). 

The yaml file is used to generate documents, that should only created with our programs while making cahnges to the yaml files. The produced files must not be changed by hand. 

Intermediate files are produced in a content directory, while the officially published files are publisched in the docs directory. as we do not publish the content directory, we only refer to the docs directory documents. If you conduct development and use our programs please look at the comntent directory for intermediate documents. The most important document is the PDF report document we produce:

* A pdf report provinding various summaries and detailed information about the benchmarks. 

    * [benchmarks,pdf](docs/tex/benchmarks.pdf)

If you like to cite this report, please use the following:

Text:

Gregor von Laszewski, Reece Shiraishi, Anjay Krishnan, Nhan Tran, Benjamin Hawks, and Geoffrey C. Fox. AI Scientific Benchmarks Comparison. GitHub, July 2025. Available at: https://mlcommons-science.github.io/benchmark/benchmarks.pdf

BibTex:

```
@misc{benchmark-collection,
    title={AI Scientific Benchmarks Comparison}
    author={Gregor von Laszewski and Reece Shiraishi and Anjay Krishnan and Nhan Tran and Benjamin Hawks and Geoffrey C. Fox}
    url={https://mlcommons-science.github.io/benchmark/benchmarks.pdf}
    howpublished={Github},
    year={2025}
    month=jul
}
```


To have some quickly accessible information in a format that you can further manipulate, we are providing you with markdown documenys.

This includes an index file pointing you to all individual benchmarks

* [benchmarks.md](https://mlcommons-science.github.io/benchmark/md/benchmarks.md)



## Instalation

The content must be modified only through the YAML
file and never directly. To simplify the generation we have created an easy to use [Makefile](Makefile).

The software will work on any OS on which we can install python, LaTeX. In case your system has LaTeX missing please install it or get inspired by our 

* make install 

target. Just make sure you install the full tex-live version as well as biber and latexmk. If you do not use our makefile.

To install the needed python requirements, make sure you start a python virtual environment and then use 

make requirements

as target.

A list of required Python packages is in the [requirements document](requirements.txt).

## Generating the documents


To generate the pdf document pleas use 

```make pdf```

To generate the markdown files use

```make md```

In case you need to start from a clean content dir, you can use

```make clean```

## Publishing

To publish the documents on github we use the `/docs` directory. However, this is supposed to be only done ofter a manual review. Please, do not publish the results from any document generated in `/docs`. Instead, contact Gregor von Laszewski with laszewski at gmail.com. At this time only he will publish new content after review.


## Adding new data

New yaml files can be added easily with a pull request. If you need to add a new entry, please use a unique identifying name and add the yaml file for that entry in 

* <https://github.com/mlcommons-science/benchmark/tree/main/source>

with a pull request. To make sure you conform to the current format, you can use the template provided at:

* <https://github.com/mlcommons-science/benchmark/blob/main/source/benchmarks-format.yaml>



The format of the a
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
