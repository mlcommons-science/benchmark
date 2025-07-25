# 4D-STEM


**Date**: 2023-12-03


**Name**: 4D-STEM


**Domain**: Material Science


**Focus**: Real-time ML for scanning transmission electron microscopy


**Keywords**: 4D-STEM, electron microscopy, real-time, image processing


**Task Types**: Image Classification, Streamed data inference


**Metrics**: Classification accuracy, Throughput


**Models**: CNN models  prototype 


**Citation**:


- Shuyu Qin, Joshua Agar, and Nhan Tran. Extremely noisy 4d-tem strain mapping using cycle consistent spatial transforming autoencoders. In AI for Accelerated Materials Design - NeurIPS 2023 Workshop. 2023. URL: https://openreview.net/forum?id=7yt3N0o0W9.

  - bibtex: |

      @inproceedings{qin2023extremely,

        title={Extremely Noisy 4D-TEM Strain Mapping Using Cycle Consistent Spatial Transforming Autoencoders},

        author={Shuyu Qin and Joshua Agar and Nhan Tran},

        booktitle={AI for Accelerated Materials Design - NeurIPS 2023 Workshop},

        year={2023},

        url={https://openreview.net/forum?id=7yt3N0o0W9}

      }



**Ratings:**


Specification:


  - **Rating:** 9.0


  - **Reason:** Peak localization task is well-defined for diffraction images; input/output described clearly, but no system constraints.


Dataset:


  - **Rating:** 8.0


  - **Reason:** Simulated diffraction images provided; reusable and downloadable, but not externally versioned or FAIR-structured.


Metrics:


  - **Rating:** 9.0


  - **Reason:** Inference speed and localization accuracy are standard and quantitatively reported.


Reference Solution:


  - **Rating:** 8.0


  - **Reason:** BraggNN model and training pipeline exist, but need stitching from separate repositories.


Documentation:


  - **Rating:** 8.0


  - **Reason:** Paper and codebase are available and usable, though not fully turnkey.


**Radar Plot:**
 ![D-Stem radar plot](../../tex/images/d-stem_radar.png)