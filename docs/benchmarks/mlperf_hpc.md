# MLPerf HPC


**Date**: 2021-10-20


**Name**: MLPerf HPC


**Domain**: Cosmology, Climate, Protein Structure, Catalysis


**Focus**: Scientific ML training and inference on HPC systems


**Keywords**: HPC, training, inference, scientific ML


**Task Types**: Training, Inference


**Metrics**: Training time, Accuracy, GPU utilization


**Models**: CosmoFlow, DeepCAM, OpenCatalyst


**Citation**:


- Steven Farrell, Murali Emani, Jacob Balma, Lukas Drescher, Aleksandr Drozd, Andreas Fink, Geoffrey Fox, David Kanter, Thorsten Kurth, Peter Mattson, Dawei Mu, Amit Ruhela, Kento Sato, Koichi Shirahata, Tsuguchika Tabaru, Aristeidis Tsaris, Jan Balewski, Ben Cumming, Takumi Danjo, Jens Domke, Takaaki Fukai, Naoto Fukumoto, Tatsuya Fukushi, Balazs Gerofi, Takumi Honda, Toshiyuki Imamura, Akihiko Kasagi, Kentaro Kawakami, Shuhei Kudo, Akiyoshi Kuroda, Maxime Martinasso, Satoshi Matsuoka, Henrique Mendonça, Kazuki Minami, Prabhat Ram, Takashi Sawada, Mallikarjun Shankar, Tom St. John, Akihiro Tabuchi, Venkatram Vishwanath, Mohamed Wahib, Masafumi Yamazaki, and Junqi Yin. Mlperf hpc: a holistic benchmark suite for scientific machine learning on hpc systems. 2021. URL: https://arxiv.org/abs/2110.11466, arXiv:2110.11466.

  - bibtex: |

      @misc{farrell2021mlperfhpcholisticbenchmark,

        archiveprefix = {arXiv},

        author        = {Steven Farrell and Murali Emani and Jacob Balma and Lukas Drescher and Aleksandr Drozd and Andreas Fink and Geoffrey Fox and David Kanter and Thorsten Kurth and Peter Mattson and Dawei Mu and Amit Ruhela and Kento Sato and Koichi Shirahata and Tsuguchika Tabaru and Aristeidis Tsaris and Jan Balewski and Ben Cumming and Takumi Danjo and Jens Domke and Takaaki Fukai and Naoto Fukumoto and Tatsuya Fukushi and Balazs Gerofi and Takumi Honda and Toshiyuki Imamura and Akihiko Kasagi and Kentaro Kawakami and Shuhei Kudo and Akiyoshi Kuroda and Maxime Martinasso and Satoshi Matsuoka and Henrique Mendonça and Kazuki Minami and Prabhat Ram and Takashi Sawada and Mallikarjun Shankar and Tom St. John and Akihiro Tabuchi and Venkatram Vishwanath and Mohamed Wahib and Masafumi Yamazaki and Junqi Yin},

        eprint        = {2110.11466},

        primaryclass  = {cs.LG},

        title         = {MLPerf HPC: A Holistic Benchmark Suite for Scientific Machine Learning on HPC Systems},

        url           = {https://arxiv.org/abs/2110.11466},

        year          = {2021}

      }



**Ratings:**


Specification:


  - **Rating:** 9.0


  - **Reason:** Focused on structured/unstructured data pipelines; clearly defined tasks spanning analytics to AI; some scenarios lack hardware constraint modeling.


Dataset:


  - **Rating:** 9.0


  - **Reason:** Built from 13 real-world sources; structured for realistic big data scenarios; partially FAIR-compliant with documented data motifs.


Metrics:


  - **Rating:** 9.0


  - **Reason:** Covers data throughput, latency, and accuracy; quantitative and benchmark-ready.


Reference Solution:


  - **Rating:** 8.0


  - **Reason:** Many pipeline and model examples provided using Hadoop/Spark/Flink; setup effort varies by task and platform.


Documentation:


  - **Rating:** 8.0


  - **Reason:** Strong documentation with examples and task specifications; centralized support exists, but task-specific tuning may require domain expertise.


**Radar Plot:**
 ![Mlperf Hpc radar plot](../../tex/images/mlperf_hpc_radar.png)