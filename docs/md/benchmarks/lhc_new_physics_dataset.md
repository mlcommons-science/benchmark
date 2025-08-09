# LHC New Physics Dataset


**Edit:** [edit this entry](https://github.com/mlcommons-science/benchmark/tree/main/source)


**Date**: 2021-07-05


**Name**: LHC New Physics Dataset


**Domain**: Particle Physics; Real-time Triggering


**Focus**: Real-time LHC event filtering for anomaly detection using proton collision data


**Keywords**: anomaly detection, proton collision, real-time inference, event filtering, unsupervised ML


**Task Types**: Anomaly detection, Event classification


**Metrics**: ROC-AUC, Detection efficiency


**Models**: Autoencoder, Variational autoencoder, Isolation forest


**Citation**:


- Thea Aarrestad, Ekaterina Govorkova, Jennifer Ngadiuba, Ema Puljak, Maurizio Pierini, and Kinga Anna Wozniak. Unsupervised new physics detection at 40 mhz: training dataset. 2021. URL: https://zenodo.org/record/5046389, doi:10.5281/ZENODO.5046389.

  - bibtex:
      ```
      @misc{https://doi.org/10.5281/zenodo.5046389,

        author    = {Aarrestad, Thea and Govorkova, Ekaterina and Ngadiuba, Jennifer and Puljak, Ema and Pierini, Maurizio and Wozniak, Kinga Anna},

        copyright = {Creative Commons Attribution 4.0 International},

        doi       = {10.5281/ZENODO.5046389},

        publisher = {Zenodo},

        title     = {Unsupervised New Physics detection at 40 MHz: Training Dataset},

        url       = {https://zenodo.org/record/5046389},

        year      = {2021}

      }

      ```

**Ratings:**


Software:


  - **Rating:** 3


  - **Reason:** While not formally evaluated in the previous version, Zenodo and paper links suggest available code for baseline models  e.g., autoencoders, GANs , though they are scattered and not unified in a single repository. 


Specification:


  - **Rating:** 3


  - **Reason:** The task and context are clearly described, but system constraints and formal inputs/outputs are not fully specified. 


Dataset:


  - **Rating:** 5


  - **Reason:** Large-scale dataset hosted on Zenodo, publicly available, well-documented, with defined train/test structure. Appears to follow at least 4 FAIR principles. 


Metrics:


  - **Rating:** 4


  - **Reason:** Uses reasonable metrics  ROC-AUC, detection efficiency  that capture performance but lacks full explanation and standard evaluation tools. 


Reference Solution:


  - **Rating:** 2


  - **Reason:** Baselines are described across multiple papers but lack centralized, reproducible implementations and hardware/software setup details. 


Documentation:


  - **Rating:** 3


  - **Reason:** Some description in papers and dataset metadata exists, but lacks a unified guide, README, or training setup in a central location. 


**Average Rating:** 3.333


**Radar Plot:**
 ![Lhc New Physics Dataset radar plot](../../tex/images/lhc_new_physics_dataset_radar.png)