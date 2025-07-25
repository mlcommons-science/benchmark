# GeSS


**Date**: 2024-12-13


**Name**: GeSS


**Domain**: Scientific ML; Geometric Deep Learning


**Focus**: Benchmark suite evaluating geometric deep learning models under real-world distribution shifts


**Keywords**: geometric deep learning, distribution shift, OOD robustness, scientific applications


**Task Types**: Classification, Regression


**Metrics**: Accuracy, RMSE, OOD robustness delta


**Models**: GCN, EGNN, DimeNet++


**Citation**:


- Deyu Zou, Shikun Liu, Siqi Miao, Victor Fung, Shiyu Chang, and Pan Li. Gess: benchmarking geometric deep learning under scientific applications with distribution shifts. In A. Globerson, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. Tomczak, and C. Zhang, editors, Advances in Neural Information Processing Systems, volume 37, 92499–92528. Curran Associates, Inc., 2024. URL: https://proceedings.neurips.cc/paper_files/paper/2024/file/a8063075b00168dc39bc81683619f1a8-Paper-Datasets_and_Benchmarks_Track.pdf.

  - bibtex: |

      @inproceedings{neurips2024_a8063075,

        author = {Zou, Deyu and Liu, Shikun and Miao, Siqi and Fung, Victor and Chang, Shiyu and Li, Pan},

        booktitle = {Advances in Neural Information Processing Systems},

        editor = {A. Globerson and L. Mackey and D. Belgrave and A. Fan and U. Paquet and J. Tomczak and C. Zhang},

        pages = {92499--92528},

        publisher = {Curran Associates, Inc.},

        title = {GeSS: Benchmarking Geometric Deep Learning under Scientific Applications with Distribution Shifts},

        url = {https://proceedings.neurips.cc/paper_files/paper/2024/file/a8063075b00168dc39bc81683619f1a8-Paper-Datasets_and_Benchmarks_Track.pdf},

        volume = {37},

        year = {2024}

      }



**Ratings:**


Specification:


  - **Rating:** 9.0


  - **Reason:** Well-defined problem  Tc prediction, generation  with strong scientific motivation  high-Tc materials , but no formal hardware constraints. 


Dataset:


  - **Rating:** 9.0


  - **Reason:** Includes curated 3D crystal structures and Tc data; readily downloadable and used in paper models. 


Metrics:


  - **Rating:** 9.0


  - **Reason:** MAE and structural validity used, well-established in materials modeling. 


Reference Solution:


  - **Rating:** 8.0


  - **Reason:** Provides two reference models  SODNet, DiffCSP-SC  with results. Code likely available post-conference. 


Documentation:


  - **Rating:** 8.0


  - **Reason:** Paper and poster explain design choices well; software availability confirms reproducibility but limited external documentation. 


**Radar Plot:**
 ![Gess radar plot](../../tex/images/gess_radar.png)