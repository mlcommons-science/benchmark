# The Well

<p><a class="md-button back-link" href="../">← Back to all benchmarks</a></p>
<div class="info-block meta-block">
  <p class="meta-row"><span class="meta-label">Date</span><span class="meta-sep">:</span> <span class="meta-value">2024-12-03</span></p>
  <p class="meta-row"><span class="meta-label">Name</span><span class="meta-sep">:</span> <span class="meta-value">The Well</span></p>
  <p class="meta-row"><span class="meta-label">Domain</span><span class="meta-sep">:</span> <span class="meta-value">biological systems, fluid dynamics, acoustic scattering, astrophysical MHD</span></p>
  <p class="meta-row"><span class="meta-label">Focus</span><span class="meta-sep">:</span> <span class="meta-value">Foundation model + surrogate dataset spanning 16 physical simulation domains</span></p>
  <p class="meta-row"><span class="meta-label">Task Types</span><span class="meta-sep">:</span> <span class="meta-value">Supervised Learning</span></p>
  <p class="meta-row"><span class="meta-label">Metrics</span><span class="meta-sep">:</span> <span class="meta-value">Dataset size, Domain breadth</span></p>
  <p class="meta-row"><span class="meta-label">Models</span><span class="meta-sep">:</span> <span class="meta-value">FNO baselines, U-Net baselines</span></p>
</div>
<h3>Keywords</h3>

<div class="chips"><a class="chip chip-link" href="../#kw=surrogate%20modeling">surrogate modeling</a> <a class="chip chip-link" href="../#kw=foundation%20model">foundation model</a> <a class="chip chip-link" href="../#kw=physics%20simulations">physics simulations</a> <a class="chip chip-link" href="../#kw=spatiotemporal%20dynamics">spatiotemporal dynamics</a> </div>
<h3>Citation</h3>

- Ruben Ohana, Michael McCabe, Lucas Meyer, Rudy Morel, Fruzsina J. Agocs, Miguel Beneitez, Marsha Berger, Blakesley Burkhart, Stuart B. Dalziel, Drummond B. Fielding, Daniel Fortunato, Jared A. Goldberg, Keiya Hirashima, Yan-Fei Jiang, Rich R. Kerswell, Suryanarayana Maddu, Jonah Miller, Payel Mukhopadhyay, Stefan S. Nixon, Jeff Shen, Romain Watteaux, Bruno Régaldo-Saint Blancard, François Rozet, Liam H. Parker, Miles Cranmer, and Shirley Ho. The well: a large-scale collection of diverse physics simulations for machine learning. In A. Globerson, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. Tomczak, and C. Zhang, editors, Advances in Neural Information Processing Systems, volume 37, 44989–45037. Curran Associates, Inc., 2024. URL: https://proceedings.neurips.cc/paper_files/paper/2024/file/4f9a5acd91ac76569f2fe291b1f4772b-Paper-Datasets_and_Benchmarks_Track.pdf.

<pre><code class="language-bibtex">@inproceedings{neurips2024_4f9a5acd,
  author = {Ohana, Ruben and McCabe, Michael and Meyer, Lucas and Morel, Rudy and Agocs, Fruzsina J. and Beneitez, Miguel and Berger, Marsha and Burkhart, Blakesley and Dalziel, Stuart B. and Fielding, Drummond B. and Fortunato, Daniel and Goldberg, Jared A. and Hirashima, Keiya and Jiang, Yan-Fei and Kerswell, Rich R. and Maddu, Suryanarayana and Miller, Jonah and Mukhopadhyay, Payel and Nixon, Stefan S. and Shen, Jeff and Watteaux, Romain and Blancard, Bruno R\&#x27;{e}galdo-Saint and Rozet, Fran\c{c}ois and Parker, Liam H. and Cranmer, Miles and Ho, Shirley},
  booktitle = {Advances in Neural Information Processing Systems},
  editor = {A. Globerson and L. Mackey and D. Belgrave and A. Fan and U. Paquet and J. Tomczak and C. Zhang},
  pages = {44989--45037},
  publisher = {Curran Associates, Inc.},
  title = {The Well: a Large-Scale Collection of Diverse Physics Simulations for Machine Learning},
  url = {https://proceedings.neurips.cc/paper_files/paper/2024/file/4f9a5acd91ac76569f2fe291b1f4772b-Paper-Datasets_and_Benchmarks_Track.pdf},
  volume = {37},
  year = {2024}
}</code></pre>
<h3>Ratings</h3>
<div class="ratings-grid">
  <div class="ratings-head ratings-cell"><span>Category</span><span>Rating</span></div>
  <div class="rating-item">  <div class="rating-cat">Software</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">BSD-licensed software and unified API are available via GitHub and PyPI.
Supports loading and manipulating large HDF5 datasets across 16 domains.
</div></div><div class="rating-item">  <div class="rating-cat">Specification</div>  <div class="rating-badge">4.00</div>  <div class="rating-bar"><span style="width:80%"></span></div>  <div class="rating-reason">The benchmark includes clearly defined surrogate modeling tasks, data structure, and metadata.
However, constraints and formal task specs vary slightly across domains.
</div></div><div class="rating-item">  <div class="rating-cat">Dataset</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">15 TB of ML-ready HDF5 datasets across 16 physics domains. Public, well-structured,
richly annotated, and designed with FAIR principles in mind.
</div></div><div class="rating-item">  <div class="rating-cat">Metrics</div>  <div class="rating-badge">3.00</div>  <div class="rating-bar"><span style="width:60%"></span></div>  <div class="rating-reason">Domain breadth and dataset size are emphasized. Standardized quantitative metrics for
model evaluation (e.g., RMSE, accuracy) are not uniformly applied across all domains.
</div></div><div class="rating-item">  <div class="rating-cat">Reference Solution</div>  <div class="rating-badge">3.00</div>  <div class="rating-bar"><span style="width:60%"></span></div>  <div class="rating-reason">Includes FNO and U-Net baselines, but does not yet provide fully trained, reproducible
models or scripts across all datasets.
</div></div><div class="rating-item">  <div class="rating-cat">Documentation</div>  <div class="rating-badge">4.00</div>  <div class="rating-bar"><span style="width:80%"></span></div>  <div class="rating-reason">The GitHub repo and NeurIPS paper provide detailed guidance on dataset use,
structure, and training setup. Tutorials and walkthroughs could be expanded further.
</div></div>
</div>
<div class="avg-rating">  <strong>Average rating:</strong> <span class="badge badge--ok badge--sm">4.00/5</span></div><h3>Radar plot</h3>

<div class="radar-wrap"><img class="radar-img" alt="The Well radar" src="../../../tex/images/the_well_radar.png" /></div>

<p><strong>Edit:</strong> <a href="https://github.com/mlcommons-science/benchmark/tree/main/source">edit this entry</a></p>
