# HEDM (BraggNN)


**Date**: 2023-10-03


**Name**: HEDM  BraggNN 


**Domain**: Material Science


**Focus**: Fast Bragg peak analysis using deep learning in diffraction microscopy


**Keywords**: BraggNN, diffraction, peak finding, HEDM


**Task Types**: Peak detection


**Metrics**: Localization accuracy, Inference time


**Models**: BraggNN


**Citation**:


- Zhengchun Liu, Hemant Sharma, Jun-Sang Park, Peter Kenesei, Antonino Miceli, Jonathan Almer, Rajkumar Kettimuthu, and Ian Foster. Braggnn: fast x-ray bragg peak analysis using deep learning. 2021. URL: https://arxiv.org/abs/2008.08198, arXiv:2008.08198.

  - bibtex: |

      @misc{liu2021braggnnfastxraybragg,

        archiveprefix = {arXiv},

        author        = {Zhengchun Liu and Hemant Sharma and Jun-Sang Park and Peter Kenesei and Antonino Miceli and Jonathan Almer and Rajkumar Kettimuthu and Ian Foster},

        eprint        = {2008.08198},

        primaryclass  = {eess.IV},

        title         = {BraggNN: Fast X-ray Bragg Peak Analysis Using Deep Learning},

        url           = {https://arxiv.org/abs/2008.08198},

        year          = {2021}

      }



**Ratings:**


Specification:


  - **Rating:** 10.0


  - **Reason:** Fully specified: describes task  data filtering/classification, system design  on-sensor inference ,  latency  25 ns , and power constraints. 


Dataset:


  - **Rating:** 8.0


  - **Reason:** In-pixel charge cluster data used, but dataset release info is minimal; FAIR metadata/versioning limited. 


Metrics:


  - **Rating:** 9.0


  - **Reason:** Data rejection rate and power per pixel are clearly defined and directly tied to hardware goals. 


Reference Solution:


  - **Rating:** 9.0


  - **Reason:** 2-layer NN implementation is evaluated in hardware; reproducible via hls4ml flow with results in paper. 


Documentation:


  - **Rating:** 8.0


  - **Reason:** Paper is clear; Zenodo asset is referenced, but additional GitHub or setup repo would improve reproducibility. 


**Radar Plot:**
 ![Hedm Braggnn radar plot](../../tex/images/hedm_braggnn_radar.png)