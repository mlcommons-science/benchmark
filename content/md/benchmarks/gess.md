# GeSS

<p><a class="md-button back-link" href="../">← Back to all benchmarks</a></p>
<div class="info-block meta-block">
  <p class="meta-row"><span class="meta-label">Date</span><span class="meta-sep">:</span> <span class="meta-value">2024-12-13</span></p>
  <p class="meta-row"><span class="meta-label">Name</span><span class="meta-sep">:</span> <span class="meta-value">GeSS</span></p>
  <p class="meta-row"><span class="meta-label">Domain</span><span class="meta-sep">:</span> <span class="meta-value">Scientific ML; Geometric Deep Learning</span></p>
  <p class="meta-row"><span class="meta-label">Focus</span><span class="meta-sep">:</span> <span class="meta-value">Benchmark suite evaluating geometric deep learning models under real-world distribution shifts</span></p>
  <p class="meta-row"><span class="meta-label">Task Types</span><span class="meta-sep">:</span> <span class="meta-value">Classification, Regression</span></p>
  <p class="meta-row"><span class="meta-label">Metrics</span><span class="meta-sep">:</span> <span class="meta-value">Accuracy, RMSE, OOD robustness delta</span></p>
  <p class="meta-row"><span class="meta-label">Models</span><span class="meta-sep">:</span> <span class="meta-value">GCN, EGNN, DimeNet++</span></p>
</div>
<h3>Keywords</h3>

<div class="chips"><a class="chip chip-link" href="../#kw=geometric%20deep%20learning">geometric deep learning</a> <a class="chip chip-link" href="../#kw=distribution%20shift">distribution shift</a> <a class="chip chip-link" href="../#kw=OOD%20robustness">OOD robustness</a> <a class="chip chip-link" href="../#kw=scientific%20applications">scientific applications</a> </div>
<h3>Citation</h3>

- Deyu Zou, Shikun Liu, Siqi Miao, Victor Fung, Shiyu Chang, and Pan Li. Gess: benchmarking geometric deep learning under scientific applications with distribution shifts. In A. Globerson, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. Tomczak, and C. Zhang, editors, Advances in Neural Information Processing Systems, volume 37, 92499–92528. Curran Associates, Inc., 2024. URL: https://proceedings.neurips.cc/paper_files/paper/2024/file/a8063075b00168dc39bc81683619f1a8-Paper-Datasets_and_Benchmarks_Track.pdf.

<pre><code class="language-bibtex">@inproceedings{neurips2024_a8063075,
  author = {Zou, Deyu and Liu, Shikun and Miao, Siqi and Fung, Victor and Chang, Shiyu and Li, Pan},
  booktitle = {Advances in Neural Information Processing Systems},
  editor = {A. Globerson and L. Mackey and D. Belgrave and A. Fan and U. Paquet and J. Tomczak and C. Zhang},
  pages = {92499--92528},
  publisher = {Curran Associates, Inc.},
  title = {GeSS: Benchmarking Geometric Deep Learning under Scientific Applications with Distribution Shifts},
  url = {https://proceedings.neurips.cc/paper_files/paper/2024/file/a8063075b00168dc39bc81683619f1a8-Paper-Datasets_and_Benchmarks_Track.pdf},
  volume = {37},
  year = {2024}
}</code></pre>
<h3>Ratings</h3>
<div class="ratings-grid">
  <div class="ratings-head ratings-cell"><span>Category</span><span>Rating</span></div>
  <div class="rating-item">  <div class="rating-cat">Software</div>  <div class="rating-badge">3.00</div>  <div class="rating-bar"><span style="width:60%"></span></div>  <div class="rating-reason">Reference code expected post-conference; current public software availability limited.
Benchmark infrastructure partially described but not fully released yet.
</div></div><div class="rating-item">  <div class="rating-cat">Specification</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">Benchmark clearly defines OOD robustness scenarios with classification and regression
tasks in scientific domains, though no explicit hardware constraints are given.
</div></div><div class="rating-item">  <div class="rating-cat">Dataset</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">Curated datasets of 3D crystal structures and material properties are included and
publicly available for reproducible research.
</div></div><div class="rating-item">  <div class="rating-cat">Metrics</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">Uses well-established metrics such as MAE and structural validity for materials modeling,
plus accuracy and OOD robustness deltas.
</div></div><div class="rating-item">  <div class="rating-cat">Reference Solution</div>  <div class="rating-badge">4.00</div>  <div class="rating-bar"><span style="width:80%"></span></div>  <div class="rating-reason">Two reference models (SODNet, DiffCSP-SC) are reported with results, code expected
to be released soon.
</div></div><div class="rating-item">  <div class="rating-cat">Documentation</div>  <div class="rating-badge">4.00</div>  <div class="rating-bar"><span style="width:80%"></span></div>  <div class="rating-reason">Paper and poster provide solid explanation of benchmarks and scientific motivation;
more extensive user documentation forthcoming.
</div></div>
</div>
<div class="avg-rating">  <strong>Average rating:</strong> <span class="badge badge--ok badge--sm">4.33/5</span></div><h3>Radar plot</h3>

<div class="radar-wrap"><img class="radar-img" alt="GeSS radar" src="../../../tex/images/gess_radar.png" /></div>

<p><strong>Edit:</strong> <a href="https://github.com/mlcommons-science/benchmark/tree/main/source">edit this entry</a></p>
