# PDEBench

<p><a class="md-button back-link" href="../">← Back to all benchmarks</a></p>
<div class="info-block meta-block">
  <p class="meta-row"><span class="meta-label">Date</span><span class="meta-sep">:</span> <span class="meta-value">2022-10-13</span></p>
  <p class="meta-row"><span class="meta-label">Name</span><span class="meta-sep">:</span> <span class="meta-value">PDEBench</span></p>
  <p class="meta-row"><span class="meta-label">Domain</span><span class="meta-sep">:</span> <span class="meta-value">CFD; Weather Modeling</span></p>
  <p class="meta-row"><span class="meta-label">Focus</span><span class="meta-sep">:</span> <span class="meta-value">Benchmark suite for ML-based surrogates solving time-dependent PDEs</span></p>
  <p class="meta-row"><span class="meta-label">Task Types</span><span class="meta-sep">:</span> <span class="meta-value">Supervised Learning</span></p>
  <p class="meta-row"><span class="meta-label">Metrics</span><span class="meta-sep">:</span> <span class="meta-value">RMSE, boundary RMSE, Fourier RMSE</span></p>
  <p class="meta-row"><span class="meta-label">Models</span><span class="meta-sep">:</span> <span class="meta-value">FNO, U-Net, PINN, Gradient-Based inverse methods</span></p>
</div>
<h3>Keywords</h3>

<div class="chips"><a class="chip chip-link" href="../#kw=PDEs">PDEs</a> <a class="chip chip-link" href="../#kw=CFD">CFD</a> <a class="chip chip-link" href="../#kw=scientific%20ML">scientific ML</a> <a class="chip chip-link" href="../#kw=surrogate%20modeling">surrogate modeling</a> <a class="chip chip-link" href="../#kw=NeurIPS">NeurIPS</a> </div>
<h3>Citation</h3>

- Makoto Takamoto, Timothy Praditia, Raphael Leiteritz, Dan MacKinlay, Francesco Alesiani, Dirk Pflüger, and Mathias Niepert. Pdebench: an extensive benchmark for scientific machine learning. 2024. URL: https://arxiv.org/abs/2210.07182, arXiv:2210.07182.

<pre><code class="language-bibtex">@misc{takamoto2024pdebenchextensivebenchmarkscientific,
  archiveprefix = {arXiv},
  author        = {Makoto Takamoto and Timothy Praditia and Raphael Leiteritz and Dan MacKinlay and Francesco Alesiani and Dirk Pflüger and Mathias Niepert},
  eprint        = {2210.07182},
  primaryclass  = {cs.LG},
  title         = {PDEBENCH: An Extensive Benchmark for Scientific Machine Learning},
  url           = {https://arxiv.org/abs/2210.07182},
  year          = {2024}
}</code></pre>
<h3>Ratings</h3>
<div class="ratings-grid">
  <div class="ratings-head ratings-cell"><span>Category</span><span>Rating</span></div>
  <div class="rating-item">  <div class="rating-cat">Software</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">GitHub repository (https://github.com/pdebench/PDEBench) is actively maintained and includes
training pipelines, data loaders, and evaluation scripts. Installation and usage are well-documented.
</div></div><div class="rating-item">  <div class="rating-cat">Specification</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">Clearly defined tasks for forward and inverse PDE problems, with structured input/output formats,
system constraints, and task specifications.
</div></div><div class="rating-item">  <div class="rating-cat">Dataset</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">Diverse PDE datasets (synthetic and real-world) hosted on DaRUS with DOIs. Datasets are
well-documented, structured, and follow FAIR practices.
</div></div><div class="rating-item">  <div class="rating-cat">Metrics</div>  <div class="rating-badge">4.00</div>  <div class="rating-bar"><span style="width:80%"></span></div>  <div class="rating-reason">Includes RMSE, boundary RMSE, and Fourier-domain RMSE. These are well-suited to PDE problems,
though rationale behind metric choices could be expanded in some cases.
</div></div><div class="rating-item">  <div class="rating-cat">Reference Solution</div>  <div class="rating-badge">4.00</div>  <div class="rating-bar"><span style="width:80%"></span></div>  <div class="rating-reason">Baselines (FNO, U-Net, PINN, etc.) are available and documented, but not every model
includes full training and evaluation reproducibility out-of-the-box.
</div></div><div class="rating-item">  <div class="rating-cat">Documentation</div>  <div class="rating-badge">4.00</div>  <div class="rating-bar"><span style="width:80%"></span></div>  <div class="rating-reason">Strong documentation on GitHub including examples, configs, and usage instructions.
Some model-specific details and tutorials could be further expanded.
</div></div>
</div>
<div class="avg-rating">  <strong>Average rating:</strong> <span class="badge badge--ok badge--sm">4.50/5</span></div><h3>Radar plot</h3>

<div class="radar-wrap"><img class="radar-img" alt="PDEBench radar" src="../../../tex/images/pdebench_radar.png" /></div>

<p><strong>Edit:</strong> <a href="https://github.com/mlcommons-science/benchmark/tree/main/source">edit this entry</a></p>
