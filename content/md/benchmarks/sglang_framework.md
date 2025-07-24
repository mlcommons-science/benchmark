# SGLang Framework


**Date**: 2023-12-12


**Name**: SGLang Framework


**Domain**: LLM Vision


**Focus**: Fast serving framework for LLMs and vision-language models


**Keywords**: LLM serving, vision-language, RadixAttention, performance, JSON decoding


**Task Types**: Model serving framework


**Metrics**: Tokens/sec, Time-to-first-token, Throughput gain vs baseline


**Models**: LLaVA, DeepSeek, Llama


**Citation**:


- Lianmin Zheng, Liangsheng Yin, Zhiqiang Xie, Chuyue Sun, Jeff Huang, Cody Hao Yu, Shiyi Cao, Christos Kozyrakis, Ion Stoica, Joseph E. Gonzalez, Clark Barrett, and Ying Sheng. Sglang: efficient execution of structured language model programs. 2024. URL: https://arxiv.org/abs/2312.07104, arXiv:2312.07104.

  - bibtex: |

      @misc{zheng2024sglangefficientexecutionstructured,

        archiveprefix = {arXiv},

        author        = {Lianmin Zheng and Liangsheng Yin and Zhiqiang Xie and Chuyue Sun and Jeff Huang and Cody Hao Yu and Shiyi Cao and Christos Kozyrakis and Ion Stoica and Joseph E. Gonzalez and Clark Barrett and Ying Sheng},

        eprint        = {2312.07104},

        primaryclass  = {cs.AI},

        title         = {SGLang: Efficient Execution of Structured Language Model Programs},

        url           = {https://arxiv.org/abs/2312.07104},

        year          = {2024}

      }



**Ratings:**


Specification:


  - **Rating:** 8.0


  - **Reason:** Clearly framed around surrogate learning across 16 domains, but not all tasks are formally posed or constrained in a unified benchmark protocol. Paper mentions performance on NVIDIA H100.


Dataset:


  - **Rating:** 9.0


  - **Reason:** FAIR-compliant physics simulation dataset, structured in HDF5 with unified metadata.


Metrics:


  - **Rating:** 7.0


  - **Reason:** Metrics like dataset size and domain coverage are listed, but standardized quantitative model evaluation metrics  e.g., RMSE, MAE  are not enforced.


Reference Solution:


  - **Rating:** 9.0


  - **Reason:** FNO and U-Net baselines available; full benchmarking implementations pending NeurIPS paper code release.


Documentation:


  - **Rating:** 10.0


  - **Reason:** Site and GitHub offer a unified API, metadata standards, and dataset loading tools; NeurIPS paper adds detailed design context.


**Radar Plot:**
 ![Sglang Framework radar plot](../../tex/images/sglang_framework_radar.png)