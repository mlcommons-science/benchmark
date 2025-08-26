# Papers With Code (SOTA Platform)

<p><a class="md-button back-link" href="../">← Back to all benchmarks</a></p>
<div class="info-block meta-block">
  <p class="meta-row"><span class="meta-label">Date</span><span class="meta-sep">:</span> <span class="meta-value">ongoing</span></p>
  <p class="meta-row"><span class="meta-label">Name</span><span class="meta-sep">:</span> <span class="meta-value">Papers With Code  SOTA Platform</span></p>
  <p class="meta-row"><span class="meta-label">Domain</span><span class="meta-sep">:</span> <span class="meta-value">General ML; All domains</span></p>
  <p class="meta-row"><span class="meta-label">Focus</span><span class="meta-sep">:</span> <span class="meta-value">Open platform tracking state-of-the-art results, benchmarks, and implementations across ML tasks and papers</span></p>
  <p class="meta-row"><span class="meta-label">Task Types</span><span class="meta-sep">:</span> <span class="meta-value">Multiple (Classification, Detection, NLP, etc.)</span></p>
  <p class="meta-row"><span class="meta-label">Metrics</span><span class="meta-sep">:</span> <span class="meta-value">Task-specific (Accuracy, F1, BLEU, etc.)</span></p>
  <p class="meta-row"><span class="meta-label">Models</span><span class="meta-sep">:</span> <span class="meta-value">All published models with code</span></p>
</div>
<h3>Keywords</h3>

<div class="chips"><a class="chip chip-link" href="../#kw=leaderboard">leaderboard</a> <a class="chip chip-link" href="../#kw=benchmarking">benchmarking</a> <a class="chip chip-link" href="../#kw=reproducibility">reproducibility</a> <a class="chip chip-link" href="../#kw=open-source">open-source</a> </div>
<h3>Citation</h3>

- Avrim Blum and Moritz Hardt. The ladder: a reliable leaderboard for machine learning competitions. In Francis Bach and David Blei, editors, Proceedings of the 32nd International Conference on Machine Learning, volume 37 of Proceedings of Machine Learning Research, 1006–1014. Lille, France, July 2015. PMLR. URL: https://proceedings.mlr.press/v37/blum15.html.

<pre><code class="language-bibtex">@InProceedings{pmlr-v37-blum15,
  title =    {The Ladder: A Reliable Leaderboard for Machine Learning Competitions},
  author =   {Blum, Avrim and Hardt, Moritz},
  booktitle =        {Proceedings of the 32nd International Conference on Machine Learning},
  pages =    {1006--1014},
  year =     {2015},
  editor =   {Bach, Francis and Blei, David},
  volume =   {37},
  series =   {Proceedings of Machine Learning Research},
  address =          {Lille, France},
  month =    jul,
  publisher =    {PMLR},
  pdf =      {http://proceedings.mlr.press/v37/blum15.pdf},
  url =      {https://proceedings.mlr.press/v37/blum15.html},
  abstract =         {The organizer of a machine learning competition faces the problem of maintaining an accurate leaderboard that faithfully represents the quality of the best submission of each competing team. What makes this estimation problem particularly challenging is its sequential and adaptive nature. As participants are allowed to repeatedly evaluate their submissions on the leaderboard, they may begin to overfit to the holdout data that supports the leaderboard. Few theoretical results give actionable advice on how to design a reliable leaderboard. Existing approaches therefore often resort to poorly understood heuristics such as limiting the bit precision of answers and the rate of re-submission. In this work, we introduce a notion of leaderboard accuracy tailored to the format of a competition. We introduce a natural algorithm called the Ladder and demonstrate that it simultaneously supports strong theoretical guarantees in a fully adaptive model of estimation, withstands practical adversarial attacks, and achieves high utility on real submission files from a Kaggle competition. Notably, we are able to sidestep a powerful recent hardness result for adaptive risk estimation that rules out algorithms such as ours under a seemingly very similar notion of accuracy. On a practical note, we provide a completely parameter-free variant of our algorithm that can be deployed in a real competition with no tuning required whatsoever.}
}</code></pre>
<h3>Ratings</h3>
<div class="ratings-grid">
  <div class="ratings-head ratings-cell"><span>Category</span><span>Rating</span></div>
  <div class="rating-item">  <div class="rating-cat">Software</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">Actively maintained open-source platform (https://paperswithcode.com) under Apache 2.0 license;
includes automatic integration with GitHub, datasets, and models for reproducibility.
</div></div><div class="rating-item">  <div class="rating-cat">Specification</div>  <div class="rating-badge">4.00</div>  <div class="rating-bar"><span style="width:80%"></span></div>  <div class="rating-reason">Task and benchmark structures are well organized and standardized, but due to its broad coverage,
input/output formats vary significantly between tasks and are not always tightly controlled.
</div></div><div class="rating-item">  <div class="rating-cat">Dataset</div>  <div class="rating-badge">3.00</div>  <div class="rating-bar"><span style="width:60%"></span></div>  <div class="rating-reason">Relies on external datasets submitted by the community. While links are available, FAIR compliance
is not guaranteed or systematically enforced across all benchmarks.
</div></div><div class="rating-item">  <div class="rating-cat">Metrics</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">Tracks state-of-the-art using task-specific metrics like Accuracy, F1, BLEU, etc., with consistent
aggregation and historical SOTA tracking.
</div></div><div class="rating-item">  <div class="rating-cat">Reference Solution</div>  <div class="rating-badge">3.00</div>  <div class="rating-bar"><span style="width:60%"></span></div>  <div class="rating-reason">Provides links to implementations of many SOTA models, but no single unified reference baseline
is required or maintained per benchmark.
</div></div><div class="rating-item">  <div class="rating-cat">Documentation</div>  <div class="rating-badge">4.00</div>  <div class="rating-bar"><span style="width:80%"></span></div>  <div class="rating-reason">Strong front-end documentation and metadata on benchmarks, tasks, and models; however, some benchmark-specific
instructions are sparse or dependent on external paper links.
</div></div>
</div>
<div class="avg-rating">  <strong>Average rating:</strong> <span class="badge badge--ok badge--sm">4.00/5</span></div><h3>Radar plot</h3>

<div class="radar-wrap"><img class="radar-img" alt="Papers With Code (SOTA Platform) radar" src="../../../tex/images/papers_with_code_sota_platform_radar.png" /></div>

<p><strong>Edit:</strong> <a href="https://github.com/mlcommons-science/benchmark/tree/main/source">edit this entry</a></p>
