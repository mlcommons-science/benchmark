# vLLM Inference and Serving Engine

<p><a class="md-button back-link" href="../">← Back to all benchmarks</a></p>
<div class="info-block meta-block">
  <p class="meta-row"><span class="meta-label">Date</span><span class="meta-sep">:</span> <span class="meta-value">2023-09-12</span></p>
  <p class="meta-row"><span class="meta-label">Name</span><span class="meta-sep">:</span> <span class="meta-value">vLLM Inference and Serving Engine</span></p>
  <p class="meta-row"><span class="meta-label">Domain</span><span class="meta-sep">:</span> <span class="meta-value">LLM; HPC/inference</span></p>
  <p class="meta-row"><span class="meta-label">Focus</span><span class="meta-sep">:</span> <span class="meta-value">High-throughput, memory-efficient inference and serving engine for LLMs</span></p>
  <p class="meta-row"><span class="meta-label">Task Types</span><span class="meta-sep">:</span> <span class="meta-value">Inference Benchmarking</span></p>
  <p class="meta-row"><span class="meta-label">Metrics</span><span class="meta-sep">:</span> <span class="meta-value">Tokens/sec, Time to First Token (TTFT), Memory footprint</span></p>
  <p class="meta-row"><span class="meta-label">Models</span><span class="meta-sep">:</span> <span class="meta-value">LLaMA, Mixtral, FlashAttention-based models</span></p>
</div>
<h3>Keywords</h3>

<div class="chips"><a class="chip chip-link" href="../#kw=LLM%20inference">LLM inference</a> <a class="chip chip-link" href="../#kw=PagedAttention">PagedAttention</a> <a class="chip chip-link" href="../#kw=CUDA%20graph">CUDA graph</a> <a class="chip chip-link" href="../#kw=streaming%20API">streaming API</a> <a class="chip chip-link" href="../#kw=quantization">quantization</a> </div>
<h3>Citation</h3>

- Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu, Joseph Gonzalez, Hao Zhang, and Ion Stoica. Efficient memory management for large language model serving with pagedattention. In Proceedings of the 29th Symposium on Operating Systems Principles, SOSP &#x27;23, 611 626. New York, NY, USA, 2023. Association for Computing Machinery. URL: https://doi.org/10.1145/3600006.3613165, doi:10.1145/3600006.3613165.

<pre><code class="language-bibtex">@inproceedings{10.1145/3600006.3613165,
  author = {Kwon, Woosuk and Li, Zhuohan and Zhuang, Siyuan and Sheng, Ying and Zheng, Lianmin and Yu, Cody Hao and Gonzalez, Joseph and Zhang, Hao and Stoica, Ion},
  title = {Efficient Memory Management for Large Language Model Serving with PagedAttention},
  year = {2023},
  publisher = {Association for Computing Machinery},
  address = {New York, NY, USA},
  url = {https://doi.org/10.1145/3600006.3613165},
  doi = {10.1145/3600006.3613165},
  abstract = {High throughput serving of large language models (LLMs) requires batching sufficiently many requests at a time. However, existing systems struggle because the key-value cache (KV cache) memory for each request is huge and grows and shrinks dynamically. When managed inefficiently, this memory can be significantly wasted by fragmentation and redundant duplication, limiting the batch size. To address this problem, we propose PagedAttention, an attention algorithm inspired by the classical virtual memory and paging techniques in operating systems. On top of it, we build vLLM, an LLM serving system that achieves (1) near-zero waste in KV cache memory and (2) flexible sharing of KV cache within and across requests to further reduce memory usage. Our evaluations show that vLLM improves the throughput of popular LLMs by 2--4\texttimes{} with the same level of latency compared to the state-of-the-art systems, such as FasterTransformer and Orca. The improvement is more pronounced with longer sequences, larger models, and more complex decoding algorithms. vLLM&#x27;s source code is publicly available at https://github.com/vllm-project/vllm.},
  booktitle = {Proceedings of the 29th Symposium on Operating Systems Principles},
  pages = {611-626},
  numpages = {16},
  location = {Koblenz, Germany},
  series = {SOSP &#x27;23}
}</code></pre>
<h3>Ratings</h3>
<div class="ratings-grid">
  <div class="ratings-head ratings-cell"><span>Category</span><span>Rating</span></div>
  <div class="rating-item">  <div class="rating-cat">Software</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">Actively maintained open-source project under Apache 2.0. GitHub repo includes
full serving engine, benchmarking scripts, CUDA integration, and deployment examples.
</div></div><div class="rating-item">  <div class="rating-cat">Specification</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">Inference benchmarks are well-defined with clear input/output formats and platform-specific constraints.
Covers multiple models, hardware backends, and batching configurations.
</div></div><div class="rating-item">  <div class="rating-cat">Dataset</div>  <div class="rating-badge">3.00</div>  <div class="rating-bar"><span style="width:60%"></span></div>  <div class="rating-reason">No traditional dataset is included. Instead, it uses structured configs and logs suitable for inference benchmarking.
FAIR principles are only partially applicable.
</div></div><div class="rating-item">  <div class="rating-cat">Metrics</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">Comprehensive performance metrics like tokens/sec, time-to-first-token (TTFT), and memory footprint
are consistently applied and benchmarked across frameworks.
</div></div><div class="rating-item">  <div class="rating-cat">Reference Solution</div>  <div class="rating-badge">4.00</div>  <div class="rating-bar"><span style="width:80%"></span></div>  <div class="rating-reason">Provides runnable scripts and configs for several models (LLaMA, Mixtral, etc.) across platforms.
Baselines are reproducible, though not all models are fully wrapped or hosted.
</div></div><div class="rating-item">  <div class="rating-cat">Documentation</div>  <div class="rating-badge">4.00</div>  <div class="rating-bar"><span style="width:80%"></span></div>  <div class="rating-reason">Well-structured GitHub documentation with setup instructions, config examples, benchmarking comparisons,
and performance tuning guides.
</div></div>
</div>
<div class="avg-rating">  <strong>Average rating:</strong> <span class="badge badge--ok badge--sm">4.33/5</span></div><h3>Radar plot</h3>

<div class="radar-wrap"><img class="radar-img" alt="vLLM Inference and Serving Engine radar" src="../../../tex/images/vllm_inference_and_serving_engine_radar.png" /></div>

<p><strong>Edit:</strong> <a href="https://github.com/mlcommons-science/benchmark/tree/main/source">edit this entry</a></p>
