# MLCommons Science


**Date**: 2023-06-01


**Name**: MLCommons Science


**Domain**: Earthquake, Satellite Image, Drug Discovery, Electron Microscope, CFD


**Focus**: AI benchmarks for scientific applications including time-series, imaging, and simulation


**Keywords**: science AI, benchmark, MLCommons, HPC


**Task Types**: Time-series analysis, Image classification, Simulation surrogate modeling


**Metrics**: MAE, Accuracy, Speedup vs simulation


**Models**: CNN, GNN, Transformer


**Citation**:


- Jeyan Thiyagalingam, Gregor von Laszewski, Junqi Yin, Murali Emani, Juri Papay, Gregg Barrett, Piotr Luszczek, Aristeidis Tsaris, Christine Kirkpatrick, Feiyi Wang, Tom Gibbs, Venkatram Vishwanath, Mallikarjun Shankar, Geoffrey Fox, and Tony Hey. Ai benchmarking for science: efforts from the mlcommons science working group. In Hartwig Anzt, Amanda Bienz, Piotr Luszczek, and Marc Baboulin, editors, High Performance Computing. ISC High Performance 2022 International Workshops, 47–64. Cham, 2022. Springer International Publishing.

  - bibtex: |

      @InProceedings{10.1007/978-3-031-23220-6_4,

        author="Thiyagalingam, Jeyan

        and von Laszewski, Gregor

        and Yin, Junqi

        and Emani, Murali

        and Papay, Juri

        and Barrett, Gregg

        and Luszczek, Piotr

        and Tsaris, Aristeidis

        and Kirkpatrick, Christine

        and Wang, Feiyi

        and Gibbs, Tom

        and Vishwanath, Venkatram

        and Shankar, Mallikarjun

        and Fox, Geoffrey

        and Hey, Tony",

        editor="Anzt, Hartwig

        and Bienz, Amanda

        and Luszczek, Piotr

        and Baboulin, Marc",

        title="AI Benchmarking for Science: Efforts from the MLCommons Science Working Group",

        booktitle="High Performance Computing. ISC High Performance 2022 International Workshops",

        year="2022",

        publisher="Springer International Publishing",

        address="Cham",

        pages="47--64",

        abstract="With machine learning (ML) becoming a transformative tool for science, the scientific community needs a clear catalogue of ML techniques, and their relative benefits on various scientific problems, if they were to make significant advances in science using AI. Although this comes under the purview of benchmarking, conventional benchmarking initiatives are focused on performance, and as such, science, often becomes a secondary criteria.",

        isbn="978-3-031-23220-6"

      }



**Ratings:**


Specification:


  - **Rating:** 10.0


  - **Reason:** Scientific ML tasks  e.g., CosmoFlow, DeepCAM  are clearly defined with HPC system-level constraints and targets.


Dataset:


  - **Rating:** 9.0


  - **Reason:** Public scientific datasets  e.g., cosmology, weather ; used consistently, though FAIR-compliance of individual datasets varies slightly.


Metrics:


  - **Rating:** 10.0


  - **Reason:** Training time, GPU utilization, and accuracy are all directly measured and benchmarked across HPC systems.


Reference Solution:


  - **Rating:** 9.0


  - **Reason:** Reference implementations available and actively maintained; HPC setup may require domain-specific environment.


Documentation:


  - **Rating:** 9.0


  - **Reason:** GitHub repo and papers provide detailed instructions; reproducibility supported across multiple institutions.


**Radar Plot:**
 ![Mlcommons Science radar plot](../../tex/images/mlcommons_science_radar.png)