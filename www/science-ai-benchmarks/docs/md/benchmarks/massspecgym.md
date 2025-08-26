# MassSpecGym

<p><a class="md-button back-link" href="../">← Back to all benchmarks</a></p>
<div class="info-block meta-block">
  <p class="meta-row"><span class="meta-label">Date</span><span class="meta-sep">:</span> <span class="meta-value">2024-12-13</span></p>
  <p class="meta-row"><span class="meta-label">Name</span><span class="meta-sep">:</span> <span class="meta-value">MassSpecGym</span></p>
  <p class="meta-row"><span class="meta-label">Domain</span><span class="meta-sep">:</span> <span class="meta-value">Cheminformatics; Molecular Discovery</span></p>
  <p class="meta-row"><span class="meta-label">Focus</span><span class="meta-sep">:</span> <span class="meta-value">Benchmark suite for discovery and identification of molecules via MS/MS</span></p>
  <p class="meta-row"><span class="meta-label">Task Types</span><span class="meta-sep">:</span> <span class="meta-value">De novo generation, Retrieval, Simulation</span></p>
  <p class="meta-row"><span class="meta-label">Metrics</span><span class="meta-sep">:</span> <span class="meta-value">Structure accuracy, Retrieval precision, Simulation MSE</span></p>
  <p class="meta-row"><span class="meta-label">Models</span><span class="meta-sep">:</span> <span class="meta-value">Graph-based generative models, Retrieval baselines</span></p>
</div>
<h3>Keywords</h3>

<div class="chips"><a class="chip chip-link" href="../#kw=mass%20spectrometry">mass spectrometry</a> <a class="chip chip-link" href="../#kw=molecular%20structure">molecular structure</a> <a class="chip chip-link" href="../#kw=de%20novo%20generation">de novo generation</a> <a class="chip chip-link" href="../#kw=retrieval">retrieval</a> <a class="chip chip-link" href="../#kw=dataset">dataset</a> </div>
<h3>Citation</h3>

- Roman Bushuiev, Anton Bushuiev, Niek F. de Jonge, Adamo Young, Fleming Kretschmer, Raman Samusevich, Janne Heirman, Fei Wang, Luke Zhang, Kai Dührkop, Marcus Ludwig, Nils A. Haupt, Apurva Kalia, Corinna Brungs, Robin Schmid, Russell Greiner, Bo Wang, David S. Wishart, Li-Ping Liu, Juho Rousu, Wout Bittremieux, Hannes Rost, Tytus D. Mak, Soha Hassoun, Florian Huber, Justin J.J. van der Hooft, Michael A. Stravs, Sebastian Böcker, Josef Sivic, and Tomáš Pluskal. Massspecgym: a benchmark for the discovery and identification of molecules. In A. Globerson, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. Tomczak, and C. Zhang, editors, Advances in Neural Information Processing Systems, volume 37, 110010–110027. Curran Associates, Inc., 2024. URL: https://proceedings.neurips.cc/paper_files/paper/2024/file/c6c31413d5c53b7d1c343c1498734b0f-Paper-Datasets_and_Benchmarks_Track.pdf.

<pre><code class="language-bibtex">@inproceedings{neurips2024_c6c31413,
  author = {Bushuiev, Roman and Bushuiev, Anton and de Jonge, Niek F. and Young, Adamo and Kretschmer, Fleming and Samusevich, Raman and Heirman, Janne and Wang, Fei and Zhang, Luke and D\&quot;{u}hrkop, Kai and Ludwig, Marcus and Haupt, Nils A. and Kalia, Apurva and Brungs, Corinna and Schmid, Robin and Greiner, Russell and Wang, Bo and Wishart, David S. and Liu, Li-Ping and Rousu, Juho and Bittremieux, Wout and Rost, Hannes and Mak, Tytus D. and Hassoun, Soha and Huber, Florian and van der Hooft, Justin J.J. and Stravs, Michael A. and B\&quot;{o}cker, Sebastian and Sivic, Josef and Pluskal, Tom\&#x27;{a}\v{s}},
  booktitle = {Advances in Neural Information Processing Systems},
  editor = {A. Globerson and L. Mackey and D. Belgrave and A. Fan and U. Paquet and J. Tomczak and C. Zhang},
  pages = {110010--110027},
  publisher = {Curran Associates, Inc.},
  title = {MassSpecGym: A benchmark for the discovery and identification of molecules},
  url = {https://proceedings.neurips.cc/paper_files/paper/2024/file/c6c31413d5c53b7d1c343c1498734b0f-Paper-Datasets_and_Benchmarks_Track.pdf},
  volume = {37},
  year = {2024}
}</code></pre>
<h3>Ratings</h3>
<div class="ratings-grid">
  <div class="ratings-head ratings-cell"><span>Category</span><span>Rating</span></div>
  <div class="rating-item">  <div class="rating-cat">Software</div>  <div class="rating-badge">3.00</div>  <div class="rating-bar"><span style="width:60%"></span></div>  <div class="rating-reason">Open-source GitHub repository available; baseline models and training code partially
provided but overall framework maturity is moderate.
</div></div><div class="rating-item">  <div class="rating-cat">Specification</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">Clearly defined tasks including molecule generation, retrieval, and spectrum simulation,
scoped for MS/MS molecular identification.
</div></div><div class="rating-item">  <div class="rating-cat">Dataset</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">Largest public MS/MS dataset with extensive annotations; minor point deducted for
lack of explicit train/validation/test splits.
</div></div><div class="rating-item">  <div class="rating-cat">Metrics</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">Well-defined metrics such as structure accuracy, retrieval precision, and simulation MSE
used consistently.
</div></div><div class="rating-item">  <div class="rating-cat">Reference Solution</div>  <div class="rating-badge">3.50</div>  <div class="rating-bar"><span style="width:70%"></span></div>  <div class="rating-reason">CNN-based baselines are referenced, but pretrained weights and comprehensive training
pipelines are not fully documented.
</div></div><div class="rating-item">  <div class="rating-cat">Documentation</div>  <div class="rating-badge">1.00</div>  <div class="rating-bar"><span style="width:20%"></span></div>  <div class="rating-reason">Paper and poster describe benchmark goals and design, but documentation and user
guides are minimal and repo status uncertain.
</div></div>
</div>
<div class="avg-rating">  <strong>Average rating:</strong> <span class="badge badge--meh badge--sm">3.75/5</span></div><h3>Radar plot</h3>

<div class="radar-wrap"><img class="radar-img" alt="MassSpecGym radar" src="../../../tex/images/massspecgym_radar.png" /></div>

<p><strong>Edit:</strong> <a href="https://github.com/mlcommons-science/benchmark/tree/main/source">edit this entry</a></p>
