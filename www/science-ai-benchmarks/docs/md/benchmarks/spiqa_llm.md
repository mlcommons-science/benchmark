# SPIQA (LLM)

<p><a class="md-button back-link" href="../">← Back to all benchmarks</a></p>
<div class="info-block meta-block">
  <p class="meta-row"><span class="meta-label">Date</span><span class="meta-sep">:</span> <span class="meta-value">2024-12-13</span></p>
  <p class="meta-row"><span class="meta-label">Name</span><span class="meta-sep">:</span> <span class="meta-value">SPIQA  LLM</span></p>
  <p class="meta-row"><span class="meta-label">Domain</span><span class="meta-sep">:</span> <span class="meta-value">Multimodal Scientific QA; Computer Vision</span></p>
  <p class="meta-row"><span class="meta-label">Focus</span><span class="meta-sep">:</span> <span class="meta-value">Evaluating LLMs on image-based scientific paper figure QA tasks  LLM Adapter performance</span></p>
  <p class="meta-row"><span class="meta-label">Task Types</span><span class="meta-sep">:</span> <span class="meta-value">Multimodal QA</span></p>
  <p class="meta-row"><span class="meta-label">Metrics</span><span class="meta-sep">:</span> <span class="meta-value">Accuracy, F1 score</span></p>
  <p class="meta-row"><span class="meta-label">Models</span><span class="meta-sep">:</span> <span class="meta-value">LLaVA, MiniGPT-4, Owl-LLM adapter variants</span></p>
</div>
<h3>Keywords</h3>

<div class="chips"><a class="chip chip-link" href="../#kw=multimodal%20QA">multimodal QA</a> <a class="chip chip-link" href="../#kw=scientific%20figures">scientific figures</a> <a class="chip chip-link" href="../#kw=image%2Btext">image+text</a> <a class="chip chip-link" href="../#kw=chain-of-thought%20prompting">chain-of-thought prompting</a> </div>
<h3>Citation</h3>

- Shraman Pramanick, Rama Chellappa, and Subhashini Venugopalan. Spiqa: a dataset for multimodal question answering on scientific papers. 2025. URL: https://arxiv.org/abs/2407.09413, arXiv:2407.09413.

<pre><code class="language-bibtex">@misc{pramanick2025spiqadatasetmultimodalquestion,
  title={SPIQA: A Dataset for Multimodal Question Answering on Scientific Papers}, 
  author={Shraman Pramanick and Rama Chellappa and Subhashini Venugopalan},
  year={2025},
  eprint={2407.09413},
  archivePrefix={arXiv},
  primaryClass={cs.CL},
  url={https://arxiv.org/abs/2407.09413}, 
}</code></pre>
<h3>Ratings</h3>
<div class="ratings-grid">
  <div class="ratings-head ratings-cell"><span>Category</span><span>Rating</span></div>
  <div class="rating-item">  <div class="rating-cat">Software</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">Well-documented codebase available on Github
</div></div><div class="rating-item">  <div class="rating-cat">Specification</div>  <div class="rating-badge">3.50</div>  <div class="rating-bar"><span style="width:70%"></span></div>  <div class="rating-reason">Task of QA over scientific figures is sufficient but not fully formalized in input/output terms. No hawrdware constraints.
</div></div><div class="rating-item">  <div class="rating-cat">Dataset</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">Full dataset available on Hugging Face with train/test/valid splits.
</div></div><div class="rating-item">  <div class="rating-cat">Metrics</div>  <div class="rating-badge">4.00</div>  <div class="rating-bar"><span style="width:80%"></span></div>  <div class="rating-reason">Reports accuracy and F1; fair but no visual reasoning-specific metric.
</div></div><div class="rating-item">  <div class="rating-cat">Reference Solution</div>  <div class="rating-badge">4.00</div>  <div class="rating-bar"><span style="width:80%"></span></div>  <div class="rating-reason">10 LLM adapter baselines; results included without constraints.
</div></div><div class="rating-item">  <div class="rating-cat">Documentation</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">Full paper available
</div></div>
</div>
<div class="avg-rating">  <strong>Average rating:</strong> <span class="badge badge--ok badge--sm">4.42/5</span></div><h3>Radar plot</h3>

<div class="radar-wrap"><img class="radar-img" alt="SPIQA (LLM) radar" src="../../../tex/images/spiqa_llm_radar.png" /></div>

<p><strong>Edit:</strong> <a href="https://github.com/mlcommons-science/benchmark/tree/main/source">edit this entry</a></p>
