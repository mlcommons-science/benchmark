# Nixtla NeuralForecast


**Edit:** [edit this entry](https://github.com/mlcommons-science/benchmark/tree/main/source)


**Date**: 2022-04-01


**Name**: Nixtla NeuralForecast


**Domain**: Time-series forecasting; General ML


**Focus**: High-performance neural forecasting library with >30 models


**Keywords**: time-series, neural forecasting, NBEATS, NHITS, TFT, probabilistic forecasting, usability


**Task Types**: Time-series forecasting


**Metrics**: RMSE, MAPE, CRPS


**Models**: NBEATS, NHITS, TFT, DeepAR


**Citation**:


- Kin G. Olivares, Cristian Challú, Federico Garza, Max Mergenthaler Canseco, and Artur Dubrawski. Neuralforecast: user friendly state-of-the-art neural forecasting models. PyCon Salt Lake City, Utah, US 2022, 2022. URL: https://github.com/Nixtla/neuralforecast.

  - bibtex:
      ```
      @misc{olivares2022library_neuralforecast,

        author={Kin G. Olivares and Cristian Challú and Federico Garza and Max Mergenthaler Canseco and Artur Dubrawski},

        title = {NeuralForecast: User friendly state-of-the-art neural forecasting models.},

        year={2022},

        howpublished={PyCon Salt Lake City, Utah, US 2022},

        url={https://github.com/Nixtla/neuralforecast}

      }

      ```

**Ratings:**


Software:


  - **Rating:** 5


  - **Reason:** Actively maintained open-source library under Apache 2.0. Offers a clean API, extensive model zoo  >30 models , integration with Ray, Optuna, and supports scalable training and inference workflows. 


Specification:


  - **Rating:** 5


  - **Reason:** Forecasting task is well-defined with clear input/output structures. Framework supports probabilistic and deterministic forecasting, with unified interfaces and support for batch evaluation. 


Dataset:


  - **Rating:** 3


  - **Reason:** NeuralForecast does not include its own datasets but supports standard datasets  e.g., M4, M5, ETT . FAIR compliance depends on user-supplied data. 


Metrics:


  - **Rating:** 5


  - **Reason:** RMSE, MAPE, CRPS, and other domain-relevant metrics are well supported and integrated into the evaluation loop. 


Reference Solution:


  - **Rating:** 4


  - **Reason:** Includes runnable model baselines and training scripts for all supported models. Some models have pretrained weights, but not all are fully benchmarked out-of-the-box. 


Documentation:


  - **Rating:** 5


  - **Reason:** Rich documentation with examples, API references, tutorials, notebooks, and CLI support. PyPI, GitHub, and official blog posts offer clear guidance for usage and extension. 


**Average Rating:** 4.5


**Radar Plot:**
 ![Nixtla Neuralforecast radar plot](../../tex/images/nixtla_neuralforecast_radar.png)