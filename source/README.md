# Benchmark YAML Files

All YAML files must follow the format listed in the [formatting file](benchmarks-format.yaml).

IMPORTANT: Indentation must use two spaces, *not tabs*.

## Additional Formatting Rules

- **Field Definition**: All fields must exist, they must not be ommitted. 

- **Field Velues**: No field can be `null`. If a field is unknown, use "unknown" instead.
    - Use `bin/check_structure.py` to automatically check YAML structures.

- **Strings:** We recommend to use "quotes" around any value that is a string. THis includes URLs and strings that contain charaters such as : _ and others.

- **Datatypes:** The datatype of each entry must match that of the formatting file. If a formatting file entry is a YAML list, the fields of all other entries must be a YAML list.

- **Multiline Fields:** Multiline fields should not use quotes. Instead, they should use newline bar notation.  

## Examples

An example for miltiline fields is:
     
```
field_name: |
  This is a multiline description of the field.
  It does not contain quotes or newline characters.
```

An example in a list, i.e. in the `cite` field is:  

```
cite:
  - |
    @misc{samplecitationlabel2020,
      title={My Awesome Discovery}, 
      author={Doe, Jane and Doe, John},
      year={2020},
      eprint={1234.56789},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://www.example.com}, 
    }
  - |
    @misc{samplecitation2024,
      title={My Second Awesome Discovery}, 
      author={Doe, Jane and Doe, John},
      year={2024},
      eprint={9876.54321},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://www.example.com}, 
    }
```

- **URLs:** Every benchmark entry's `url` field must point to the benchmark's GitHub, official website, or associated paper. *`url` cannot be "unknown".*

- **Citation Labels**: All citation labels in BibTeX citations across *all* given files must be unique.


### Sample of properly formatted YAML document

Please use 2 charachters for indentations.
Bug: this example is incomlete as it includes ... (should be fixed)

```
- date: "2025-02-15"
  version: "1"
  last_updated: "2025-02-15"
  expired: "false"
  valid: "yes"
  valid_date: "2025-02-15"
  name: "MATH-500"
  url: "https://huggingface.co/datasets/HuggingFaceH4/MATH-500"
  doi: "unknown"
  domain: "Mathematics"
  focus: "Math reasoning generalization"
  keywords:
  - "calculus"
  - "algebra"
  - "number theory"
  - "geometry"
  summary: |
    MATH-500 is a curated subset of 500 problems from the OpenAI MATH dataset, spanning
    high-school to advanced levels, designed to evaluate LLMs mathematical reasoning and 
    generalization.
  ...
  datasets:
    links:
    - name: "Hugging Face"
      url: "https://huggingface.co/datasets/HuggingFaceH4/MATH-500"
  results:
    links:
    - name: "unknown"
      url: "unknown"
  fair:
    reproducible: true
    benchmark_ready: true
  ratings:
    software:
    rating: 0
    reason: |
      Not yet evaluated
    specification:
      rating: 3
      reason: |
        Known what the problems are, but method of presentation and evaluation is not stated. No HW constraints
      dataset:
        rating: 9.9
        reason: |
            Problems and solutions are easily downloaded. Could not find a way to download the data
      metrics:
        rating: 2
        reason: |
            Problem spec states that all of the AI reasoning steps are subject to grading, but no specified way to evaluate the steps
      reference_solution:
        rating: 0
        reason: |
            Not given
      documentation:
        rating: 0.5
        reason: |
            Not given. Implicit instructions to download dataset.
...
```
