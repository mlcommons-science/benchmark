# Benchmark YAML Files

All YAML files must follow the format listed in the [formatting file](benchmarks-format.yaml).

IMPORTANT: Indentation must use two spaces, *not tabs*.

## Additional Formatting Rules

- **Field Definition**: All fields must exist, they must not be ommitted. 

- **Field Values**: No field can be `null`. If a field is unknown, use "unknown" instead.
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

```
- date: "2020-09-07"
  version: "1"
  last_updated: "2020-09-07"
  expired: "false"
  valid: "yes"
  valid_date: "2025-07-28"
  name: "MMLU (Massive Multitask Language Understanding)"
  url: "https://paperswithcode.com/dataset/mmlu"
  doi: "10.48550/arXiv.2009.03300"
  domain: "Multidomain"
  focus: "Academic knowledge and reasoning across 57 subjects"
  keywords:
  - "multitask"
  - "multiple-choice"
  - "zero-shot"
  - "few-shot"
  - "knowledge probing"
  summary: |
    Measuring Massive Multitask Language Understanding (MMLU) is a benchmark of 57 
    multiple-choice tasks covering elementary mathematics, US history, computer science, 
    law, and more, designed to evaluate a model's breadth and depth of knowledge in 
    zero-shot and few-shot settings.
  licensing: "MIT License"
  task_types:
  - "Multiple choice"
  ai_capability_measured:
  - "General reasoning, subject-matter understanding"
  metrics:
  - "Accuracy"
  models:
  - "GPT-4o"
  - "Gemini 1.5 Pro"
  - "o1"
  - "DeepSeek-R1"
  ml_motif:
  - "General knowledge"
  type: "Benchmark"
  ml_task:
  - "Supervised Learning"
  solutions: "1"
  notes: "Good"
  contact:
    name: "Dan Hendrycks"
    email: "dan (at) safe.ai"
  cite:
  - |
    @misc{hendrycks2021measuring,
      title={Measuring Massive Multitask Language Understanding},
      author={Hendrycks, Dan and Burns, Collin and Kadavath, Saurav},
      journal={arXiv preprint arXiv:2009.03300},
      year={2021},
      url={https://arxiv.org/abs/2009.03300}
    }
  datasets:
    links:
    - name: "Papers with Code datasets"
      url: "https://github.com/paperswithcode/paperswithcode-data"
  results:
    links:
    - name: "Chinchilla"
      url: "https://arxiv.org/abs/2203.15556"
  fair:
    reproducible: true
    benchmark_ready: true
  ratings:
    software:
      rating: 10
      reason: |
        Well documented Github, instructions and dataset easy to download
    specification:
      rating: 9
      reason: |
        Clearly defined method of giving inputs, although it lacks hardware specifications.
    dataset:
      rating: 9
      reason: |
        Contains predefined few-shot development, validation, and testing set. Easy to access and download, but not versioned.
    metrics:
      rating: 9
      reason: |
        Clearly defined primary metric of number of multiple-choice questions answered correctly.
        Secondary metric of confidence requires models to self-report.
    reference_solution:
      rating: 10
      reason: |
        Performance and links to several top models linked on the Github.
    documentation:
      rating: 8
      reason: |
        Code and datasets provided and easy to find, but no environment setup instructions given.
```
