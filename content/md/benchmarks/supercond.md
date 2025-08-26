# SuperCon3D

<p><a class="md-button back-link" href="../">← Back to all benchmarks</a></p>
<div class="info-block meta-block">
  <p class="meta-row"><span class="meta-label">Date</span><span class="meta-sep">:</span> <span class="meta-value">2024-12-13</span></p>
  <p class="meta-row"><span class="meta-label">Name</span><span class="meta-sep">:</span> <span class="meta-value">SuperCon3D</span></p>
  <p class="meta-row"><span class="meta-label">Domain</span><span class="meta-sep">:</span> <span class="meta-value">Materials Science; Superconductivity</span></p>
  <p class="meta-row"><span class="meta-label">Focus</span><span class="meta-sep">:</span> <span class="meta-value">Dataset and models for predicting and generating high-Tc superconductors using 3D crystal structures</span></p>
  <p class="meta-row"><span class="meta-label">Task Types</span><span class="meta-sep">:</span> <span class="meta-value">Regression (Tc prediction), Generative modeling</span></p>
  <p class="meta-row"><span class="meta-label">Metrics</span><span class="meta-sep">:</span> <span class="meta-value">MAE (Tc), Validity of generated structures</span></p>
  <p class="meta-row"><span class="meta-label">Models</span><span class="meta-sep">:</span> <span class="meta-value">SODNet, DiffCSP-SC</span></p>
</div>
<h3>Keywords</h3>

<div class="chips"><a class="chip chip-link" href="../#kw=superconductivity">superconductivity</a> <a class="chip chip-link" href="../#kw=crystal%20structures">crystal structures</a> <a class="chip chip-link" href="../#kw=equivariant%20GNN">equivariant GNN</a> <a class="chip chip-link" href="../#kw=generative%20models">generative models</a> </div>
<h3>Citation</h3>

- Pin Chen, Luoxuan Peng, Rui Jiao, Qing Mo, Zhen Wang, Wenbing Huang, Yang Liu, and Yutong Lu. Learning superconductivity from ordered and disordered material structures. In A. Globerson, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. Tomczak, and C. Zhang, editors, Advances in Neural Information Processing Systems, volume 37, 108902–108928. Curran Associates, Inc., 2024. URL: https://proceedings.neurips.cc/paper_files/paper/2024/file/c4e3b55ed4ac9ba52d7df11f8bddbbf4-Paper-Datasets_and_Benchmarks_Track.pdf.

<pre><code class="language-bibtex">@inproceedings{neurips2024_c4e3b55e,
  author = {Chen, Pin and Peng, Luoxuan and Jiao, Rui and Mo, Qing and Wang, Zhen and Huang, Wenbing and Liu, Yang and Lu, Yutong},
  booktitle = {Advances in Neural Information Processing Systems},
  editor = {A. Globerson and L. Mackey and D. Belgrave and A. Fan and U. Paquet and J. Tomczak and C. Zhang},
  pages = {108902--108928},
  publisher = {Curran Associates, Inc.},
  title = {Learning Superconductivity from Ordered and Disordered Material Structures},
  url = {https://proceedings.neurips.cc/paper_files/paper/2024/file/c4e3b55ed4ac9ba52d7df11f8bddbbf4-Paper-Datasets_and_Benchmarks_Track.pdf},
  volume = {37},
  year = {2024}
}</code></pre>
<h3>Ratings</h3>
<div class="ratings-grid">
  <div class="ratings-head ratings-cell"><span>Category</span><span>Rating</span></div>
  <div class="rating-item">  <div class="rating-cat">Software</div>  <div class="rating-badge">3.00</div>  <div class="rating-bar"><span style="width:60%"></span></div>  <div class="rating-reason">Baseline models (SODNet, DiffCSP-SC) are described in the paper; however,
fully reproducible code and pretrained models are not publicly available yet.
</div></div><div class="rating-item">  <div class="rating-cat">Specification</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">Tasks for regression (Tc prediction) and generative modeling with clear input/output
structures and domain constraints are well defined.
</div></div><div class="rating-item">  <div class="rating-cat">Dataset</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">Dataset contains 3D crystal structures and associated properties; well-curated but
not fully released publicly at this time.
</div></div><div class="rating-item">  <div class="rating-cat">Metrics</div>  <div class="rating-badge">4.00</div>  <div class="rating-bar"><span style="width:80%"></span></div>  <div class="rating-reason">Metrics such as MAE for Tc prediction and validity checks for generated structures
are appropriate and clearly described.
</div></div><div class="rating-item">  <div class="rating-cat">Reference Solution</div>  <div class="rating-badge">4.00</div>  <div class="rating-bar"><span style="width:80%"></span></div>  <div class="rating-reason">Paper provides model architecture details and some training insights, but no
complete open-source reference implementations yet.
</div></div><div class="rating-item">  <div class="rating-cat">Documentation</div>  <div class="rating-badge">4.00</div>  <div class="rating-bar"><span style="width:80%"></span></div>  <div class="rating-reason">Paper and GitHub provide good metadata and data processing descriptions; tutorials
and user guides could be expanded.
</div></div>
</div>
<div class="avg-rating">  <strong>Average rating:</strong> <span class="badge badge--ok badge--sm">4.17/5</span></div><h3>Radar plot</h3>

<div class="radar-wrap"><img class="radar-img" alt="SuperCon3D radar" src="../../../tex/images/supercond_radar.png" /></div>

<p><strong>Edit:</strong> <a href="https://github.com/mlcommons-science/benchmark/tree/main/source">edit this entry</a></p>
