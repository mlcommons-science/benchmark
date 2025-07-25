# Ultrafast jet classification at the HL-LHC


**Date**: 2024-07-08


**Name**: Ultrafast jet classification at the HL-LHC


**Domain**: Particle Physics


**Focus**: FPGA-optimized real-time jet origin classification at the HL-LHC


**Keywords**: jet classification, FPGA, quantization-aware training, Deep Sets, Interaction Networks


**Task Types**: Classification


**Metrics**: Accuracy, Latency, Resource utilization


**Models**: MLP, Deep Sets, Interaction Network


**Citation**:


- Patrick Odagiu, Zhiqiang Que, Javier Duarte, Johannes Haller, Gregor Kasieczka, Artur Lobanov, Vladimir Loncar, Wayne Luk, Jennifer Ngadiuba, Maurizio Pierini, Philipp Rincke, Arpita Seksaria, Sioni Summers, Andre Sznajder, Alexander Tapper, and Thea K. Aarrestad. Ultrafast jet classification on fpgas for the hl-lhc. 2024. URL: https://arxiv.org/abs/2402.01876, arXiv:2402.01876, doi:https://doi.org/10.1088/2632-2153/ad5f10.

  - bibtex: |

      @misc{odagiu2024ultrafastjetclassificationfpgas,

        archiveprefix = {arXiv},

        author        = {Patrick Odagiu and Zhiqiang Que and Javier Duarte and Johannes Haller and Gregor Kasieczka and Artur Lobanov and Vladimir Loncar and Wayne Luk and Jennifer Ngadiuba and Maurizio Pierini and Philipp Rincke and Arpita Seksaria and Sioni Summers and Andre Sznajder and Alexander Tapper and Thea K. Aarrestad},

        doi           = {https://doi.org/10.1088/2632-2153/ad5f10},

        eprint        = {2402.01876},

        primaryclass  = {hep-ex},

        title         = {Ultrafast jet classification on FPGAs for the HL-LHC},

        url           = {https://arxiv.org/abs/2402.01876},

        year          = {2024}

      }



**Ratings:**


Specification:


  - **Rating:** 8.0


  - **Reason:** Task is clear  RL control of beam stability , with BOOSTR-based simulator; control objectives are well motivated, but system constraints and reward structure are still under refinement. 


Dataset:


  - **Rating:** 7.0


  - **Reason:** BOOSTR dataset exists and is cited, but integration into the benchmark is in early stages; metadata and FAIR structure are limited. 


Metrics:


  - **Rating:** 7.0


  - **Reason:** Stability and control loss are mentioned, but metrics are not yet formalized with clear definitions or baselines. 


Reference Solution:


  - **Rating:** 5.5


  - **Reason:** DDPG baseline mentioned; PPO planned; implementation is still in progress with no reproducible results available yet. 


Documentation:


  - **Rating:** 6.0


  - **Reason:** GitHub has a defined structure but is incomplete; setup and execution instructions for training/evaluation are not fully established. 


**Radar Plot:**
 ![Ultrafast Jet Classification At The Hl-Lhc radar plot](../../tex/images/ultrafast_jet_classification_at_the_hl-lhc_radar.png)