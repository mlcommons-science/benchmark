# The Well


**Edit:** [edit this entry](https://github.com/mlcommons-science/benchmark/tree/main/source)


**Date**: 2024-12-03


**Name**: The Well


**Domain**: biological systems, fluid dynamics, acoustic scattering, astrophysical MHD


**Focus**: Foundation model + surrogate dataset spanning 16 physical simulation domains


**Keywords**: surrogate modeling, foundation model, physics simulations, spatiotemporal dynamics


**Task Types**: Supervised Learning


**Metrics**: Dataset size, Domain breadth


**Models**: FNO baselines, U-Net baselines


**Citation**:


- Ruben Ohana, Michael McCabe, Lucas Meyer, Rudy Morel, Fruzsina J. Agocs, Miguel Beneitez, Marsha Berger, Blakesley Burkhart, Stuart B. Dalziel, Drummond B. Fielding, Daniel Fortunato, Jared A. Goldberg, Keiya Hirashima, Yan-Fei Jiang, Rich R. Kerswell, Suryanarayana Maddu, Jonah Miller, Payel Mukhopadhyay, Stefan S. Nixon, Jeff Shen, Romain Watteaux, Bruno Régaldo-Saint Blancard, François Rozet, Liam H. Parker, Miles Cranmer, and Shirley Ho. The well: a large-scale collection of diverse physics simulations for machine learning. In A. Globerson, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. Tomczak, and C. Zhang, editors, Advances in Neural Information Processing Systems, volume 37, 44989–45037. Curran Associates, Inc., 2024. URL: https://proceedings.neurips.cc/paper_files/paper/2024/file/4f9a5acd91ac76569f2fe291b1f4772b-Paper-Datasets_and_Benchmarks_Track.pdf.

  - bibtex:
      ```
      @inproceedings{neurips2024_4f9a5acd,

        author = {Ohana, Ruben and McCabe, Michael and Meyer, Lucas and Morel, Rudy and Agocs, Fruzsina J. and Beneitez, Miguel and Berger, Marsha and Burkhart, Blakesley and Dalziel, Stuart B. and Fielding, Drummond B. and Fortunato, Daniel and Goldberg, Jared A. and Hirashima, Keiya and Jiang, Yan-Fei and Kerswell, Rich R. and Maddu, Suryanarayana and Miller, Jonah and Mukhopadhyay, Payel and Nixon, Stefan S. and Shen, Jeff and Watteaux, Romain and Blancard, Bruno R\'{e}galdo-Saint and Rozet, Fran\c{c}ois and Parker, Liam H. and Cranmer, Miles and Ho, Shirley},

        booktitle = {Advances in Neural Information Processing Systems},

        editor = {A. Globerson and L. Mackey and D. Belgrave and A. Fan and U. Paquet and J. Tomczak and C. Zhang},

        pages = {44989--45037},

        publisher = {Curran Associates, Inc.},

        title = {The Well: a Large-Scale Collection of Diverse Physics Simulations for Machine Learning},

        url = {https://proceedings.neurips.cc/paper_files/paper/2024/file/4f9a5acd91ac76569f2fe291b1f4772b-Paper-Datasets_and_Benchmarks_Track.pdf},

        volume = {37},

        year = {2024}

      }

      ```

**Ratings:**


Software:


  - **Rating:** 5


  - **Reason:** BSD-licensed software and unified API are available via GitHub and PyPI. Supports loading and manipulating large HDF5 datasets across 16 domains. 


Specification:


  - **Rating:** 4


  - **Reason:** The benchmark includes clearly defined surrogate modeling tasks, data structure, and metadata. However, constraints and formal task specs vary slightly across domains. 


Dataset:


  - **Rating:** 5


  - **Reason:** 15 TB of ML-ready HDF5 datasets across 16 physics domains. Public, well-structured, richly annotated, and designed with FAIR principles in mind. 


Metrics:


  - **Rating:** 3


  - **Reason:** Domain breadth and dataset size are emphasized. Standardized quantitative metrics for model evaluation  e.g., RMSE, accuracy  are not uniformly applied across all domains. 


Reference Solution:


  - **Rating:** 3


  - **Reason:** Includes FNO and U-Net baselines, but does not yet provide fully trained, reproducible models or scripts across all datasets. 


Documentation:


  - **Rating:** 4


  - **Reason:** The GitHub repo and NeurIPS paper provide detailed guidance on dataset use, structure, and training setup. Tutorials and walkthroughs could be expanded further. 


**Average Rating:** 4.0


**Radar Plot:**
 ![The Well radar plot](../../tex/images/the_well_radar.png)