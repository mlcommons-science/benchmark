# MLPerf HPC

<p><a class="md-button back-link" href="../">← Back to all benchmarks</a></p>
<div class="info-block meta-block">
  <p class="meta-row"><span class="meta-label">Date</span><span class="meta-sep">:</span> <span class="meta-value">2021-10-20</span></p>
  <p class="meta-row"><span class="meta-label">Name</span><span class="meta-sep">:</span> <span class="meta-value">MLPerf HPC</span></p>
  <p class="meta-row"><span class="meta-label">Domain</span><span class="meta-sep">:</span> <span class="meta-value">Cosmology, Climate, Protein Structure, Catalysis</span></p>
  <p class="meta-row"><span class="meta-label">Focus</span><span class="meta-sep">:</span> <span class="meta-value">Scientific ML training and inference on HPC systems</span></p>
  <p class="meta-row"><span class="meta-label">Task Types</span><span class="meta-sep">:</span> <span class="meta-value">Training, Inference</span></p>
  <p class="meta-row"><span class="meta-label">Metrics</span><span class="meta-sep">:</span> <span class="meta-value">Training time, Accuracy, GPU utilization</span></p>
  <p class="meta-row"><span class="meta-label">Models</span><span class="meta-sep">:</span> <span class="meta-value">CosmoFlow, DeepCAM, OpenCatalyst</span></p>
</div>
<h3>Keywords</h3>

<div class="chips"><a class="chip chip-link" href="../#kw=HPC">HPC</a> <a class="chip chip-link" href="../#kw=training">training</a> <a class="chip chip-link" href="../#kw=inference">inference</a> <a class="chip chip-link" href="../#kw=scientific%20ML">scientific ML</a> </div>
<h3>Citation</h3>

- Steven Farrell, Murali Emani, Jacob Balma, Lukas Drescher, Aleksandr Drozd, Andreas Fink, Geoffrey Fox, David Kanter, Thorsten Kurth, Peter Mattson, Dawei Mu, Amit Ruhela, Kento Sato, Koichi Shirahata, Tsuguchika Tabaru, Aristeidis Tsaris, Jan Balewski, Ben Cumming, Takumi Danjo, Jens Domke, Takaaki Fukai, Naoto Fukumoto, Tatsuya Fukushi, Balazs Gerofi, Takumi Honda, Toshiyuki Imamura, Akihiko Kasagi, Kentaro Kawakami, Shuhei Kudo, Akiyoshi Kuroda, Maxime Martinasso, Satoshi Matsuoka, Henrique Mendonça, Kazuki Minami, Prabhat Ram, Takashi Sawada, Mallikarjun Shankar, Tom St. John, Akihiro Tabuchi, Venkatram Vishwanath, Mohamed Wahib, Masafumi Yamazaki, and Junqi Yin. Mlperf hpc: a holistic benchmark suite for scientific machine learning on hpc systems. 2021. URL: https://arxiv.org/abs/2110.11466, arXiv:2110.11466.

<pre><code class="language-bibtex">@misc{farrell2021mlperfhpcholisticbenchmark,
  archiveprefix = {arXiv},
  author        = {Steven Farrell and Murali Emani and Jacob Balma and Lukas Drescher and Aleksandr Drozd and Andreas Fink and Geoffrey Fox and David Kanter and Thorsten Kurth and Peter Mattson and Dawei Mu and Amit Ruhela and Kento Sato and Koichi Shirahata and Tsuguchika Tabaru and Aristeidis Tsaris and Jan Balewski and Ben Cumming and Takumi Danjo and Jens Domke and Takaaki Fukai and Naoto Fukumoto and Tatsuya Fukushi and Balazs Gerofi and Takumi Honda and Toshiyuki Imamura and Akihiko Kasagi and Kentaro Kawakami and Shuhei Kudo and Akiyoshi Kuroda and Maxime Martinasso and Satoshi Matsuoka and Henrique Mendonça and Kazuki Minami and Prabhat Ram and Takashi Sawada and Mallikarjun Shankar and Tom St. John and Akihiro Tabuchi and Venkatram Vishwanath and Mohamed Wahib and Masafumi Yamazaki and Junqi Yin},
  eprint        = {2110.11466},
  primaryclass  = {cs.LG},
  title         = {MLPerf HPC: A Holistic Benchmark Suite for Scientific Machine Learning on HPC Systems},
  url           = {https://arxiv.org/abs/2110.11466},
  year          = {2021}
}</code></pre>
<h3>Ratings</h3>
<div class="ratings-grid">
  <div class="ratings-head ratings-cell"><span>Category</span><span>Rating</span></div>
  <div class="rating-item">  <div class="rating-cat">Software</div>  <div class="rating-badge">3.00</div>  <div class="rating-bar"><span style="width:60%"></span></div>  <div class="rating-reason">Reference implementations exist but containerization and environment setup require manual effort across HPC systems.
</div></div><div class="rating-item">  <div class="rating-cat">Specification</div>  <div class="rating-badge">4.00</div>  <div class="rating-bar"><span style="width:80%"></span></div>  <div class="rating-reason">Hardware constraints and I/O formats are not fully defined for all scenarios.
</div></div><div class="rating-item">  <div class="rating-cat">Dataset</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">Not all data is independently versioned or comes with standardized FAIR metadata.
</div></div><div class="rating-item">  <div class="rating-cat">Metrics</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">None
</div></div><div class="rating-item">  <div class="rating-cat">Reference Solution</div>  <div class="rating-badge">4.00</div>  <div class="rating-bar"><span style="width:80%"></span></div>  <div class="rating-reason">Reproducibility and environment tuning depend on system configuration; baseline models not uniformly bundled.
</div></div><div class="rating-item">  <div class="rating-cat">Documentation</div>  <div class="rating-badge">4.00</div>  <div class="rating-bar"><span style="width:80%"></span></div>  <div class="rating-reason">Central guidance is available but requires domain-specific effort to replicate results across systems.
</div></div>
</div>
<div class="avg-rating">  <strong>Average rating:</strong> <span class="badge badge--ok badge--sm">4.17/5</span></div><h3>Radar plot</h3>

<div class="radar-wrap"><img class="radar-img" alt="MLPerf HPC radar" src="../../../tex/images/mlperf_hpc_radar.png" /></div>

<p><strong>Edit:</strong> <a href="https://github.com/mlcommons-science/benchmark/tree/main/source">edit this entry</a></p>
