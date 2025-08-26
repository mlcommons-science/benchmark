# MedQA

<p><a class="md-button back-link" href="../">← Back to all benchmarks</a></p>
<div class="info-block meta-block">
  <p class="meta-row"><span class="meta-label">Date</span><span class="meta-sep">:</span> <span class="meta-value">2020-09-28</span></p>
  <p class="meta-row"><span class="meta-label">Name</span><span class="meta-sep">:</span> <span class="meta-value">MedQA</span></p>
  <p class="meta-row"><span class="meta-label">Domain</span><span class="meta-sep">:</span> <span class="meta-value">Medical Question Answering</span></p>
  <p class="meta-row"><span class="meta-label">Focus</span><span class="meta-sep">:</span> <span class="meta-value">Medical board exam QA</span></p>
  <p class="meta-row"><span class="meta-label">Task Types</span><span class="meta-sep">:</span> <span class="meta-value">Multiple choice</span></p>
  <p class="meta-row"><span class="meta-label">Metrics</span><span class="meta-sep">:</span> <span class="meta-value">Accuracy</span></p>
  <p class="meta-row"><span class="meta-label">Models</span><span class="meta-sep">:</span> <span class="meta-value">Neural reader, Retrieval-based QA systems</span></p>
</div>
<h3>Keywords</h3>

<div class="chips"><a class="chip chip-link" href="../#kw=USMLE">USMLE</a> <a class="chip chip-link" href="../#kw=diagnostic%20QA">diagnostic QA</a> <a class="chip chip-link" href="../#kw=medical%20knowledge">medical knowledge</a> <a class="chip chip-link" href="../#kw=multilingual">multilingual</a> </div>
<h3>Citation</h3>

- Di Jin, Eileen Pan, Nassim Oufattole, Wei-Hung Weng, Hanyi Fang, and Peter Szolovits. What disease does this patient have? a large-scale open domain question answering dataset from medical exams. 2020. URL: https://arxiv.org/abs/2009.13081, arXiv:2009.13081.

<pre><code class="language-bibtex">@misc{jin2020diseasedoespatienthave,
    archiveprefix = {arXiv},
    author        = {Di Jin and Eileen Pan and Nassim Oufattole and Wei-Hung Weng and Hanyi Fang and Peter Szolovits},
    eprint        = {2009.13081},
    primaryclass  = {cs.CL},
    title         = {What Disease does this Patient Have? A Large-scale Open Domain Question Answering Dataset from Medical Exams},
    url           = {https://arxiv.org/abs/2009.13081},
    year          = {2020}
  }</code></pre>
<h3>Ratings</h3>
<div class="ratings-grid">
  <div class="ratings-head ratings-cell"><span>Category</span><span>Rating</span></div>
  <div class="rating-item">  <div class="rating-cat">Software</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">All code available on the github
</div></div><div class="rating-item">  <div class="rating-cat">Specification</div>  <div class="rating-badge">3.00</div>  <div class="rating-bar"><span style="width:60%"></span></div>  <div class="rating-reason">Task is clearly defined as multiple-choice QA for medical board exams; input and output formats are explicit; task scope is rigorous and structured. System constraints not specified.
</div></div><div class="rating-item">  <div class="rating-cat">Dataset</div>  <div class="rating-badge">4.00</div>  <div class="rating-bar"><span style="width:80%"></span></div>  <div class="rating-reason">Dataset is publicly available (GitHub, paper, Hugging Face), well-structured. However, versioning and metadata could be more standardized to fully meet FAIR criteria.
</div></div><div class="rating-item">  <div class="rating-cat">Metrics</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">Uses clear, quantitative metric (accuracy), standard for multiple-choice benchmarks; easily comparable across models.
</div></div><div class="rating-item">  <div class="rating-cat">Reference Solution</div>  <div class="rating-badge">0.00</div>  <div class="rating-bar"><span style="width:0%"></span></div>  <div class="rating-reason">No reference solution mentioned.
</div></div><div class="rating-item">  <div class="rating-cat">Documentation</div>  <div class="rating-badge">4.00</div>  <div class="rating-bar"><span style="width:80%"></span></div>  <div class="rating-reason">Paper is available. Evaluation criteria are not mentioned.
</div></div>
</div>
<div class="avg-rating">  <strong>Average rating:</strong> <span class="badge badge--meh badge--sm">3.50/5</span></div><h3>Radar plot</h3>

<div class="radar-wrap"><img class="radar-img" alt="MedQA radar" src="../../../tex/images/medqa_radar.png" /></div>

<p><strong>Edit:</strong> <a href="https://github.com/mlcommons-science/benchmark/tree/main/source">edit this entry</a></p>
