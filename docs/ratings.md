# Benchmark Rating System

Benchmarks are rated in six categories. Each category receives a score from **0** (lowest; criterion not met) to **5** (highest). Non-integer scores are allowed when evidence is partial or uncertain.

- **C1: Software-Environment and Codebase Setup**
- **C2: Problem Specification and Constraints**
- **C3: Dataset with FAIR Principles**
- **C4: Performance Metrics**
- **C5: Reference Solution**
- **C6: Documentation**

The detailed guidance for each category matches the original rubric and is reproduced below.

## C1: Software-Environment and Codebase Setup

Clarity of task, inputs, outputs, and system constraints. Award 1 point for each “yes”:

1. Is code available to reproduce the baseline/reference results?
2. Is it complete?
3. Is it well documented?
4. Does the provided code run without modifications?
5. Is it containerized, or are environment/setup instructions provided?

## C2: Problem Specification and Constraints

Award 1 point for every statement that is true:

1. System constraints are provided.
2. The task is clear.
3. The dataset format is mentioned.
4. Inputs are specified.
5. Outputs are specified.

## C3: Dataset with FAIR Principles

Measures how well the dataset follows FAIR principles (Findability, Accessibility, Interoperability, Reusability) and whether stable splits exist.

- Award 1 point for each FAIR principle that is met.
- Add 1 additional point if the dataset provides training/validation/testing splits (or an equivalent structure).

## C4: Performance Metrics

Quantifiable measures for comparison:

- **3 points** if the metrics are fully defined.
- **1–2 points** if metrics exist but are only partially defined.
- **0 points** if metrics are undefined.

Capture of benchmark goals:

- **2 points** when the metrics fully capture model performance for the stated goal.
- **1 point** if the metrics partially capture the goal.
- **0 points** if the metrics do not assess performance.

## C5: Reference Solution

Baseline implementation demonstrating task feasibility. Award 1 point for each “yes”:

1. Is a reference solution available?
2. Is it well documented?
3. Are hardware and software requirements listed?
4. Are all metrics evaluated?
5. Is the baseline model trainable and available for study?

## C6: Documentation

Award 1 point for each of the following that is explained:

1. Task
2. Background
3. Motivation
4. Evaluation criteria

Add 1 additional point if at least one academic paper about the benchmark exists.
