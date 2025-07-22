# Delta Squared‑DFT


**Date**: 2024-12-13


**Name**: Delta Squared‑DFT


**Domain**: Computational Chemistry; Materials Science


**Focus**: Benchmarking machine-learning corrections to DFT using Delta Squared-trained models for reaction energies


**Keywords**: density functional theory, Delta Squared‑ML correction, reaction energetics, quantum chemistry


**Task Types**: Regression


**Metrics**: Mean Absolute Error  eV , Energy ranking accuracy


**Models**: Delta Squared‑ML correction networks, Kernel ridge regression


**Citation**:


- Kuzma Khrabrov, Anton Ber, Artem Tsypin, Konstantin Ushenin, Egor Rumiantsev, Alexander Telepov, Dmitry Protasov, Ilya Shenbin, Anton Alekseev, Mikhail Shirokikh, Sergey Nikolenko, Elena Tutubalina, and Artur Kadurin. $\nabla ^2$dft: a universal quantum chemistry dataset of drug-like molecules and a benchmark for neural network potentials. 2024. URL: https://arxiv.org/abs/2406.14347, arXiv:2406.14347.

  - bibtex: |

      @misc{khrabrov2024nabla2dftuniversalquantumchemistry,

        title={$\nabla^2$DFT: A Universal Quantum Chemistry Dataset of Drug-Like Molecules and a Benchmark for Neural Network Potentials}, 

        author={Kuzma Khrabrov and Anton Ber and Artem Tsypin and Konstantin Ushenin and Egor Rumiantsev and Alexander Telepov and Dmitry Protasov and Ilya Shenbin and Anton Alekseev and Mikhail Shirokikh and Sergey Nikolenko and Elena Tutubalina and Artur Kadurin},

        year={2024},

        eprint={2406.14347},

        archivePrefix={arXiv},

        primaryClass={physics.chem-ph},

        url={https://arxiv.org/abs/2406.14347}, 

      }



**Ratings:**


Specification:


  - **Rating:** 8.0


  - **Reason:** Clear goals around unifying urban data formats and tasks  e.g., air quality prediction , though some specifics could be more formal.


Dataset:


  - **Rating:** 9.0


  - **Reason:** Multi-modal data is standardized and accessible; GitHub repo available.


Metrics:


  - **Rating:** 8.0


  - **Reason:** Uses common task metrics like accuracy/RMSE, though varies by task.


Reference Solution:


  - **Rating:** 7.0


  - **Reason:** Baseline regression/classification models included.


Documentation:


  - **Rating:** 8.0


  - **Reason:** Source code supports pipeline reuse, but formal evaluation splits may vary.


**Radar Plot:**
 ![Delta Squareddft radar plot](../../tex/images/delta_squareddft_radar.png)