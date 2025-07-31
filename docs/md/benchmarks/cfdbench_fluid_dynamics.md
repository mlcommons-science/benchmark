# CFDBench (Fluid Dynamics)


**Date**: 2024-10-01


**Name**: CFDBench  Fluid Dynamics 


**Domain**: Fluid Dynamics; Scientific ML


**Focus**: Neural operator surrogate modeling


**Keywords**: neural operators, CFD, FNO, DeepONet


**Task Types**: Surrogate modeling


**Metrics**: L2 error, MAE


**Models**: FNO, DeepONet, U-Net


**Citation**:


- Yining Luo, Yingfa Chen, and Zhen Zhang. Cfdbench: a large-scale benchmark for machine learning methods in fluid dynamics. 2024. URL: https://arxiv.org/abs/2310.05963.

  - bibtex: |

      @misc{luo2024cfdbenchlargescalebenchmarkmachine,

        title={CFDBench: A Large-Scale Benchmark for Machine Learning Methods in Fluid Dynamics},

        author={Luo, Yining and Chen, Yingfa and Zhang, Zhen},

        year={2024},

        url={https://arxiv.org/abs/2310.05963}

      }



**Ratings:**


Specification:


  - **Rating:** 10


  - **Reason:** Tasks are clearly framed  PDE regression, surrogate modeling , with explicit details on the four canonical CFD problems, input/output structure, and generalization goals. 


Dataset:


  - **Rating:** 10


  - **Reason:** Publicly available on Zenodo, versioned, with metadata and splits; covers thousands of simulations with proper documentation. 


Metrics:


  - **Rating:** 9


  - **Reason:** Quantitative metrics  L2 error, MAE, relative error  are clearly defined and align with regression task objectives. 


Reference Solution:


  - **Rating:** 8


  - **Reason:** Baseline models like FNO and DeepONet are implemented, but full reproduction pipelines or eval scripts may require additional user configuration. 


Documentation:


  - **Rating:** 6


  - **Reason:** GitHub and Zenodo provide data and code, but setup for evaluating across all 739 cases requires moderate user effort and technical fluency with PyTorch-based frameworks. Reproducibility depends on full implementation details. 


**Radar Plot:**
 ![Cfdbench Fluid Dynamics radar plot](../../tex/images/cfdbench_fluid_dynamics_radar.png)