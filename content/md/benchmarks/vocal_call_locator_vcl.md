# Vocal Call Locator (VCL)

<p><a class="md-button back-link" href="../">← Back to all benchmarks</a></p>
<div class="info-block meta-block">
  <p class="meta-row"><span class="meta-label">Date</span><span class="meta-sep">:</span> <span class="meta-value">2024-12-13</span></p>
  <p class="meta-row"><span class="meta-label">Name</span><span class="meta-sep">:</span> <span class="meta-value">Vocal Call Locator  VCL</span></p>
  <p class="meta-row"><span class="meta-label">Domain</span><span class="meta-sep">:</span> <span class="meta-value">Neuroscience; Bioacoustics</span></p>
  <p class="meta-row"><span class="meta-label">Focus</span><span class="meta-sep">:</span> <span class="meta-value">Benchmarking sound-source localization of rodent vocalizations from multi-channel audio</span></p>
  <p class="meta-row"><span class="meta-label">Task Types</span><span class="meta-sep">:</span> <span class="meta-value">Sound source localization</span></p>
  <p class="meta-row"><span class="meta-label">Metrics</span><span class="meta-sep">:</span> <span class="meta-value">Localization error (cm), Recall/Precision</span></p>
  <p class="meta-row"><span class="meta-label">Models</span><span class="meta-sep">:</span> <span class="meta-value">CNN-based SSL models</span></p>
</div>
<h3>Keywords</h3>

<div class="chips"><a class="chip chip-link" href="../#kw=source%20localization">source localization</a> <a class="chip chip-link" href="../#kw=bioacoustics">bioacoustics</a> <a class="chip chip-link" href="../#kw=time-series">time-series</a> <a class="chip chip-link" href="../#kw=SSL">SSL</a> </div>
<h3>Citation</h3>

- Ralph E Peterson, Aramis Tanelus, Christopher Ick, Bartul Mimica, Niegil Francis, Violet J Ivan, Aman Choudhri, Annegret L Falkner, Mala Murthy, David M Schneider, Dan H Sanes, and Alex H Williams. Vocal call locator benchmark (vcl) for localizing rodent vocalizations from multi-channel audio. In A. Globerson, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. Tomczak, and C. Zhang, editors, Advances in Neural Information Processing Systems, volume 37, 106370–106382. Curran Associates, Inc., 2024. URL: https://proceedings.neurips.cc/paper_files/paper/2024/file/c00d37d6b04d73b870b963a4d70051c1-Paper-Datasets_and_Benchmarks_Track.pdf.

<pre><code class="language-bibtex">@inproceedings{neurips2024_c00d37d6,
  author = {Peterson, Ralph E and Tanelus, Aramis and Ick, Christopher and Mimica, Bartul and Francis, Niegil and Ivan, Violet J and Choudhri, Aman and Falkner, Annegret L and Murthy, Mala and Schneider, David M and Sanes, Dan H and Williams, Alex H},
  booktitle = {Advances in Neural Information Processing Systems},
  editor = {A. Globerson and L. Mackey and D. Belgrave and A. Fan and U. Paquet and J. Tomczak and C. Zhang},
  pages = {106370--106382},
  publisher = {Curran Associates, Inc.},
  title = {Vocal Call Locator Benchmark (VCL) for localizing rodent vocalizations from multi-channel audio},
  url = {https://proceedings.neurips.cc/paper_files/paper/2024/file/c00d37d6b04d73b870b963a4d70051c1-Paper-Datasets_and_Benchmarks_Track.pdf},
  volume = {37},
  year = {2024}
}</code></pre>
<h3>Ratings</h3>
<div class="ratings-grid">
  <div class="ratings-head ratings-cell"><span>Category</span><span>Rating</span></div>
  <div class="rating-item">  <div class="rating-cat">Software</div>  <div class="rating-badge">3.00</div>  <div class="rating-bar"><span style="width:60%"></span></div>  <div class="rating-reason">Some baseline CNN models for sound source localization are reported,
but no publicly available or fully integrated runnable codebase yet.
</div></div><div class="rating-item">  <div class="rating-cat">Specification</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">Well-defined localization tasks with multiple scenarios and real-world
environment conditions; input/output formats clearly described.
</div></div><div class="rating-item">  <div class="rating-cat">Dataset</div>  <div class="rating-badge">4.00</div>  <div class="rating-bar"><span style="width:80%"></span></div>  <div class="rating-reason">Large-scale audio dataset covering real and simulated data with
standardized splits, though exact data formats are not fully detailed.
</div></div><div class="rating-item">  <div class="rating-cat">Metrics</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">Includes localization error, precision, recall, and other relevant metrics
for robust evaluation.
</div></div><div class="rating-item">  <div class="rating-cat">Reference Solution</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">Multiple baselines evaluated over diverse models and architectures,
supporting reproducibility of benchmark comparisons.
</div></div><div class="rating-item">  <div class="rating-cat">Documentation</div>  <div class="rating-badge">1.00</div>  <div class="rating-bar"><span style="width:20%"></span></div>  <div class="rating-reason">Methodology and paper are thorough, but setup instructions and runnable
code are not publicly provided, limiting user onboarding.
</div></div>
</div>
<div class="avg-rating">  <strong>Average rating:</strong> <span class="badge badge--meh badge--sm">3.83/5</span></div><h3>Radar plot</h3>

<div class="radar-wrap"><img class="radar-img" alt="Vocal Call Locator (VCL) radar" src="../../../tex/images/vocal_call_locator_vcl_radar.png" /></div>

<p><strong>Edit:</strong> <a href="https://github.com/mlcommons-science/benchmark/tree/main/source">edit this entry</a></p>
