# Quench detection


**Date**: 2024-10-15


**Name**: Quench detection


**Domain**: Accelerators and Magnets


**Focus**: Real-time detection of superconducting magnet quenches using ML


**Keywords**: quench detection, autoencoder, anomaly detection, real-time


**Task Types**: Anomaly detection, Quench localization


**Metrics**: ROC‑AUC, Detection latency


**Models**: Autoencoder, RL agents  in development 


**Citation**:


- Could not parse citation: 

  - bibtex: |



**Ratings:**


Specification:


  - **Rating:** 10.0


  - **Reason:** Real-time jet origin classification under FPGA constraints is clearly defined, with explicit latency targets  ~100 ns  and I/O formats.


Dataset:


  - **Rating:** 9.0


  - **Reason:** Data available on Zenodo with DOI, includes constituent-level jets; accessible and well-documented, though not deeply versioned with full FAIR metadata.


Metrics:


  - **Rating:** 10.0


  - **Reason:** Accuracy, latency, and hardware resource usage  LUTs, DSPs  are rigorously measured and aligned with real-time goals.


Reference Solution:


  - **Rating:** 9.0


  - **Reason:** Includes models  MLP, Deep Sets, Interaction Networks  with quantization-aware training and synthesis results via hls4ml; reproducible but tightly coupled with specific toolchains.


Documentation:


  - **Rating:** 8.0


  - **Reason:** Paper and code  via hls4ml  are sufficient, but a centralized, standalone repo for reproducing all models would enhance accessibility.


**Radar Plot:**
 ![Quench Detection radar plot](../../tex/images/quench_detection_radar.png)