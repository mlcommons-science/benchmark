# MLCommons Science Working Group AI Benchmarks Collection

This repository holds a list of scientific AI benchmarks. 

It is maintained through a [YAML file](source/benchmarks.yaml) to which anyone can add through a pull request.
*Note: Future versions may separate the inclusion of benchmarks in separate YAML files.*

To edit, go to our
[edit link](https://github.com/mlcommons-science/benchmark/edit/main/source/benchmarks.yaml) and create a pull request when done.

All benchmark entries must follow the format as defined in `source/benchmarks-format.yaml`.  This file also includes a simple explanation for each field. The file contains placeholder attributes that should be substituted for the benchmark's content. Attribute explanations are at the end of this README.

Make sure that YAML indentation is **2 spaces** and do not use tabs. 

To rate benchmarks, use the [rating system](README-ratings.md). 

The YAML file is used to generate documents, which should only be created with our programs while making changes to the YAML files. The produced files must not be changed by hand. 

Intermediate files are produced in a content directory, while the officially published files are published in the docs directory. As we do not publish the content directory, we only refer to the docs directory documents. If you conduct development and use our programs, please look at the content directory for intermediate documents. The most important document is the PDF report document we produce:

* A PDF report providing various summaries and detailed information about the benchmarks. 

    * [benchmarks,pdf](docs/tex/benchmarks.pdf)

If you like to cite this report, please use the following:

Text:

Gregor von Laszewski, Reece Shiraishi, Anjay Krishnan, Nhan Tran, Benjamin Hawks, Marco Colombo, and Geoffrey C. Fox. AI Scientific Benchmarks Comparison. GitHub, July 2025. Available at: https://mlcommons-science.github.io/benchmark/benchmarks.pdf

BibTex:

```
@misc{www-las-mlcommons-benchmark-coolection,
      author = {
        Gregor von Laszewski and 
        Ben Hawks and 
        Marco Colombo and
        Reece Shiraishi and
        Anjay Krishnan and
        Nhan Tran and
        Geoffrey C. Fox},
      title = {MLCommons Science Working Group AI Benchmarks Collection},
      url = {https://mlcommons-science.github.io/benchmark/benchmarks.pdf},
      note = "Online Collection: \url={https://mlcommons-science.github.io/benchmark/}",
      month = jun,
      year = 2025,
      howpublished = "GitHub"
    } 
```


To have some quickly accessible information in a format that you can further manipulate, we are providing you with markdown documents.

This includes an index file pointing you to all individual benchmarks

* [benchmarks.md](https://mlcommons-science.github.io/benchmark/md/benchmarks_table/)



## Instalation

The content must be modified only through the YAML
file and never directly. To simplify the generation, we have created an easy-to-use [Makefile](Makefile).

The software will work on any OS on which we can install Python, LaTeX. In case your system has LaTeX missing, please install it or get inspired by our 

```make install```

target. Just make sure you install the full tex-live version as well as biber and latexmk. If you do not use our makefile.

To install the needed Python requirements, make sure you start a Python virtual environment and then use 

```make requirements```

as target.

A list of required Python packages is in the [requirements document](requirements.txt).

## Generating the documents


To generate the PDF document please use 

```make pdf```

To generate the markdown files, use

```make md```

In case you need to start from a clean content dir, you can use

```make clean```

## Publishing

To publish the documents on GitHub we use the `/docs` directory. However, this is supposed to be only done after a manual review. Please, do not publish the results from any document generated in `/docs`. Instead, contact Gregor von Laszewski with laszewski at gmail.com. At this time, only he will publish new content after review.


## Adding new data

New YAML files can be added easily with a pull request. If you need to add a new entry, please use a unique identifying name and add the YAML file for that entry in 

* <https://github.com/mlcommons-science/benchmark/tree/main/source>

with a pull request. To make sure you conform to the current format, you can use the template provided at:

* <https://github.com/mlcommons-science/benchmark/blob/main/source/benchmarks-format.yaml>

## Important additional documentation

* [READEME-bin](RAEDME-bin.md)
* [READEME-ratings](RAEDME-ratings.md)
* [READEME-yaml](RAEDME-yaml.md)
* [requirements.txt](requirements.txt)

* [benchmarks-format.yaml](source/benchmarks-format.yaml])
* [benchmarks-sample.yaml](source/benchmarks-sample.yaml])

## YAML Contents

* [benchmarks.yaml](source/benchmarks.yaml])
* [benchmarks-addon.yaml](source/benchmarks-addon.yaml])

## Code Contributors

* <https://github.com/mlcommons-science/benchmark/graphs/contributors>

## Developers documentation

```
make pdf
make mkdocs
make view
make view-local

```

# Docker (Quick Start)

## Build
```bash
docker build -t benchmark .
```

## Run (shell in repo)
```bash
docker run --rm -it -v "$PWD":/workspace -e SERVE_HOST=0.0.0.0 -p 8000:8000 benchmark
```
