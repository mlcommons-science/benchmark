# BenchCouncil BigDataBench


**Date**: 2020-01-01


**Name**: BenchCouncil BigDataBench


**Domain**: General


**Focus**: Big data and AI benchmarking across structured, semi-structured, and unstructured data workloads


**Keywords**: big data, AI benchmarking, data analytics


**Task Types**: Data preprocessing, Inference, End-to-end data pipelines


**Metrics**: Data throughput, Latency, Accuracy


**Models**: CNN, LSTM, SVM, XGBoost


**Citation**:


- Wanling Gao, Jianfeng Zhan, Lei Wang, Chunjie Luo, Daoyi Zheng, Xu Wen, Rui Ren, Chen Zheng, Xiwen He, Hainan Ye, Haoning Tang, Zheng Cao, Shujie Zhang, and Jiahui Dai. Bigdatabench: a scalable and unified big data and ai benchmark suite. 2018. URL: https://arxiv.org/abs/1802.08254, arXiv:1802.08254.

  - bibtex: |

      @misc{gao2018bigdatabenchscalableunifiedbig,

        archiveprefix = {arXiv},

        author        = {Wanling Gao and Jianfeng Zhan and Lei Wang and Chunjie Luo and Daoyi Zheng and Xu Wen and Rui Ren and Chen Zheng and Xiwen He and Hainan Ye and Haoning Tang and Zheng Cao and Shujie Zhang and Jiahui Dai},

        eprint        = {1802.08254},

        primaryclass  = {cs.DC},

        title         = {BigDataBench: A Scalable and Unified Big Data and AI Benchmark Suite},

        url           = {https://arxiv.org/abs/1802.08254},

        year          = {2018}

      }



**Ratings:**


Specification:


  - **Rating:** 9.0


  - **Reason:** Evaluates AI at multiple levels  micro to end-to-end ; tasks and workloads are clearly defined, though specific I/O formats and constraints vary. 


Dataset:


  - **Rating:** 9.0


  - **Reason:** Realistic datasets across diverse domains; FAIR structure for many components, but individual datasets may not all be versioned or richly annotated. 


Metrics:


  - **Rating:** 9.0


  - **Reason:** Latency, throughput, and accuracy clearly defined for end-to-end tasks; consistent across models and setups. 


Reference Solution:


  - **Rating:** 8.0


  - **Reason:** Reference implementations for several tasks exist, but setup across all tasks is complex and not fully streamlined. 


Documentation:


  - **Rating:** 8.0


  - **Reason:** Central documentation exists, with detailed component breakdowns; environment setup across platforms  e.g., hardware variations  can require manual adjustment. 


**Radar Plot:**
 ![Benchcouncil Bigdatabench radar plot](../../tex/images/benchcouncil_bigdatabench_radar.png)