# MLCommons Science Working Group AI Benchmarks Collection

This site curates a collection of AI benchmarks developed and maintained by the **MLCommons Science Working Group**. The repository provides a structured *ontology* of benchmark definitions, tooling for validation and publication, and a generated website for browsing the collection.

The primary artifact of this project is the benchmark report:

- **Report (PDF):** [benchmarks.pdf](benchmarks.pdf)

Users can explore the benchmark collection through the web interfaces described below. Contributions to the ontology and tooling are welcome, and citation guidelines are provided at the end of this document.

## Online Browsing Views

We provide three views for browsing (each entry links to its detailed page):

- **[Cards view](md/benchmarks/cards/)**: richest UI with advanced filtering, tag-based quick filters, and interactive sorting controls.
- **[Table view](md/benchmarks_table/)**: compact table where you can toggle visible columns and download the data as CSV or JSON.
- **[List view](md/benchmarks/)**: straightforward alphabetical list of benchmark names.

> **Note:** The Markdown pages are generated for web browsing and should **not** be cited.

## Contributing

Contributions to the benchmark collection are welcome. For full guidelines, please see the repository documentation. In brief:

- Proposed changes, new benchmarks, or corrections should follow the workflow described in `CONTRIBUTING.md`.
- Benchmark definitions should adhere to the YAML schema provided in the repository.
- All generated content (Markdown, LaTeX, MkDocs pages) is automatically produced; please do not edit generated files directly.

For the complete contribution workflow, consult: <https://github.com/mlcommons-science/benchmark>.

## How to Cite

If you use this repository, the benchmark collection, or any derived artifacts, please cite all relevant works associated with this project, including the benchmark collection itself and the companion papers.

### MLCommons Science Working Group AI Benchmarks Collection

Gregor von Laszewski, Ben Hawks, Marco Colombo, Reece Shiraishi, Anjay Krishnan, Nhan Tran, and Geoffrey C. Fox. 2025. *MLCommons Science Working Group AI Benchmarks Collection.* MLCommons Science Working Group. Available at: https://mlcommons-science.github.io/benchmark/benchmarks.pdf

<details class="bibtex">
<summary>BibTeX entry</summary>

```bibtex
@misc{mlcommons-benchmarks-collection,
  author = {
    Gregor von Laszewski and 
    Ben Hawks and 
    Marco Colombo and
    Reece Shiraishi and
    Anjay Krishnan and
    Nhan Tran and
    Geoffrey C. Fox
  },
  title = {MLCommons Science Working Group AI Benchmarks Collection},
  url = {https://mlcommons-science.github.io/benchmark/benchmarks.pdf},
  note = "Online Collection: \url{https://mlcommons-science.github.io/benchmark/}",
  month = jun,
  year = 2025,
  howpublished = {GitHub}
}
```

</details>

### An MLCommons Scientific Benchmarks Ontology

Ben Hawks, Gregor von Laszewski, Matthew D. Sinclair, Marco Colombo, Shivaram Venkataraman, Rutwik Jain, Yiwei Jiang, Nhan Tran, and Geoffrey Fox. 2025. *An MLCommons Scientific Benchmarks Ontology.* arXiv:2511.05614.

<details class="bibtex">
<summary>BibTeX entry</summary>

```bibtex
@misc{hawks2025mlcommonsscientificbenchmarksontology,
      title={An MLCommons Scientific Benchmarks Ontology}, 
      author={Ben Hawks and Gregor von Laszewski and Matthew D. Sinclair and Marco Colombo and Shivaram Venkataraman and Rutwik Jain and Yiwei Jiang and Nhan Tran and Geoffrey Fox},
      year={2025},
      eprint={2511.05614},
      archivePrefix={arXiv},
      primaryClass={cs.LG},
      url={https://arxiv.org/abs/2511.05614}, 
}
```

</details>

### AI Benchmarks Carpentry and Democratization

Gregor von Laszewski, Wesley Brewer, Jeyan Thiyagalingam, Juri Papay, Armstrong Foundjem, Piotr Luszczek, Murali Emani, Shirley V. Moore, Vijay Janapa Reddi, Matthew D. Sinclair, Sebastian Lobentanzer, Sujata Goswami, Benjamin Hawks, Marco Colombo, Nhan Tran, Christine R. Kirkpatrick, Abdulkareem Alsudais, Gregg Barrett, Tianhao Li, Kirsten Morehouse, Shivaram Venkataraman, Rutwik Jain, Kartik Mathur, Victor Lu, Tejinder Singh, Khojasteh Z. Mirza, Kongtao Chen, Sasidhar Kunapuli, Gavin Farrell, Renato Umeton, and Geoffrey C. Fox. 2025. *AI Benchmark Democratization and Carpentry.* arXiv:2512.11588.

<details class="bibtex">
<summary>BibTeX entry</summary>

```bibtex
@misc{vonlaszewski2025aibenchmarkdemocratizationcarpentry,
  title = {AI Benchmark Democratization and Carpentry},
  author = {Gregor von Laszewski and Wesley Brewer and Jeyan Thiyagalingam and Juri Papay and Armstrong Foundjem and Piotr Luszczek and Murali Emani and Shirley V. Moore and Vijay Janapa Reddi and Matthew D. Sinclair and Sebastian Lobentanzer and Sujata Goswami and Benjamin Hawks and Marco Colombo and Nhan Tran and Christine R. Kirkpatrick and Abdulkareem Alsudais and Gregg Barrett and Tianhao Li and Kirsten Morehouse and Shivaram Venkataraman and Rutwik Jain and Kartik Mathur and Victor Lu and Tejinder Singh and Khojasteh Z. Mirza and Kongtao Chen and Sasidhar Kunapuli and Gavin Farrell and Renato Umeton and Geoffrey C. Fox},
  year = {2025},
  eprint = {2512.11588},
  archivePrefix = {arXiv},
  primaryClass = {cs.AI},
  url = {https://arxiv.org/abs/2512.11588}
}
```

</details>

For program-level improvements, contact **Gregor von Laszewski** at `laszewski at gmail.com`.
