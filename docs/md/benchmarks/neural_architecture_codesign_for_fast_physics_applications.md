# Neural Architecture Codesign for Fast Physics Applications


**Date**: 2025-01-09


**Name**: Neural Architecture Codesign for Fast Physics Applications


**Domain**: Physics; Materials Science; Particle Physics


**Focus**: Automated neural architecture search and hardware-efficient model codesign for fast physics applications


**Keywords**: neural architecture search, FPGA deployment, quantization, pruning, hls4ml


**Task Types**: Classification, Peak finding


**Metrics**: Accuracy, Latency, Resource utilization


**Models**: NAC-based BraggNN, NAC-optimized Deep Sets  jet 


**Citation**:


- Jason Weitz, Dmitri Demler, Luke McDermott, Nhan Tran, and Javier Duarte. Neural architecture codesign for fast physics applications. 2025. URL: https://arxiv.org/abs/2501.05515, arXiv:2501.05515.

  - bibtex: |

      @misc{weitz2025neuralarchitecturecodesignfast,

        archiveprefix={arXiv},

        author={Jason Weitz and Dmitri Demler and Luke McDermott and Nhan Tran and Javier Duarte},

        eprint={2501.05515},

        primaryclass={cs.LG},

        title={Neural Architecture Codesign for Fast Physics Applications},

        url={https://arxiv.org/abs/2501.05515},

        year={2025}

      }



**Ratings:**


Specification:


  - **Rating:** 10.0


  - **Reason:** Task is clearly defined  triggering on rare events with sub-10 micros latency ; architecture, constraints, and system context  FPGA, Alveo  are well detailed. 


Dataset:


  - **Rating:** 7.0


  - **Reason:** Simulated tracking data from sPHENIX and EIC; internally structured but not yet released in a public FAIR-compliant format. 


Metrics:


  - **Rating:** 10.0


  - **Reason:** Accuracy, latency, and hardware resource utilization  LUTs, DSPs  are clearly defined and used in evaluation. 


Reference Solution:


  - **Rating:** 9.0


  - **Reason:** Graph-based models  BGN-ST, GarNet  are implemented and tested on real hardware; reproducibility possible with hls4ml but full scripts not bundled. 


Documentation:


  - **Rating:** 8.0


  - **Reason:** Paper is detailed and tool usage  FlowGNN, hls4ml  is described, but repo release and dataset access remain in progress. 


**Radar Plot:**
 ![Neural Architecture Codesign For Fast Physics Applications radar plot](../../tex/images/neural_architecture_codesign_for_fast_physics_applications_radar.png)