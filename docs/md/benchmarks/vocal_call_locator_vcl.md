# Vocal Call Locator (VCL)


**Date**: 2024-12-13


**Name**: Vocal Call Locator  VCL 


**Domain**: Neuroscience; Bioacoustics


**Focus**: Benchmarking sound-source localization of rodent vocalizations from multi-channel audio


**Keywords**: source localization, bioacoustics, time-series, SSL


**Task Types**: Sound source localization


**Metrics**: Localization error  cm , Recall/Precision


**Models**: CNN-based SSL models


**Citation**:


- Ralph E Peterson, Aramis Tanelus, Christopher Ick, Bartul Mimica, Niegil Francis, Violet J Ivan, Aman Choudhri, Annegret L Falkner, Mala Murthy, David M Schneider, Dan H Sanes, and Alex H Williams. Vocal call locator benchmark (vcl) for localizing rodent vocalizations from multi-channel audio. In A. Globerson, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. Tomczak, and C. Zhang, editors, Advances in Neural Information Processing Systems, volume 37, 106370–106382. Curran Associates, Inc., 2024. URL: https://proceedings.neurips.cc/paper_files/paper/2024/file/c00d37d6b04d73b870b963a4d70051c1-Paper-Datasets_and_Benchmarks_Track.pdf.

  - bibtex: |

      @inproceedings{neurips2024_c00d37d6,

        author = {Peterson, Ralph E and Tanelus, Aramis and Ick, Christopher and Mimica, Bartul and Francis, Niegil and Ivan, Violet J and Choudhri, Aman and Falkner, Annegret L and Murthy, Mala and Schneider, David M and Sanes, Dan H and Williams, Alex H},

        booktitle = {Advances in Neural Information Processing Systems},

        editor = {A. Globerson and L. Mackey and D. Belgrave and A. Fan and U. Paquet and J. Tomczak and C. Zhang},

        pages = {106370--106382},

        publisher = {Curran Associates, Inc.},

        title = {Vocal Call Locator Benchmark (VCL) for localizing rodent vocalizations from multi-channel audio},

        url = {https://proceedings.neurips.cc/paper_files/paper/2024/file/c00d37d6b04d73b870b963a4d70051c1-Paper-Datasets_and_Benchmarks_Track.pdf},

        volume = {37},

        year = {2024}

      }



**Ratings:**


Specification:


  - **Rating:** 9.0


  - **Reason:** Clear benchmark scenarios across GDL tasks under multiple real-world shift settings; OOD settings precisely categorized. 


Dataset:


  - **Rating:** 8.0


  - **Reason:** Scientific graph datasets provided in multiple shift regimes; standardized splits across domains. Exact format of data not specified. 


Metrics:


  - **Rating:** 9.0


  - **Reason:** Includes base metrics  accuracy, RMSE  plus OOD delta robustness for evaluation under shifts. 


Reference Solution:


  - **Rating:** 9.0


  - **Reason:** Multiple baselines  11 algorithms x 3 backbones  evaluated; setup supports reproducible comparison. 


Documentation:


  - **Rating:** 2.0


  - **Reason:** Paper, poster, and source code provide thorough access to methodology and implementation. Setup instructions and accompanying code not present. 


**Radar Plot:**
 ![Vocal Call Locator Vcl radar plot](../../tex/images/vocal_call_locator_vcl_radar.png)