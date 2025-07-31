# Rating System Details

## 0-10 Ratings (deprecated)
Benchmarks are rated on 5 categories: problem specification and constraints, dataset, performance metrics, reference solution and reproducible protocol. Each category received a score from 0 (lowest; nonexistent) to 10 (maximum score).

A category may receive a score of NA. NA means that the required information is known to exist, but cannot be verified.  
Non-integer scores are possible.

This system is deemed too subjective. The wide range of possible ratings allows the reviewer to include personal opinion, decreasing the rating's precision.  
The system is deprecated as of 2025-07-30.

### Problem Specification and Constraints
Clarity of task, inputs, outputs, and system constraints.
- 9–10: Clear task, inputs/outputs defined and format specified, system constraints quantified (e.g., latency, hardware).
- 7–8: Well-defined task, most constraints present / Slight lack of clarity about either inputs or outputs
- 5–6: Moderately well defined task / critical information about inputs and outputs (i.e. question type, format) are unclear or missing, but most other info is present
- 3–4: Vague task description, inputs or outputs not specified.
- 1–2: Task intent unclear.
- 0: Not present

### Dataset (FAIR Principles)
Follows FAIR principles (Findability, Accessibility, Interoperability, Reusability); versioned, stable splits.
- 9–10: Fully FAIR, documented, versioned, reproducible with train/test/validation set splits.
- 7–8: Mostly FAIR, good documentation but minor gaps. At most 1 of the FAIR principles missing or questionable.
- 5–6: Usable dataset, but not fully FAIR or missing metadata/versioning. <=2 FAIR principles missing or questionable.
- 3–4: Partially accessible or inconsistently formatted. <=3 FAIR principles missing or questionable.
- 1–2: Closed or unstandardized data. All FAIR principles missing or questionable.
- 0: No dataset available 

### Performance Metrics
Quantifiable measures for comparison
- 9–10: Methods for comparison quantitative. Measured model’s output entirely falls within the stated comparison method. Reviewers do not need to guess the meaning of the benchmark results.
- 7–8: Some subjective measures / small portions of the model’s output may not be covered by the metrics / reviewer must take minor inferences to interpret the results
- 5–6: Mostly subjective measures / metrics do not cover significant portions of model output / output requires substantial guesswork to interpret
- 3–4: Nearly all subjective measures / model output is mostly outside of the metrics / meaning of the output is poorly specified
- 1–2: Metrics do not explain model output / results are extremely difficult to quantify or measure
- 0: No metrics stated

### Reference Solution
Baseline implementation demonstrating task feasibility.
- 9–10: Well documented, reproducible baseline provided with performance results. 
- 7–8: Functional baseline included and evaluated, but lacks full documentation or reproducibility details.
- 5–6: Baseline exists but is not evaluated using the benchmark or has little instructions for reproduction
- 3–4: Baseline performance briefly mentioned but not run with the benchmark, or partial implementation with no reported results.
- 1–2: Reference solution briefly mentioned but is vague
- 0: No reference solution or baseline presented

### Reproducible Protocol
Code, environment, and instructions to reproduce results.
- 9–10: Full code, environments, and scripts. Any resources that are not provided have easily followed instructions to obtain and use them.
- 7–8: Code provided but environment setup or instructions incomplete.
- 5–6: Partial code or missing critical environment setup details.
- 3–4: Code inaccessible or incomplete. Environment setup details missing.
- 1–2: Missing 2 of the 3 of: accessible code, environment install instructions, use instructions
- 0: No code, environment or instructions to reproduce results provided