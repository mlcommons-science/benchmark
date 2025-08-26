# SGLang Framework

<p><a class="md-button back-link" href="../">← Back to all benchmarks</a></p>
<div class="info-block meta-block">
  <p class="meta-row"><span class="meta-label">Date</span><span class="meta-sep">:</span> <span class="meta-value">2023-12-12</span></p>
  <p class="meta-row"><span class="meta-label">Name</span><span class="meta-sep">:</span> <span class="meta-value">SGLang Framework</span></p>
  <p class="meta-row"><span class="meta-label">Domain</span><span class="meta-sep">:</span> <span class="meta-value">LLM Vision</span></p>
  <p class="meta-row"><span class="meta-label">Focus</span><span class="meta-sep">:</span> <span class="meta-value">Fast serving framework for LLMs and vision-language models</span></p>
  <p class="meta-row"><span class="meta-label">Task Types</span><span class="meta-sep">:</span> <span class="meta-value">Model serving framework</span></p>
  <p class="meta-row"><span class="meta-label">Metrics</span><span class="meta-sep">:</span> <span class="meta-value">Tokens/sec, Time-to-first-token, Throughput gain vs baseline</span></p>
  <p class="meta-row"><span class="meta-label">Models</span><span class="meta-sep">:</span> <span class="meta-value">LLaVA, DeepSeek, Llama</span></p>
</div>
<h3>Keywords</h3>

<div class="chips"><a class="chip chip-link" href="../#kw=LLM%20serving">LLM serving</a> <a class="chip chip-link" href="../#kw=vision-language">vision-language</a> <a class="chip chip-link" href="../#kw=RadixAttention">RadixAttention</a> <a class="chip chip-link" href="../#kw=performance">performance</a> <a class="chip chip-link" href="../#kw=JSON%20decoding">JSON decoding</a> </div>
<h3>Citation</h3>

- Lianmin Zheng, Liangsheng Yin, Zhiqiang Xie, Chuyue Sun, Jeff Huang, Cody Hao Yu, Shiyi Cao, Christos Kozyrakis, Ion Stoica, Joseph E. Gonzalez, Clark Barrett, and Ying Sheng. Sglang: efficient execution of structured language model programs. 2024. URL: https://arxiv.org/abs/2312.07104, arXiv:2312.07104.

<pre><code class="language-bibtex">@misc{zheng2024sglangefficientexecutionstructured,
  archiveprefix = {arXiv},
  author        = {Lianmin Zheng and Liangsheng Yin and Zhiqiang Xie and Chuyue Sun and Jeff Huang and Cody Hao Yu and Shiyi Cao and Christos Kozyrakis and Ion Stoica and Joseph E. Gonzalez and Clark Barrett and Ying Sheng},
  eprint        = {2312.07104},
  primaryclass  = {cs.AI},
  title         = {SGLang: Efficient Execution of Structured Language Model Programs},
  url           = {https://arxiv.org/abs/2312.07104},
  year          = {2024}
}</code></pre>
<h3>Ratings</h3>
<div class="ratings-grid">
  <div class="ratings-head ratings-cell"><span>Category</span><span>Rating</span></div>
  <div class="rating-item">  <div class="rating-cat">Software</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">Actively maintained and production-deployed (e.g., xAI, NVIDIA); source code available under
Apache 2.0. Includes efficient backends (RadixAttention, quantization, batching) and full
serving infrastructure.
</div></div><div class="rating-item">  <div class="rating-cat">Specification</div>  <div class="rating-badge">4.00</div>  <div class="rating-bar"><span style="width:80%"></span></div>  <div class="rating-reason">The framework clearly defines performance targets, serving logic, and model integration.
Input/output expectations are consistent, but not all benchmarks are standardized.
</div></div><div class="rating-item">  <div class="rating-cat">Dataset</div>  <div class="rating-badge">2.00</div>  <div class="rating-bar"><span style="width:40%"></span></div>  <div class="rating-reason">Does not introduce new datasets; instead, it evaluates performance using existing model benchmarks.
Only configuration files are included.
</div></div><div class="rating-item">  <div class="rating-cat">Metrics</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">Serving-related metrics such as tokens/sec, time-to-first-token, and throughput gain vs. baselines
are well-defined and consistently applied.
</div></div><div class="rating-item">  <div class="rating-cat">Reference Solution</div>  <div class="rating-badge">3.00</div>  <div class="rating-bar"><span style="width:60%"></span></div>  <div class="rating-reason">Provides benchmark configs and example integrations (e.g., with LLaVA, DeepSeek), but not all
models or scripts are runnable out-of-the-box.
</div></div><div class="rating-item">  <div class="rating-cat">Documentation</div>  <div class="rating-badge">4.00</div>  <div class="rating-bar"><span style="width:80%"></span></div>  <div class="rating-reason">Strong GitHub documentation, install guides, and benchmarks. Some advanced topics (e.g.,
scaling, hardware tuning) could use deeper walkthroughs.
</div></div>
</div>
<div class="avg-rating">  <strong>Average rating:</strong> <span class="badge badge--meh badge--sm">3.83/5</span></div><h3>Radar plot</h3>

<div class="radar-wrap"><img class="radar-img" alt="SGLang Framework radar" src="../../../tex/images/sglang_framework_radar.png" /></div>

<p><strong>Edit:</strong> <a href="https://github.com/mlcommons-science/benchmark/tree/main/source">edit this entry</a></p>
