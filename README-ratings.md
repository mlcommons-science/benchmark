# Rating System Details

Benchmarks are rated on 6 categories: 

* C1: Software-Environment and Codebase Setup
* C2: Problem Specification and Constraints
* C3: Dataset with FAIR Principles
* C4: Performance Metrics
* C5: Reference Solution
* C6: Documentation

Each category receives a score from 0 (lowest; nonexistent) to 5 (maximum score). Non-integer scores are possible if a criterion is questionable.

## C1: Software-Environment and Codebase Setup

Clarity of task, inputs, outputs, and system constraints.  
1 point is awarded for each "yes" answer:

- Is code available to reproduce the baseline/reference results? 
- Is it complete? 
- Is it well documented? 
- Does the provided code run without modifications?
- Is it containerized? / Are environments or setup instructions provided?

## C2: Problem Specification and Constraints

1 point is awarded for every true statement:

- System constraints are provided
- Task is clear
- Dataset format is mentioned
- Inputs specified
- Outputs specified
 
## C3: Dataset (FAIR Principles)

Follows FAIR principles (Findability, Accessibility, Interoperability, Reusability); versioned, stable splits.

1 point is awarded for each FAIR principle met. 1 additional point is awarded if the dataset has training/testing/validation splits or a combination thereof.

## C4: Performance Metrics

Quantifiable measures for comparison.

3 points are awarded if the metrics are fully defined.  
1-2 points are for partially defined metrics.  
0 points are for undefined metrics.

2 points are given if the metrics fully captures a model's performance, in the context of the benchmark's goal.  
1 point is for partially capturing the goal.  
0 points are for not assessing performance.

## C5: Reference Solution

Baseline implementation demonstrating task feasibility.  
1 point is awarded for every "yes" answer:

- Is a reference solution available?
- Is it well documented?
- Does it list all hardware & software requirements? 
- Are all metrics evaluated?
- Is the baseline model trainable and available for study?

## C6: Documentation

1 point is awarded for each of the following explained:

- task
- background
- motivation
- evaluation criteria

1 point is awarded if at least one academic paper about the benchmark exists.